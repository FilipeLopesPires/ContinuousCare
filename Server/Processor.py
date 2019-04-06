import requests
import json
import string
from random import *
import threading
from datetime import datetime, timedelta
from database import *

'''
Component responsable for doing all the information gathering and processing
'''
class Processor:

    def __init__(self):
        self.configFile=json.loads(open("config.json").read().replace("\n", "").replace("\t", "").strip())
        self.supportedDevices=self.configFile["devices"]
        self.gps=self.configFile["gps"]
        self.externalAPI=self.configFile["externalAPI"]
        self.database=database.Database()
       
        self.userThreads={}
        self.userTokens={}
        self.userURLS={}
        allUsers=self.database.getAllUsers()
        for user in allUsers:
            urls={}   #{GPS: {url:url, updateTime, updateTime}, HealthStatus: {FitBit-Heartrate:{url:url, header:header, updatetime:10}, FitBit-Steps:{...}}}, PersonalStatus:{}, Sleep:{}}
            userDevices=self.database.getAllDevices(user)
            for device in userDevices:
                if device["type"] in  self.supportedDevices:
                    for metric in self.supportedDevices[device["type"]]["metrics"]:
                        if metric["type"] not in urls:
                            urls[metric["type"]]={}
                        urls[metric["type"]][device["type"]+"-"+metric]["url"]=self.supportedDevices[device["type"][metric]["url"]].replace("VARIABLE_UUID", device["uuid"])
                        urls[metric["type"]][device["type"]+"-"+metric]["header"]=self.supportedDevices[device["type"]["header"]].replace("VARIABLE_TOKEN",device["token"])
                        urls[metric["type"]][device["type"]+"-"+metric]["updateTime"]=self.supportedDevices[device["type"][metric]["updateTime"]]
                        #urls[metric]["savingTime"]=self.supportedDevices[device["type"][metric]["savingTime"]]

            urls["GPS"]={"url":self.gps["url"], "updateTime":self.gps["updateTime"], "header":self.gps["header"]}

            self.userURLS[user]=urls

            self.userThreads[user]=myThread(self, urls,user)
            self.userThreads[user].start()


        #urls["https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json"]=[{"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRLMlgiLCJzdWIiOiI3Q05RV1oiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJudXQgcnBybyByc2xlIiwiZXhwIjoxNTUzODAxNjA5LCJpYXQiOjE1NTM3NzI4MDl9.6_hSXgYG36430e-ZaRfcEYSzDezGJeaMF5R2PiSr4bk"}, 1]
        #urls["http://api.foobot.io/v2/device/240D676D40002482/datapoint/10/last/0/"]=[{"Accept":"application/json;charset=UTF-8","X-API-KEY-TOKEN":"eyJhbGciOiJIUzI1NiJ9.eyJncmFudGVlIjoiam9hby5wQHVhLnB0IiwiaWF0IjoxNTUyMDY2Njc5LCJ2YWxpZGl0eSI6LTEsImp0aSI6IjRiNmY2NzhiLWJjNTYtNDYxNi1hYmMyLTRiNjlkMTNkMjUzOSIsInBlcm1pc3Npb25zIjpbInVzZXI6cmVhZCIsImRldmljZTpyZWFkIl0sInF1b3RhIjoyMDAsInJhdGVMaW1pdCI6NX0.aeLLsrhh1-DVXSwl-Z_qDx1Xbr9oIid1IKsOyGQxwqQ"},1]

    #REAL THING

    def signup(self, data):
        jsonData=json.loads(data.decode("UTF-8"))
        try:
            self.database.register(jsonData)
            return json.dumps({"status":0 , "error":"Successfull operation."}).encode("UTF-8")
        except Exception as e:
            return  json.dumps({"status":1, "error":"Database internal error. "+str(e)}).encode("UTF-8")


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
        #ADD DEVICE TO THE THREAD


        if token not in self.userTokens:
            return  json.dumps({"status":1, "error":"Invalid Token."}).encode("UTF-8")

        user=self.userTokens[token]
        try:
            jsonData=json.loads(data.decode("UTF-8"))
            deviceToken=jsonData["token"]

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



    def normalizeData(self, metric, data):
        jsonData=json.loads(data)
        types=metric.split("-")
        return eval(self.supportedDevices[types[0]]["metrics"][types[1]]["getData"])

    def process(self, responses, user):
        '''
        jsonData=json.loads(data)
        types=metric.split("-")
        if eval(self.supportedDevices[types[0]]["metrics"][types[1]]["saveCondition"]):
            self.save(metric, data, user)
        '''

    
    def save(self, metric, data, user):
        normalData=self.normalizeData(metric, data)
        try:
            self.database.insert(metric, normalData, user)
        except Exception as e:
            raise e


    def end(self):
        for k in self.userThreads:
            self.userThreads[k].end()
        return ""

    

