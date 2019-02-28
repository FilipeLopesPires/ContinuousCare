from flask import Flask, request
import requests
import json

app = Flask(__name__)

@app.route('/pollution/<string:city>', methods = ['GET'])
def pollution(city):
	aux=requests.get("http://api.airvisual.com/v2/city?city="+city+"&state=Aveiro&country=Portugal&key=grJBqR7PN3NjzTZnL")
	return aux.text