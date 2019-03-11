from flask import Flask, request
import json
from Processor import Processor
from flask_cors import CORS

'''
Component responsable for defining and supporting the interface to the system.
'''

app = Flask(__name__)
CORS(app)
processor=Processor()

@app.route('/pollution/lat=<string:lat>/long=<string:longi>', methods = ['GET'])
def pollution(lat, longi):
    return processor.getPollutionGPS(lat,longi)

@app.route('/heartRate', methods = ['GET'])
def heartRate():
    return processor.getAverageHeartRate()