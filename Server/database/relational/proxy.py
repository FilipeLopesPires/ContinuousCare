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


class MySqlProxy:
    """Proxy used to interact with a MySql database allowing ..."""

    def __init__(self,):
        """Constructs a pool of connection according to the config.py file"""
        self.__pool = MySQLConnectionPool(
            pool_size = config.POOL_SIZE,
            host      = config.HOST,
            database  = config.DATABASE,
            user      = config.USERNAME,
            password  = config.PASSWORD
        )

    @property
    def _pool(self):
        return self.__pool

    def _get_connection(self):
        """Gets a connection to the database from the pool"""
        return self._pool.get_connection()
