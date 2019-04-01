from flask import Flask, request
import json
from Processor import Processor
from flask_cors import CORS
import ssl
'''
Component responsable for defining and supporting the interface to the system.
'''

app = Flask(__name__)
CORS(app)
processor=Processor()


#TESTS

@app.route('/pollution/lat=<string:lat>/long=<string:longi>', methods = ['GET'])
def pollution(lat, longi):
    return processor.getPollutionGPS(lat,longi)

@app.route('/heartRate', methods = ['GET'])
def heartRate():
    return processor.getAverageHeartRate()

@app.route('/teste', methods = ['GET','POST'])
def teste():
    return processor.teste(request.data)

@app.route('/end', methods = ['GET'])
def end():
    return processor.end()




#REAL THING

@app.route('/signup', methods = ['POST'])
def signup():
    return processor.signup(request.data)

@app.route('/signin', methods = ['POST'])
def signin():
    return processor.signin(request.data)

@app.route('/devices', methods = ['GET', 'POST'])
def devices():
    userToken=request.headers["AuthToken"]
    if request.method == 'GET':
        return processor.getAllDevices(userToken)
    else:
        return processor.addDevice(userToken, request.data)

@app.route('/environment', endpoint="environment", methods = ['GET'])
@app.route('/environment/<string:datatype>', endpoint="environmentSpecific", methods = ['GET'])
@app.route('/healthstatus', endpoint="healthStatus", methods = ['GET'])
@app.route('/healthstatus/<string:datatype>', endpoint="healthStatusSpecific", methods = ['GET'])
@app.route('/personalstatus', endpoint="personalStatus", methods = ['GET'])
@app.route('/download', endpoint="download",methods = ['GET'])
def getData(datatype=None):
    userToken=request.headers["AuthToken"]
    start=request.args.get('start', default="*", type=str)
    end=request.args.get('end', default="*", type=str)
    interval=request.args.get('interval', default="*", type=str)
    if start=="*" and end=="*" and interval=="*":
        if request.endpoint=="environment":
            function="getCurrentEnvironment(user)"
        elif request.endpoint=="environmentSpecific":
            function="getCurrentEnvironmentSpecific(user, datatype)"
        elif request.endpoint=="healthStatus":
            function="getCurrentHealthStatus(user)"
        elif request.endpoint=="healthStatusSpecific":
            function="getCurrentHealthStatusSpecific(user, datatype)"
        elif request.endpoint=="personalStatus":
            function="getCurrentPersonalStatus(user)"
        elif request.endpoint=="download":
            function="getAllData()"
    elif end=="*":
        if request.endpoint=="environment":
            function="getEnvironmentStartInterval(user,start, interval)"
        elif request.endpoint=="environmentSpecific":
            function="getEnvironmentSpecificStartInterval(user,datatype, start, interval)"
        elif request.endpoint=="healthStatus":
            function="getHealthStatusStartInterval(user,start, interval)"
        elif request.endpoint=="healthStatusSpecific":
            function="getHealthStatusSpecificStartInterval(user,datatype, start, interval)"
        elif request.endpoint=="personalStatus":
            function="getPersonalStatusStartInterval(user,start, interval)"
            elif request.endpoint=="download":
            function="getAllDataStartInterval(user, start, interval)"
    elif interval=="*":
        if request.endpoint=="environment":
            function="getEnvironmentStartEnd(user,start, end)"
        elif request.endpoint=="environmentSpecific":
            function="getEnvironmentSpecificStartEnd(user, datatype, start, end)"
        elif request.endpoint=="healthStatus":
            function="getHealthStatusStartEnd(user,start, end)"
        elif request.endpoint=="healthStatusSpecific":
            function="getHealthStatusSpecificStartEnd(user, datatype, start, end)"
        elif request.endpoint=="personalStatus":
            function="getPersonalStatusStartEnd(user,start, end)"
        elif request.endpoint=="download":
            function="getAllDataStartEnd(user,start, end)"
    elif start=="*":
        if request.endpoint=="environment":
            function="getEnvironmentEndInterval(user,end, interval)"
        elif request.endpoint=="environmentSpecific":
            function="getEnvironmentSpecificEndInterval(user, datatype, end, interval)"
        elif request.endpoint=="healthStatus":
            function="getHealthStatusEndInterval(user,end, interval)"
        elif request.endpoint=="healthStatusSpecific":
            function="getHealthStatusSpecificEndInterval(user, datatype, end, interval)"
        elif request.endpoint=="personalStatus":
            function="getPersonalStatusEndInterval(user,end, interval)"
        elif request.endpoint=="download":
            function="getAllDataEndInterval(user,end, interval)"

    return processor.getData(userToken, function, datatype, start, end, interval)

@app.route('/profile', methods = ['GET', 'POST', 'DELETE'])
def profile():
    userToken=request.headers["AuthToken"]
    if request.method == 'POST':
        return processor.updateProfile(userToken, request.data)
    elif request.method == 'GET':
        return processor.getProfile(userToken)
    else:
        return processor.deleteProfile(userToken)

@app.route('/supportedDevices', methods = ['GET'])
def supportedDevices():
    return processor.getSupportedDevices()


@app.route('/gps', methods = ['POST'])
def userGPSCoordinates():
    userToken=request.headers["AuthToken"]
    return processor.userGPSCoordinates(userToken, request.data)

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain("MyRootCA.crt", "MyRootCA.key")
app.run(host='0.0.0.0',port='5000', debug = False/True, ssl_context=context)