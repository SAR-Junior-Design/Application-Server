
from flask import Flask
from flask import request

from flaskapp import app, db

from API.User import User as User
from API.Drone import Drone as Drone
from API.Mission import Mission as Mission
from API.Document import Document as Document

#db.drop_all()
db.create_all()

@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000)
