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

    def getAllUsers(self):
        return ["joao"]

    def getAllDevices(self, user):
        return [{"type":"FitBit Charge 3", "token":"eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRLMlgiLCJzdWIiOiI3Q05RV1oiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTU0NjY3NDUxLCJpYXQiOjE1NTQ2Mzg2NTF9.gpfMfYc2qXry9__uoSO1Q_gm4J4tMqPNZhsbXKXms1k", "refresh_token": "a30345a6d6809a05f65db20e5ed510fbdfa3d3d69b2cc97dac794d6032ae12fd","device":"123"},{"type":"Foobot ", "token":"123", "device":"234","latitude":50,"longitude":10, "uuid":"10"} ]

    def register(self, data):
        """
        Register a client on the database

        :param data: keys : [username:str, password:str, name:str, email:str, phpn:int,
                             birth_date:##, weight:float, height:float, diseases:str]
        TODO define date class
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

        :param data: keys : [username:str, password:str]
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
        :param data: keys : [type:int, token:str]
        :type data: dict
        :return: id of the new device created
        :rtype: int
        """
        return self.relational_proxy.register_device(
            user,
            data["type"],
            data["token"]
        )

    '''
    def getAllDevices(self, user):
        """
        Get all devices associated with the client passed on the arguments

        :param user: username of the client to query
        :type user: str
        :return: all devices associated with the specific client
        [{device:int, type:int, token:str}, ...]
        :rtype: list
        """
        return self.relational_proxy.get_all_devices_of_user(user)
    '''

    def getSupportedDevices(self):
        """
        Obtains all supported devices, that are integrated with the system,
        that the client can purchase/use

        :return: all supported devices by the system
        [{id:int, type:str, brand:str, model:str, metrics:[{name:str, unit:str}, ...]}, ...]
        :rtype: list
        """
        return self.relational_proxy.get_all_supported_devices()

    def _get_environment_metrics(self):
        """
        Obtains all environment metrics.
        This method is used before a query to get all environment values.

        :return: all supported environment metrics by the system
        :rtype: list
        """
        return self.relational_proxy.get_all_environment_metrics()

    def _time_series_read(self, username, measurements, start=None, end=None, interval=None):
        """
        Method used to read from the time_series database. Was created mainly to reduce
        the redundancy of code on the functions bellow.

        :param username: of the client
        :type username: str
        :param measurements: which measurements to get from database
        :type measurements: list
        :param start: values after this time
        :type start: # TODO define time type
        :param end: values before this time
        :type end: # TODO define time type
        :param interval: size of interval like influx (ns, u, ms, s, m, h, d, w)
        :type interval: str
        :return: # TODO see what influx returns
        :rtype: list or dict
        """
        return_value = []

        for metric in measurements:
            return_value.append(self.time_series_proxy.read(username, metric, start, end, interval))

        return return_value

    def getCurrentEnvironment(self, user):
        """
        Gets CURRENT values of ALL ENVIRONMENT MEASUREMENTS

        :param user: username of the client
        :type user: str
        :return: data
        :rtype: # TODO see what influx returns
        """
        return self._time_series_read(user, self._get_environment_metrics())

    def getEnvironmentStartInterval(self, user, start, interval):
        """
        Gets ALL ENVIRONMENT MEASUREMENTS values within an interval STARTING from a given time plus a given INTERVAL

        :param user: username of the client
        :type user: str
        :param start: values after this time
        :type start: # TODO define time type
        :param interval: size of interval like influx (ns, u, ms, s, m, h, d, w)
        :type interval: str
        :return: data
        :rtype: # TODO see what influx returns
        """
        return self._time_series_read(user, self._get_environment_metrics(), start, interval=interval)

    def getEnvironmentStartEnd(self, user, start, end):
        """
        Gets ALL ENVIRONMENT MEASUREMENTS values within an interval STARTING from
        a given time and ENDING at a given time

        :param user: username of the client
        :type user: str
        :param start: values after this time
        :type start: #TODO define time type
        :param end: values before this time
        :type end: #TODO define time type
        :return: data
        :rtype: #TODO see what influx returns
        """
        return self._time_series_read(user, self._get_environment_metrics(), start, end)

    def getEnvironmentEndInterval(self, user, end, interval):
        """
        Gets ALL ENVIRONMENT MEASUREMENTS values within an interval ENDING from
        a given time minus a given INTERVAL

        :param user: username of the client
        :type user: str
        :param end: values before this time
        :type end: #TODO define time type
        :param interval: size of interval like influx (ns, u, ms, s, m, h, d, w)
        :type interval: str
        :return: data
        :rtype: #TODO see what influx returns
        """
        return self._time_series_read(user, self._get_environment_metrics(), end=end, interval=interval)

    def currentEnvironmentSpecific(self, user, measurement):
        """
        Gets CURRENT values of a SPECIFIC ENVIRONMENT measurement

        :param user: username of the client
        :type user: str
        :param measurement: name of the specific measurement to get form the database
        :type measurement: str
        :return: data
        :rtype: #TODO see what influx returns
        """
        return self._time_series_read(user, [measurement])

    def currentEnvironmentSpecificStartInterval(self, user, measurement, start, interval):
        """
        Gets values of a SPECIFIC ENVIRONMENT MEASUREMENT within an interval STARTING from a given
        time plus a given INTERVAL

        :param user: username of the client
        :type user: str
        :param measurement: name of the specific measurement to get form the database
        :type measurement: str
        :param start: values after this time
        :type start: #TODO define time type
        :param interval: size of interval like influx (ns, u, ms, s, m, h, d, w)
        :type interval: str
        :return: data
        :rtype: #TODO see what influx returns
        """
        return self._time_series_read(user, [measurement], start, interval=interval)

    def currentEnvironmentSpecificStartEnd(self, user, measurement, start, end):
        """
        Gets values of a SPECIFIC ENVIRONMENT MEASUREMENT within an interval STARTING from a given
        time and ENDING on a given time

        :param user: username of the client
        :type user: str
        :param measurement: name of the specific measurement to get from the database
        :type measurement: str
        :param start: values after this time
        :type start: #TODO define time type
        :param end: values before this time
        :type end: #TODO define time type
        :return: data
        :rtype: #TODO see what influx returns
        """
        return self._time_series_read(user, [measurement], start, end)

    def currentEnvironmentSpecificEndInterval(self, user, measurement, end, interval):
        """
        Gets values of a SPECIFIC ENVIRONMENT MEASUREMENT within an interval STARTING from a given
        time minus a given INTERVAL

        :param user: username of the client
        :type user: str
        :param measurement: name of the specific measurement to get from the database
        :type measurement: str
        :param end: values before this time
        :type end: #TODO define time type
        :param interval: size of interval like influx (ns, u, ms, s, m, h, d, w)
        :type interval: str
        :return: data
        :rtype: #TODO see what influx returns
        """
        return self._time_series_read(user, [measurement], end=end, interval=interval)

    def _get_health_status_metrics(self):
        """
        Obtains all health status metrics.
        This method is used before a query to get all health status values.

        :return: all supported health status metrics by the system
        :rtype: list
        """
        return self.relational_proxy.get_all_health_status_metrics()

    def getCurrentHealthStatus(self, user):
        """
        Gets CURRENT values of ALL HEALTH STATUS MEASUREMENTS

        :param user: username of the client
        :type user: str
        :return: data
        :rtype: # TODO see what influx returns
        """
        return self._time_series_read(user, self._get_health_status_metrics())

    def getCurrentHealthStatusStartInterval(self, user, start, interval):
        """
        Gets ALL HEALTH STATUS MEASUREMENTS values within an interval STARTING from a
        given time plus a given INTERVAL

        :param user: username of the client
        :type user: str
        :param start: values after this time
        :type start: # TODO define time type
        :param interval: size of interval like influx (ns, u, ms, s, m, h, d, w)
        :type interval: str
        :return: data
        :rtype: # TODO see what influx returns
        """
        return self._time_series_read(user, self._get_health_status_metrics(), start, interval=interval)

    def getCurrentHealthStatusStartEnd(self, user, start, end):
        """
        Gets ALL HEALTH STATUS MEASUREMENTS values within an interval STARTING from
        a given time and ENDING at a given time

        :param user: username of the client
        :type user: str
        :param start: values after this time
        :type start: #TODO define time type
        :param end: values before this time
        :type end: #TODO define time type
        :return: data
        :rtype: #TODO see what influx returns
        """
        return self._time_series_read(user, self._get_health_status_metrics(), start, end)

    def getCurrentHealthStatusEndInterval(self, user, end, interval):
        """
        Gets ALL HEALTH STATUS MEASUREMENTS values within an interval ENDING from
        a given time minus a given INTERVAL

        :param user: username of the client
        :type user: str
        :param end: values before this time
        :type end: #TODO define time type
        :param interval: size of interval like influx (ns, u, ms, s, m, h, d, w)
        :type interval: str
        :return: data
        :rtype: #TODO see what influx returns
        """
        return self._time_series_read(user, self._get_health_status_metrics(), end=end, interval=interval)

    def getCurrentHealthStatusSpecific(self, user, measurement):
        """
        Gets CURRENT values of a SPECIFIC HEALTH STATUS measurement

        :param user: username of the client
        :type user: str
        :param measurement: name of the specific measurement to get form the database
        :type measurement: str
        :return: data
        :rtype: #TODO see what influx returns
        """
        return self._time_series_read(user, [measurement])

    def getCurrentHealthStatusSpecificStartInterval(self, user, measurement, start, interval):
        """
        Gets values of a SPECIFIC HEALTH STATUS MEASUREMENT within an interval STARTING from a given
        time plus a given INTERVAL

        :param user: username of the client
        :type user: str
        :param measurement: name of the specific measurement to get form the database
        :type measurement: str
        :param start: values after this time
        :type start: #TODO define time type
        :param interval: size of interval like influx (ns, u, ms, s, m, h, d, w)
        :type interval: str
        :return: data
        :rtype: #TODO see what influx returns
        """
        return self._time_series_read(user, [measurement], start, interval=interval)

    def getCurrentHealthStatusSpecificStartEnd(self, user, measurement, start, end):
        """
        Gets values of a SPECIFIC HEALTH STATUS MEASUREMENT within an interval STARTING from a given
        time and ENDING on a given time

        :param user: username of the client
        :type user: str
        :param measurement: name of the specific measurement to get from the database
        :type measurement: str
        :param start: values after this time
        :type start: #TODO define time type
        :param end: values before this time
        :type end: #TODO define time type
        :return: data
        :rtype: #TODO see what influx returns
        """
        return self._time_series_read(user, [measurement], start, end=end)

    def getCurrentHealthStatusSpecificEndInterval(self, user, measurement, end, interval):
        """
        Gets values of a SPECIFIC HEALTH STATUS MEASUREMENT within an interval STARTING from a given
        time minus a given INTERVAL

        :param user: username of the client
        :type user: str
        :param measurement: name of the specific measurement to get from the database
        :type measurement: str
        :param end: values before this time
        :type end: #TODO define time type
        :param interval: size of interval like influx (ns, u, ms, s, m, h, d, w)
        :type interval: str
        :return: data
        :rtype: #TODO see what influx returns
        """
        return self._time_series_read(user, [measurement], end=end, interval=interval)

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
        """
        Updates the profile data of a client with the username received from the arguments

        :param user: username of the client to update
        :type user: str
        :param data: keys : [password:str, name:str, email:str, phpn:int, birth_date:str,
                             weight:float, height:float, diseases:str]
        TODO define date class
        :type data: dict
        """
        self.relational_proxy.update_user_profile_data(
            user,
            data["password"],
            data["name"],
            data["email"],
            data["phpn"],
            data["birth_date"], # TODO may require conversion
            data["weight"],
            data["height"],
            data["diseases"]
        )

    def getProfile(self, user):
        """
        Gets all profile data associated with the username (user) in the arguments

        :param user: username of the client
        :type user: str
        :return: all profile data
        {client_id:int, full_name:str, email:str, health_number:int, birth_date:datetime, weight:float, height:float}
        :rtype: dict
        """
        return self.relational_proxy.get_user_profile_data(user)

    def deleteProfile(self, user):
        """"""
        pass
