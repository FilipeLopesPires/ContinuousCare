import json
import requests
from abstract.DataSource import DataSource
from abstract.Metric import Metric
import dateutil.parser as dp


class FitBit_Charge_3(DataSource):
    def __init__(self, token, refreshToken, uuid, user, id, location):
        super().__init__(token, refreshToken, uuid, user, id, location)

    @property
    def metrics(self):
        return [HearthRate(self), Sleep(self), Calories(self), Steps(self), Activity(self)]

    @property
    def _headerTemplate(self):
        return json.dumps({"Authorization": "Bearer TOKEN"})

    @property
    def _refreshHeaderTemplate(self):
        return json.dumps({"Authorization": "Basic MjJESzJYOjUyNDRmZjEwNzliMTZlODQ4ZGE1YWI1NTc3ZDg5YzVl", "Content-Type": "application/x-www-form-urlencoded"})

    @property
    def _refreshURL(self):
        return "https://api.fitbit.com/oauth2/token"

    @property
    def _refreshDataTemplate(self):
        return json.dumps({"grant_type": "refresh_token", "refresh_token": "REFRESH_TOKEN"})

    def refreshToken(self):
        try:
            response=requests.post(self._refreshURL, headers=self.refreshHeader, data=self.refreshData)
            jsonData=json.loads(response.text)
            tokens={"token":jsonData["access_token"],"refresh_token":jsonData["refresh_token"]}
            self._token=tokens["token"]
            self._refreshToken=tokens["refresh_token"]
            return tokens
        except Exception as e:
            raise Exception("Unable to refresh tokens due to error: "+str(e))


class HearthRate(Metric):
    def __init__(self, dataSource):
        super().__init__(dataSource)

    @property
    def URLTemplate(self):
        return "https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json"

    @property
    def updateTime(self):
        return 0.20

    @property
    def metricType(self):
        return "HealthStatus"

    @property
    def metricLocation(self):
        return ""

    def getData(self, latitude=None, longitude=None):
        try:
            data=requests.get(self.url, headers=self.dataSource.header)
            jsonData=json.loads(data.text)
            if "success" in jsonData:
                raise Exception("Couldn't fetch information at "+self.__class__.__name__+": "+jsonData["errors"][0]["errorType"])
            return jsonData
        except Exception as e:
            raise Exception("Error while fetching information for "+self.__class__.__name__+": "+str(e))

    def normalizeData(self, jsonData):
        return {"heartRate":jsonData["activities-heart"][0]["value"]["restingHeartRate"] if "restingHeartRate" in jsonData["activities-heart"][0]["value"] else None}

    def checkEvent(self, normalJsonData):
        hr = normalJsonData["heartRate"]
        if hr:
            if hr <= 50 or hr>=100:
                return "HighHeartRate"
        return None

class Sleep(Metric):
    def __init__(self, dataSource):
        super().__init__(dataSource)

    @property
    def URLTemplate(self):
        return "https://api.fitbit.com/1.2/user/-/sleep/date/today.json"

    @property
    def updateTime(self):
        return 360

    @property
    def metricType(self):
        return "Sleep"

    @property
    def metricLocation(self):
        return ""

    def getData(self, latitude=None, longitude=None):
        try:
            data=requests.get(self.url, headers=self.dataSource.header)
            jsonData=json.loads(data.text)
            if "success" in jsonData:
                raise Exception("Couldn't fetch information at "+self.__class__.__name__+": "+jsonData["errors"][0]["errorType"])
            return jsonData
        except Exception as e:
            raise Exception("Error while fetching information for "+self.__class__.__name__+": "+str(e))

    def normalizeData(self, jsonData):
        duration=round(jsonData["sleep"][0]["duration"]/1000)
        begin=int(dp.parse(jsonData["sleep"][0]["startTime"]+"Z").strftime("%s"))
        end=int(dp.parse(jsonData["sleep"][0]["endTime"]+"Z").strftime("%s"))
        sleepEvents=[{k if k!="dateTime" else "time" : v if k!="dateTime" else int(dp.parse(v+"Z").strftime("%s")) for k,v in e.items()} for e in jsonData["sleep"][0]["levels"]["data"]]
        return {"duration":duration, "day":jsonData["sleep"][0]["dateOfSleep"], "begin":begin, "end":end, "sleep":sleepEvents}

    def checkEvent(self, normalJsonData):
        duration = normalJsonData["duration"]
        if duration:
            if duration < 4:
                return "VeryLittleSleep"
        return None

