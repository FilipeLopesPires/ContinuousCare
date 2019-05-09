from flask import Flask, request
import json
from Processor import Processor
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

class ArgumentValidator:
    """
    Holds the functions that validate the arguments
        of rest paths
    """

    @staticmethod
    def _validate(data, validation):
        """
        Validates that data received on rest path
            follow the expected arguments

        :param data: data to validate
        :type data: dict
        :param validation: list of tuples with KEY of mandatory fields
            EXPECTEDTYPES for those filds and if that field is mandatory
        :type validation: list
        :return: all errors presents on arguments
        :rtype: list
        """
        errors = []
        for key, expectedType, mandatory in validation:
            try:
                value = data[key] # some values have value null that's why I didn't use get(key, default)
            except KeyError:
                if mandatory:
                    errors.append("Missing key \"" + key + "\"")
                continue

            if not value:
                if mandatory:
                    errors.append("Value \"" + key + "\" can't be null")
                continue

            if not isinstance(value, expectedType):
                if isinstance(value, str):
                    if  (expectedType == int and re.match(r"^[-+]?\d+$", value)) \
                    or (expectedType == float and re.match(r"^[-+]?\d+(\.\d+)?$", value)):
                        continue
                elif isinstance(value, int) and expectedType == float:
                    continue

                errors.append("Value \"" + key + "\" is type "
                              + type(value).__name__ + " but "
                              + expectedType.__name__ + " was expected")

        return errors

    @staticmethod
    def signupAndUpdateProfile(data):
        userType = data.get("type")
        if not userType:
            return ["Missing \"type\" parameter"]

        userType = userType.lower()

        if userType not in ["client", "medic"]:
            return ["Type can only be \"client\" or \"medic\""]

        if userType == "client":
            result =  ArgumentValidator._validate(
                data, [
                    ("username", str, True),
                    ("password", str, True),
                    ("name", str, True),
                    ("email", str, True),
                    ("health_number", int, True),
                    ("birth_date", str, False),
                    ("weight", float, False),
                    ("height", float, False),
                    ("additional_info", str, False)]
            )

            birth_date = data.get("birth_date")
            if birth_date and isinstance(birth_date, str):
                if not re.match(r"^\d{1,2}-\d{1,2}-\d{4}$", birth_date):
                    result.append("Invalid date format. Should follow dd-mm-yyyy.")
                else:
                    try:
                        day, month, year = birth_date.split("-")
                        datetime.date(day, month, year)
                    except ValueError:
                        result.append("Invalid date.")

            return result

        return ArgumentValidator._validate(
            data, [
                ("username", str, True),
                ("password", str, True),
                ("name", str, True),
                ("email", str, True),
                ("company", str, False),
                ("specialities", str, False)]
        )

    @staticmethod
    def signin(data):
        return ArgumentValidator._validate(
            data, [
                ("username", str, True),
                ("password", str, True)
            ]
        )

    @staticmethod
    def _addAndUpdateDevice(isAdd, data):
        """
        Use to validate arguments for both addDevice and updateDevice

        :param isAdd: true if it's to validate addDevice fields,
            or false if it's to validate updateDevice
        :type isAdd: bool
        :param data: data to validate
        :type data: dict
        :return: list of errors
        :rtype: list
        """
        fields = [
            ("authentication_fields", list, True),
            ("latitude", float, False),
            ("longitude", float, False)
        ]

        if isAdd:
            fields.append(("type", str, True))
        else:
            fields.append(("id", int, True))

        result = ArgumentValidator._validate(data, fields)

        auth_fields = data.get("authentication_fields")

        if auth_fields and isinstance(auth_fields, list):
            for value in auth_fields.values():
                if not isinstance(value, str):
                    result.append("Authentication fields have to be strings.")
                    break

        return result

    @staticmethod
    def addDevice(data):
        return ArgumentValidator._addAndUpdateDevice(True, data)

    @staticmethod
    def updateDevice(data):
        return ArgumentValidator._addAndUpdateDevice(False, data)

    @staticmethod
    def deleteDevice(data):
        return ArgumentValidator._validate(
            data, [
                ("id", int, True)
            ]
        )

