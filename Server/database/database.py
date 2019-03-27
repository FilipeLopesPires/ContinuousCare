#!/usr/bin/python3

__all__ = [
        "Database"
        ]

from database.time_series.proxy import *
from database.relational.proxy import *


class Database:
    """
    """
    def __init__(self):
        """
        """
        self.time_series_proxy = InfluxProxy()
        self.relational_proxy = MySqlProxy()

    def register(self, data):
        """
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
        """"""
        pass

    def getAllDevices(self, user):
        """"""
        pass

    def addDevices(self, user, data):
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

    def getSupportedDevices(self):
        """"""
        pass
