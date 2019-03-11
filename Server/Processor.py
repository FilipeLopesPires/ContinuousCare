import requests
import json
import threading
from datetime import datetime, timedelta
from Database import Database

'''
Component responsable for doing all the information gathering and processing
'''
class Processor:

    def __init__(self):
        self.database=Database()

    '''
    def getPollution(self, city):
        aux=requests.get("http://api.airvisual.com/v2/city?city="+city+"&state=Aveiro&country=Portugal&key=grJBqR7PN3NjzTZnL")
        jsondata=json.loads(aux.text)
        return str(jsondata["data"]["current"]["pollution"])
    '''

    def getAverageHeartRate(self):
        #FitBit
        url="https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json"
        header={"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRLMlgiLCJzdWIiOiI3Q05RV1oiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcmFjdCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTUyMzUwMDk2LCJpYXQiOjE1NTIzMjEyOTZ9.hhFY1zZliDYP3Kb9Cfe1OdxUBpduk7vP37zET2r05HY"}

        response=requests.get(url, headers=header)
        jsondata=json.loads(response.text)
        return str(jsondata["activities-heart"][0]["value"]["restingHeartRate"])

    def getHomePollution(self):
        #FooBot
        header={"Accept":"text/csv;charset=UTF-8","X-API-KEY-TOKEN":"eyJhbGciOiJIUzI1NiJ9.eyJncmFudGVlIjoiam9hby5wQHVhLnB0IiwiaWF0IjoxNTUyMDY2Njc5LCJ2YWxpZGl0eSI6LTEsImp0aSI6IjRiNmY2NzhiLWJjNTYtNDYxNi1hYmMyLTRiNjlkMTNkMjUzOSIsInBlcm1pc3Npb25zIjpbInVzZXI6cmVhZCIsImRldmljZTpyZWFkIl0sInF1b3RhIjoyMDAsInJhdGVMaW1pdCI6NX0.aeLLsrhh1-DVXSwl-Z_qDx1Xbr9oIid1IKsOyGQxwqQ"}
        url="http://api.foobot.io/v2/device/240D676D40002482/datapoint/10/last/0/"
        response=requests.get(url, headers=header)
        return response.text

    def getPollutionGPS(self,lat,longi):
        #https://api.breezometer.com/air-quality/v2/current-conditions?lat=40.6&lon=-8.6&key=407f495d1f744a8c86c700e5fe83a752&features=breezometer_aqi,local_aqi,health_recommendations,sources_and_effects,pollutants_concentrations,pollutants_aqi_information
        #https://api.waqi.info/feed/geo:40.6;-8.6/?token=453f8f3898bd238302fe5f84e3526a90c5da9496
        response=requests.get("https://api.breezometer.com/air-quality/v2/current-conditions?lat="+lat+"&lon="+longi+"&key=407f495d1f744a8c86c700e5fe83a752&features=breezometer_aqi,local_aqi,health_recommendations,sources_and_effects,pollutants_concentrations,pollutants_aqi_information")
        jsondata=json.loads(response.text)
        out={}
        for k in jsondata["data"]["pollutants"]:
            out[jsondata["data"]["pollutants"][k]["full_name"]]=jsondata["data"]["pollutants"][k]["aqi_information"]["baqi"]["aqi_display"]

        out[jsondata["data"]["indexes"]["baqi"]["display_name"]]=jsondata["data"]["indexes"]["baqi"]["aqi_display"]

        self.database.insert(out, lat, longi, "teste1", "1234")

        return str(out)
    


#TODO finish thread, run not complete
class myThread (threading.Thread):
    def __init__(self, time_interval, url, header=None):
        threading.Thread.__init__(self)
        self.header=header
        self.url=url
        self.time_interval=time_interval

    def run(self):
        old_time=datetime.now()
        while True:
            if datetime.now()-timedelta(minutes=self.time_interval)>old_time:
                response=requests.get(self.url, headers=self.header)
      


#thread1 = myThread(1, "Thread-1", 1)
#thread1.start()