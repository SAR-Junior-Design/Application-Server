import json
import uuid
from Utility.Encryptor import Encryptor
from Utility.color_print import ColorPrint
from flaskapp import db, app
from flask import request, Response, send_file, send_from_directory, make_response, session
from sqlalchemy.dialects.postgresql import JSON
from Models.User_DBModel import User_DBModel
import datetime
import hashlib

encryptor = Encryptor()
seconds_in_hour = 60*60
session_inactivity_timeout = datetime.timedelta(0, seconds_in_hour * 2)

class User():

	@staticmethod
	def login():

		parsed_json = request.get_json()
		if "email" not in parsed_json.keys():
			dict_local = {'message': "No email attribute."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')
		email = parsed_json["email"]

		if "password" not in parsed_json.keys():
			dict_local = {'message': "No password attribute."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')
		password = parsed_json["password"]
		password = str(hashlib.sha256(password.encode()).hexdigest())

		user_info = User_DBModel.authenticate_email_password(email, password)
		if user_info is not None:
			#then this data is good, and we're in.

			user = {'id': user_info.id, 'name': user_info.name, 'email' : email, 'password' : password}
			
			if 'user' in session.keys():
				dict_local = {'message': "already logged in"}
			else:
				session['user'] = user
				session.modified=True
				dict_local = {'message': "Logged in successfully."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=200, mimetype='application/json')
		else:
			#not a good cookie and no login.
			dict_local = {'message': "login failed"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')

	@staticmethod
	def logoff():
		if 'user' not in session.keys():
			dict_local = {'message': "User not logged in anyways."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=200, mimetype='application/json')
		else:
			session.pop('user', None)
			session.modified = True
			dict_local = {'message': "User logged off successfully."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string


	@staticmethod
	def register_user():
		parsed_json = request.get_json()
		email = parsed_json["email"]
		password = parsed_json["password"]
		password = str(hashlib.sha256(password.encode()).hexdigest())
		name = parsed_json["name"]
		account_type = 'operator'

		if User_DBModel.query.filter_by(email = email).first() is None:
			id = str(uuid.uuid4())
			user = User_DBModel(id, name, password, email, account_type)
			db.session.add(user)
			db.session.commit()

			return_json = {'code': 200}
			return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			return_json = {'code': 31, 'message': 'Email already taken.'}
			return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string


app.add_url_rule('/v1_1/login', '/v1_1/login', User.login, methods=['POST'])
app.add_url_rule('/v1_1/logoff', '/v1_1/logoff', User.logoff, methods=['GET'])
app.add_url_rule('/v1_1/register_user', '/v1_1/register_user', User.register_user, methods=['POST'])



