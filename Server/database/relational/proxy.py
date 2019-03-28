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

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

import base64


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

        self.__hash_algorithm = hashes.SHA256()
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

    @property
    def _get_connection(self):
        """
        Gets a connection to the database from the pool"""
        return self._pool.get_connection()

    def _init_connection(self):
        """

        :return:
        :rtype: tuple
        """
        conn = self._get_connection
        cursor = conn.cursor()

        return conn, cursor

    def _close_conenction(self, conn, cursor):
        """

        :param conn:
        :type conn:
        :param cursor:
        :type cursor: :class:``
        """
        cursor.close()
        conn.close()

    def register_client(self, username, password, full_name, email, health_number, birth_date, weight, height, diseases):
        """

        :param username:
        :type username: str
        :param password:
        :type password: str
        :param full_name:
        :type full_name: str
        :param email:
        :type email: str
        :param health_number:
        :type health_number: int
        :param birth_date:
        :type birth_date: str
        :param weight:
        :type weight: float
        :param height:
        :type height: float
        :param diseases:
        :type diseases: list
        :return:
        """
        hash_parser = hashes.Hash(hashes.SHA256(), default_backend())
        hash_parser.update(bytes(password, "utf-8"))
        password = base64.b64encode(hash_parser.finalize()).decode()

        try:
            conn, cursor = self._init_connection()

            cursor.callproc("register_client", (username, password, full_name, email, health_number, birth_date, weight, height))

            new_id = next(cursor.stored_results()).fetchone()[0]

            for disease in diseases:
                cursor.callproc("insert_client_disease", (new_id, disease))

            conn.commit()
        except Exception:
            raise Exception
        finally:
            self._close_conenction(conn, cursor)

        return new_id

    def register_medic(self, username, password, full_name, email, specialization, company):
        """"""
        pass
