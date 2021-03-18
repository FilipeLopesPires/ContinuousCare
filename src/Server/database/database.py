#!/usr/bin/python3

from database.time_series.proxy import *
from database.relational.proxy import *

from database.exceptions import ProxyException, InternalException, LogicException

import datetime
import time

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
        Register a user on the database

        :param data: common : [type:str, username:str, password:str, name:str, email:str]
            client : [health_number:str, birth_date: str dd-mm-yyyy, weight:float, height:float, additional_info:str]
            medic : [company: str, specialities:str]
        :type data: dict
        :return: the id for the new client/medic
        :rtype: int
        """
        try:
            if data["type"].lower() == "client":
                additional_info = data.get("additional_info")
                additional_info = None if not additional_info else additional_info #converts "" (empty string to None)
                return self.relational_proxy.register_client(
                    data["username"],
                    data["password"],
                    data["name"],
                    data["email"],
                    data["health_number"],
                    data.get("birth_date"),
                    data.get("weight"),
                    data.get("height"),
                    additional_info
                )
            elif data["type"].lower() == "medic":
                return self.relational_proxy.register_medic(
                    data["username"],
                    data["password"],
                    data["name"],
                    data["email"],
                    data.get("company"),
                    data.get("specialities")
                )
            else:
                raise Exception("Unkown type of user!")
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def verifyUser(self, data):
        """
        Verifies if the received credentials are correct

        :param data: keys : [username:str, password:str]
        :type data:  dict
        :return: true if credentials are ok, false otherwise
        :rtype: bool
        """
        try:
            return self.relational_proxy.check_credentials(
                data["username"],
                data["password"]
            )
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def updateProfile(self, user_type, user, data):
        """
        Updates the profile data of a client with the username received from the arguments

        :param user_type: user type
        :type user_type: str
        :param user: username of the client to update
        :type user: str
        :param data: common : [type:str, username:str, password:str, new_password:str name:str, email:str]
            client : [health_number:str, birth_date: str dd-mm-yyyy, weight:float, height:float, additional_info:str]
            medic : [company: str, specialities:str]
        :type data: dict
        """
        try:
            if user_type == "client":
                self.relational_proxy.update_client_profile_data(
                    user,
                    data.get("password"),
                    data.get("new_password"),
                    data["name"],
                    data["email"],
                    data["health_number"],
                    data.get("birth_date"),
                    data.get("weight"),
                    data.get("height"),
                    data.get("additional_info")
                )
            elif user_type == "medic":
                self.relational_proxy.update_medic_profile_data(
                    user,
                    data.get("password"),
                    data.get("new_password"),
                    data["name"],
                    data["email"],
                    data.get("company"),
                    data.get("specialities")
                )
            else:
                raise Exception("Unkown type of user!")
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def getProfile(self, user):
        """
        Gets all profile data associated with the username (user) in the arguments

        :param user: username of the client
        :type user: str
        :return: all profile data
        {client_id:int, full_name:str, email:str, health_number:int, birth_date:datetime, weight:float, height:float}
        :rtype: dict
        """
        try:
            return self.relational_proxy.get_user_profile_data(user)
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def getPatientProfile(self, medic, patient):
        """
        Allows a medic to get the additional information that the client
          inserted on his profile section

        :param medic: the one requesting
        :type medic: str
        :param patient: the one to get the information
        :type patient: str
        :return: keys: birth_date, height, weight, additional_info
        :rtype: dict
        """
        try:
            if not self.relational_proxy.has_permission(medic, patient):
                raise LogicException("You don't have permission to access this data")

            profile = self.relational_proxy.get_user_profile_data(patient)
            if "medic_id" in profile:
                return json.dumps({"status":1, "msg":"There is no patient with the given username."}).encode("UTF-8")

            for key in ["client_id", "full_name", "email", "health_number"]:
                del profile[key]

            return profile
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def getAllUsers(self):
        """
        Obtain all usernames of all clients registered on the system

        :return: all usernames of all clients
        :rtype: list
        """
        try:
            return self.relational_proxy.get_all_usernames()
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

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
        try:
            return self.relational_proxy.register_device(
                user,
                data["type"],
                data["authentication_fields"],
                data.get("latitude"),
                data.get("longitude")
            )
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def updateDevice(self, user, data):
        """
        Only used to change the authentications fields of some device of
        a client, the type can never change.

        :param user: username of the client
        :type user: str
        :param data: new data to associate with an existing device
        {id:int, token:asdf, ...}
        :type data: dict
        """
        try:
            device_id = data["id"]
            del data["id"]

            self.relational_proxy.updtate_device(user, device_id, data)
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def deleteDevice(self, user, device_id):
        """
        Deassociates a device from a user deleating associated infor with the device

        :param user: username of the client
        :type user: str
        :param device_id: id of the device to update
        :type device_id: int
        """
        try:
            self.relational_proxy.delete_device(user, device_id)
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def getAllDevices(self, user):
        """
        Get all devices associated with the client passed on the arguments

        :param user: username of the client to query
        :type user: str
        :return: all devices associated with the specific client
        [{device:int, type:int,  token:str}, ...]
        :rtype: list
        """
        try:
            return self.relational_proxy.get_all_devices_of_user(user)
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def getSupportedDevices(self):
        """
        Obtains all supported devices, that are integrated with the system,
        that the client can purchase/use

        :return: all supported devices by the system
        [{id:int, type:str, brand:str, model:str, metrics:[{name:str, unit:str}, ...]}, ...]
        :rtype: list
        """
        try:
            return self.relational_proxy.get_all_supported_devices()
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

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
        try:
            data = {}

            if measurement == "Sleep":
                if start is not None and end is not None: # within
                    start_date = datetime.date.fromtimestamp(start)
                    end_date = datetime.date.fromtimestamp(end)
                    results = self.relational_proxy.get_sleep_sessions(user, start_date, end_date)
                elif start is not None: # just end None -> from start to now
                    start_date = datetime.date.fromtimestamp(start)
                    results = self.relational_proxy.get_sleep_sessions(user, begin=start_date)
                elif end is not None: # just start None -> all from until end
                    end_date = datetime.date.fromtimestamp(start)
                    results = self.relational_proxy.get_sleep_sessions(user, end=end_date)
                else: #both None -> last
                    results = self.relational_proxy.get_sleep_sessions(user)

                return_value = []
                for day, sleep_begin, sleep_end, duration in results:
                    data = {
                        "info": {
                            "day": day.strftime("%d-%m-%Y"),
                            "begin": time.mktime(sleep_begin.timetuple()),
                            "end": time.mktime(sleep_end.timetuple()),
                            "duration": duration
                        }
                    }
                    session_data = {}
                    for read in self.time_series_proxy.read(user, measurement, sleep_begin.timestamp(),
                                                                               sleep_end.timestamp()):
                        for key, value in read.items():
                            if key == "username":
                                continue
                            if key not in session_data.keys():
                                session_data[key] = []

                            session_data[key].append(value)
                    data["data"] = session_data

                    return_value.append(data)

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
                    if value is None:
                        none_count[key] += 1

            for key, count in none_count.items():
                if count == values_count:
                    del data[key]

            return data
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def getDataByMedic(self, medic, measurement, client, start, end, interval):
        """
        Allows a medic to query a client's data
        First the server first verifies if the medic has permission to
            access that data, if he has retrives the data else raises an exception

        :param medic: username of the client
        :type medic: str
        :param measurement: which measurement to get from database
        :type measurement: str
        :param client: username of the client
        :type client: str
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
        :raises Exception: if the medic doesn't have permission
            to acess the client's data
        """
        try:
            if not self.relational_proxy.has_permission(medic, client):
                raise LogicException("You don't have permission to access this data")

            return self.getData(measurement, client, start, end, interval)
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    #def getData(self): #TODO all db data
    #    """"""

    def insert(self, measurement, data, user):
        """
        Inserts new data to the influx database. This is historical data retrived from
        devices or external apis.

        :param measurement: nome of the measument to where to write the values
        :type measurement: str
        :param data: several fields to write
        :type data: dict
        :param user: username of the client
        :type user: str
        """
        try:
            if measurement == "Sleep":

                self.relational_proxy.insert_sleep_session(user,
                    data["day"],
                    data["duration"],
                    datetime.datetime.fromtimestamp(data["begin"]),
                    datetime.datetime.fromtimestamp(data["end"]))

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
                time = data["time"]
                del data["time"]
                if data == {}:
                    return
                self.time_series_proxy.write(
                    [{
                        "measurement": measurement,
                        "time":time,
                        "tags": {
                            "username": user,
                        },
                        "fields": data
                    }]
                )
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def delete(self, measurement, time, user):
        """
        Deletes a value from the time series database
         associated with a given user and measurement
         on a given time

        :param measurement: from where to delete
        :type measurement: str
        :param time: timestamp
        :type time: int
        :param user: of the client
        :type user: str
        """
        self.time_series_proxy.delete(user, measurement, time)

    def requestPermission(self, medic, data):
        """
        A medic requests temporary permission to see a client's data

        :param medic: username of the medic
        :type medic: str
        :param data: keys : {username: str, health_number: int, duration: int}
        :type data: dict
        :return: information of source and destination intervenients of the permission
        :rtype: (dict, dict)
        """
        try:
            return self.relational_proxy.request_permission(
                medic,
                data.get("username"),
                data.get("health_number"),
                datetime.timedelta(minutes=int(data["duration"])))
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def deleteRequestPermission(self, medic, client):
        """
        Allows a medic to delete a request permission done previously

        :param medic: username of the medic
        :type medic: str
        :param client: username of the client
        :type client: str
        """
        self.relational_proxy.delete_request_permission(medic, client)

    def grantPermission(self, client, data):
        """
        A clients grants temporary permission to a medic to let him see his data

        :param client: username of the client
        :type client: str
        :param data: keys : {username:str, duration: int}
        :type data: dict
        :return: information of source and destination intervenients of the permission
        :rtype: (dict, dict)
        """
        try:
            return self.relational_proxy.grant_permission(
                client,
                data["username"],
                datetime.timedelta(minutes=int(data["duration"])))
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def acceptPermission(self, client, medic):
        """
        A client accepts a pending request created by a medic to see his data

        :param client: username of the client
        :type client: str
        :param medic: username of the medic
        :type medic: str
        """
        try:
            self.relational_proxy.accept_permission(client, medic)
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def removeAcceptedPermission(self, client, medic):
        """
        Allows a client to delete an accepted
        permission

        :param client: username of the client
        :type client: str
        :param medic: username of the medic
        :type medic: str
        """
        try:
            self.relational_proxy.remove_accepted_permission(client, medic)
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def rejectPermission(self, client, medic):
        """
        A client rejects a pending request created by a medic to see his data

        :param client: username of the client
        :type client: str
        :param medic: username of the medic
        :type medic: str
        """
        try:
            self.relational_proxy.reject_permission(client, medic)
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def getPendingPermissions(self, user):
        """
        Used internally by the server

        :param user: username of the USER (can be both client and medic)
        :param user: str
        :return: pending permissions
        :return: list
        """
        try:
            return self.relational_proxy.get_pending_permissions(user)
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))

    def allPermissionsData(self, user):
        """
        Used by both medic and client

        :param user: username of the USER (can be both client and medic)
        :param user: str
        :return: three lists concerning the three types of permissions (pending, accepted and expired)
        :return: dict
        """
        try:
            return self.relational_proxy.get_all_permissions_data(user)
        except (InternalException, LogicException):
            raise
        except Exception as e:
            raise ProxyException(str(e))
