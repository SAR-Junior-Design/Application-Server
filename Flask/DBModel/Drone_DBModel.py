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

class Drone_DBModel(db.Model):
    """
    This is the main table for any kinds of clients, if the user is not on this table, it won't get authenticated!
    """
    __tablename__ = 'drones'
    # Here we define db.Columns for the table person
    # Notice that each db.Column is also a normal Python instance attribute.
    id = db.Column(db.Text, primary_key=True)
    owner = db.Column(db.Text, db.ForeignKey('users.id', ondelete = 'CASCADE'), primary_key=True)
    description = db.Column(db.Text)
    live_data = db.Column(db.Text, db.ForeignKey('live_drone_data.id', ondelete = 'CASCADE'), primary_key=True)


    def __init__(self, id, owner, description, live_data):
        self.id = id
        self.owner = owner
        self.description = description
        self.live_data = live_data



