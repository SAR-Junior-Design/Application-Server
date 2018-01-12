from flask import Flask
from flask import request

#from authentication import UserAuthentication
from flask_cors import CORS, cross_origin

from flask_sqlalchemy import SQLAlchemy

app = Flask('SarOS Back-End')

# app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ubuntu:elephants_remember_1984@localhost/sar'
app.config['COOKIE_KEY'] = b'Zwo81Qe3Pi7aAHnsPVGkjyW2FApg9ekJVN26iWPRps4='
CORS(app)
db = SQLAlchemy(app)

db.create_all()