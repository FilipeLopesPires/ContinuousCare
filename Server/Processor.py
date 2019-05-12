import json
import asyncio
import logging
import string
import threading
import time
from datetime import datetime, timedelta
from math import sqrt
from random import *

import requests
from geopy.distance import vincenty

from validation import ArgumentValidator

from database import *
from database.exceptions import DatabaseException, LogicException
from devices import *

from WebSocket import WebSocket

'''
Component responsable for doing all the information gathering and processing, scheduling all necessary operations.
Is this component that is also responsable for answering all the requests that may come form the API.

error codes
 0 - successfull
-1 - internal error - database or server
 1 - logical error - i.e. username already exists. Important to show on the web page
 2 - arguments error - missing arguments
 3 - unauthorized error - user uses a path that he doesn't have access
 4 - authentication error - invalid token
'''


RADIUS=50       #variable that defines the distance from the personal home device the system should consider its information instead of the external one


class Processor:

    def __init__(self):
        self.socket = WebSocket("0.0.0.0", 5678, self)
        self.socket.start()
        self.database=database.Database()
        self.externalAPI=ExternalAPI("","","","",None, None).metrics
       
        self.userThreads={}
        self.clientTokens={}
        self.medicTokens={}
        self.userMetrics={}
        allUsers=self.database.getAllUsers()
        for user in allUsers:
            metrics={}   #{GPS: [metric], HealthStatus: [metric, metric], Sleep:[metric]}
            userDevices=self.database.getAllDevices(user)
            for device in userDevices:
                deviceType=device["type"].strip().replace(" ", "_")
                userDevice=eval(deviceType+"(\""+device.get("token","")+"\",\""+device.get("refresh_token","")+"\",\""+device.get("uuid","")+"\",\""+user+"\",\""+str(device.get("id", ""))+"\", ["+str(device.get("latitude",str(None)))+","+str(device.get("longitude", str(None)))+"])")
                for metric in userDevice.metrics:    
                    if metric.metricType not in metrics:
                        metrics[metric.metricType]=[]
                    metrics[metric.metricType].append(metric)

            for metric in GPS("","","",user,None, None).metrics+self.externalAPI:
                if metric.metricType not in metrics:
                    metrics[metric.metricType]=[]
                metrics[metric.metricType].append(metric)

            self.userMetrics[user]=metrics

            #print(metrics)

            #passing only the GPS, HealthStatus and Sleep to the Thread
            self.userThreads[user]=myThread(self, {k:v for k,v in metrics.items() if k in ["GPS", "HealthStatus", "Sleep"]},user)
            self.userThreads[user].start()


        #urls["https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json"]=[{"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRLMlgiLCJzdWIiOiI3Q05RV1oiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJudXQgcnBybyByc2xlIiwiZXhwIjoxNTUzODAxNjA5LCJpYXQiOjE1NTM3NzI4MDl9.6_hSXgYG36430e-ZaRfcEYSzDezGJeaMF5R2PiSr4bk"}, 1]
        #urls["http://api.foobot.io/v2/device/240D676D40002482/datapoint/10/last/0/"]=[{"Accept":"application/json;charset=UTF-8","X-API-KEY-TOKEN":"eyJhbGciOiJIUzI1NiJ9.eyJncmFudGVlIjoiam9hby5wQHVhLnB0IiwiaWF0IjoxNTUyMDY2Njc5LCJ2YWxpZGl0eSI6LTEsImp0aSI6IjRiNmY2NzhiLWJjNTYtNDYxNi1hYmMyLTRiNjlkMTNkMjUzOSIsInBlcm1pc3Npb25zIjpbInVzZXI6cmVhZCIsImRldmljZTpyZWFkIl0sInF1b3RhIjoyMDAsInJhdGVMaW1pdCI6NX0.aeLLsrhh1-DVXSwl-Z_qDx1Xbr9oIid1IKsOyGQxwqQ"},1]


    def signup(self, jsonData):
        try:
            self.database.register(jsonData)

            if jsonData["type"] == "client":
                user=jsonData["username"]
                if user not in self.userMetrics:
                    self.userMetrics[user]={}

                    for metric in GPS("","","", user, None, None).metrics+self.externalAPI:
                        if metric.metricType not in self.userMetrics[user]:
                            self.userMetrics[user][metric.metricType]=[]
                        self.userMetrics[user][metric.metricType].append(metric)

                    self.userThreads[user]=myThread(self, {k:v for k, v in self.userMetrics[user].items() if k in ["GPS", "HealthStatus", "Sleep"]},user)
                    self.userThreads[user].start()

            return json.dumps({"status":0, "msg":"Successfull operation."}).encode("UTF-8")
        except LogicException as e:
            return json.dumps({"status":1, "msg":str(e)}).encode("UTF-8")
        except DatabaseException as e:
            return json.dumps({"status":-1, "msg":str(e)}).encode("UTF-8")
        except Exception as e:
            return json.dumps({"status":-1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def logout(self, token):
        client = self.clientTokens.get(token, None)
        medic = self.medicTokens.get(token, None)
        if not client and not medic:
            return  json.dumps({"status":4, "msg":"Invalid Token."}).encode("UTF-8")
        elif client:
            del self.clientTokens[token]
        elif medic:
            del self.medicTokens[token]

        return json.dumps({"status":0 , "msg":"Successfull operation."}).encode("UTF-8")

    def _generateToken(self, tokenMap, username):
        """
        Generates a new token for a user and stores it

        :param tokenMap: self.clientTokens or self.medicTokens
        :type tokenMap: dict
        :param username: of the user loggedin
        :type username: str
        :return: the new token
        :rtype: str
        """
        min_char = 30
        max_char = 40
        allchar = string.ascii_letters + string.digits

        token = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
        while token in tokenMap:
            token = "".join(choice(allchar) for x in range(randint(min_char, max_char)))

        aux=tokenMap.copy()
        for t, n in aux.items():
                if n==username:
                    self.socket.delToken(t)
                    del tokenMap[t]
        tokenMap[token] = username

        return token

    def signin(self, jsonData):
        userType = self.database.verifyUser(jsonData)

        if userType == 0: # invalid login
            return json.dumps({"status":1, "msg":"Incorrect username or password."}).encode("UTF-8")

        elif userType == 1: # valid login and user is a client
            token = self._generateToken(self.clientTokens, jsonData["username"])
        elif userType == 2: # valid login and user is a medic
            token = self._generateToken(self.medicTokens, jsonData["username"])

        return json.dumps({"status":0 , "msg":"Successfull operation.", "data":{"token":token}}).encode("UTF-8")

    def getAllDevices(self, token):
        if self.medicTokens.get(token):
            return  json.dumps({"status":1, "msg":"Medic users don't have devices associated."}).encode("UTF-8")

        user = self.clientTokens.get(token, None)
        if not user:
            return  json.dumps({"status":1, "msg":"Invalid Token."}).encode("UTF-8")

        try:
            devices=self.database.getAllDevices(user)
        except LogicException as e:
            return json.dumps({"status":1, "msg":str(e)}).encode("UTF-8")
        except DatabaseException as e:
            return json.dumps({"status":-1, "msg":str(e)}).encode("UTF-8")

        return json.dumps({"status":0 , "msg":"Successfull operation.", "data":devices}).encode("UTF-8")

    def updateDevice(self, token, deviceConf):
        if self.medicTokens.get(token):
            return  json.dumps({"status":3, "msg":"Medic users don't have devices associated."}).encode("UTF-8")

        user = self.clientTokens.get(token, None)
        if not user:
            return  json.dumps({"status":4, "msg":"Invalid Token."}).encode("UTF-8")

        try:
            userDevices={submetric.dataSource for metric in self.userMetrics[user] for submetric in self.userMetrics[user][metric]}
            for device in userDevices:
                if device.id==str(deviceConf["id"]):
                    deviceId=device.id
                    deviceToken=deviceConf["authentication_fields"]["token"] if "authentication_fields" in deviceConf and "token" in deviceConf["authentication_fields"] else device._token
                    deviceRefreshToken=deviceConf["authentication_fields"]["refresh_token"] if "authentication_fields" in deviceConf and "refresh_token" in deviceConf["authentication_fields"] else device._refreshToken
                    deviceUUID=deviceConf["authentication_fields"]["uuid"] if "authentication_fields" in deviceConf and "uuid" in deviceConf["authentication_fields"] else device._uuid
                    latitude=deviceConf["latitude"] if "latitude" in deviceConf else device._location[0]
                    longitude=deviceConf["longitude"] if "longitude" in deviceConf else device._location[1]
                    device.update(deviceToken,deviceRefreshToken, deviceUUID, user, deviceId, [latitude, longitude])
                    if user in self.userThreads:
                        self.userThreads[user].end()
                    self.userThreads[user]=myThread(self, {k:v for k, v in self.userMetrics[user].items() if k in ["GPS", "HealthStatus", "Sleep"]},user)
                    self.userThreads[user].start()
            result=self.database.updateDevice(user, deviceConf)
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data": result}).encode("UTF-8")
        except LogicException as e:
            return json.dumps({"status":1, "msg":str(e)}).encode("UTF-8")
        except DatabaseException as e:
            return  json.dumps({"status":-1, "msg":str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":-1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")


    def deleteDevice(self, token, data):
        if self.medicTokens.get(token):
            return  json.dumps({"status":3, "msg":"Medic users don't have devices associated."}).encode("UTF-8")

        user = self.clientTokens.get(token, None)
        if not user:
            return  json.dumps({"status":4, "msg":"Invalid Token."}).encode("UTF-8")

        try:
            deviceId=data["id"]
            for metric in self.userMetrics[user]:
                for submetric in self.userMetrics[user][metric]:
                    if submetric.dataSource.id == deviceId:
                        self.userMetrics[user][metric].remove(submetric)
                
            result=self.database.deleteDevice(user, deviceId)
            if user in self.userThreads:
                self.userThreads[user].end()
            self.userThreads[user]=myThread(self, {k:v for k, v in self.userMetrics[user].items() if k in ["GPS", "HealthStatus", "Sleep"]},user)
            self.userThreads[user].start()

            return json.dumps({"status":0 , "msg":"Successfull operation.", "data": result}).encode("UTF-8")
        except LogicException as e:
            return json.dumps({"status":1, "msg":str(e)}).encode("UTF-8")
        except DatabaseException as e:
            return  json.dumps({"status":-1, "msg":str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":-1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def addDevice(self, token, jsonData):
        if self.medicTokens.get(token):
            return  json.dumps({"status":3, "msg":"Medic users don't have devices associated."}).encode("UTF-8")

        user = self.clientTokens.get(token, None)
        if not user:
            return  json.dumps({"status":4, "msg":"Invalid Token."}).encode("UTF-8")

        try:
            id=str(self.database.addDevice(user, jsonData))
            print(id)

            if id not in [submetric.dataSource.id for metric in self.userMetrics[user] for submetric in self.userMetrics[user][metric]]:
                deviceType=jsonData["type"].strip().replace(" ", "_")
                device=eval(deviceType+"(\""+jsonData["authentication_fields"].get("token","")+"\",\""+jsonData["authentication_fields"].get("refresh_token","")+"\",\""+jsonData["authentication_fields"].get("uuid","")+"\",\""+user+"\",\""+str(id)+"\", ["+jsonData.get("latitude",str(None))+","+jsonData.get("longitude", str(None))+"])")
                for metric in device.metrics:
                    if metric.metricType not in self.userMetrics[user]:
                        self.userMetrics[user][metric.metricType]=[]
                    self.userMetrics[user][metric.metricType].append(metric)


                print(self.userMetrics)
                if user in self.userThreads:
                    self.userThreads[user].end()
                self.userThreads[user]=myThread(self, {k:v for k, v in self.userMetrics[user].items() if k in ["GPS", "HealthStatus", "Sleep"]},user)
                self.userThreads[user].start()


            
            return json.dumps({"status":0 , "msg":"Successfull operation."}).encode("UTF-8")
        except LogicException as e:
            return json.dumps({"status":1, "msg":str(e)}).encode("UTF-8")
        except DatabaseException as e:
            return  json.dumps({"status":-1, "msg":str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":-1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def getData(self, token, endpoint, start, end, interval, patient):
        client = self.clientTokens.get(token, None)
        medic = self.medicTokens.get(token, None)
        if not client and not medic:
            return  json.dumps({"status":2, "msg":"Invalid Token."}).encode("UTF-8")

        try:
            if client:
                values = self.database.getData(endpoint, client, start, end, interval)
            elif medic:
                if endpoint == "Path":
                    return json.dumps({"status":4, "msg":"Only accecible to patitents."}).encode("UTF-8")

                if not patient:
                    return json.dumps({"status":2, "msg":"Missing argument \"patient\""}).encode("UTF-8")

                values = self.database.getDataByMedic(medic, endpoint, patient, start, end, interval)
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data":values}).encode("UTF-8")
        except LogicException as e:
            return json.dumps({"status":1, "msg":str(e)}).encode("UTF-8")
        except DatabaseException as e:
            return  json.dumps({"status":-1, "msg":str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":-1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def updateProfile(self, token, data):
        client = self.clientTokens.get(token, None)
        medic = self.medicTokens.get(token, None)
        if not client and not medic:
            return json.dumps({"status":4, "msg":"Invalid Token."}).encode("UTF-8")
        elif client:
            user = client
        elif medic:
            user = medic

        argsErrors = ArgumentValidator.signupAndUpdateProfile(True if client else False, True, data)
        if len(argsErrors) > 0:
            return json.dumps({"status":2, "msg":"Argument errors : " + ", ".join(argsErrors)}).encode("UTF-8")

        try:
            self.database.updateProfile("client" if client else "medic", user, data)
            return json.dumps({"status":0 , "msg":"Successfull operation."}).encode("UTF-8")
        except LogicException as e:
            return json.dumps({"status":1, "msg":str(e)}).encode("UTF-8")
        except DatabaseException as e:
            return  json.dumps({"status":-1, "msg":str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":-1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def getProfile(self, token):
        client = self.clientTokens.get(token, None)
        medic = self.medicTokens.get(token, None)
        if not client and not medic:
            return json.dumps({"status":4, "msg":"Invalid Token."}).encode("UTF-8")
        elif client:
            user = client
        elif medic:
            user = medic

        try:
            profile=self.database.getProfile(user)
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data": profile}).encode("UTF-8")
        except LogicException as e:
            return json.dumps({"status":1, "msg":str(e)}).encode("UTF-8")
        except DatabaseException as e:
            return  json.dumps({"status":-1, "msg":str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":-1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def deleteProfile(self, token):
        client = self.clientTokens.get(token, None)
        medic = self.medicTokens.get(token, None)
        if not client and not medic:
            return json.dumps({"status":4, "msg":"Invalid Token."}).encode("UTF-8")
        elif client:
            user = client
        elif medic:
            user = medic

        try:
            self.database.deleteProfile(user)
            return json.dumps({"status":0 , "msg":"Successfull operation."}).encode("UTF-8")
        except LogicException as e:
            return json.dumps({"status":1, "msg":str(e)}).encode("UTF-8")
        except DatabaseException as e:
            return  json.dumps({"status":-1, "msg":str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":-1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def getSupportedDevices(self):
        try:
            values=self.database.getSupportedDevices()
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data":values}).encode("UTF-8")
        except LogicException as e:
            return json.dumps({"status":1, "msg":str(e)}).encode("UTF-8")
        except DatabaseException as e:
            return  json.dumps({"status":-1, "msg":str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":-1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def uploadPermission(self, token, jsonData):
        """
        Use by both medic and client
        grants/requests for a permission. calls 'grantPermission' and 'requestPermission' on database.py

        args:
        username - str - of the user the he wants to grant or request permission
        data - {username:str, health_number: int, duration: int}
        """
        client = self.clientTokens.get(token, None)
        medic = self.medicTokens.get(token, None)
        if not client and not medic:
            return json.dumps({"status":4, "msg":"Invalid Token."}).encode("UTF-8")

        argsErrors = ArgumentValidator.uploadPermissions("medic" if medic else "client", jsonData)
        if len(argsErrors) > 0:
            return json.dumps({"status":2, "msg":"Argument errors : " + ", ".join(argsErrors)}).encode("UTF-8")

        try:
            target = jsonData["username"]
            targetToken=None
            for (k1, v1), (k2,v2) in zip(self.medicTokens.items(), self.clientTokens.items()):
                if v1==target or v2==target:
                    targetToken = (k1 if v1==target else k2) 

            if client:
                data = self.database.grantPermission(client, jsonData)
            elif medic:
                data = self.database.requestPermission(medic, jsonData)
        
            permissionThread(data, targetToken, self.socket).start()

            return json.dumps({"status":0 , "msg":"Successfull operation.", "data":data}).encode("UTF-8")
        except LogicException as e:
            return json.dumps({"status":1, "msg":str(e)}).encode("UTF-8")
        except DatabaseException as e:
            return  json.dumps({"status":-1, "msg":str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":-1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")


    def getAllPermissions(self, token):
        """
        Use by both medic and client
        gets all current permissions. calls 'allPermissionsData' on database.py
        """
        client = self.clientTokens.get(token, None)
        medic = self.medicTokens.get(token, None)
        if not client and not medic:
            return json.dumps({"status":4, "msg":"Invalid Token."}).encode("UTF-8")
        
        try:
            data = self.database.allPermissionsData(client if client else medic)
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data":data}).encode("UTF-8")
        except LogicException as e:
            return json.dumps({"status":1, "msg":str(e)}).encode("UTF-8")
        except DatabaseException as e:
            return  json.dumps({"status":-1, "msg":str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":-1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def acceptPermission(self, token, medic):
        """
        Used only by the client, accepts a pending permission

        args:
        token - str - token representing the user
        medic - str - of the medic that he wants to reject request for permission
        """
        if self.medicTokens.get(token):
            return json.dumps({"status":1, "msg":"Only accessible to patients"}).encode("UTF-8")

        client = self.clientTokens.get(token)
        if not client:
            return json.dumps({"status":4, "msg":"Invalid Token."}).encode("UTF-8")

        try:
            self.database.acceptPermission(client, medic)
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data":"Permission accepted with success."}).encode("UTF-8")
        except LogicException as e:
            return json.dumps({"status":1, "msg":str(e)}).encode("UTF-8")
        except DatabaseException as e:
            return  json.dumps({"status":-1, "msg":str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":-1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")


    def rejectPermission(self, token, medic):
        """
        Used only by the client, rejects a pending permission

        args:
        token - str - token representing the user
        medic - str - of the medic that he wants to reject request for permission
        """
        if self.medicTokens.get(token):
            return json.dumps({"status":1, "msg":"Only accessible to patients"}).encode("UTF-8")

        client = self.clientTokens.get(token)
        if not client:
            return json.dumps({"status":4, "msg":"Invalid Token."}).encode("UTF-8")

        try:
            self.database.rejectPermission(client, medic)
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data":"Permission rejected with success."}).encode("UTF-8")
        except LogicException as e:
            return json.dumps({"status":1, "msg":str(e)}).encode("UTF-8")
        except DatabaseException as e:
            return  json.dumps({"status":-1, "msg":str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":-1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def removePendingPermission(self, token, client):
        """
        Used only by the medic, removes a pending permission (requests not responded by the client)

        args
        token - str - token representing the user
        client - str - of the client that he wants to remove the active permission
        """
        if self.clientTokens.get(token):
            return json.dumps({"status":1, "msg":"Only accessible to medics"}).encode("UTF-8")

        medic = self.medicTokens.get(token)
        if not medic:
            return json.dumps({"status":4, "msg":"Invalid Token."}).encode("UTF-8")

        try:
            self.database.deleteRequestPermission(medic, client)
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data":"Permission removed with success."}).encode("UTF-8")
        except LogicException as e:
            return json.dumps({"status":1, "msg":str(e)}).encode("UTF-8")
        except DatabaseException as e:
            return  json.dumps({"status":-1, "msg":str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":-1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def removeAcceptedPermission(self, token, medic):
        """
        Used only by the client, removes an accepted permission

        args
        token - str - token representing the user
        username - str - of the medic that he wants to remove an accepted permission
        """
        if self.medicTokens.get(token):
            return json.dumps({"status":1, "msg":"Only accessible to patients"}).encode("UTF-8")

        client = self.clientTokens.get(token)
        if not client:
            return json.dumps({"status":4, "msg":"Invalid Token."}).encode("UTF-8")

        try:
            self.database.removeAcceptedPermission(client, medic)
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data":"Permission removed with success."}).encode("UTF-8")
        except LogicException as e:
            return json.dumps({"status":1, "msg":str(e)}).encode("UTF-8")
        except DatabaseException as e:
            return  json.dumps({"status":-1, "msg":str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":-1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def process(self, responses, user):
        normalData={}
        for resp in responses:
            metric=resp[0]
            if metric not in normalData:
                normalData[metric]={}
            normalData[metric]=dict(normalData[metric], **resp[1])


        if "GPS" in normalData:
            envMetrics=[submetric for metric in self.userMetrics[user] for submetric in self.userMetrics[user][metric] if submetric.metricType=="Environment"]
            if normalData["GPS"]["latitude"]!=None and normalData["GPS"]["longitude"]!=None:
                if float(normalData["GPS"]["latitude"])>-90 and float(normalData["GPS"]["latitude"])<90 and float(normalData["GPS"]["longitude"])>-180 and float(normalData["GPS"]["longitude"])<180: 
                    for metric in [metric for metric in envMetrics if metric.metricLocation=="inside"]:    
                        distance=round(vincenty([float(normalData["GPS"]["latitude"]), float(normalData["GPS"]["longitude"])], metric.dataSource.location).m)
                        if distance <= RADIUS:
                            try:
                                jsonData=metric.getData()
                                data=metric.normalizeData(jsonData)
                                normalData["Environment"]=dict(normalData["Environment"], **data)
                            except Exception as e:
                                logging.error("<"+user+">Exception caught while refetching the data: "+str(e))
                                try:
                                    tokens=metric.dataSource.refreshToken()
                                    self.updateDevice(metric.dataSource.user, {"id":metric.dataSource.id, "token":tokens["token"],"refresh_token":tokens["refresh_token"]})
                                    resp=metric.normalizeData(metric.getData())
                                    normalData["Environment"]=dict(normalData["Environment"], **data)
                                except Exception as e:
                                    logging.error("<"+user+">Tried to refresh tokens and couldn't, caught error: "+str(e))
                    if normalData["Environment"]=={}:
                        for metric in [metric for metric in envMetrics if metric.metricLocation=="outside"]:
                            try:
                                jsonData=metric.getData()
                                data=metric.normalizeData(jsonData)
                                normalData["Environment"]=dict(normalData["Environment"], **data)
                            except Exception as e:
                                logging.error("<"+user+">Exception caught while refetching the data: "+str(e))
                                try:
                                    tokens=metric.dataSource.refreshToken()
                                    self.updateDevice(metric.dataSource.user, {"id":metric.dataSource.id, "token":tokens["token"],"refresh_token":tokens["refresh_token"]})
                                    resp=metric.normalizeData(metric.getData())
                                    normalData["Environment"]=dict(normalData["Environment"], **data)
                                except Exception as e:
                                    logging.error("<"+user+">Tried to refresh tokens and couldn't, caught error: "+str(e))
                    #print(normalData["GPS"])
                    normalData["Environment"]["latitude"]=normalData["GPS"]["latitude"]
                    normalData["Environment"]["longitude"]=normalData["GPS"]["longitude"]

            else:
                logging.error("Couldn't process GPS: "+ str(normalData["GPS"]))

            del normalData["GPS"]

        try: 
            coords=self.userMetrics[user]["GPS"][0].normalizeData(self.userMetrics[user]["GPS"][0].getData())
            responses.append(("Path", {"path":coords}))
            for metric in normalData:
                if metric!="Environment":
                    normalData[metric]["latitude"]=coords["latitude"]
                    normalData[metric]["longitude"]=coords["longitude"]
        except Exception as e:
            logging.error("<"+user+">Error while fetching GPS Coordinates. "+str(e))


        for metric in normalData:
            if time not in normalData[metric]:
                normalData[metric]["time"]=int(time.time())

        print(normalData)
        try: 
            self._save(normalData, user)
        except Exception as e:
            logging.error("<"+user+">Error while saving data. "+str(e))

    def registerMood(self, token, data):
        user=self.clientTokens.get(token)
        if not user:
            return json.dumps({"status":4, "msg":"Invalid Token."}).encode("UTF-8")
        if data=={}:
            return  json.dumps({"status":2, "msg":"No moods were passed to register."}).encode("UTF-8")
        moods=data["moods"]
        concatMoods="moods[0]"
        allMoods={}
        for m in moods:
            allMoods[m]="PersonalStatus"
            concatMoods+=m+","
        try: 
            self.process([("PersonalStatus", {"moods":concatMoods[:-1]}),("Event", allMoods)], user)
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data":"Mood(s) registered with success."}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":-1, "msg":"While saving data.Database internal error. "+str(e)}).encode("UTF-8")
        
    
    def _save(self, data, user):
        try:
            for key in data:
                self.database.insert(key, data[key], user)
        except Exception as e:
            raise e


    def end(self):
        for k in self.userThreads:
            self.userThreads[k].end()
        return ""

    def checkPermissions(self, token):
        client = self.clientTokens.get(token, None)
        medic = self.medicTokens.get(token, None)
        if not client and not medic:
            logging.error("Invalid Token in check permissions of " + client if client else medic)
            return
        try:
            data = self.database.getPendingPermissions(client if client else medic)
            permissionThread(data, token, self.socket).start()
        except DatabaseException as e:
            logging.error("Database error in check permissions of " + client if client else medic+" -> "+str(e))
            return
        except Exception as e:
            print(e)
            logging.error("Server error in check permissions of " + client if client else medic+" -> "+str(e))
            return
        

class permissionThread(threading.Thread):

    def __init__(self, permissions, token, socket):
        threading.Thread.__init__(self)
        self.permissions=permissions
        self.socket=socket
        self.token=token

    def run(self):
        loop = asyncio.new_event_loop()  
        asyncio.set_event_loop(loop)
        asyncio.get_event_loop().run_until_complete(self.send())  
        asyncio.get_event_loop().close() 

    async def send(self):
        await self.socket.send(str(self.permissions), self.token)
    

class myThread (threading.Thread):
    def __init__(self, processor, urls, user):
        threading.Thread.__init__(self)
        self.processor=processor
        self.user=user
        self.urls=urls
        self.deltaTimes=[(timedelta(minutes=submetric.updateTime),submetric) for metric in urls for submetric in urls[metric] if submetric.updateTime>0]
        self.running=True
        print(self.deltaTimes)


    def run(self):
        now=datetime.now().replace(microsecond=0)
        old_times=[now for x in range(len(self.deltaTimes))]
        print("started")
        while self.running:
            now1=datetime.now().replace(microsecond=0)
            updating=[now1-old >= delta[0] for old,delta in zip(old_times, self.deltaTimes)]
            if any(updating):
                print(updating)
                responses=[]
                allEvents={}
                for i,v in enumerate(updating):
                    if v:
                        try:
                            old_times[i]=now1
                            resp=self.deltaTimes[i][1].getData()
                            normalMetric=self.deltaTimes[i][1].normalizeData(resp)
                            event=self.deltaTimes[i][1].checkEvent(resp)
                            if event:
                                eventInfo=""
                                for key,item in normalMetric.items():
                                    eventInfo+=str(key)+","+str(item)+"/"
                                allEvents[event]=normalMetric[:-1]
                            responses.append((self.deltaTimes[i][1].metricType, normalMetric))
                        except Exception as e:
                            logging.error("<"+self.user+">Exception caught: "+str(e))
                            try:
                                tokens=self.deltaTimes[i][1].dataSource.refreshToken()
                                self.processor.database.updateDevice(self.deltaTimes[i][1].dataSource.user, {"id":self.deltaTimes[i][1].dataSource.id, "token":tokens["token"],"refresh_token":tokens["refresh_token"]})
                                resp=self.deltaTimes[i][1].getData()
                                normalMetric=self.deltaTimes[i][1].normalizeData(resp)
                                event=self.deltaTimes[i][1].checkEvent(normalMetric)
                                if event:
                                    eventInfo=""
                                for key,item in normalMetric.items():
                                    eventInfo+=str(key)+","+str(item)+"/"
                                allEvents[event]=normalMetric[:-1]
                                responses.append((self.deltaTimes[i][1].metricType, normalMetric))
                            except DatabaseException as e:
                                logging.error("<"+self.user+">Tried to refresh tokens and couldn't, caught error: "+str(e))
                            except Exception as e:
                                logging.error("<"+self.user+">Tried to refresh tokens and couldn't, caught error: "+str(e))

                if allEvents!={}:
                    responses.append(("Event", allEvents)) 
                self.processor.process(responses, self.user)
        print("ended")
      
    def end(self):
        self.running=False



'''

refresh FITBIT Token

assume response

jsonData=json.loads(response.text)
if jsonData["success"] == False and jsonData[errors][0][errorType]=="expired_token":
    refresh



header={"Authorization": "Basic MjJESzJYOjUyNDRmZjEwNzliMTZlODQ4ZGE1YWI1NTc3ZDg5YzVl", "Content-Type": "application/x-www-form-urlencoded"}
data={"grant_type":"refresh_token", "refresh_token": "167bc73c28c5fafc63aa0718d9a6e57d2d102512a344cb43f856479dd59012d4"}
a=requests.post("https://api.fitbit.com/oauth2/token", headers=header, data=data)
print(a.text)

'''
