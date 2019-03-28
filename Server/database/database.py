#!/usr/bin/python3

"""
This class uses acts as a proxy for the proxies of the different database used.
This allows the main server only having to use just one class. Also the development of
the specific proxies and the Processor can be done separably, this class being the communication
point of both ends.
"""

__all__ = [
        "Database"
        ]

from database.time_series.proxy import *
from database.relational.proxy import *


class Database:
    """
    Proxy of proxies. Creates a global api to interact with all database types.
    """
    def __init__(self):
        """
        Constructs a Database object, initializing the required specific proxies.
        """
        self.time_series_proxy = InfluxProxy()
        self.relational_proxy = MySqlProxy()

    def register(self, data):
        """
        Register a client on the database

        :param data: keys : [username, password, name, email, phpn, birth_date, weight, height, diseases]
        :type data: dict
        :return: the client_id for the new client
        :rtype: int
        """
        return self.relational_proxy.register_client(
            data["username"],
            data["password"],
            data["name"],
            data["email"],
            data["phpn"],
            data["birth_date"], # TODO may require conversion
            data["weight"],
            data["height"],
            data["diseases"]
        )

    def verifyUser(self, data):
        """
        Verifies if the received credentials are correct

        :param data: keys : [username, password]
        :type data:  dict
        :return: true if credentials are ok, false otherwise
        :rtype: bool
        """
        return self.relational_proxy.check_credentials(
            data["username"],
            data["password"]
        )

    def addDevices(self, user, data):
        """
        Stores a new device on the database

        :param user: username of the client to associate
        :type user: str
        :param data: keys : [type, token]
        :type data: dict
        :return: id of the new device created
        :rtype: int
        """
        return self.relational_proxy.register_device(
            user,
            data["type"],
            data["token"]
        )

    def getAllDevices(self, user):
        """
        Get all devices associated with the client passed on the arguments

        :param user: username of the client to query
        :type user: str
        :return: all devices associated with the specific client
        :rtype: list
        """
        return self.relational_proxy.get_all_devices_of_user(user)

    def getSupportedDevices(self):
        """"""
        pass

    def getCurrentEnviroment(self, user):
        """"""
        pass

    def getEnviromentStartInterval(self, user, start, interval):
        """"""
        pass

    def getEnviromentStartEnd(self, user, start, end):
        """"""
        pass

    def getEnviromentEndInterval(self, user, end, interval):
        """"""
        pass

    def currentEnviromentSpecific(self, user, measurement):
        """"""
        pass

    def currentEnviromentSpecificStartInterval(self, user, measurement, start, interval):
        """"""
        pass

    def currentEnviromentSpecificStartEnd(self, user, measurement, start, end):
        """"""
        pass

    def currentEnviromentSpecificEndInterval(self, user, measurement, end, interval):
        """"""
        pass

    def getCurrentHealthStatus(self, user):
        """"""
        pass

    def getCurrentHealthStatusStartInterval(self, user, start, interval):
        """"""
        pass

    def getCurrentHealthStatusStartEnd(self, user, start, end):
        """"""
        pass

    def getCurrentHealthStatusEndInterval(self, user, end, interval):
        """"""
        pass

    def getCurrentHealthStatusSpecific(self, user, measurement):
        """"""
        pass

    def getCurrentHealthStatusSpecificStartInterval(self, user, measurement, start, interval):
        """"""
        pass

    def getCurrentHealthStatusSpecificStartEnd(self, user, measurement, start, end):
        """"""
        pass

    def getCurrentHealthStatusSpecificEndInterval(self, user, measurement, end, interval):
        """"""
        pass

    def personalStatus(self, user):
        """"""
        pass

    def personalStatusStartInterval(self, user, start, interval):
        """"""
        pass

    def personalStatusStartEnd(self, user, start, end):
        """"""
        pass

    def personalStatusEndInterval(self, user, end, interval):
        """"""
        pass

    def updateProfile(self, user, data):
        """"""
        pass

    def getProfile(self, user):
        """"""
        pass

    def deleteProfile(self, user):
        """"""
        pass