class myThread (threading.Thread):
    def __init__(self, processor, urls, user):
        threading.Thread.__init__(self)
        self.processor=processor
        self.user=user
        self.urls=urls
        metrics=[metric for metric in urls]
        self.deltaTimes=[(timedelta(minutes=urls[metric]["updateTime"]), metric) for metric in self.getMetrics([m  for m in urls])]
        self.running=True

    def getMetrics(self, metrics):
        aux=[]
        for m in metrics:
            aux+=[m] if m=="GPS" else [m+"/"+n for n in self.urls[m]]
        return aux


    def run(self):
        old_times=[datetime.now() for x in range(len(self.deltaTimes))]
        print("started")
        while self.running:
            updating=[datetime.now()-old > delta[0] for old,delta in zip(old_times, self.deltaTimes)]
            if any(updating):
                responses=[]
                for i,v in enumerate(updating):
                    if v:
                        old_times[i]=datetime.now()
                        metric=self.deltaTimes[i].split("/")
                        url=self.urls[metric[0]]["url"] if len(metric)==1 else self.urls[metric[0]][metric[1]]["url"]
                        resp=requests.get(url, headers=self.urls[self.deltaTimes[i]]["header"])
                        responses.append([self.deltaTimes[i], resp.text])

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
def getAverageHeartRate(self):
    #FitBit
    url="https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json"
    header={"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRLMlgiLCJzdWIiOiI3Q05RV1oiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJudXQgcnBybyByc2xlIiwiZXhwIjoxNTUzODAxNjA5LCJpYXQiOjE1NTM3NzI4MDl9.6_hSXgYG36430e-ZaRfcEYSzDezGJeaMF5R2PiSr4bk"}

    response=requests.get(url, headers=header)
    jsondata=json.loads(response.text)
    return str(jsondata["activities-heart"][0]["value"]["restingHeartRate"])

def getHomePollution(self):
    #FooBot
    header={"Accept":"application/json;charset=UTF-8","X-API-KEY-TOKEN":"eyJhbGciOiJIUzI1NiJ9.eyJncmFudGVlIjoiam9hby5wQHVhLnB0IiwiaWF0IjoxNTUyMDY2Njc5LCJ2YWxpZGl0eSI6LTEsImp0aSI6IjRiNmY2NzhiLWJjNTYtNDYxNi1hYmMyLTRiNjlkMTNkMjUzOSIsInBlcm1pc3Npb25zIjpbInVzZXI6cmVhZCIsImRldmljZTpyZWFkIl0sInF1b3RhIjoyMDAsInJhdGVMaW1pdCI6NX0.aeLLsrhh1-DVXSwl-Z_qDx1Xbr9oIid1IKsOyGQxwqQ"}
    url="http://api.foobot.io/v2/device/240D676D40002482/datapoint/10/last/0/"
    response=requests.get(url, headers=header)
    return response.text

def getPollutionGPS(self,lat,longi):
    #https://api.breezometer.com/air-quality/v2/current-conditions?lat=40.6&lon=-8.6&key=407f495d1f744a8c86c700e5fe83a752&features=breezometer_aqi,local_aqi,health_recommendations,sources_and_effects,pollutants_concentrations,pollutants_aqi_information
    #https://api.waqi.info/feed/geo:40.6;-8.6/?token=453f8f3898bd238302fe5f84e3526a90c5da9496
    #http://api.openweathermap.org/data/2.5/weather?lat=40&lon=8&appid=a5168e6057120df470e1dcd0b02d9b38
    response=requests.get("https://api.breezometer.com/air-quality/v2/current-conditions?lat="+lat+"&lon="+longi+"&key=407f495d1f744a8c86c700e5fe83a752&features=breezometer_aqi,local_aqi,health_recommendations,sources_and_effects,pollutants_concentrations,pollutants_aqi_information")
    jsondata=json.loads(response.text)
    out={}
    for k in jsondata["data"]["pollutants"]:
        out[jsondata["data"]["pollutants"][k]["full_name"]]=jsondata["data"]["pollutants"][k]["aqi_information"]["baqi"]["aqi_display"]

    out[jsondata["data"]["indexes"]["baqi"]["display_name"]]=jsondata["data"]["indexes"]["baqi"]["aqi_display"]

    self.database.insert(out, lat, longi, "teste1", "1234")
    return str(out)

def teste(self, data):
    print(data)
    return json.dumps({"resposta":"sim"}).encode("UTF-8")


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
