#!/usr/bin/python3

"""
On this file is present a class that serves has a proxy to the
communication to the database.

With it the code relative to this specific database type is only
present on this file and the other classes can be independent of
the database (in what concerns the connections)
"""

from mysql.connector.pooling import MySQLConnectionPool

from database.relational import config
from database.exceptions import RelationalDBException

# for password hashing
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import base64


class StoredProcedures:
    REGISTER_CLIENT = "insert_client"
    GET_ALL_USERNAMES = "get_all_usernames"
    INSERT_DEVICE = "insert_device"
    VERIFY_CREDENTIALS = "verify_credentials"
    GET_ALL_CLIENT_DEVICES = "get_all_client_devices"
    GET_ALL_SUPPORTED_DEVICES = "get_all_supported_devices"
    GET_USER_PROFILE_DATA = "get_user_info"
    UPDATE_USER_PROFILE_DATA = "update_user_info"
    REGISTER_SLEEP_SESSION = "register_sleep_session"
    INSERT_SLEEP_SESSION = "insert_sleep_session"
    GET_SLEEP_SESSIONS = "get_sleep_sessions"
    UPDATE_DEVICE = "update_device"
    #DELETE_DEVICE = "delete_device"


class MySqlProxy:
    """Proxy used to interact with a MySql database allowing ..."""

    def __init__(self,):
        """Constructs a pool of connection according to the config.py file"""
        self.__pool = MySQLConnectionPool(
            pool_name = config.POOL_NAME,
            pool_size = config.POOL_SIZE,
            host      = config.HOST,
            port      = config.PORT,
            database  = config.DATABASE,
            user      = config.USERNAME,
            password  = config.PASSWORD
        )

        self.__hash_algorithm = hashes.SHA512()
        self.__cipher_backend = default_backend()

    @property
    def _hash_algorithm(self):
        return self.__hash_algorithm

    @property
    def _cipher_backend(self):
        return self.__cipher_backend

    @property
    def _pool(self):
        return self.__pool

    def _init_connection(self):
        """
        Gets a connection to the database from the pool, creating a cursor from it

        :return: :class:`PooledMySQLConnection` and :class:`MySQLCursor`
        :rtype: tuple
        """
        conn = self._pool.get_connection()
        cursor = conn.cursor()

        return conn, cursor

    def _close_conenction(self, conn, cursor):
        """
        Closes both the cursor and the connection. Because pooled connection are being used this
            is just returning the connection to the pool

        :param conn: connection object to the database
        :type conn: :class:`PooledMySQLConnection`
        :param cursor: cursor created from the connection object
        :type cursor: :class:`MySQLCursor`
        """
        cursor.close()
        conn.close()

    def _hash_password(self, password):
        """
        Applies a hash function (SHA512) to a clear text password to
        either compared or stored.

        :param password: clear text password
        :type password: str
        :return: password after hash function applied and encoded in base 64
        :rtype: str
        """
        hash_parser = hashes.Hash(self._hash_algorithm, self._cipher_backend)
        hash_parser.update(bytes(password, "utf-8"))
        password = base64.b64encode(hash_parser.finalize()).decode()

        return password

    def register_client(self, username, password, full_name, email, health_number,
                              birth_date, weight, height, additional_information):
        """
        Creates a new user on the database. The `register_client` SP is used to create all user related data.
        On this function the password is hashed to be stored.
        The write to the database can fail if an user with the same username or health_number already exists.

        :raises Exception: In case if something goes wrong when calling stored procedures

        :param username: can't exist another user with the same value
        :type username: str
        :param password: clear text password to be hashed
        :type password: str
        :param full_name: full name of the client
        :type full_name: str
        :param email: email of the client
        :type email: str
        :param health_number: number used on the country of the client to identify him in which concerns the health
            department
        :type health_number: int
        :param birth_date: with format (day, month, year)
        :type birth_date: tuple
        :param weight: in kilograms
        :type weight: float
        :param height: in meters
        :type height: float
        :param additional_information: information that can be important to mention so a medic can be more contextualized
        :type additional_information: list
        :return: client_id of the client created on the database
        :rtype: int
        """
        try:
            conn, cursor = self._init_connection()

            password = self._hash_password(password)

            birth_day, birth_month, birth_year = birth_date
            cursor.callproc(
                StoredProcedures.REGISTER_CLIENT,
                (username, password, full_name, email, health_number,
                 "%s-%s-%s" % (birth_year, birth_month, birth_day), weight, height, additional_information)
            )

            new_id = next(cursor.stored_results()).fetchone()[0]

            conn.commit()

            return new_id
        except Exception as e:
            raise RelationalDBException(str(e))
        finally:
            self._close_conenction(conn, cursor)

    def register_medic(self, username, password, full_name, email, specialization, company):
        """"""
        pass

    def check_credentials(self, username, password):
        """
        Verifies if the received credential are correct

        :param username: of a client or medic
        :type username: str
        :param password:
        :type password: str
        :return: true if the credentials are ok, false otherwise
        :rtype: bool
        """
        try:
            conn, cursor = self._init_connection()

            password = self._hash_password(password)

            cursor.callproc(StoredProcedures.VERIFY_CREDENTIALS, (username, password))

            return next(cursor.stored_results()).fetchone()[0] == 1
        except Exception as e:
            raise RelationalDBException(str(e))
        finally:
            self._close_conenction(conn, cursor)

    def register_device(self, username, type, authentication_fields, latitude=None, longitude=None):
        """
        Inserts a new device on the database and associates it with the user

        :param username: client to associate
        :type username: str
        :param type: type of the device (brand + " " + model)
        :type type: str
        :param authentication_fields: fields to access device's APIs
        :type authentication_fields: list
        :param latitude: location of the device (only applicable for home devices)
        :type latitude: float
        :param longitude: location of the device (only applicable for home devices)
        :type longitude: float
        :return: id of the new device
        :rtype: int
        """
        try:
            auth_fields = [(name, value) for name, value in authentication_fields.items()]

            conn, cursor = self._init_connection()

            cursor.execute("CREATE TEMPORARY TABLE IF NOT EXISTS tmp_authentication_fields(name VARCHAR(30)," +
                                                                                          "value VARCHAR(500))")
            cursor.execute("DELETE FROM tmp_authentication_fields")
            cursor.executemany("INSERT INTO tmp_authentication_fields values (%s, %s)", auth_fields)
            cursor.callproc(StoredProcedures.INSERT_DEVICE, (username, type, latitude, longitude))

            conn.commit()

            return next(cursor.stored_results()).fetchone()[0]
        except Exception as e:
            raise RelationalDBException(str(e))
        finally:
            self._close_conenction(conn, cursor)

    def get_all_devices_of_user(self, username):
        """
        Obtains all devices associated with the user with the same
        username as the one received from the arguments

        :param username: of the client
        :type username: str
        :return: info of all devices. In case of a home device the
        object will also contain a longitude and latitude field
        [{device:int, type:int, token:str, uuid:str}, ...]
        :rtype: list
        """
        try:
            conn, cursor = self._init_connection()

            cursor.callproc(StoredProcedures.GET_ALL_CLIENT_DEVICES, [username])

            devices = dict()
            for (device_id,
                 type_id,
                 type,
                 brand,
                 model,
                 photo, auth_field_name,
                        auth_field_value, latitude,
                                          longitude) in next(cursor.stored_results()).fetchall():
                if device_id not in devices.keys():
                    device = {
                        "id": device_id,
                        "type": "%s %s" % (brand, model),
                        "photo": photo
                    }
                    if latitude: # if one exist both exist
                        device["latitude"] = latitude
                        device["longitude"] = longitude
                    devices[device_id] = device

                if auth_field_name:
                    devices[device_id][auth_field_name] = auth_field_value

            return list(devices.values())
        except Exception as e:
            raise RelationalDBException(str(e))
        finally:
            self._close_conenction(conn, cursor)

    def get_all_supported_devices(self):
        """
        Retrieves all supported devices by the system giving also
        the metrics that that device can read

        :return: all information of the supported devices
        [{id:int, type:str, brand:str, model:str, metrics:[{name:str, unit:str}, ...]}, ...]
        :rtype: list
        """
        try:
            conn, cursor = self._init_connection()

            cursor.callproc(StoredProcedures.GET_ALL_SUPPORTED_DEVICES)

            retval = {}
            for (device_id, device_type, device_brand, device_model,
                 metric_name, metric_unit) in next(cursor.stored_results()).fetchall():
                if device_id not in retval.keys():
                    retval[device_id] = {
                        "id": device_id,
                        "type": device_type,
                        "brand": device_brand,
                        "model": device_model,
                        "metrics": []
                    }

                retval[device_id]["metrics"].append({ # TODO maybe append tuple instead of dict
                    "name": metric_name,
                    "unit": metric_unit
                })

            return list(retval.values())
        except Exception as e:
            raise RelationalDBException(str(e))
        finally:
            self._close_conenction(conn, cursor)

    def get_user_profile_data(self, username):
        """
        Obtains all profile data associated with the username received

        :param username: of the client to search for
        :type username: str
        :return: all client's profile data
        {client_id:int, full_name:str, email:str, health_number:int, birth_date:datetime, weight:float, height:float}
        :rtype: dict
        """
        try:
            conn, cursor = self._init_connection()

            cursor.callproc(StoredProcedures.GET_USER_PROFILE_DATA, [username])

            results = next(cursor.stored_results()).fetchall()[0]

            return {key: (results[i] if key != "birth_date" else results[i].strftime("%d-%m-%Y"))
                    for i, key in enumerate(["client_id",
                                             "full_name",
                                             "email",
                                             "health_number",
                                             "birth_date",
                                             "weight",
                                             "height",
                                             "additional_info"])}
        except Exception as e:
            raise RelationalDBException(str(e))
        finally:
            self._close_conenction(conn, cursor)

    def update_user_profile_data(self, username, password, full_name, email, health_number, #TODO they may not send this field
                                       birth_date, weight, height, additional_information):
        """
        Updates the profile information for a user. The function receives all information
        to overload all data, assuming that some of it is the same as the stored one.

        :param username: of the client to update the data
        :type username: str
        :param password: clear text password
        :type password: str
        :param full_name: full name of the client
        :type full_name: str
        :param email: email of the client
        :type email: str
        :param health_number: number used on the country of the client to identify him in which concerns the health
            department
        :type health_number: int
        :param birth_date: with format (day, month, year)
        :type birth_date: tuple
        :param weight: in kilograms
        :type weight: float
        :param height: in meters
        :type height: float
        :param additional_information: information that can be important to mention so a medic can be more contextualized
        :type additional_information: str
        """
        try:
            conn, cursor = self._init_connection()

            password = self._hash_password(password)

            birth_day, birth_month, birth_year = birth_date

            cursor.callproc(StoredProcedures.UPDATE_USER_PROFILE_DATA, (username, password, full_name, email,
                                                                        "%s-%s-%s" % (birth_year,
                                                                                      birth_month,
                                                                                      birth_year),
                                                                        birth_date, weight,
                                                                        height, additional_information))

            conn.commit()
        except Exception as e:
            raise RelationalDBException(str(e))
        finally:
            self._close_conenction(conn, cursor)

    def insert_sleep_session(self, username, day, duration, begin, end):
        """
        Register a new sleep session on the database. Can fail if the new session
        overlaps with existing ones in which concerns begin and end time

        :param username: of the client
        :type username: str
        :param day: with a format of %d-%m-%y
        :type day: str
        :param duration: with a format of %H-%M-%S
        :type duration: str
        :param begin: with a format of %d-%m-%y %H-%M-%S
        :type begin: str
        :param end: with a format of %d-%m-%y %H-%M-%S
        :type end: str
        """
        try:
            conn, cursor = self._init_connection()

            cursor.callproc(StoredProcedures.INSERT_SLEEP_SESSION, (username, day, duration, begin, end))

            conn.commit()
        except Exception as e:
            raise RelationalDBException(str(e))
        finally:
            self._close_conenction(conn, cursor)

    def get_sleep_sessions(self, username, begin=None, end=None):
        """"""
        try:
            conn, cursor = self._init_connection()

            cursor.callproc(StoredProcedures.GET_SLEEP_SESSIONS, (username, begin, end))

            return next(cursor.stored_results()).fetchall()
        except Exception as e:
            raise RelationalDBException(str(e))
        finally:
            self._close_conenction(conn, cursor)

    def get_all_usernames(self):
        """
        Used by the main server to get all username so he can start to
        quety data from devices/external api's

        :return: list of all usernames OF CLIENTS
        :rtype: list
        """
        try:
            conn, cursor = self._init_connection()

            cursor.callproc(StoredProcedures.GET_ALL_USERNAMES)

            return [username[0] for username in next(cursor.stored_results()).fetchall()]
        except Exception as e:
            raise RelationalDBException(str(e))
        finally:
            self._close_conenction(conn, cursor)

    def updtate_device(self, username, device_id, data):
        """

        :param username: of the client
        :type username: str
        :param device_id: of the device owned by the client
            to change data
        :type device_id: int
        :param data: fields to change (authentication fields and/or longitude, latitude)
        :type data: dict
        """
        try:
            latitude, longitude = None, None
            if "latitude" in data.keys(): # assume that if latitude is in dict, longitude is also
                latitude = data["latitude"]
                longitude = data["longitude"]
                del data["latitude"]
                del data["longitude"]

            auth_fields = [(name, value) for name, value in data.items()]

            conn, cursor = self._init_connection()

            cursor.execute("CREATE TEMPORARY TABLE IF NOT EXISTS tmp_authentication_fields(name VARCHAR(30)," +
                           "value VARCHAR(500))")
            cursor.execute("DELETE FROM tmp_authentication_fields")
            cursor.executemany("INSERT INTO tmp_authentication_fields values (%s, %s)", auth_fields)
            cursor.callproc(StoredProcedures.UPDATE_DEVICE, (username, device_id, latitude, longitude))

            conn.commit()
        except Exception as e:
            raise RelationalDBException(str(e))
        finally:
            self._close_conenction(conn, cursor)
