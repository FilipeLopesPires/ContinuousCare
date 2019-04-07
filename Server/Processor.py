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

'''
Component responsable for doing all the information gathering and processing, scheduling all necessary operations.
Is this component that is also responsable for answering all the requests that may come form the API.
'''


RADIUS=50       #variable that defines the distance from the personal home device the system should consider its information instead of the external one


class Processor:

    def __init__(self):
        self.database=database.Database()
        self.configFile=json.loads(open("config.json").read().replace("\n", "").replace("\t", "").strip())
        self.supportedDevices=self.configFile["devices"]
        self.gps=self.configFile["GPS"]
        self.externalAPI={}   #{Environment: {WAQI:{header:header, metrics:{All:{url:url,updatetime:10}}}}, ...}
        auxAPI=self.configFile["externalAPI"]
        for api in auxAPI:
            for metric in auxAPI[api]["metrics"]:
                metricType=auxAPI[api]["metrics"][metric]["type"]
                if metricType not in self.externalAPI:
                    self.externalAPI[metricType]={}
                if api not in self.externalAPI[metricType]:
                    self.externalAPI[metricType][api]={"metrics":{}}
                    self.externalAPI[metricType][api]["header"]=auxAPI[api]["header"]
                    self.externalAPI[metricType][api]["location"]=auxAPI[api]["metrics"][metric]["location"]
            
                self.externalAPI[metricType][api]["metrics"][metric]={}
                self.externalAPI[metricType][api]["metrics"][metric]["url"]=auxAPI[api]["metrics"][metric]["url"]
                if "updateTime" in auxAPI[api]["metrics"][metric]:
                    self.externalAPI[metricType][api]["metrics"][metric]["updatetime"]=auxAPI[api]["metrics"][metric]["updateTime"]
            
        
       
        self.userThreads={}
        self.userTokens={}
        self.userURLS={}
        allUsers=self.database.getAllUsers()
        for user in allUsers:
            urls={}   #{GPS: {url:url, updateTime, updateTime}, HealthStatus: {FitBit:{header:header, refresh_url:refresh, refresh_header:..., refresh_data:..., metrics:{Heartrate:{url:url, updatetime:10}, Steps:{...}}}}}, PersonalStatus:{}, Sleep:{}}
            userDevices=self.database.getAllDevices(user)
            for device in userDevices:
                deviceType=device["type"].strip()
                if deviceType in  self.supportedDevices:
                    metrics=self.supportedDevices[deviceType]["metrics"]
                    for metric in metrics:
                        metricType=metrics[metric]["type"]
                        if metricType not in urls:
                            urls[metricType]={}
                        if deviceType not in urls[metricType]:
                            urls[metricType][deviceType]={"metrics":{}}
                            urls[metricType][deviceType]["header"]=self.supportedDevices[deviceType]["header"].replace("VARIABLE_TOKEN",device["token"])
                            for refreshParam in ["refresh_url", "refresh_header", "refresh_data"]:
                                if refreshParam in self.supportedDevices[deviceType]:
                                    urls[metricType][deviceType][refreshParam]=self.supportedDevices[deviceType][refreshParam].replace("VARIABLE_REFRESH_TOKEN", device.get("refresh_token",""))

                        urls[metricType][deviceType]["metrics"][metric]={}        
                        urls[metricType][deviceType]["metrics"][metric]["url"]=self.supportedDevices[deviceType]["metrics"][metric]["url"].replace("VARIABLE_UUID", device.get("uuid", ""))
                        urls[metricType][deviceType]["metrics"][metric]["updateTime"]=self.supportedDevices[deviceType]["metrics"][metric]["updateTime"]
                        
                        if metricType=="Environment" and self.supportedDevices[deviceType]["metrics"][metric]["location"]:
                            urls[metricType][deviceType]["location"]=True
                            urls[metricType][deviceType]["latitude"]=device["latitude"]
                            urls[metricType][deviceType]["longitude"]=device["longitude"]

                        #urls[metric]["savingTime"]=self.supportedDevices[deviceType[metric]["savingTime"]]

            urls["GPS"]={"url":self.gps["url"].replace("VARIABLE_USER", user), "updateTime":self.gps["updateTime"], "header":self.gps["header"]}

            self.userURLS[user]=urls

            for key in self.externalAPI:
                if key in urls:
                    urls[key]=dict(urls[key], **self.externalAPI[key])
                else:
                    urls[key]=self.externalAPI[key]



            print(urls)

            #passing only the GPS and the HealthStatus to the Thread
            self.userThreads[user]=myThread(self, {k:v for k, v in urls.items() if k in ["GPS", "HealthStatus", "Sleep"]},user)
            self.userThreads[user].start()


        #urls["https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json"]=[{"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRLMlgiLCJzdWIiOiI3Q05RV1oiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJudXQgcnBybyByc2xlIiwiZXhwIjoxNTUzODAxNjA5LCJpYXQiOjE1NTM3NzI4MDl9.6_hSXgYG36430e-ZaRfcEYSzDezGJeaMF5R2PiSr4bk"}, 1]
        #urls["http://api.foobot.io/v2/device/240D676D40002482/datapoint/10/last/0/"]=[{"Accept":"application/json;charset=UTF-8","X-API-KEY-TOKEN":"eyJhbGciOiJIUzI1NiJ9.eyJncmFudGVlIjoiam9hby5wQHVhLnB0IiwiaWF0IjoxNTUyMDY2Njc5LCJ2YWxpZGl0eSI6LTEsImp0aSI6IjRiNmY2NzhiLWJjNTYtNDYxNi1hYmMyLTRiNjlkMTNkMjUzOSIsInBlcm1pc3Npb25zIjpbInVzZXI6cmVhZCIsImRldmljZTpyZWFkIl0sInF1b3RhIjoyMDAsInJhdGVMaW1pdCI6NX0.aeLLsrhh1-DVXSwl-Z_qDx1Xbr9oIid1IKsOyGQxwqQ"},1]

    #REAL THING

    def signup(self, data):
        jsonData=json.loads(data.decode("UTF-8"))
        try:
            self.database.register(jsonData)
            return json.dumps({"status":0, "error":"Successfull operation."}).encode("UTF-8")
        except Exception as e:
            return json.dumps({"status":1, "error":"Database internal error. "+str(e)}).encode("UTF-8")


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
            return json.dumps({"status":0 , "error":"Successfull operation.", "data":{"token":"\""+token+"\""}}).encode("UTF-8")
        return json.dumps({"status":1, "error":"Incorrect username or password."}).encode("UTF-8")

    def getAllDevices(self, token):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "error":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        devices=self.database.getAllDevices(user)
        return json.dumps({"status":0 , "error":"Successfull operation.", "data":devices}).encode("UTF-8")

    def addDevice(self, token, data):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "error":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            jsonData=json.loads(data.decode("UTF-8"))
            deviceToken=jsonData["token"]

            if jsonData["type"] not in [submetric for metric in self.userURLS[user] for submetric in self.userURLS[user][metric]]:
                deviceType=jsonData["type"].strip()
                if deviceType in  self.supportedDevices:
                    metrics=self.supportedDevices[deviceType]["metrics"]
                    for metric in metrics:
                        metricType=metrics[metric]["type"]
                        if metricType not in urls:
                            self.userURLS[metricType]={}
                        if deviceType not in urls[metricType]:
                            self.userURLS[metricType][deviceType]={"metrics":{}}
                            self.userURLS[metricType][deviceType]["header"]=self.supportedDevices[deviceType]["header"].replace("VARIABLE_TOKEN",jsonData["token"])
                            for refreshParam in ["refresh_url", "refresh_header", "refresh_data"]:
                                if refreshParam in self.supportedDevices[deviceType]:
                                    self.userURLS[metricType][deviceType][refreshParam]=self.supportedDevices[deviceType][refreshParam].replace("VARIABLE_REFRESH_TOKEN", jsonData.get("refresh_token",""))

                        self.userURLS[metricType][deviceType]["metrics"][metric]={}        
                        self.userURLS[metricType][deviceType]["metrics"][metric]["url"]=self.supportedDevices[deviceType]["metrics"][metric]["url"].replace("VARIABLE_UUID", jsonData.get("uuid", ""))
                        self.userURLS[metricType][deviceType]["metrics"][metric]["updateTime"]=self.supportedDevices[deviceType]["metrics"][metric]["updateTime"]
                        
                        if metricType=="Environment" and self.supportedDevices[deviceType]["metrics"][metric]["location"]:
                            self.userURLS[metricType][deviceType]["location"]=True
                            self.userURLS[metricType][deviceType]["latitude"]=jsonData["latitude"]
                            self.userURLS[metricType][deviceType]["longitude"]=jsonData["longitude"]


            self.database.addDevice(user, jsonData)
            return json.dumps({"status":0 , "error":"Successfull operation."}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "error":"Database internal error. "+str(e)}).encode("UTF-8")

    def getData(self, token, function, datatype, start, end, interval):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "error":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            values=eval("self.database."+function)
            return json.dumps({"status":0 , "error":"Successfull operation.", "data":values}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "error":"Database internal error. "+str(e)}).encode("UTF-8")
        return  json.dumps({"status":1, "error":"Bad combination of arguments. It can only be start+end, start+interval or end+interval"}).encode("UTF-8")
                

    def updateProfile(self, token, data):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "error":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            self.database.updateProfile(user, json.loads(data.decode("UTF-8")))
            return json.dumps({"status":0 , "error":"Successfull operation."}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "error":"Database internal error. "+str(e)}).encode("UTF-8")

    def getProfile(self, token):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "error":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            profile=self.database.getProfile(user)
            return json.dumps({"status":0 , "error":"Successfull operation.", "data": profile}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "error":"Database internal error. "+str(e)}).encode("UTF-8")

    def deleteProfile(self, token):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "error":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            self.database.deleteProfile(user)
            return json.dumps({"status":0 , "error":"Successfull operation."}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "error":"Database internal error. "+str(e)}).encode("UTF-8")

    def getsupportedDevices(self):
        try:
            values=self.database.getsupportedDevices()
            return json.dumps({"status":0 , "error":"Successfull operation.", "data":values}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "error":"Database internal error. "+str(e)}).encode("UTF-8")

    '''
    def userGPSCoordinates(self, token, data):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "error":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        jsonData=json.loads(data.decode("UTF-8"))
        lat=jsonData["latitude"]
        longi=jsonData["longitude"]
        response=requests.get("https://api.waqi.info/feed/geo:"+lat+";"+longi+"/?token=453f8f3898bd238302fe5f84e3526a90c5da9496")
        response=json.loads(response.text)
        normalData={metric:reponse["data"]["iaqi"][metric]["v"] for metric in reponse["data"]["iaqi"]}
        normalData["aqi"]=response["data"]["aqi"]
        normalData["lat"]=lat
        normalData["longi"]=longi

        #CHECK HOME


        try:
            self.database.insert("Environment", normalData, user)
            return json.dumps({"status":0 , "error":"Successfull operation."}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "error":"Database internal error. "+str(e)}).encode("UTF-8")    
    '''


    def normalizeData(self, path, data):
        jsonData=json.loads(data)
        subpath=[y for y in path.split("-")][1:]
        try:
            if len(subpath)==1:
                return eval(self.configFile[subpath[0]]["getData"])
            return eval(self.configFile[subpath[0]][subpath[1]]["metrics"][subpath[2]]["getData"], {"jsonData":jsonData, "dp":dp})
        except Exception as e:
            raise Exception("Error on calculating the relevant data. "+str(e))


    def refreshTokens(self, errors, user):
        refreshData={}
        for metric in errors:
            if metric=="GPS":
                deviceConf=self.userURLS[user][metric]
                if "refresh_url" in deviceConf:
                    try:
                        jsonData=json.loads(requests.get(deviceConf["refresh_url"], headers=deviceConf.get("refresh_header", ""), data=deviceConf.get("refresh_data", "")).text)
                        result=eval(self.configFile[metric]("getRefreshData"))
                        deviceConf["header"]=self.configFile[metric]["header"].replace("VARIABLE_TOKEN",result["access_token"])
                        for refreshParam in ["refresh_url", "refresh_header", "refresh_data"]:
                            if refreshParam in deviceConf:
                                deviceConf[refreshParam]=self.configFile[metric][refreshParam].replace("VARIABLE_REFRESH_TOKEN", result.get("refresh_token",""))

                        url=deviceConf["url"]
                        header=deviceConf["header"]
                        refreshData[metric]=self.normalizeData(metric+"-"+errors[metric], requests.get(url, headers=header).text)
                    except Exception as e:
                        raise Exception("Error while refreshing. "+str(e))
                raise Exception("Impossible to refresh. No URL.")
            else:
                for path in errors[metric]:
                    for subpath in errors[metric][path]:
                        deviceConf=self.userURLS[user][path][subpath]
                        if "refresh_url" in deviceConf:
                            try:
                                jsonData=json.loads(requests.get(deviceConf["refresh_url"], headers=deviceConf.get("refresh_header", ""), data=deviceConf.get("refresh_data", "")).text)
                                result=eval(self.configFile[path][subpath]("getRefreshData"))
                                deviceConf["header"]=self.configFile[path][subpath]["header"].replace("VARIABLE_TOKEN",result["access_token"])
                                for refreshParam in ["refresh_url", "refresh_header", "refresh_data"]:
                                    if refreshParam in deviceConf:
                                        deviceConf[refreshParam]=self.configFile[path][subpath][refreshParam].replace("VARIABLE_REFRESH_TOKEN", result.get("refresh_token",""))

                                header=deviceConf["header"]
                                refreshData[metric]={}
                                for submetric in errors[metric][path][subpath]:
                                    url=deviceConf["metrics"][submetric]["url"]
                                    refreshData[metric]=dict(refreshData[metric], **self.normalizeData(metric+"-"+path+"-"+subpath+"-"+submetric, requests.get(url, headers=header).text))
                            except Exception as e:
                                raise Exception("Error while refreshing. "+str(e))
                        raise Exception("Impossible to refresh. No URL.")
        return refreshData

        '''
        subpaths=path.split("-")[1:]
        if len(subpaths)==1:
            deviceConf=self.userURLS[user][subpaths[0]]
            if "refresh_url" in deviceConf:
                try:
                    jsonData=json.loads(requests.get(deviceConf["refresh_url"], headers=deviceConf.get("refresh_header", ""), data=deviceConf.get("refresh_data", "")).text)
                    result=eval(self.configFile[subpaths[0]]("getRefreshData"))
                    deviceConf["header"]=self.configFile[subpaths[0]]["header"].replace("VARIABLE_TOKEN",result["access_token"])
                    for refreshParam in ["refresh_url", "refresh_header", "refresh_data"]:
                        if refreshParam in deviceConf:
                            deviceConf[refreshParam]=self.configFile[subpaths[0]][refreshParam].replace("VARIABLE_REFRESH_TOKEN", result.get("refresh_token",""))

                    url=deviceConf["url"]
                    header=deviceConf["header"]
                except Exception as e:
                    raise Exception("Error while refreshing. "+str(e))

            raise Exception("Impossible to refresh. No URL.")
        else:
            deviceConf=self.userURLS[user][subpaths[0]][subpaths[1]]
            if "refresh_url" in deviceConf:
                try:
                    jsonData=json.loads(requests.get(deviceConf["refresh_url"], headers=deviceConf.get("refresh_header", ""), data=deviceConf.get("refresh_data", "")).text)
                    result=eval(self.configFile[subpaths[0]][subpaths[1]]("getRefreshData"))
                    deviceConf["header"]=self.configFile[subpaths[0]][subpaths[1]]["header"].replace("VARIABLE_TOKEN",result["access_token"])
                    for refreshParam in ["refresh_url", "refresh_header", "refresh_data"]:
                        if refreshParam in deviceConf:
                            deviceConf[refreshParam]=self.configFile[subpaths[0]][subpaths[1]][refreshParam].replace("VARIABLE_REFRESH_TOKEN", result.get("refresh_token",""))

                    url=deviceConf["metrics"][subpaths[2]]["url"]
                    header=deviceConf["header"]
                except Exception as e:
                    raise Exception("Error while refreshing. "+str(e))
            raise Exception("Impossible to refresh. No URL.")


        try:
            return requests.get(url, headers=header)
        except Exception as e:
            raise Exception("Error after refreshing, on the retry fetch. "+str(e))
        '''
        

    def process(self, responses, user):
        normalData={}
        errors={}
        for resp in responses:
            subpaths=resp[0].split("-")
            metric=subpaths[0]
            if metric not in normalData:
                normalData[metric]={}
            try:
                normalData[metric]=dict(normalData[metric], **self.normalizeData(resp[0], resp[1]))
            except Exception as e:
                logging.error(str(e)+"->"+resp[1])
                if subpaths[0]=="GPS":
                    errors["GPS"]="GPS"
                else:
                    if subpaths[0] not in errors:
                        errors[subpaths[0]]={}
                    if subpaths[1] not in errors[subpaths[0]]:
                        errors[subpaths[0]][subpaths[1]]={}
                    if subpaths[2] not in errors[subpaths[0]][subpaths[1]]:
                        errors[subpaths[0]][subpaths[1]][subpaths[2]]=[]
                    errors[subpaths[0]][subpaths[1]][subpaths[2]].append(subpaths[3])


        if len(errors)!=0:
            logging.error("Trying to refresh tokens")
            try:
                refreshData=self.refreshTokens(errors, user)
                for metric in refreshData:
                    if metric in normalData:
                        normalData[metric]=dict(normalData[metric], refreshData[metric])
                    else:
                        normalData[metric]=refreshData[metric]
            except Exception as ex:
                logging.error("Couldn't refresh tokens. "+str(ex))


        if "GPS" in normalData:
            normalData["Environment"]={}
            for device in self.userURLS[user]["Environment"]:
                deviceConf=self.userURLS[user]["Environment"][device]
                if deviceConf["location"]:
                    distance=round(vincenty([float(normalData["GPS"]["latitude"]), float(normalData["GPS"]["longitude"])], [float(deviceConf["latitude"]), float(deviceConf["longitude"])]).m)
                    if distance <= RADIUS:
                        for metric in deviceConf["metrics"]:
                            url=deviceConf["metrics"][metric]["url"]
                            header=deviceConf["header"]
                            try:
                                jsonData=requests.get(url, headers=json.loads(header))
                                normalData["Environment"]=dict(normalData["Environment"], **self.normalizeData("Environment-"+self.getStartPath(device)+"-"+device+"-"+metric,jsonData.text))
                            except Exception as e:
                                logging.error("Exception caught: "+str(e))
            if normalData["Environment"]=={}:
                for device in self.userURLS[user]["Environment"]:
                    deviceConf=self.userURLS[user]["Environment"][device]
                    if not deviceConf["location"]:
                        for metric in deviceConf["metrics"]:
                            url=deviceConf["metrics"][metric]["url"].replace("VARIABLE_LATITUDE", str(normalData["GPS"]["latitude"])).replace("VARIABLE_LONGITUDE", str(normalData["GPS"]["longitude"]))
                            header=deviceConf["header"]
                            try:
                                jsonData=requests.get(url, headers=json.loads(header))
                                normalData["Environment"]=dict(normalData["Environment"], **self.normalizeData("Environment-"+self.getStartPath(device)+"-"+device+"-"+metric,jsonData.text))
                            except Exception as e:
                                logging.error("Exception caught: "+str(e))
            #print(normalData["GPS"])
            normalData["Environment"]["latitude"]=normalData["GPS"]["latitude"]
            normalData["Environment"]["longitude"]=normalData["GPS"]["longitude"]
            del normalData["GPS"]

        coords=self.normalizeData("GPS-GPS", requests.get(self.userURLS[user]["GPS"]["url"], headers=json.loads(self.userURLS[user]["GPS"]["header"])).text)

        for metric in normalData:
            if time not in normalData[metric]:
                normalData[metric]["time"]=int(time.time())
            if metric!="Environment":
                normalData[metric]["latitude"]=coords["latitude"]
                normalData[metric]["longitude"]=coords["longitude"]

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
        self.deltaTimes=self.getDeltas([m for m in urls])
        self.running=True
        print(self.deltaTimes)

    def getDeltas(self, metrics):
        aux=[]
        for m in metrics:
            print(m)
            aux+=[(timedelta(minutes=self.urls[m]["updateTime"]), m+"-GPS")] if m=="GPS" else [(timedelta(minutes=self.urls[m][n]["metrics"][o]["updateTime"]), m+"-"+self.processor.getStartPath(n)+"-"+n+"-"+o) for n in self.urls[m] for o in self.urls[m][n]["metrics"]]
        return aux


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
                        old_times[i]=now1
                        metric=self.deltaTimes[i][1].split("-")
                        url=self.urls[metric[1]]["url"] if len(metric)==2 else self.urls[metric[0]][metric[2]]["metrics"][metric[3]]["url"]
                        header=json.loads(self.urls[metric[1]]["header"] if len(metric)==2 else self.urls[metric[0]][metric[2]]["header"])
                        try:
                            resp=requests.get(url, headers=header)
                            responses.append([self.deltaTimes[i][1], resp.text])
                        except Exception as e:
                            logging.error("Exception caught: "+str(e))
                        
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
data={"grant_type":"refresh_token", "refresh_token": "e1bbbf6729924395bf5e47f98cbc090cbdea5b8701e6161c53250ca697f55397"}
a=requests.post("https://api.fitbit.com/oauth2/token", headers=header, data=data)
print(a.text)

'''