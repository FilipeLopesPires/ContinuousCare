import requests
import json
import string
from random import *
import threading
from datetime import datetime, timedelta
from database import *
import logging
import time
import dateutil.parser as dp
from math import sqrt
from geopy.distance import vincenty
from devices import *

'''
Component responsable for doing all the information gathering and processing, scheduling all necessary operations.
Is this component that is also responsable for answering all the requests that may come form the API.
'''


RADIUS=50       #variable that defines the distance from the personal home device the system should consider its information instead of the external one


class Processor:

    def __init__(self):
        self.database=database.Database()
        self.externalAPI=ExternalAPI("","","","",None, None).metrics
       
        self.userThreads={}
        self.userTokens={}
        self.userMetrics={}
        allUsers=self.database.getAllUsers()
        for user in allUsers:
            metrics={}   #{GPS: [metric], HealthStatus: [metric, metric], Sleep:[metric]}
            userDevices=self.database.getAllDevices(user)
            for device in userDevices:
                deviceType=device["type"].strip().replace(" ", "_")
                metric=eval(deviceType+"("+device.get("token","")+","+device.get("refresh_token","")+","+device.get("uuid","")+","+user+","+str(device["id"])+", ["+device.get("latitude",None)+","+device.get("longitude", None)+"])")
                if metric.metricType not in metrics:
                    metrics[metric.metricType]=[]
                metrics[metric.metricType].append(metric)

            for metric in GPS("","","",user,None, None).metrics+self.externalAPI:
                if metric.metricType not in metrics:
                    metrics[metric.metricType]=[]
                metrics[metric.metricType].append(metric)

            self.userMetrics[user]=metrics

            print(metrics)

            #passing only the GPS, HealthStatus and Sleep to the Thread
            self.userThreads[user]=myThread(self, {k:v for k,v in metrics.items() if k in ["GPS", "HealthStatus", "Sleep"]},user)
            self.userThreads[user].start()


        #urls["https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json"]=[{"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRLMlgiLCJzdWIiOiI3Q05RV1oiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJudXQgcnBybyByc2xlIiwiZXhwIjoxNTUzODAxNjA5LCJpYXQiOjE1NTM3NzI4MDl9.6_hSXgYG36430e-ZaRfcEYSzDezGJeaMF5R2PiSr4bk"}, 1]
        #urls["http://api.foobot.io/v2/device/240D676D40002482/datapoint/10/last/0/"]=[{"Accept":"application/json;charset=UTF-8","X-API-KEY-TOKEN":"eyJhbGciOiJIUzI1NiJ9.eyJncmFudGVlIjoiam9hby5wQHVhLnB0IiwiaWF0IjoxNTUyMDY2Njc5LCJ2YWxpZGl0eSI6LTEsImp0aSI6IjRiNmY2NzhiLWJjNTYtNDYxNi1hYmMyLTRiNjlkMTNkMjUzOSIsInBlcm1pc3Npb25zIjpbInVzZXI6cmVhZCIsImRldmljZTpyZWFkIl0sInF1b3RhIjoyMDAsInJhdGVMaW1pdCI6NX0.aeLLsrhh1-DVXSwl-Z_qDx1Xbr9oIid1IKsOyGQxwqQ"},1]

    #REAL THING

    def signup(self, data):
        jsonData=json.loads(data.decode("UTF-8"))
        try:
            self.database.register(jsonData)
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
        except Exception as e:
            return json.dumps({"status":1, "msg":"Database internal error. "+str(e)}).encode("UTF-8")

    def logout(self, token):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "msg":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        if self.userTokens==user:
            del self.userTokens[token]
            return json.dumps({"status":0 , "msg":"Successfull operation."}).encode("UTF-8")
        return  json.dumps({"status":1, "msg":"Something went wrong logging out."}).encode("UTF-8")

    def signin(self, data):
        min_char = 30
        max_char = 40
        allchar = string.ascii_letters + string.digits
        token = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
        while token in self.userTokens:
            token = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
        

        jsonData=json.loads(data.decode("UTF-8"))
        if self.database.verifyUser(jsonData):
            self.userTokens[token]=jsonData["username"]
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data":{"token":token}}).encode("UTF-8")
        return json.dumps({"status":1, "msg":"Incorrect username or password."}).encode("UTF-8")

    def getAllDevices(self, token):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "msg":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        devices=self.database.getAllDevices(user)
        return json.dumps({"status":0 , "msg":"Successfull operation.", "data":devices}).encode("UTF-8")

    def updateDevice(self, token, data): #!!!!!!!!!!!!!!update threads!!!!!!!!!!!!!
        if token not in self.userTokens:
            return  json.dumps({"status":1, "msg":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            result=self.database.updateDevice(user, json.loads(data.decode("UTF-8")))
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data": profile}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "msg":"Database internal error. "+str(e)}).encode("UTF-8")

    def addDevice(self, token, data):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "msg":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            jsonData=json.loads(data.decode("UTF-8"))


            deviceToken=jsonData["authentication_fields"]["token"]
            
            id=str(self.database.addDevice(user, jsonData))

            if jsonData["id"] not in [submetric.dataSource.id for metric in self.userMetrics[user] for submetric in self.userMetrics[user][metric]]:
                deviceType=jsonData["type"].strip().replace(" ", "_")
                metric=eval(deviceType+"("+device.get("token","")+","+device.get("refresh_token","")+","+device.get("uuid","")+","+user+","+str(id)+", ["+device.get("latitude",None)+","+device.get("longitude", None)+"])")
                if metric.metricType not in self.userMetrics[user]:
                    self.userMetrics[user][metric.metricType]=[]
                self.userMetrics[user][metric.metricType].append(metric)


                print(self.userMetrics)
                if user in self.userThreads:
                    self.userThreads[user].end()
                self.userThreads[user]=myThread(self, {k:v for k, v in self.userMetrics[user].items() if k in ["GPS", "HealthStatus", "Sleep"]},user)
                self.userThreads[user].start()


            
            return json.dumps({"status":0 , "msg":"Successfull operation."}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "msg":"Database internal error. "+str(e)}).encode("UTF-8")

    def getData(self, token, function, datatype, start, end, interval):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "msg":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            values=eval("self.database."+function)
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data":values}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "msg":"Database internal error. "+str(e)}).encode("UTF-8")
        return  json.dumps({"status":1, "msg":"Bad combination of arguments. It can only be start+end, start+interval or end+interval"}).encode("UTF-8")
                

    def updateProfile(self, token, data):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "msg":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            self.database.updateProfile(user, json.loads(data.decode("UTF-8")))
            return json.dumps({"status":0 , "msg":"Successfull operation."}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "msg":"Database internal error. "+str(e)}).encode("UTF-8")

    def getProfile(self, token):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "msg":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            profile=self.database.getProfile(user)
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data": profile}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "msg":"Database internal error. "+str(e)}).encode("UTF-8")

    def deleteProfile(self, token):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "msg":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            self.database.deleteProfile(user)
            return json.dumps({"status":0 , "msg":"Successfull operation."}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "msg":"Database internal error. "+str(e)}).encode("UTF-8")

    def getSupportedDevices(self):
        try:
            values=self.database.getSupportedDevices()
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data":values}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "msg":"Database internal error. "+str(e)}).encode("UTF-8")

    def process(self, responses, user):
        normalData={}
        errors={}
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
                                logging.error("Exception caught while refetching the data: "+str(e))
                                try:
                                    tokens=self.deltaTimes[i][1].dataSource.refreshToken()
                                    self.processor.database.updateDevice(metric.dataSource.user, {"id":metric.dataSource.id, "token":tokens["token"],"refresh_token":tokens["refresh_token"]})
                                    resp=self.deltaTimes[i][1].getData()
                                    data=metric.normalizeData(resp)
                                    normalData["Environment"]=dict(normalData["Environment"], **data)
                                except Exception as e:
                                    logging.error("Tried to refresh tokens and couldn't, caught error: "+str(e))
                    if normalData["Environment"]=={}:
                        for metric in [metric for metric in envMetrics if metric.metricLocation=="outside"]:
                            try:
                                jsonData=metric.getData()
                                data=metric.normalizeData(jsonData)
                                normalData["Environment"]=dict(normalData["Environment"], **data)
                            except Exception as e:
                                logging.error("Exception caught while refetching the data: "+str(e))
                                try:
                                    tokens=self.deltaTimes[i][1].dataSource.refreshToken()
                                    self.processor.database.updateDevice(metric.dataSource.user, {"id":metric.dataSource.id, "token":tokens["token"],"refresh_token":tokens["refresh_token"]})
                                    resp=self.deltaTimes[i][1].getData()
                                    data=metric.normalizeData(resp)
                                    normalData["Environment"]=dict(normalData["Environment"], **data)
                                except Exception as e:
                                    logging.error("Tried to refresh tokens and couldn't, caught error: "+str(e))
                    #print(normalData["GPS"])
                    normalData["Environment"]["latitude"]=normalData["GPS"]["latitude"]
                    normalData["Environment"]["longitude"]=normalData["GPS"]["longitude"]

            else:
                logging.error("Couldn't process GPS: "+ str(normalData["GPS"]))

            del normalData["GPS"]

        try: 
            coords=self.userMetrics[user]["GPS"][0].normalizeData(self.userMetrics[user]["GPS"][0].getData())
            for metric in normalData:
                if metric!="Environment":
                    normalData[metric]["latitude"]=coords["latitude"]
                    normalData[metric]["longitude"]=coords["longitude"]
        except Exception as e:
            logging.error("Error while fetching GPS Coordinates. "+str(e))


        for metric in normalData:
            if time not in normalData[metric]:
                normalData[metric]["time"]=int(time.time())

        print(normalData)
        self.save(normalData,user)
                        

    
    def save(self, data, user):
        try:
            for key in data:
                self.database.insert(key, data[key], user)
        except Exception as e:
            raise e


    def end(self):
        for k in self.userThreads:
            self.userThreads[k].end()
        return ""

    def getStartPath(self, device):
        for t in self.configFile:
            if device in self.configFile[t]:
                return t

    

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
                for i,v in enumerate(updating):
                    if v:
                        try:
                            old_times[i]=now1
                            resp=self.deltaTimes[i][1].getData()
                            responses.append((self.deltaTimes[i][1].metricType, resp))
                        except Exception as e:
                            logging.error("Exception caught: "+str(e))
                            try:
                                tokens=self.deltaTimes[i][1].dataSource.refreshToken()
                                self.processor.database.updateDevice(self.deltaTimes[i][1].dataSource.user, {"id":self.deltaTimes[i][1].dataSource.id, "token":tokens["token"],"refresh_token":tokens["refresh_token"]})
                                resp=self.deltaTimes[i][1].getData()
                                responses.append((self.deltaTimes[i][1].metricType, resp))
                            except Exception as e:
                                logging.error("Tried to refresh tokens and couldn't, caught error: "+str(e))
                        
                self.processor.process(responses, self.user)
            '''
            saving=[datetime.now()-old[1] > delta[1] for old,delta in zip(old_times, self.deltaTimes)]
            if any(saving):
                for i,v in enumerate(saving):
                    if v:
                        old_times[i][1]=datetime.now()
                        response=requests.get(self.urls[self.deltaTimes[i]]["url"], headers=self.urls[self.deltaTimes[i]]["header"])
                        self.processor.save(response.text, self.user)
            '''
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