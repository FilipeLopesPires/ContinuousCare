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
		url="https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json"
		header={"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRLMlgiLCJzdWIiOiI3Q05RV1oiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcmFjdCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTUxOTg0ODcwLCJpYXQiOjE1NTE5NTYwNzB9.sQVpRYMYm2Rohe-0W7x4B7fuadWC8TIr-J3Wo8t7UEg"}

		response=requests.get(url, headers=header)
		jsondata=json.loads(response.text)
		return str(jsondata["activities-heart"][0]["value"]["restingHeartRate"])