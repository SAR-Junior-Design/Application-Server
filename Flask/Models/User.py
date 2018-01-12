import json
import uuid
from Utility.Encryptor import Encryptor
from Utility.color_print import ColorPrint
from flaskapp import db, app
from flask import request, Response, send_file, send_from_directory, make_response
from sqlalchemy.dialects.postgresql import JSON
from DBModel.User_DBModel import User_DBModel
from DBModel.Session_DBModel import Session_DBModel
import datetime

encryptor = Encryptor()
seconds_in_hour = 60*60
session_inactivity_timeout = datetime.timedelta(0, seconds_in_hour * 2)

class User():

    @staticmethod
    def login():
        encrypted_cookie = request.cookies.get('sessionID')

        parsed_json = request.get_json()
        email = parsed_json["email"]
        password = parsed_json["password"]
        if User_DBModel.authenticate_user_cookie(encrypted_cookie):
            #then we've already logged on.
            dict_local = {'code': 200, 'message': "Already logged in."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string 
        elif User_DBModel.authenticate_email_password(email, password):
            #then there's not a good cookie, and we're loggin in.
            user = User_DBModel.query.filter_by(email = email).first();
            id = uuid.uuid4()
            session = Session_DBModel(id, str(request.remote_addr), user.email)
            db.session.add(session)
            db.session.commit()

            jsonCookie = {'email' : user.email, 'password' : user.password, 'address': request.remote_addr}
            cook_str = json.dumps(jsonCookie, sort_keys=True, indent=4, separators=(',', ': '))
            encodedCookie = encryptor.encryptMessage(cook_str)
            dict_local = {'code': 200}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            response = make_response(return_string)  
            response.set_cookie('sessionID',value=encodedCookie)
            return response
        else:
            #not a good cookie and no login.
            dict_local = {'code': 31, 'message': "login failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string


    @staticmethod
    def logoff():
        encrypted_cookie = request.cookies.get('sessionID')
        if User_DBModel.authenticate_user_cookie(encrypted_cookie):
            cookie = User_DBModel.decrypt_cookie(encrypted_cookie)
            session = Session_DBModel.query.filter(Session_DBModel.email == cookie['email'], 
                 Session_DBModel.closed_at == None).first()
            if session is None:
                dict_local = {'code': 31, 'message': "User not logged in anyways."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            else:
                session.closed_at = datetime.datetime.now()
                db.session.commit()
                dict_local = {'code': 200}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            dict_local = {'code': 31, 'message': "User not logged in anyways."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string


    @staticmethod
    def list_all_users():
        encrypted_cookie = request.cookies.get('sessionID')
        if User_DBModel.authenticate_user_cookie(encrypted_cookie):
            cookie = User_DBModel.decrypt_cookie(encrypted_cookie)
            if cookie is None:
                dict_local = {'code': 31, 'message': "auth error"}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            if User_DBModel.query.filter_by(email = cookie["email"]).first().account_type == "admin":
                db_user_devices = User_DBModel.query.all()
                return_json_list = []
                for report in db_user_devices:
                    dict_local = {'name': report.name,
                                                    'email': report.email,
                                                    'password' : report.password,
                                                    'created_at': str(report.created_at),
                                                    'account_type': report.account_type}

                    return_json_list.append(dict_local)
                return_string = json.dumps(return_json_list, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            else:
                dict_local = {'code': 37, 'message': "Permission error " + cookie["email"]}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            dict_local = {'code': 31, 'message': "auth error"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def register_user():
        encrypted_cookie = request.cookies.get('sessionID')
        if User_DBModel.authenticate_user_cookie(encrypted_cookie):
            parsed_json = request.get_json()
            email = parsed_json["email"]
            password = parsed_json["password"]
            name = parsed_json["name"]
            account_type = parsed_json["account_type"]

            user = User_DBModel(name, password, email, account_type)
            db.session.add(user)
            db.session.commit()

            return_json = {'code': 200}
            return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

        else:
            dict_local = {'code': 31, 'message': "auth error"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string	

app.add_url_rule('/login', 'login', User.login, methods=['POST'])
app.add_url_rule('/logoff', 'logoff', User.logoff, methods=['GET'])
app.add_url_rule('/list_all_users', 'list_all_users', User.list_all_users, methods=['GET'])
app.add_url_rule('/register_user', 'register_user', User.register_user, methods=['POST'])
