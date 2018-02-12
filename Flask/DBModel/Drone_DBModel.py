import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint
import datetime
from Utility.Encryptor import Encryptor

from DBModel.Session_DBModel import Session_DBModel

encryptor = Encryptor()
seconds_in_hour = 60*60
session_inactivity_timeout = datetime.timedelta(0, seconds_in_hour * 2)

class Drone_DBModel(db.Model):
    __tablename__ = 'drones'
    id = db.Column(db.Text, primary_key=True)
    owner = db.Column(db.Text, db.ForeignKey('users.email', ondelete = 'CASCADE'))
    type = db.Column(db.Text)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    # this will be the mission the drone is tied to.

    def __init__(self, id, owner, type):
        self.id = id
        self.owner = owner
        self.type = type

    def __repr__(self):
        return '<id {}>'.format(self.id)
