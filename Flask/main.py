
from flask import Flask
from flask import request

from flaskapp import app, db

from API.V1_0.User import User as V1_0_User
from API.V1_0.Drone import Drone as V1_0_Drone
from API.V1_0.Mission import Mission as V1_0_Mission

from API.V1_1.Drone import Drone as V1_1_Drone
from API.V1_1.Mission import Mission as V1_1_Mission
from API.V1_1.User import User as V1_1_User

#db.drop_all()
db.create_all()

@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000)