class Calories(Metric):
    def __init__(self, dataSource):
        super().__init__(dataSource)

    @property
    def URLTemplate(self):
        return "https://api.fitbit.com/1/user/-/activities/date/today.json"

    @property
    def updateTime(self):
        return 360

    @property
    def metricType(self):
        return "HealthStatus"

    @property
    def metricLocation(self):
        return ""

    def getData(self, latitude=None, longitude=None):
        try:
            data=requests.get(self.url, headers=self.dataSource.header)
            jsonData=json.loads(data.text)
            if "success" in jsonData:
                raise Exception("Couldn't fetch information at "+self.__class__.__name__+": "+jsonData["errors"][0]["errorType"])
            return jsonData
        except Exception as e:
            raise Exception("Error while fetching information for "+self.__class__.__name__+": "+str(e))

    def normalizeData(self, jsonData):
        return {"calories":jsonData["summary"]["caloriesOut"]}


class Activity(Metric):
    def __init__(self, dataSource):
        super().__init__(dataSource)

    @property
    def URLTemplate(self):
        return "https://api.fitbit.com/1/user/-/activities/date/today.json"

    @property
    def updateTime(self):
        return 360

    @property
    def metricType(self):
        return "HealthStatus"

    @property
    def metricLocation(self):
        return ""

    def getData(self, latitude=None, longitude=None):
        try:
            data=requests.get(self.url, headers=self.dataSource.header)
            jsonData=json.loads(data.text)
            if "success" in jsonData:
                raise Exception("Couldn't fetch information at "+self.__class__.__name__+": "+jsonData["errors"][0]["errorType"])
            return jsonData
        except Exception as e:
            raise Exception("Error while fetching information for "+self.__class__.__name__+": "+str(e))

    def normalizeData(self, jsonData):
        return {"fairlyActiveMinutes":jsonData["summary"]["fairlyActiveMinutes"], "lightlyActiveMinutes":jsonData["summary"]["lightlyActiveMinutes"], "sedentaryMinutes":jsonData["summary"]["sedentaryMinutes"], "veryActiveMinutes":jsonData["summary"]["veryActiveMinutes"]}

    def checkEvent(self, normalJsonData):
        sedentaryMinutes = normalJsonData["sedentaryMinutes"]
        if sedentaryMinutes:
            if sedentaryMinutes > 8*60:
                return "VerySedentary"
        return None

class Steps(Metric):
    def __init__(self, dataSource):
        super().__init__(dataSource)

    @property
    def URLTemplate(self):
        return "https://api.fitbit.com/1/user/-/activities/date/today.json" 

    @property
    def updateTime(self):
        return 360

    @property
    def metricType(self):
        return "HealthStatus"

    @property
    def metricLocation(self):
        return ""

    def getData(self, latitude=None, longitude=None):
        try:
            data=requests.get(self.url, headers=self.dataSource.header)
            jsonData=json.loads(data.text)
            if "success" in jsonData:
                raise Exception("Couldn't fetch information at "+self.__class__.__name__+": "+jsonData["errors"][0]["errorType"])
            return jsonData
        except Exception as e:
            raise Exception("Error while fetching information for "+self.__class__.__name__+": "+str(e))

    def normalizeData(self, jsonData):
        return {"steps":jsonData["summary"]["steps"]}

    def checkEvent(self, normalJsonData):
        steps = normalJsonData["steps"]
        if steps:
            if steps < 1000:
                return "VeryLittleMoviment"
        return None


class Foobot(DataSource):
    def __init__(self, token, refreshToken, uuid, user, id, location):
        super().__init__(token, refreshToken, uuid, user, id, location)

    @property
    def metrics(self):
        return [Foobotmetric(self)]

    @property
    def _headerTemplate(self):
        return json.dumps({"Accept":"application/json;charset=UTF-8","X-API-KEY-TOKEN":"TOKEN"})

    @property
    def _refreshHeaderTemplate(self):
        return ""

    @property
    def _refreshURL(self):
        return ""

    @property
    def _refreshDataTemplate(self):
        return ""

    def refreshToken(self):
        raise Exception("Impossible to refresh tokens.")


class Foobotmetric(Metric):
    def __init__(self, dataSource):
        super().__init__(dataSource)

    @property
    def URLTemplate(self):
        return "http://api.foobot.io/v2/device/UUID/datapoint/10/last/0/"

    @property
    def updateTime(self):
        return 0 #irrelevant

    @property
    def metricType(self):
        return "Environment"

    @property
    def metricLocation(self):
        return "inside"

    def getData(self, latitude=None, longitude=None):
        try:
            data=requests.get(self.url, headers=self.dataSource.header)
            jsonData=json.loads(data.text)
            if "message" in jsonData:
                raise Exception("Couldn't fetch information at "+self.__class__.__name__+": "+jsonData["errors"][0]["errorType"])
            return jsonData
        except Exception as e:
            raise Exception("Error while fetching information for "+self.__class__.__name__+": "+str(e))

    def normalizeData(self, jsonData):
        return { metric : float(value) for metric, value in zip(["time","pm10","t","h","co2","voc","aqi"], jsonData["datapoints"][0])}

    def checkEvent(self, normalJsonData):
        aqi = normalJsonData["aqi"]
        output=""
        if aqi:
            if aqi >= 75:
                output+="VeryHighGeneralPollution,"
        pm10 = normalJsonData["pm10"]
        if pm10:
            if pm10 >= 40:
                output+="VeryHighParticleMatter10,"
        voc = normalJsonData["voc"]
        if voc:
            if voc >= 350:
                output+="VeryHighVolatileCompounds,"
        if output!="":
            return output[:-1]
        return None


