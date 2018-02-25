import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint
import datetime
from Utility.Encryptor import Encryptor



class Mission_DBModel(db.Model):
    __tablename__ = 'missions'
    id = db.Column(db.Text, primary_key=True)
    commander = db.Column(db.Text, db.ForeignKey('users.id'))
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    area = db.Column(db.JSON) #the area of a mission is described in GeoJSON
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    starts_at = db.Column(db.DateTime, default=None)
    ends_at = db.Column(db.DateTime, default=None)
    closed_at = db.Column(db.DateTime, default=None)
    current_action = db.column(db.Text, db.ForeignKey('actions.id'))

    def __init__(self, id, title, commander, area, description, starts_at, ends_at):
        self.id = id
        self.title = title
        self.commander = commander
        self.area = area
        self.description = description
        self.starts_at = starts_at
        self.ends_at = ends_at

    def __repr__(self):
        return '<id {}>'.format(self.id)