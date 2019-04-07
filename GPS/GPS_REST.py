from flask import Flask, request
import json


app = Flask(__name__)

userLocations={}

@app.route('/gps/<string:user>', methods = ['POST', 'GET'])
def userGPSCoordinates(user):
    if request.method=='POST':
        coords=json.loads(request.data.decode("UTF-8"))
        lat=coords["lat"]
        longi=coords["longi"]
        userLocations[user]={"lat":lat, "longi":longi}
        return json.dumps({"status":0, "message":"All Good"}).encode("UTF-8")
    else:
        if user not in userLocations:
            return json.dumps({"status":1, "message":"User Unknown"}).encode("UTF-8")
        return json.dumps({"status":0, "message":"All Good", "data":userLocations[user].encode("UTF-8")}).encode("UTF-8")


app.run(host='0.0.0.0',port='5555')