from flask import Flask, request
import json
from Processor import Processor
from flask_cors import CORS
import ssl
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

@app.route('/devices', methods = ['GET', 'POST'])
def devices():
    userToken=request.headers["AuthToken"]
    if request.method == 'GET':
        return processor.getAllDevices(userToken)
    else:
        return processor.addDevice(userToken, request.data)

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


@app.route('/sleep', methods = ['GET'])
def userGPSCoordinates():
    userToken=request.headers["AuthToken"]
    start=request.args.get('start', default="*", type=str)
    start=start if start!="*" else None
    end=request.args.get('end', default="*", type=str)
    end=end if end!="*" else None
    function="getData(\"Sleep\",user,"+start+","+end+")"
    return processor.getData(userToken, function, datatype, start, end, None)

#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#context.load_cert_chain("MyRootCA.crt", "MyRootCA.key")
#app.run(host='0.0.0.0',port='5000', debug = False/True, ssl_context=context)
app.run(host='0.0.0.0',port='5000')
