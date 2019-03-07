from flask import Flask, request
import json
from Processor import Processor

'''
Component responsable for defining and supporting the interface to the system.
'''

app = Flask(__name__)
processor=Processor()

@app.route('/pollution/<string:city>', methods = ['GET'])
def pollution(city):
	return processor.getPollution(city)

@app.route('/heartRate', methods = ['GET'])
def heartRate():
	return processor.getAverageHeartRate()