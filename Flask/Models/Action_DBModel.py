import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint
import datetime
from Utility.Encryptor import Encryptor

from sqlalchemy import Column, VARCHAR, TEXT, TIMESTAMP, func, FLOAT, Integer, JSON


encryptor = Encryptor()
seconds_in_hour = 60*60
session_inactivity_timeout = datetime.timedelta(0, seconds_in_hour * 2)

class Action_DBModel(db.Model):
    """
    This is the main table for any kinds of clients, if the user is not on this table, it won't get authenticated!
    """
    __tablename__ = 'actions'
    # Here we define db.Columns for the table person
    # Notice that each db.Column is also a normal Python instance attribute.
    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text)
    

    def __init__(self, id, name):
        self.id = id
        self.name = name



