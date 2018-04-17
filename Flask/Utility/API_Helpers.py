from flask import request, Response, send_file, send_from_directory, make_response, session

#from authentication import UserAuthentication
from flask_cors import CORS, cross_origin

from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_mail import Mail
from functools import wraps

from Models.User_DBModel import User_DBModel

import json

#UTILITY

def row2dict(row):
	d = {}
	for column in row.__table__.columns:
		d[column.name] = str(getattr(row, column.name))
	return d

#WRAPS
def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if 'user' not in session.keys():
			dict_local = {'message': "Auth error."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')
		return f(*args, **kwargs)
	return decorated_function

def must_be_gov_official(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		user = session['user']
		if User_DBModel.query.filter_by(id = user["id"]).first().account_type != "government_official":
			dict_local = {'message': "Must be a government official to use this call."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')
		return f(*args, **kwargs)
	return decorated_function

def must_be_admin(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		user = session['user']
		if User_DBModel.query.filter_by(id = user["id"]).first().account_type != "admin":
			dict_local = {'message': "Must be an admin to use this call."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')
		return f(*args, **kwargs)
	return decorated_function