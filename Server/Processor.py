import requests
import json

'''
Component responsable for doing all the information gathering and processing
'''
class Processor:

	def __init__(self):
		pass

	def getPollution(self, city):
		aux=requests.get("http://api.airvisual.com/v2/city?city="+city+"&state=Aveiro&country=Portugal&key=grJBqR7PN3NjzTZnL")
		jsondata=json.loads(aux.text)
		return str(jsondata["data"]["current"]["pollution"])

	def getAverageHeartRate(self):
		#FitBit
		url="https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json"
		header={"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRLMlgiLCJzdWIiOiI3Q05RV1oiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcmFjdCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTUxOTg0ODcwLCJpYXQiOjE1NTE5NTYwNzB9.sQVpRYMYm2Rohe-0W7x4B7fuadWC8TIr-J3Wo8t7UEg"}

		response=requests.get(url, headers=header)
		jsondata=json.loads(response.text)
		return str(jsondata["activities-heart"][0]["value"]["restingHeartRate"])


	def getPollutionGPS(lat,long):
		#https://api.breezometer.com/air-quality/v2/current-conditions?lat=40.6&lon=-8.6&key=407f495d1f744a8c86c700e5fe83a752&features=breezometer_aqi,local_aqi,health_recommendations,sources_and_effects,pollutants_concentrations,pollutants_aqi_information
		#https://api.waqi.info/feed/geo:40.6;-8.6/?token=453f8f3898bd238302fe5f84e3526a90c5da9496
		response=requests.get("https://api.breezometer.com/air-quality/v2/current-conditions?lat=40.6&lon=-8.6&key=407f495d1f744a8c86c700e5fe83a752&features=breezometer_aqi,local_aqi,health_recommendations,sources_and_effects,pollutants_concentrations,pollutants_aqi_information")
		return response.text


	def getHomePollution():
		#FooBot
		header={"Accept":"text/csv;charset=UTF-8","X-API-KEY-TOKEN":"eyJhbGciOiJIUzI1NiJ9.eyJncmFudGVlIjoiam9hby5wQHVhLnB0IiwiaWF0IjoxNTUyMDY2Njc5LCJ2YWxpZGl0eSI6LTEsImp0aSI6IjRiNmY2NzhiLWJjNTYtNDYxNi1hYmMyLTRiNjlkMTNkMjUzOSIsInBlcm1pc3Npb25zIjpbInVzZXI6cmVhZCIsImRldmljZTpyZWFkIl0sInF1b3RhIjoyMDAsInJhdGVMaW1pdCI6NX0.aeLLsrhh1-DVXSwl-Z_qDx1Xbr9oIid1IKsOyGQxwqQ"}
		url="http://api.foobot.io/v2/device/240D676D40002482/datapoint/10/last/0/"
		response=requests.get(url, headers=header)
		return response.text

	
	