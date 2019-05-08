from flask import Flask, request
import json
from Processor import Processor
from flask_cors import CORS
import ssl
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
    return processor.signup(request.data)

@app.route('/signin', methods = ['POST'])
def signin():
    return processor.signin(request.data)

@app.route('/logout', methods = ['GET'])
def logout():
    userToken=request.headers["AuthToken"]
    return processor.logout(userToken)

@app.route('/devices', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def devices():
    userToken=request.headers["AuthToken"]
    if request.method == 'GET':
        return processor.getAllDevices(userToken)
    elif request.method == 'POST':
        return processor.addDevice(userToken, request.data)
    elif request.method == 'PUT':
        return processor.updateDevice(userToken, request.data)
    else:
        return processor.deleteDevice(userToken, request.data)

@app.route('/environment', endpoint="Environment", methods = ['GET'])
@app.route('/healthstatus', endpoint="HealthStatus", methods = ['GET'])
@app.route('/personalstatus', endpoint="PersonalStatus", methods = ['GET'])
@app.route('/download', endpoint="download",methods = ['GET'])
def getData(datatype=None):
    userToken=request.headers["AuthToken"]
    start=request.args.get('start', default="*", type=str)
    start=start if start!="*" else None
    end=request.args.get('end', default="*", type=str)
    end=end if end!="*" else None
    interval=request.args.get('interval', default="*", type=str)
    interval=interval if interval!="*" else None
    function="getData(\""+request.endpoint+"\",user,"+str(start)+","+str(end)+","+str(interval)+")"
    if request.endpoint=="download":
        function="getData(None, None,"+str(start)+","+str(end)+","+str(interval)+")"

    return processor.getData(userToken, function)


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


@app.route('/sleep', methods = ['GET'])
def userGPSCoordinates():
    userToken=request.headers["AuthToken"]
    start=request.args.get('start', default="*", type=str)
    start=start if start!="*" else None
    end=request.args.get('end', default="*", type=str)
    end=end if end!="*" else None
    function="getData(\"Sleep\",user,"+start+","+end+")"
    return processor.getData(userToken, function)


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
        requestBody - (client) {type:"create"|"accept", username:str, duration:int(in case grant permit)}
                      (medic) {username:str}
    """
    userToken=request.headers["AuthToken"]
    if request.method == 'GET':
        return processor.getAllPermissions(userToken)
    elif request.method == 'POST':
        return processor.uploadPermission(userToken, request.data)

@app.route('/permission/<string:medic>/reject', methods = ['GET'])
def rejectPermission(medic):
    """
    Used only by the client, rejects a pending permission
    """
    userToken=request.headers["AuthToken"]
    return processor.rejectPermission(userToken, medic)

@app.route('/permission/<string:client>/pause', methods = ['GET'])
def pausePermission(client):
    """
    Used only by the medic, pauses an active permission so he can save time for later, still has permission
    """
    userToken=request.headers["AuthToken"]
    return processor.pausePermission(userToken, client)

@app.route('/permission/<string:client>/pending', methods = ['DELETE'])
def removePendingPermission(client):
    """
    Used only by the medic, removes a pending permission (requests not responded by the client)
    """
    userToken=request.headers["AuthToken"]
    return processor.removePendingPermission(userToken, client)

@app.route('/permission/<string:medic>/accepted', methods = ['DELETE'])
def removeAcceptedPermission(medic):
    """
    Used only by the client, removes an accepted permission
    """
    userToken=request.headers["AuthToken"]
    return processor.removeAcceptedPermission(userToken, medic)

@app.route('/permission/<string:medic>/active', methods = ['DELETE'])
def removeActivePermission(medic):
    """
    Used only by the client, removes and active permission, accepted permission are not removed
    """
    userToken=request.headers["AuthToken"]
    return processor.removeActivePermission(userToken, medic)

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain("MyRootCA.crt", "MyRootCA.key")

#http_server = WSGIServer(('0.0.0.0', 5000), app, ssl_context=context)
http_server = WSGIServer(('0.0.0.0', 5000), app)
http_server.serve_forever()