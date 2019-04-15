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
        apiID="0"
        for api in auxAPI:
            for metric in auxAPI[api]["metrics"]:
                metricType=auxAPI[api]["metrics"][metric]["type"]
                if metricType not in self.externalAPI:
                    self.externalAPI[metricType]={}
                if api not in self.externalAPI[metricType]:
                    self.externalAPI[metricType][api]={apiID:{}}
                    self.externalAPI[metricType][api][apiID]={"metrics":{}}
                    self.externalAPI[metricType][api][apiID]["header"]=auxAPI[api]["header"]
                    self.externalAPI[metricType][api][apiID]["location"]=auxAPI[api]["metrics"][metric]["location"]
            
                self.externalAPI[metricType][api][apiID]["metrics"][metric]={}
                self.externalAPI[metricType][api][apiID]["metrics"][metric]["url"]=auxAPI[api]["metrics"][metric]["url"]
                if "updateTime" in auxAPI[api]["metrics"][metric]:
                    self.externalAPI[metricType][api][apiID]["metrics"][metric]["updatetime"]=auxAPI[api]["metrics"][metric]["updateTime"]

       
        self.userThreads={}
        self.userTokens={}
        self.userURLS={}
        allUsers=self.database.getAllUsers()
        for user in allUsers:
            urls={}   #{GPS: {url:url, updateTime, updateTime}, HealthStatus: {FitBit:{header:header, refresh_url:refresh, refresh_header:..., refresh_data:..., metrics:{Heartrate:{url:url, updatetime:10}, Steps:{...}}}}}, PersonalStatus:{}, Sleep:{}}
            userDevices=self.database.getAllDevices(user)
            for device in userDevices:
                deviceType=device["type"].strip()
                deviceID=str(device["id"])
                if deviceType in  self.supportedDevices:
                    metrics=self.supportedDevices[deviceType]["metrics"]
                    for metric in metrics:
                        metricType=metrics[metric]["type"]
                        if metricType not in urls:
                            urls[metricType]={}
                        if deviceType not in urls[metricType]:
                            urls[metricType][deviceType]={}
                        if deviceID not in urls[metricType][deviceType]:
                            urls[metricType][deviceType][deviceID]={"metrics":{}}
                            urls[metricType][deviceType][deviceID]["header"]=self.supportedDevices[deviceType]["header"].replace("VARIABLE_TOKEN",device["token"])
                            for refreshParam in ["refresh_url", "refresh_header", "refresh_data"]:
                                if refreshParam in self.supportedDevices[deviceType]:
                                    urls[metricType][deviceType][deviceID][refreshParam]=self.supportedDevices[deviceType][refreshParam].replace("VARIABLE_REFRESH_TOKEN", device.get("refresh_token",""))
                        
                        if metric not in urls[metricType][deviceType][deviceID]["metrics"]:
                            urls[metricType][deviceType][deviceID]["metrics"][metric]={}

                        urls[metricType][deviceType][deviceID]["metrics"][metric]["url"]=self.supportedDevices[deviceType]["metrics"][metric]["url"].replace("VARIABLE_UUID", device.get("uuid", ""))
                        urls[metricType][deviceType][deviceID]["metrics"][metric]["updateTime"]=self.supportedDevices[deviceType]["metrics"][metric]["updateTime"]
                        if metricType=="Environment" and self.supportedDevices[deviceType]["metrics"][metric]["location"]:
                            urls[metricType][deviceType][deviceID]["location"]=True
                            urls[metricType][deviceType][deviceID]["latitude"]=device["latitude"]
                            urls[metricType][deviceType][deviceID]["longitude"]=device["longitude"]

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
            user=jsonData["username"]
            if user not in self.userURLS:
                self.userURLS[user]={}

                for key in self.externalAPI:
                    if key in self.userURLS[user]:
                        self.userURLS[user][key]=dict(self.userURLS[user][key], **self.externalAPI[key])
                    else:
                        self.userURLS[user][key]=self.externalAPI[key]


                self.userURLS[user]["GPS"]={"url":self.gps["url"].replace("VARIABLE_USER", user), "updateTime":self.gps["updateTime"], "header":self.gps["header"]}
                self.userThreads[user]=myThread(self, {k:v for k, v in self.userURLS[user].items() if k in ["GPS", "HealthStatus", "Sleep"]},user)
                self.userThreads[user].start()
            return json.dumps({"status":0, "msg":"Successfull operation."}).encode("UTF-8")
        except RelationalDBException as e:
            return json.dumps({"status":1, "msg":"Relational database internal error. "+str(e)}).encode("UTF-8")
        except Exception as e:
            return json.dumps({"status":1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

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

    def updateDevice(self, token, data):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "msg":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]

        try:
            result=self.database.updateDevice(user, json.loads(data.decode("UTF-8")))
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data": profile}).encode("UTF-8")
        except RelationalDBException as e:
            return  json.dumps({"status":1, "msg":"Relational database internal error. "+str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def addDevice(self, token, data):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "msg":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            jsonData=json.loads(data.decode("UTF-8"))


            deviceToken=jsonData["authentication_fields"]["token"]
            
            id=str(self.database.addDevice(user, jsonData))

            if user not in self.userURLS:
                self.userURLS[user]={}
                self.userURLS[user]["GPS"]={"url":self.gps["url"].replace("VARIABLE_USER", user), "updateTime":self.gps["updateTime"], "header":self.gps["header"]}
            if jsonData["type"] not in [device for metric in self.userURLS[user] for device in self.userURLS[user][metric]]:
                deviceType=jsonData["type"].strip()
                if deviceType in self.supportedDevices:
                    metrics=self.supportedDevices[deviceType]["metrics"]
                    for metric in metrics:
                        metricType=metrics[metric]["type"]
                        if metricType not in self.userURLS[user]:
                            self.userURLS[user][metricType]={}
                        if deviceType not in self.userURLS[user][metricType]:
                            self.userURLS[user][metricType][deviceType]={}
                        if id not in self.userURLS[user][metricType][deviceType]:
                            self.userURLS[user][metricType][deviceType][id]={"metrics":{}}
                            self.userURLS[user][metricType][deviceType][id]["header"]=self.supportedDevices[deviceType]["header"].replace("VARIABLE_TOKEN",jsonData["authentication_fields"]["token"])
                            for refreshParam in ["refresh_url", "refresh_header", "refresh_data"]:
                                if refreshParam in self.supportedDevices[deviceType]:
                                    self.userURLS[user][metricType][deviceType][id][refreshParam]=self.supportedDevices[deviceType][refreshParam].replace("VARIABLE_REFRESH_TOKEN", jsonData["authentication_fields"].get("refresh_token",""))

                        self.userURLS[user][metricType][deviceType][id]["metrics"][metric]={}        
                        self.userURLS[user][metricType][deviceType][id]["metrics"][metric]["url"]=self.supportedDevices[deviceType]["metrics"][metric]["url"].replace("VARIABLE_UUID", jsonData["authentication_fields"].get("uuid", ""))
                        self.userURLS[user][metricType][deviceType][id]["metrics"][metric]["updateTime"]=self.supportedDevices[deviceType]["metrics"][metric]["updateTime"]
                        
                        if metricType=="Environment" and self.supportedDevices[deviceType]["metrics"][metric]["location"]:
                            self.userURLS[user][metricType][deviceType][id]["location"]=True
                            self.userURLS[user][metricType][deviceType][id]["latitude"]=jsonData["latitude"]
                            self.userURLS[user][metricType][deviceType][id]["longitude"]=jsonData["longitude"]


                print(self.userURLS)
                if user in self.userThreads:
                    self.userThreads[user].end()
                self.userThreads[user]=myThread(self, {k:v for k, v in self.userURLS[user].items() if k in ["GPS", "HealthStatus", "Sleep"]},user)
                self.userThreads[user].start()


            
            return json.dumps({"status":0 , "msg":"Successfull operation."}).encode("UTF-8")
        except RelationalDBException as e:
            return  json.dumps({"status":1, "msg":"Relational database internal error. "+str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def getData(self, token, function, datatype, start, end, interval):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "msg":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            values=eval("self.database."+function)
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data":values}).encode("UTF-8")
        except RelationalDBException as e:
            return  json.dumps({"status":1, "msg":"Relational database internal error. "+str(e)}).encode("UTF-8")
        except TimeSeriesDBException as e:
            return  json.dumps({"status":1, "msg":"Time series database internal error. "+str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")
        return  json.dumps({"status":1, "msg":"Bad combination of arguments. It can only be start+end, start+interval or end+interval"}).encode("UTF-8")
                

    def updateProfile(self, token, data):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "msg":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            self.database.updateProfile(user, json.loads(data.decode("UTF-8")))
            return json.dumps({"status":0 , "msg":"Successfull operation."}).encode("UTF-8")
        except RelationalDBException as e:
            return  json.dumps({"status":1, "msg":"Relational database internal error. "+str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def getProfile(self, token):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "msg":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            profile=self.database.getProfile(user)
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data": profile}).encode("UTF-8")
        except RelationalDBException as e:
            return  json.dumps({"status":1, "msg":"Relational database internal error. "+str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def deleteProfile(self, token):
        if token not in self.userTokens:
            return  json.dumps({"status":1, "msg":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            self.database.deleteProfile(user)
            return json.dumps({"status":0 , "msg":"Successfull operation."}).encode("UTF-8")
        except RelationalDBException as e:
            return  json.dumps({"status":1, "msg":"Relational database internal error. "+str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")

    def getSupportedDevices(self):
        try:
            values=self.database.getSupportedDevices()
            return json.dumps({"status":0 , "msg":"Successfull operation.", "data":values}).encode("UTF-8")
        except RelationalDBException as e:
            return  json.dumps({"status":1, "msg":"Relational database internal error. "+str(e)}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "msg":"Server internal error. "+str(e)}).encode("UTF-8")


    def normalizeData(self, path, data):
        jsonData=json.loads(data)
        subpath=[y for y in path.split("-")][1:]
        print(subpath)
        try:
            if len(subpath)==1:
                return eval(self.configFile[subpath[0]]["getData"])
            return eval(self.configFile[subpath[0]][subpath[1]]["metrics"][subpath[3]]["getData"], {"jsonData":jsonData, "dp":dp})
        except Exception as e:
            raise Exception("Error on calculating the relevant data. "+str(e))


    def refreshTokens(self, errors, user):
        refreshData={}
        for metric in errors:
            if metric=="GPS":
                deviceConf=self.userURLS[user][metric]
                if "refresh_url" in deviceConf:
                    try:
                        jsonData=json.loads(requests.post(deviceConf["refresh_url"], headers=deviceConf.get("refresh_header", ""), data=deviceConf.get("refresh_data", "")).text)
                        result=eval(self.configFile[metric]("getRefreshData"))
                        deviceConf["header"]=self.configFile[metric]["header"].replace("VARIABLE_TOKEN",result["access_token"])
                        for refreshParam in ["refresh_url", "refresh_header", "refresh_data"]:
                            if refreshParam in deviceConf:
                                deviceConf[refreshParam]=self.configFile[metric][refreshParam].replace("VARIABLE_REFRESH_TOKEN", result.get("refresh_token",""))

                        url=deviceConf["url"]
                        header=deviceConf["header"]
                        refreshData[metric]=self.normalizeData(metric+"-"+errors[metric], requests.get(url, headers=header).text)
                    except Exception as e:
                        raise Exception("REFRESH: Error while refreshing. "+str(e))
                raise Exception("REFRESH: Impossible to refresh. No URL.")
            else:
                for path in errors[metric]:
                    for device in errors[metric][path]:
                        for id in errors[metric][path][device]:
                            deviceConf=self.userURLS[user][metric][device][id]
                            if "refresh_url" in deviceConf:
                                try:
                                    jsonData=json.loads(requests.post(deviceConf["refresh_url"], headers=json.loads(deviceConf.get("refresh_header", "")), data=json.loads(deviceConf.get("refresh_data", ""))).text)
                                    print(jsonData)
                                    result=eval(self.configFile[path][device]["getRefreshData"])
                                    deviceConf["header"]=self.configFile[path][device]["header"].replace("VARIABLE_TOKEN",result["access_token"])
                                    for refreshParam in ["refresh_url", "refresh_header", "refresh_data"]:
                                        if refreshParam in deviceConf:
                                            deviceConf[refreshParam]=self.configFile[path][device][refreshParam].replace("VARIABLE_REFRESH_TOKEN", result.get("refresh_token",""))

                                    self.database.updateDevice(user, {"id":id, "token":result["access_token"],"refresh_token":result["refresh_token"]})
                                    print(deviceConf)
                                    header=deviceConf["header"]
                                    refreshData[metric]={}
                                    for submetric in errors[metric][path][device][id]:
                                        url=deviceConf["metrics"][submetric]["url"]
                                        result=requests.get(url, headers=json.loads(header))
                                        #print(url, result)
                                        normalizedData=self.normalizeData(metric+"-"+path+"-"+device+"-"+id+"-"+submetric, result.text)
                                        #print(normalizedData)
                                        refreshData[metric]=dict(refreshData[metric], **normalizedData)
                                except Exception as e:
                                    raise Exception("REFRESH: Error while refreshing. "+str(e))
                            else:
                                raise Exception("REFRESH: Impossible to refresh. No URL.")
        return refreshData
        

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
                        errors[subpaths[0]][subpaths[1]][subpaths[2]]={}
                    if subpaths[3] not in errors[subpaths[0]][subpaths[1]][subpaths[2]]:
                        errors[subpaths[0]][subpaths[1]][subpaths[2]][subpaths[3]]=[]
                    errors[subpaths[0]][subpaths[1]][subpaths[2]][subpaths[3]].append(subpaths[4])


        if len(errors)!=0:
            logging.warning("Trying to refresh tokens")
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
            if normalData["GPS"]["latitude"]!=None and normalData["GPS"]["longitude"]!=None:
                if float(normalData["GPS"]["latitude"])>-90 and float(normalData["GPS"]["latitude"])<90 and float(normalData["GPS"]["longitude"])>-180 and float(normalData["GPS"]["longitude"])<180: 
                    normalData["Environment"]={}
                    for device in self.userURLS[user]["Environment"]:
                        devices=self.userURLS[user]["Environment"][device]
                        for id in devices:
                            deviceConf=devices[id]
                            if deviceConf["location"]:
                                distance=round(vincenty([float(normalData["GPS"]["latitude"]), float(normalData["GPS"]["longitude"])], [float(deviceConf["latitude"]), float(deviceConf["longitude"])]).m)
                                if distance <= RADIUS:
                                    for metric in deviceConf["metrics"]:
                                        url=deviceConf["metrics"][metric]["url"]
                                        header=deviceConf["header"]
                                        try:
                                            jsonData=requests.get(url, headers=json.loads(header))
                                            normalData["Environment"]=dict(normalData["Environment"], **self.normalizeData("Environment-"+self.getStartPath(device)+"-"+device+"-"+id+"-"+metric,jsonData.text))
                                        except Exception as e:
                                            logging.error("Exception caught while refetching the data: "+str(e))
                    if normalData["Environment"]=={}:
                        for device in self.userURLS[user]["Environment"]:
                            devices=self.userURLS[user]["Environment"][device]
                            for id in devices:
                                deviceConf=devices[id]
                                if not deviceConf["location"]:
                                    for metric in deviceConf["metrics"]:
                                        url=deviceConf["metrics"][metric]["url"].replace("VARIABLE_LATITUDE", str(normalData["GPS"]["latitude"])).replace("VARIABLE_LONGITUDE", str(normalData["GPS"]["longitude"]))
                                        header=deviceConf["header"]
                                        try:
                                            jsonData=requests.get(url, headers=json.loads(header))
                                            print(device, id)
                                            normalData["Environment"]=dict(normalData["Environment"], **self.normalizeData("Environment-"+self.getStartPath(device)+"-"+device+"-"+id+"-"+metric,jsonData.text))
                                        except Exception as e:
                                            logging.error("Exception caught: "+str(e))
                    #print(normalData["GPS"])
                    normalData["Environment"]["latitude"]=normalData["GPS"]["latitude"]
                    normalData["Environment"]["longitude"]=normalData["GPS"]["longitude"]

            else:
                logging.error("Couldn't process GPS: "+ str(normalData["GPS"]))

            del normalData["GPS"]

        try: 
            coords=self.normalizeData("GPS-GPS", requests.get(self.userURLS[user]["GPS"]["url"], headers=json.loads(self.userURLS[user]["GPS"]["header"])).text)
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
        self.deltaTimes=self.getDeltas([m for m in urls])
        self.running=True
        print(self.deltaTimes)

    def getDeltas(self, metrics):
        aux=[]
        for m in metrics:
            aux+=[(timedelta(minutes=self.urls[m]["updateTime"]), m+"-GPS")] if m=="GPS" else [(timedelta(minutes=self.urls[m][n][i]["metrics"][o]["updateTime"]), m+"-"+self.processor.getStartPath(n)+"-"+n+"-"+i+"-"+o) for n in self.urls[m] for i in self.urls[m][n] for o in self.urls[m][n][i]["metrics"]]
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
                        url=self.urls[metric[1]]["url"] if len(metric)==2 else self.urls[metric[0]][metric[2]][metric[3]]["metrics"][metric[4]]["url"]
                        header=json.loads(self.urls[metric[1]]["header"] if len(metric)==2 else self.urls[metric[0]][metric[2]][metric[3]]["header"])
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
data={"grant_type":"refresh_token", "refresh_token": "167bc73c28c5fafc63aa0718d9a6e57d2d102512a344cb43f856479dd59012d4"}
a=requests.post("https://api.fitbit.com/oauth2/token", headers=header, data=data)
print(a.text)

'''
