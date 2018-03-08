import json
import uuid
from Utility.Encryptor import Encryptor
from Utility.color_print import ColorPrint
from flaskapp import db, app
from flask import request, Response, send_file, send_from_directory, make_response, session
from sqlalchemy.dialects.postgresql import JSON
from DBModel.User_DBModel import User_DBModel
import datetime

encryptor = Encryptor()
seconds_in_hour = 60*60
session_inactivity_timeout = datetime.timedelta(0, seconds_in_hour * 2)

class User():

	@staticmethod
	def is_government_official():
		if 'user' in session.keys():
			user = session['user']
			if User_DBModel.query.filter_by(id = user["id"]).first().account_type == "government_official":
				return make_response(str(True))
			else:
				return make_response(str(False))
		else:
			return make_response(str(False))

	@staticmethod
	def isLoggedIn():
		return make_response(str('user' in session.keys()))

	@staticmethod
	def login():

		parsed_json = request.get_json()
		email = parsed_json["email"]
		password = parsed_json["password"]

		user_info = User_DBModel.authenticate_email_password(email, password)
		if user_info is not None:
			#then this data is good, and we're in.

			user = {'id': user_info.id, 'email' : email, 'password' : password}
			
			if 'user' in session.keys():
				dict_local = {'code': 200, 'message': "already logged in"}
			else:
				session['user'] = user
				session.modified=True
				dict_local = {'code': 200}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			response = make_response(return_string)  
			return response
		else:
			#not a good cookie and no login.
			dict_local = {'code': 31, 'message': "login failed"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def logoff():
		if 'user' not in session.keys():
			dict_local = {'code': 31, 'message': "User not logged in anyways."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			session.pop('user', None)
			session.modified = True
			dict_local = {'code': 200}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string


	@staticmethod
	def list_all_users():
		if 'user' in session.keys():
			user = session['user']
			if User_DBModel.query.filter_by(id = user["id"]).first().account_type == "admin":
				db_user_devices = User_DBModel.query.all()
				return_json_list = []
				for report in db_user_devices:
					dict_local = {'id': report.id,
													'name': report.name,
													'email': report.email,
													'password' : report.password,
													'created_at': str(report.created_at),
													'account_type': report.account_type}

					return_json_list.append(dict_local)
				return_string = json.dumps(return_json_list, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
			else:
				dict_local = {'code': 37, 'message': "Permission error " + user["email"]}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
		else:
			dict_local = {'code': 31, 'message': "auth error"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def register_user():
		parsed_json = request.get_json()
		email = parsed_json["email"]
		password = parsed_json["password"]
		name = parsed_json["name"]
		account_type = parsed_json["account_type"]

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

	@staticmethod
	def update_user_info():
		if 'user' in session.keys():
			user = session['user']
			parsed_json = request.get_json()
			user_info = User_DBModel.query.filter_by(id = user["id"]).first()

			if 'email' in parsed_json:
				user_info.email = parsed_json['email']
			if 'password' in parsed_json:
				user_info.password = parsed_json['password']
			if 'name' in parsed_json:
				user_info.name = parsed_json['name']

			db.session.commit()

			return_dict = {'code': 200}
			return_string = json.dumps(return_dict, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			dict_local = {'code': 31, 'message': "auth error"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def get_user_info():
		if 'user' in session.keys():
			user = session['user']
			user_info = User_DBModel.query.filter_by(id = user["id"]).first()

			return_dict = {
				'email': user_info.email,
				'name': user_info.name,
				'created_at': str(user_info.created_at),
				'id': user['id']
			}

			return_string = json.dumps(return_dict, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			dict_local = {'code': 31, 'message': "auth error"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

app.add_url_rule('/isLoggedIn', 'isLoggedIn', User.isLoggedIn, methods=['GET'])
app.add_url_rule('/is_government_official', 'is_government_official', User.is_government_official, methods=['GET'])
app.add_url_rule('/login', 'login', User.login, methods=['POST'])
app.add_url_rule('/logoff', 'logoff', User.logoff, methods=['GET'])
app.add_url_rule('/list_all_users', 'list_all_users', User.list_all_users, methods=['GET'])
app.add_url_rule('/register_user', 'register_user', User.register_user, methods=['POST'])
app.add_url_rule('/get_user_info', 'get_user_info', User.get_user_info, methods=['GET'])
app.add_url_rule('/update_user_info', 'update_user_info', User.update_user_info, methods=['POST'])
