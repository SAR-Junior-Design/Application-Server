
from flask import Flask
from flask import request

from flaskapp import app, db

from Models.User import User
from Models.Drone import Drone
from Models.Mission import Mission


#db.drop_all()
db.create_all()

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000)
