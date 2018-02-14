import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint
import datetime
from Utility.Encryptor import Encryptor
from Utility.color_print import ColorPrint

from DBModel.Session_DBModel import Session_DBModel

encryptor = Encryptor()
seconds_in_hour = 60*60
session_inactivity_timeout = datetime.timedelta(0, seconds_in_hour * 2)

class User_DBModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Text, primary_key=True)
    email = db.Column(db.Text)
    name = db.Column(db.Text)
    password = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    account_type = db.Column(db.Text)

    def __init__(self, id, name, password, email, account_type):
        self.id = id
        self.name = name
        self.password = password
        self.email = email
        #self.created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        self.account_type = account_type

    def __repr__(self):
        return '<id {}>'.format(self.id)


    @staticmethod
    def authenticate_email_password(email, password):
        if not email or not password:
            return False
        user_info = User_DBModel.query.filter_by(email = email).first()
        if user_info is None:
                return False
        if user_info.password is not None:
                if user_info.password == password:
                        return True
        return False

    @staticmethod
    def authenticate_user_cookie(encrypted_cookie):
        if not encrypted_cookie:
            return False
        cookie = encryptor.decryptMessage(encrypted_cookie)
        email = cookie['email']
        user = User_DBModel.query.filter_by(email = email).first()

        if user is None:
            return False

        session = Session_DBModel.query.filter(Session_DBModel.email == cookie['email'], 
                 Session_DBModel.closed_at == None).first()
        isNewSession = False

        #is the session over? Does it not exist
        if session is None:
            return False               
        elif datetime.datetime.now() > session.last_activity + session_inactivity_timeout:
            #this case the session is old.
            #make sure to close this session.
            session.closed_at = session.last_activity
            db.session.commit()
            return False
        elif request.remote_addr != cookie['address']: #then someone is spoofing this from afar.
            return False
        else:
            session.last_activity = datetime.datetime.now()
            db.session.commit()

        if user.password is not None:
                if user.password == cookie['password']:
                        return True
        return False

    @staticmethod
    def decrypt_cookie(encrypted_cookie):
        if not encrypted_cookie:
            return None
        cookie = encryptor.decryptMessage(encrypted_cookie)
        return cookie
