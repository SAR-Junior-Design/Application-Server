import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint
import datetime
from Utility.Encryptor import Encryptor


encryptor = Encryptor()
seconds_in_hour = 60*60
session_inactivity_timeout = datetime.timedelta(0, seconds_in_hour * 2)

class Drone_DBModel(db.Model):
    __tablename__ = 'drones'
    # Here we define db.Columns for the table person
    # Notice that each db.Column is also a normal Python instance attribute.
    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text),

    manufacturer = db.Column(db.Text),
    type = db.Column(db.Text),
    color = db.Column(db.Text),
    number_of_blades = db.Column(db.Integer),


    owner = db.Column(db.Text, db.ForeignKey('users.id', ondelete = 'CASCADE'))
    description = db.Column(db.Text)
    live_data = db.Column(db.Text, db.ForeignKey('live_drone_data.id', ondelete = 'CASCADE'))


    def __init__(self, id, owner, description, live_data, manufacturer = "", type="", color="", number_of_blades = 0):
        self.id = id
        self.owner = owner
        self.description = description
        self.live_data = live_data

        self.manufacturer = manufacturer
        self.type = type
        self.color = color
        self.number_of_blades = number_of_blades



