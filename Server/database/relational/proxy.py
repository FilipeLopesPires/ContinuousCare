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

# for password hashing
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import base64


class StoredProcedures:
    REGISTER_CLIENT = "insert_client"
    INSERT_DEVICE = "insert_device"
    VERIFY_CREDENTIALS = "verify_credentials"
    GET_ALL_CLIENT_DEVICES = "get_all_client_devices"
    GET_ALL_SUPPORTED_DEVICES = "get_all_supported_devices"
    GET_USER_PROFILE_DATA = "get_user_info"
    UPDATE_USER_PROFILE_DATA = "update_user_info"
    GET_ENVIRONMENT_METRICS = "get_environment_metrics"
    GET_HEALTH_STATUS_METRICS = "get_health_status_metrics"


class MySqlProxy:
    """Proxy used to interact with a MySql database allowing ..."""

    def __init__(self,):
        """Constructs a pool of connection according to the config.py file"""
        self.__pool = MySQLConnectionPool(
            pool_name = config.POOL_NAME,
            pool_size = config.POOL_SIZE,
            host      = config.HOST,
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
        :param birth_date: with format dd-mm-yyyy
        :type birth_date: str
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

            cursor.callproc(
                StoredProcedures.REGISTER_CLIENT,
                (username, password, full_name, email, health_number,
                 birth_date, weight, height, additional_information)
            )

            new_id = next(cursor.stored_results()).fetchone()[0]

            conn.commit()

            return new_id
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
        finally:
            self._close_conenction(conn, cursor)

    def register_device(self, username, type_id, token):
        """
        Inserts a new device on the database and associates it with the user

        :param username: client to associate
        :type username: str
        :param type_id: type of the device
        :type type_id: int
        :param token: token to access device's APIs
        :type token: str
        :return: id of the new device
        :rtype: int
        """
        try:
            conn, cursor = self._init_connection()

            cursor.callproc(StoredProcedures.INSERT_DEVICE, (username, type_id, token))

            conn.commit()

            return next(cursor.stored_results()).fetchone()[0]
        finally:
            self._close_conenction(conn, cursor)

    def get_all_devices_of_user(self, username):
        """
        Obtains all devices associated with the user with the same
        username as the one received from the arguments

        :param username: of the client
        :type username: str
        :return: info of all devices
        [{device:int, type:int, token:str}, ...]
        :rtype: list
        """
        try:
            conn, cursor = self._init_connection()

            cursor.callproc(StoredProcedures.GET_ALL_CLIENT_DEVICES, [username])

            retval = []
            for (device_id, type_id, token) in next(cursor.stored_results()).fetchall():
                retval.append(
                    {
                        "device": device_id,
                        "type"  : type_id,
                        "token" : token
                    }
                )

            return retval
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

                retval[device_id]["metrics"].append({
                    "name": metric_name,
                    "unit": metric_unit
                })

            return list(retval.values())
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

            results = next(cursor.stored_results()).fetchall()

            return {key: results[i] for i, key in enumerate(["client_id",
                                                             "full_name",
                                                             "email",
                                                             "health_number",
                                                             "birth_date",
                                                             "weight",
                                                             "height"])}
        finally:
            self._close_conenction(conn, cursor)

    def update_user_profile_data(self, username, password, full_name, email, health_number,
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
        :param birth_date: with format dd-mm-yyyy
        :type birth_date: str
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

            cursor.callproc(StoredProcedures.UPDATE_USER_PROFILE_DATA, (username, password, full_name, email,
                                                                        health_number, birth_date, weight, height,
                                                                        additional_information))

            conn.commit()
        finally:
            self._close_conenction(conn, cursor)

    def get_all_environment_metrics(self):
        """
        Gets all environment metrics names

        :return: all metric names
        :rtype: list
        """
        try:
            conn, cursor = self._init_connection()

            cursor.callproc(StoredProcedures.GET_ENVIRONMENT_METRICS)

            return [line[0] for line in next(cursor.stored_results()).fetchall()]
        finally:
            self._close_conenction(conn, cursor)

    def get_all_health_status_metrics(self):
        """
        Gets all health status metrics names

        :return: all metric names
        :rtype: list
        """
        try:
            conn, cursor = self._init_connection()

            cursor.callproc(StoredProcedures.GET_HEALTH_STATUS_METRICS)

            return [line[0] for line in next(cursor.stored_results()).fetchall()]
        finally:
            self._close_conenction(conn, cursor)
