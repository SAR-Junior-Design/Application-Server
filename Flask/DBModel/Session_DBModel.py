import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint
import datetime


class Session_DBModel(db.Model):
	__tablename__ = 'session'

	id = db.Column(db.Text, primary_key=True)
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	closed_at = db.Column(db.DateTime)
	last_activity = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	remote_addr = db.Column(db.Text)
	email = db.Column(db.Text, db.ForeignKey('users.email', ondelete = 'CASCADE'),
					primary_key = True)

	def __init__(self, id, remote_addr, email):
		self.id = id
		self.remote_addr = remote_addr
		self.email = email


	def __repr__(self):
		return 'Session <{}>'.format(self.id)




