from flask import Flask
from flask import request

#from authentication import UserAuthentication
from flask_cors import CORS, cross_origin

from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_mail import Mail


app = Flask('SarOS Back-End')

# app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ubuntu:elephants_remember_1984@localhost/sar'
app.config['COOKIE_KEY'] = b'Zwo81Qe3Pi7aAHnsPVGkjyW2FApg9ekJVN26iWPRps4='
CORS(app)
db = SQLAlchemy(app)
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
app.config['SECRET_KEY'] = 'Zwo81Qe3Pi7aAHnsPVGkjyW2FApg9ekJVN26iWPRps4='
app.config['SESSION_COOKIE_NAME'] = 'sar-session'

Session(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_DEBUG'] = 'app.debug'
app.config['MAIL_USERNAME'] = 'samcrane8@gmail.com'
app.config['MAIL_PASSWORD'] = 'tbbkptgsqxsfiuwn'
app.config['MAIL_DEFAULT_SENDER'] = None
app.config['MAIL_MAX_EMAILS'] = None
#app.config['MAIL_SUPPRESS_SEND'] = True
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app) #use this to send mail messages.

db.create_all()