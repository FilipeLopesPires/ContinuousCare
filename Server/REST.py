from flask import Flask, request
import json
from Processor import Processor
from validation import ArgumentValidator
from flask_cors import CORS
import ssl
import re
import datetime
import asyncio
from gevent.pywsgi import WSGIServer

'''
Component responsable for defining and supporting the interface to the system.
The API supports https and on authorized operations should receive the personal token on the header.
'''

app = Flask(__name__)
CORS(app)
processor=Processor()


@app.route('/signup', methods = ['POST'])
def signup():
    data = request.json
    if not data:
        data = {}

    argsErrors =  ArgumentValidator.signup(data)
    if len(argsErrors) > 0:
        return json.dumps({"status":2, "msg":"Argument errors : " + ", ".join(argsErrors)}).encode("UTF-8")

    return processor.signup(data)

@app.route('/signin', methods = ['POST'])
def signin():
    data = request.json
    if not data:
        data = {}

    argsErrors =  ArgumentValidator.signin(data)
    if len(argsErrors) > 0:
        return json.dumps({"status":2, "msg":"Argument errors : " + ", ".join(argsErrors)}).encode("UTF-8")

    return processor.signin(data)

@app.route('/logout', methods = ['GET'])
def logout():

    authToken = request.headers.get("AuthToken")
    if not authToken:
        return json.dumps({"status":2, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    return processor.logout(authToken)

@app.route('/devices', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def devices():
    authToken = request.headers.get("AuthToken")
    if not authToken:
        return json.dumps({"status":2, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    data = request.json
    if not data:
        data = {}

    if request.method == 'GET':
        return processor.getAllDevices(authToken)
    elif request.method == 'POST':

        argsErrors =  ArgumentValidator.addDevice(data)
        if len(argsErrors) > 0:
            return json.dumps({"status":2, "msg":"Argument errors : " + ", ".join(argsErrors)}).encode("UTF-8")

        return processor.addDevice(authToken, data)
    elif request.method == 'PUT':

        argsErrors =  ArgumentValidator.updateDevice(data)
        if len(argsErrors) > 0:
            return json.dumps({"status":2, "msg":"Argument errors : " + ", ".join(argsErrors)}).encode("UTF-8")

        return processor.updateDevice(authToken, data)
    else:

        argsErrors =  ArgumentValidator.deleteDevice(data)
        if len(argsErrors) > 0:
            return json.dumps({"status":2, "msg":"Argument errors : " + ", ".join(argsErrors)}).encode("UTF-8")

    return processor.deleteDevice(authToken, data)

@app.route('/mood',methods = ['POST', 'DELETE'])
def registerMood():
    userToken = request.headers.get("AuthToken")
    if not userToken:
        return json.dumps({"status":2, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    data = request.json
    if not data:
        data = {}

    if request.method=="POST":
        argsErrors =  ArgumentValidator.registerMood(data)
        if len(argsErrors) > 0:
            return json.dumps({"status":2, "msg":"Argument errors : " + ", ".join(argsErrors)}).encode("UTF-8")

        return processor.registerMood(userToken, data)
    else:
        argsErrors =  ArgumentValidator.deleteMood(data)
        if len(argsErrors) > 0:
            return json.dumps({"status":2, "msg":"Argument errors : " + ", ".join(argsErrors)}).encode("UTF-8")

        return processor.deleteMood(userToken, data)


def _interval_to_timedelta(interval):
    if "ns" in interval:
        return datetime.timedelta(microseconds=0)
    elif "u" in interval:
        return datetime.timedelta(microseconds=interval[:-1])
    elif "ms" in interval:
        return datetime.timedelta(milliseconds=interval[:-2])
    elif "s" in interval:
        return datetime.timedelta(seconds=interval[:-1])
    elif "m" in interval:
        return datetime.timedelta(minutes=interval[:-1])
    elif "h" in interval:
        return datetime.timedelta(hours=interval[:-1])
    elif "d" in interval:
        return datetime.timedelta(days=interval[:-1])
    elif "w" in interval:
        return datetime.timedelta(weeks=interval[:-1])


@app.route('/environment', endpoint="Environment", methods = ['GET'])
@app.route('/healthstatus', endpoint="HealthStatus", methods = ['GET'])
@app.route('/personalstatus', endpoint="PersonalStatus", methods = ['GET'])
@app.route('/sleep', endpoint="Sleep", methods = ['GET'])
@app.route('/event', endpoint="Event", methods = ['GET'])
@app.route('/path', endpoint="Path", methods = ['GET'])
@app.route('/download', endpoint="download",methods = ['GET'])
def getData():
    userToken = request.headers.get("AuthToken")
    if not userToken and request.endpoint != "download":
        return json.dumps({"status":2, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    start=request.args.get('start', type=int)
    end=request.args.get('end', type=int)
    interval=request.args.get('interval')
    patient=request.args.get('patient')

    argsErrors =  ArgumentValidator.getData({
        'start': start,
        'end': end,
        'interval': interval,
        'patient': patient
    })
    if len(argsErrors) > 0:
        return json.dumps({"status":2, "msg":"Argument errors : " + ", ".join(argsErrors)}).encode("UTF-8")

    # Verify if the interval requested extends 30 days
    interval = 0

    if interval:
        if start and end:
            return json.dumps({"status": 1, "msg": "Only combination of two and one paremeters are allowed,"
                                                    "ex: start and end, start and interval"}).endode("UTF-8")
        else:
            interval = _interval_to_timedelta(interval)
    else:
        if start and end:
            interval = datetime.datetime.fromtimestamp(int(end)) - datetime.datetime.fromtimestamp(int(start))
        elif start:
            interval = datetime.datetime.now() - datetime.datetime.fromtimestamp(int(start))
        elif end:
            interval = datetime.timedelta.max

    if interval > datetime.timedelta(days=30):
        return json.dumps({"status": 1, "msg": "Interval requested extends 30 days."}).encode("UTF-8")

    return processor.getData(userToken, request.endpoint, start, end, interval, patient)

@app.route('/profile', methods = ['GET', 'PUT', 'DELETE'])
def profile():
    userToken = request.headers.get("AuthToken")
    if not userToken:
        return json.dumps({"status":2, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    if request.method == 'PUT':
        data = request.json
        if not data:
            data = {}

        return processor.updateProfile(userToken, data)
    elif request.method == 'GET':
        return processor.getProfile(userToken)
    else:
        return processor.deleteProfile(userToken)

@app.route('/supportedDevices', methods = ['GET'])
def supportedDevices():
    return processor.getSupportedDevices()


@app.route('/permission', methods = ['GET','POST'])
def permissions():
    """
    GET:
        Use by both medic and client
        gets all current permissions. calls 'allPermissionsData' on database.py

    POST:
        Use by both medic and client
        client -> grant permission/accept permission
        medic -> asks for permission
        args:
        requestBody - (client) {username:str, duration:int(in case grant permit)}
                      (medic) {username:str, health_number:int, duration:int}
    """
    userToken = request.headers.get("AuthToken")
    if not userToken:
        return json.dumps({"status":2, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    if request.method == 'GET':
        return processor.getAllPermissions(userToken)
    elif request.method == 'POST':
        data = request.json
        if not data:
            data = {}

        return processor.uploadPermission(userToken, data)

@app.route('/permission/<string:medic>/accept', methods = ['GET'])
def acceptPermission(medic):
    """
    Used only by the client, accepts a pending permission
    """
    userToken = request.headers.get("AuthToken")
    if not userToken:
        return json.dumps({"status":2, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    return processor.acceptPermission(userToken, medic)

@app.route('/permission/<string:medic>/reject', methods = ['GET'])
def rejectPermission(medic):
    """
    Used only by the client, rejects a pending permission
    """
    userToken = request.headers.get("AuthToken")
    if not userToken:
        return json.dumps({"status":2, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    return processor.rejectPermission(userToken, medic)

@app.route('/permission/<string:client>/pending', methods = ['DELETE'])
def removePendingPermission(client):
    """
    Used only by the medic, removes a pending permission (requests not responded by the client)
    """
    userToken = request.headers.get("AuthToken")
    if not userToken:
        return json.dumps({"status":2, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    return processor.removePendingPermission(userToken, client)

@app.route('/permission/<string:medic>/accepted', methods = ['DELETE'])
def removeAcceptedPermission(medic):
    """
    Used only by the client, removes an accepted permission
    """
    userToken = request.headers.get("AuthToken")
    if not userToken:
        return json.dumps({"status":2, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    return processor.removeAcceptedPermission(userToken, medic)


#If later in the project it is necessary to extablish a https server, this are the configurations needed for taht
#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#context.load_cert_chain("MyRootCA.crt", "MyRootCA.key")
#http_server = WSGIServer(('0.0.0.0', 5000), app, ssl_context=context)

http_server = WSGIServer(('0.0.0.0', 5000), app)
http_server.serve_forever()
