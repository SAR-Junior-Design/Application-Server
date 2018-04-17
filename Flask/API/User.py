import json
import uuid
from Utility.Encryptor import Encryptor
from Utility.color_print import ColorPrint
from flaskapp import db, app
from Utility.API_Helpers import row2dict, login_required, must_be_gov_official, must_be_admin
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
	@login_required
	@must_be_admin
	def list_all_users():
		user = session['user']
		db_user_devices = User_DBModel.query.all()
		return_json_list = []
		for report in db_user_devices:
			return_json_list.append(row2dict(report))
		return_string = json.dumps(return_json_list, sort_keys=True, indent=4, separators=(',', ': '))
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

	@staticmethod
	@login_required
	def update_user_info():
		user = session['user']
		parsed_json = request.get_json()
		user_info = User_DBModel.query.filter_by(id = user["id"]).first()

		if 'email' in parsed_json:
			user_info.email = parsed_json['email']
		if 'password' in parsed_json:
			user_info.password = parsed_json['password']
		if 'name' in parsed_json:
			user_info.name = parsed_json['name']
		if 'picture' in parsed_json:
			user_info.picture = parsed_json['picture']

		db.session.commit()

		return_dict = {'code': 200}
		return_string = json.dumps(return_dict, sort_keys=True, indent=4, separators=(',', ': '))
		return return_string

	@staticmethod
	@login_required
	def get_user_info():
		user = session['user']
		user_info = User_DBModel.query.filter_by(id = user["id"]).first()

		return_dict = {
			'email': user_info.email,
			'name': user_info.name,
			'created_at': str(user_info.created_at),
			'id': user['id'],
			'account_type': user_info.account_type,
			'picture': user_info.picture
		}

		return_string = json.dumps(return_dict, sort_keys=True, indent=4, separators=(',', ': '))
		return return_string

	@staticmethod
	def login_v1_1():

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
			dict_local = {'message': "Bad login credentials."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')

	@staticmethod
	def logoff_v1_1():
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
	def register_user_v1_1():
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

			return_json = {'message': 'User successfully registered.'}
			return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			dict_local = {'message': "Email already taken."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')

#v1.1
app.add_url_rule('/v1_1/login', '/v1_1/login', User.login_v1_1, methods=['POST'])
app.add_url_rule('/v1_1/logoff', '/v1_1/logoff', User.logoff_v1_1, methods=['GET'])
app.add_url_rule('/v1_1/register_user', '/v1_1/register_user', User.register_user_v1_1, methods=['POST'])

#v1.0
app.add_url_rule('/v1_0/isLoggedIn', '/v1_0/isLoggedIn', User.isLoggedIn, methods=['GET'])
app.add_url_rule('/v1_0/is_government_official', '/v1_0/is_government_official', User.is_government_official, methods=['GET'])
app.add_url_rule('/v1_0/list_all_users', '/v1_0/list_all_users', User.list_all_users, methods=['GET'])
app.add_url_rule('/v1_0/register_user', '/v1_0/register_user', User.register_user, methods=['POST'])
app.add_url_rule('/v1_0/get_user_info', '/v1_0/get_user_info', User.get_user_info, methods=['GET'])
app.add_url_rule('/v1_0/update_user_info', '/v1_0/update_user_info', User.update_user_info, methods=['POST'])
