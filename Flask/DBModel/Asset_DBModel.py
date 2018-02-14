import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint
import datetime
from Utility.Encryptor import Encryptor


class Asset_DBModel(db.Model):
    __tablename__ = 'assets'
    drone_id = db.Column(db.Text, db.ForeignKey('drones.id', ondelete = 'CASCADE'), primary_key=True)
    operator = db.Column(db.Text, db.ForeignKey('users.id', ondelete = 'CASCADE'), primary_key=True)
    mission_id = db.Column(db.Text, db.ForeignKey('missions.id', ondelete = 'CASCADE'), primary_key=True)

    def __init__(self, drone_id, operator, mission_id):
        self.drone_id = drone_id
        self.operator = operator
        self.mission_id = mission_id

    def __repr__(self):
        return '<id {}>'.format(self.id)