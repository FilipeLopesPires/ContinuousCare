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
    data = request.data

    type = data.get("type", None).lower()
    if not type:
        return json.dumps({"status":2, "msg":"Missing \"type\" parameter"}).encode("UTF-8")

    if type not in ["client", "medic"]:
        return json.dumps({"status":2, "msg":"Type can only be \"client\" or \"medic\""}).encode("UTF-8")

    """
    if type == "client":
        for key in [
            ("username", str, False),
            ("password", str, False),
            ("name", str, False),
            ("email", str, False),
            ("health_number", (int, str), False),
            ("birth_date", str, True),
            ("weight", float, True),
            ("height", float, True),
            ("additional_info", str, True)]:
            pass
    else:
        pass
    """

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

@app.route('/permission', methods = ['POST'])
def permission():
    """
    Use by both medic and client
    grants/requests for a permission. calls 'grantPermission' and 'requestPermission' on database.py

    args:
    username - str - of the user the he wants to grant or request permission
    duration - int
    """
    return processor.permission(request.headers["AuthToken"], request.data)

@app.route('/permissions', methods = ['GET'])
def permissions():
    """
    Use by both medic and client
    gets all current permissions. calls 'allPermissionsData' on database.py
    """
    pass

@app.route('/permission/accept', methods = ['POST'])
def acceptPermission():
    """
    Used only by the client, accepts a pending permission

    args:
    username - str - of the medic that he wants to accept request for permission
    """
    pass

@app.route('/permission/reject', methods = ['POST'])
def rejectPermission():
    """
    Used only by the client, rejects a pending permission

    args:
    username - str - of the medic that he wants to reject request for permission
    """
    pass

@app.route('/permission/pause', methods = ['POST'])
def pausePermission():
    """
    Used only by the medic, pauses an active permission so he can save time for later, still has permission

    args
    username - str - of the client that he wants to pause the active permission
    """
    pass

@app.route('/permission/pending', methods = ['DELETE'])
def removePendingPermission():
    """
    Used only by the medic, removes a pending permission (requests not responded by the client)
    """
    pass

@app.route('/permission/accepted', methods = ['DELETE'])
def removeAcceptedPermission():
    """
    Used only by the client, removes an accepted permission

    args
    username - str - of the medic that he wants to remove an accepted permission
    """
    pass

@app.route('/permission/active', methods = ['DELETE'])
def removeActivePermission():
    """
    Used only by the client, removes and active permission, accepted permission are not removed

    args
    username - str - of the medic that he wants to remove and active permission
    """
    pass

#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#context.load_cert_chain("MyRootCA.crt", "MyRootCA.key")
#app.run(host='0.0.0.0',port='5000', debug = False/True, ssl_context=context)
app.run(host='0.0.0.0',port='5000')