@app.route('/signup', methods = ['POST'])
def signup():
    data = request.json
    if not data:
        data = {}

    argsErrors =  ArgumentValidator.signupAndUpdateProfile(data)
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
        return json.dumps({"status":4, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    return processor.logout(authToken)

@app.route('/devices', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def devices():
    authToken = request.headers.get("AuthToken")
    if not authToken:
        return json.dumps({"status":4, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

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
    userToken = request.headers.get("AuthToken")
    if not userToken:
        return json.dumps({"status":4, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    if request.method == 'POST':
        data = request.json
        if not data:
            data = {}

        argsErrors =  ArgumentValidator.signupAndUpdateProfile(data)
        if len(argsErrors) > 0:
            return json.dumps({"status":2, "msg":"Argument errors : " + ", ".join(argsErrors)}).encode("UTF-8")

        return processor.updateProfile(userToken, data)
    elif request.method == 'GET':
        return processor.getProfile(userToken)
    else:
        return processor.deleteProfile(userToken)

@app.route('/supportedDevices', methods = ['GET'])
def supportedDevices():
    return processor.getSupportedDevices()


@app.route('/sleep', methods = ['GET'])
def userGPSCoordinates():
    userToken = request.headers.get("AuthToken")
    if not userToken:
        return json.dumps({"status":4, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

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
        requestBody - (client) {type:"grant"|"accept", username:str, duration:int(in case grant permit)}
                      (medic) {username:str}
    """
    userToken = request.headers.get("AuthToken")
    if not userToken:
        return json.dumps({"status":4, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    if request.method == 'GET':
        return processor.getAllPermissions(userToken)
    elif request.method == 'POST':
        data = request.json
        if not data:
            data = {}

        #argsErrors =  ArgumentValidator.(data) # TODO
        if len(argsErrors) > 0:
            return json.dumps({"status":2, "msg":"Argument errors : " + ", ".join(argsErrors)}).encode("UTF-8")

        return processor.uploadPermission(userToken, request.data)

@app.route('/permission/<string:medic>/reject', methods = ['GET'])
def rejectPermission(medic):
    """
    Used only by the client, rejects a pending permission
    """
    userToken = request.headers.get("AuthToken")
    if not userToken:
        return json.dumps({"status":4, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    return processor.rejectPermission(userToken, medic)

@app.route('/permission/<string:client>/pause', methods = ['GET'])
def pausePermission(client):
    """
    Used only by the medic, pauses an active permission so he can save time for later, still has permission
    """
    userToken = request.headers.get("AuthToken")
    if not userToken:
        return json.dumps({"status":4, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    return processor.pausePermission(userToken, client)

@app.route('/permission/<string:client>/pending', methods = ['DELETE'])
def removePendingPermission(client):
    """
    Used only by the medic, removes a pending permission (requests not responded by the client)
    """
    userToken = request.headers.get("AuthToken")
    if not userToken:
        return json.dumps({"status":4, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    return processor.removePendingPermission(userToken, client)

@app.route('/permission/<string:medic>/accepted', methods = ['DELETE'])
def removeAcceptedPermission(medic):
    """
    Used only by the client, removes an accepted permission
    """
    userToken = request.headers.get("AuthToken")
    if not userToken:
        return json.dumps({"status":4, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    return processor.removeAcceptedPermission(userToken, medic)

@app.route('/permission/<string:medic>/active', methods = ['DELETE'])
def removeActivePermission(medic):
    """
    Used only by the client, removes and active permission, accepted permission are not removed
    """
    userToken = request.headers.get("AuthToken")
    if not userToken:
        return json.dumps({"status":4, "msg":"This path requires an authentication token on headers named \"AuthToken\""}).encode("UTF-8")

    return processor.removeActivePermission(userToken, medic)

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain("MyRootCA.crt", "MyRootCA.key")

#http_server = WSGIServer(('0.0.0.0', 5000), app, ssl_context=context)
http_server = WSGIServer(('0.0.0.0', 5000), app)
http_server.serve_forever()