class ExternalAPI(DataSource):
    def __init__(self, token, refreshToken, uuid, user, id, location):
        super().__init__(token, refreshToken, uuid, user, id, location)

    @property
    def metrics(self):
        return [WAQI(self)]

    @property
    def _headerTemplate(self):
        return ""

    @property
    def _refreshHeaderTemplate(self):
        return ""

    @property
    def _refreshURL(self):
        return ""

    @property
    def _refreshDataTemplate(self):
        return ""

    def refreshToken(self):
        raise Exception("Impossible to refresh tokens.")


class WAQI(Metric):
    def __init__(self, dataSource):
        super().__init__(dataSource)

    @property
    def URLTemplate(self):
        return "https://api.waqi.info/feed/geo:LATITUDE;LONGITUDE/?token=453f8f3898bd238302fe5f84e3526a90c5da9496"

    @property
    def updateTime(self):
        return 0 #irrelevant

    @property
    def metricType(self):
        return "Environment"

    @property
    def metricLocation(self):
        return "outside"

    def getData(self, latitude=None, longitude=None):
        try:
            lat="" if latitude is None else latitude
            longi="" if longitude is None else longitude
            data=requests.get(self.url.replace("LATITUDE", lat).replace("LONGITUDE", longi), headers=self.dataSource.header)
            jsonData=json.loads(data.text)
            if "status" in jsonData and jsonData["status"]=="error":
                raise Exception("Couldn't fetch information at "+self.__class__.__name__+": "+jsonData["errors"][0]["errorType"])
            return jsonData
        except Exception as e:
            raise Exception("Error while fetching information for "+self.__class__.__name__+": "+str(e))

    def normalizeData(self, jsonData):
        return dict({metric:float(jsonData["data"]["iaqi"][metric]["v"]) for metric in jsonData["data"]["iaqi"]}, **{"aqi":float(jsonData["data"]["aqi"])})

    def checkEvent(self, normalJsonData):
        aqi = normalJsonData["aqi"]
        output=""
        if aqi:
            if aqi >= 75:
                output+="VeryHighGeneralPollution,"
        pm10 = normalJsonData["pm10"]
        if pm10:
            if pm10 >= 40:
                output+="VeryHighParticleMatter10,"
        o3 = normalJsonData["o3"]
        if o3:
            if o3 >= 130:
                output+="VeryHighOzono,"
        pm25 = normalJsonData["pm25"]
        if pm25:
            if pm25 >= 55:
                output+="VeryHighParticleMatter25,"
        so2 = normalJsonData["so2"]
        if so2:
            if so2 >= 180:
                output+="VeryHighSulfurDioxide,"
        if output!="":
            return output[:-1]
        return None



class GPS(DataSource):
    def __init__(self, token, refreshToken, uuid, user, id, location):
        super().__init__(token, refreshToken, uuid, user, id, location)

    @property
    def metrics(self):
        return [GPSmetric(self)]

    @property
    def _headerTemplate(self):
        return ""

    @property
    def _refreshHeaderTemplate(self):
        return ""

    @property
    def _refreshURL(self):
        return ""

    @property
    def _refreshDataTemplate(self):
        return ""

    def refreshToken(self):
        raise Exception("Impossible to refresh tokens.")


class GPSmetric(Metric):
    def __init__(self, dataSource):
        super().__init__(dataSource)

    @property
    def URLTemplate(self):
        return "http://mednat.ieeta.pt:8343/gps/USER"

    @property
    def updateTime(self):
        return 360

    @property
    def metricType(self):
        return "GPS"

    @property
    def metricLocation(self):
        return ""

    def getData(self, latitude=None, longitude=None):
        try:
            data=requests.get(self.url.replace("USER", self.dataSource.user), headers=self.dataSource.header)
            jsonData=json.loads(data.text)
            if jsonData["status"]==1:
                raise Exception("Couldn't fetch information at "+self.__class__.__name__+": "+jsonData["msg"])
            return jsonData
        except Exception as e:
            raise Exception("Error while fetching information for "+self.__class__.__name__+": "+str(e))

    def normalizeData(self, jsonData):
        return {"latitude":jsonData["data"]["latitude"],"longitude":jsonData["data"]["longitude"]}

    def checkEvent(self, normalJsonData):
        #irrelevant
        return None