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
    INSERT_CLIENT_DISEASE = "insert_client_disease"
    VERIFY_CREDENTIALS = "verify_credentials"
    GET_ALL_CLIENT_DEVICES = "get_all_client_devices"


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

    def register_client(self, username, password, full_name, email, health_number, birth_date, weight, height, diseases):
        """
        Creates a new user on the database. The `register_client` SP is used to create all user related
        data and `insert_client_disease` SP is used to associate to the clients his several diseases.
        On this function the password is hashed to be stored.
        The write to the database can fail if a user with the same username or heal_number already exists.

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
        :param diseases: conditions that can be important to mention so a medic can me more contextualized
        :type diseases: list
        :return: client_id of the client created on the database
        """
        try:
            conn, cursor = self._init_connection()

            password = self._hash_password(password)

            cursor.callproc(
                StoredProcedures.REGISTER_CLIENT,
                (username, password, full_name, email, health_number, birth_date, weight, height)
            )

            new_id = next(cursor.stored_results()).fetchone()[0]

            for disease in diseases:
                cursor.callproc(StoredProcedures.INSERT_CLIENT_DISEASE, (new_id, disease))

            conn.commit()
        finally:
            self._close_conenction(conn, cursor)

        return new_id

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
                        "type": type_id,
                        "token": token
                    }
                )

            return retval
        finally:
            self._close_conenction(conn, cursor)
