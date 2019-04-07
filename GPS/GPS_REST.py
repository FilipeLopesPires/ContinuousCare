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
        return json.dumps({"status":0, "message":"All Good"})
    else:
        return json.dumps({"data":{"latitude":40, "longitude":-8}})
        if user not in userLocations:
            return json.dumps({"status":1, "message":"User Unknown"})
        return json.dumps({"status":0, "message":"All Good", "data":userLocations[user]})


app.run(host='0.0.0.0',port='5555')