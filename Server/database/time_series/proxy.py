#!/usr/bin/python3

"""
On this file is present a class that serves has a proxy to the
communication to the database.

With it the code relative to this specific database type is only
present on this file and the other classes can be independent of
the database (in what concerns the connections)
"""

import influxdb
import json
from database.time_series import config
from database.exceptions import TimeSeriesDBException, LogicException


class InfluxProxy:
    """
    Proxy used to interact with a Influx database allowing writes and reads
    """

    def __init__(self):
        """
        Constructs InfluxProxy objects according to the config.py file
        """
        self.__conn = influxdb.InfluxDBClient(
            host      = config.HOST,
            port      = config.PORT,
            username  = config.USERNAME,
            password  = config.PASSWORD,
            database  = config.DATABASE,
            pool_size = config.POOL_SIZE
        )

    @property
    def _get_connection(self):
        return self.__conn

    def write(self, data):
        """
        Write to the database data

        :param data: data to write
        :type data: list
        """
        try:
            self._get_connection.write_points(data, 's')
        except Exception as e:
            raise TimeSeriesDBException(str(e))

    def read(self, username, measurement, begin_time=None, end_time=None, interval=None):
        """
        Get from the database data of a specific user and a specific measurement
        allowing also filtering results within a time interval

        :param username: username of the client
        :type username: str
        :param measurement: measurement of the value
        :type measurement: str
        :param begin_time: values after this (seconds)
        :type begin_time: int
        :param end_time: values before this (seconds)
        :type end_time: int
        :param interval: size of interval like influx (ns, u, ms, s, m, h, d, w)
            (nanoseconds, microseconds, milliseconds, seconds, minutes, hours, days, weeks)
        :type interval: str
        :return: list of maps
        :rtype: list
        """
        if begin_time and end_time and interval:
            raise LogicException("Combination of start, end and interval arguments invalid.")

        # Parameters on query only work on the where clause
        params = {
            "username": username
        }

        query = "SELECT * " + \
                "FROM %s " % measurement + \
                "WHERE username = $username"

        if interval:

            if begin_time:
                query += " AND time >= $begin_time AND time <= $begin_time + " + interval
                params["begin_time"] = begin_time * 1000000000

            elif end_time:
                query += " AND time <= $end_time AND time >= $end_time - " + interval
                params["end_time"] = end_time * 1000000000
            else:
                query += " AND time >= now() - " + interval

        elif not begin_time and not end_time:
            query += " ORDER BY time DESC LIMIT 1"

        else:
            if begin_time:
                query += " AND time >= $begin_time"
                params["begin_time"] = begin_time * 1000000000

            if end_time:
                query += " AND time <= $end_time"
                params["end_time"] = end_time * 1000000000

        try:
            result = self._get_connection.query(query, {"params": json.dumps(params)}) # , epoch="s")
        except LogicException:
            raise
        except Exception as e:
            raise TimeSeriesDBException(str(e))
        return list(result.get_points(measurement))

    def delete(self, username, measurement, time):
        """
        Deletes a single value associated with an user of a specific measurement

        :param username: of the client
        :type username: str
        :param measurement: measurement of the value to delete
        :type measurement: str
        :param time: timestamp
        :param time: int
        """
        query = "DELETE FROM %s " % measurement + \
                "WHERE username = $username " + \
                  "AND time = $time"

        params = {
            "username": username,
            "time": time * 1000000000
        }

        try:
            result = self._get_connection.query(query, {"params": json.dumps(params)})
        except Exception as e:
            raise TimeSeriesDBException(str(e))
        return list(result.get_points(measurement))
