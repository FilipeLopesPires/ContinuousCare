#!/usr/bin/python3

from database.time_series.proxy import *
from database.relational.proxy import *

import datetime

"""
This class uses acts as a proxy for the proxies of the different database used.
This allows the main server only having to use just one class. Also the development of
the specific proxies and the Processor can be done separably, this class being the communication
point of both ends.
"""

"""get timestamp from date string datetime.datetime.strptime(s, "%d/%m/%Y").timestamp()"""

__all__ = [
        "Database"
        ]


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

        :param data: keys : [username:str, password:str, name:str, email:str, phpn:int,
                             birth_date:tuple dd-mm-yyyy, weight:float, height:float, diseases:str]
        :type data: dict
        :return: the client_id for the new client
        :rtype: int
        """
        birth_day, birth_month, birth_year = data["birth_date"].split("-")

        return self.relational_proxy.register_client(
            data["username"],
            data["password"],
            data["name"],
            data["email"],
            data["phpn"],
            (birth_day, birth_month, birth_year),
            data["weight"],
            data["height"],
            data["additional_information"]
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

    def updateProfile(self, user, data):
        """
        Updates the profile data of a client with the username received from the arguments

        :param user: username of the client to update
        :type user: str
        :param data: keys : [password:str, name:str, email:str, phpn:int,
                             birth_date:str dd-mm-yyyy, weight:float, height:float, diseases:str]
        :type data: dict
        """
        birth_day, birth_month, birth_year = data["birth_date"].split("-")
        self.relational_proxy.update_user_profile_data(
            user,
            data["password"],
            data["name"],
            data["email"],
            data["phpn"], # TODO do they send me this?
            (birth_day, birth_month, birth_year),
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


    def getAllUsers(self):
        """"""
        return self.relational_proxy.get_all_usernames()

    def addDevice(self, user, data):
        """
        Stores a new device on the database

        :param user: username of the client to associate
        :type user: str
        :param data: keys : [type:int, authentication:str]
        :type data: dict
        :return: id of the new device created
        :rtype: int
        """
        return self.relational_proxy.register_device(
            user,
            data["type"], # TODO may not receive an int here
            data["authentication_fields"], # TODO may not be this name
            data.get("latitude", None), # TODO may not be this key
            data.get("longitude", None) # TODO may not be this key
        )

    def updateDevice(self, user, data):
        """"""

    def deleteDevice(self, user, device_id):
        """"""

    def getAllDevices(self, user):
        """
        Get all devices associated with the client passed on the arguments

        :param user: username of the client to query
        :type user: str
        :return: all devices associated with the specific client
        [{device:int, type:int,  token:str}, ...]
        :rtype: list
        """
        return self.relational_proxy.get_all_devices_of_user(user)

    def getSupportedDevices(self):
        """
        Obtains all supported devices, that are integrated with the system,
        that the client can purchase/use

        :return: all supported devices by the system
        [{id:int, type:str, brand:str, model:str, metrics:[{name:str, unit:str}, ...]}, ...]
        :rtype: list
        """
        return self.relational_proxy.get_all_supported_devices()

    def getData(self, measurement, user, start, end, interval):
        """
        Method used to read from the time_series database.

        :param measurement: which measurement to get from database
        :type measurement: str
        :param user: username of the client
        :type user: str
        :param start: values after this time (seconds)
        :type start: int
        :param end: values before this time (seconds)
        :type end: int
        :param interval: size of interval like influx (ns, u, ms, s, m, h, d, w)
        :type interval: str
        :return: {
                    time:[],
                    value:[],
                    lat:[],
                    long:[],
                    hearth_rate:[],calories:[],...
                 }
        :rtype: dict
        """
        data = {}

        if measurement == "sleep":
            if not start and not end: #both None last
                results = self.relational_proxy.get_sleep_sessions(user)
            elif start: # just end None  from start
                start_date = datetime.date.fromtimestamp(start)
                results = self.relational_proxy.get_sleep_sessions(user, start_date)
            else: # within
                start_date = datetime.date.fromtimestamp(start)
                end_date = datetime.date.fromtimestamp(end)
                results = self.relational_proxy.get_sleep_sessions(user, start_date, end_date)

            return_value = {
                "sessions_info": [], # list of dicts
                "sessions_data": [] # list of dicts [{time:[...], level:[...], duration:[...]},{X},...]
            }
            for day, sleep_begin, sleep_end, duration in results:
                return_value["sessions_info"].append({
                    "day": day,
                    "begin": sleep_begin,
                    "end": sleep_end,
                    "duration": duration
                })
                session_data = {}
                for read in self.time_series_proxy.read(user, measurement, sleep_begin, sleep_end):
                    for key, value in read.items():
                        if key == "username":
                            continue
                        if key not in session_data.keys():
                            session_data[key] = []

                        session_data[key].append(value)
                return_value["sessions_data"].append(session_data)

            return return_value

        none_count = {}
        values_count = 0
        for read in self.time_series_proxy.read(user, measurement, start, end, interval):
            values_count += 1

            for key, value in read.items():
                if key == "username":
                    continue
                if key not in data.keys():
                    data[key] = []
                    none_count[key] = 0

                data[key].append(value)
                if not value:
                    none_count[key] += 1

        for key, count in none_count.items():
            if count == values_count:
                del data[key]

        return data

    #def getData(self): #TODO all db data
    #    """"""

    def insert(self, measurement, data, user):
        """

        :param measurement:
        :type measurement: str
        :param data:
        :type data: list or dict
        :param user: username of the client
        :type user: str
        """

        if measurement == "sleep":
            if type(data) != list:
                raise TypeError("list was expected received ", type(data))


            self.relational_proxy.insert_sleep_session(user,
                                                       data["day"], #TODO may receive, Agree format
                                                       data["duration"], #TODO agree format
                                                       data["begin"], #TODO may not be this key. Agree format
                                                       data["end"]) #TODO may not be this key. Agree format

            to_write = []
            for point in data["sleep"]:
                time = point["time"]
                del point["time"]

                to_write.append(
                    {
                        "measurement": measurement,
                        "time": time,
                        "tags": {
                            "username": user,
                        },
                        "fields": point
                    }
                )

            self.time_series_proxy.write(to_write)
        else:
            self.time_series_proxy.write(
                [{
                    "measurement": measurement,
                    "tags": {
                        "username": user,
                    },
                    "fields": data
                }]
            )
