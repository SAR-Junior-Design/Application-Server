import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint
import datetime
from Utility.Encryptor import Encryptor

class Document_DBModel(db.Model):
	__tablename__ = 'document'
	id = db.Column(db.Text, primary_key=True)
	owner = db.Column(db.Text, db.ForeignKey('users.id', ondelete = 'CASCADE'))
	location = db.Column(db.Text)
	document_type = db.Column(db.Text)

	def __init__(self, id, owner, location, document_type):
		self.id = id
		self.owner = owner
		self.location = location
		self.document_type = document_type