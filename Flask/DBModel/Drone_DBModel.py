import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint
import datetime
from Utility.Encryptor import Encryptor

from DBModel.Session_DBModel import Session_DBModel

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
    username = db.Column(VARCHAR(66), primary_key=True)
    description = db.Column(TEXT, nullable=False)
    creation_date = db.Column(TIMESTAMP(0), server_default=func.now())

    owner = db.Column(VARCHAR(60), nullable=False)

    latitude = db.Column(FLOAT) # TODO make sure that it doesn't round up!
    longitude = db.Column(FLOAT)
    altitude = db.Column(FLOAT)

    speed_x = db.Column(FLOAT)
    speed_y = db.Column(FLOAT)
    speed_z = db.Column(FLOAT)

    accel_x = db.Column(FLOAT)
    accel_y = db.Column(FLOAT)
    accel_z = db.Column(FLOAT)

    voltage = db.Column(FLOAT)
    consumption = db.Column(FLOAT)
    mAh_remaining = db.Column(FLOAT)

    connection_type = db.Column(VARCHAR(40))
    connection_ssid = db.Column(VARCHAR(60), default=0)
    connection_rssi = db.Column(Integer, default=0)

    current_action = db.Column(JSON)

    def __init__(self, username, description):
        self.username = username
        self.description = description

    @staticmethod
    def update_drone_info(username,location, speed, accel, battery, connection, current_action):
        drone = Drone_db.query.filter_by(filter=username).first()
        drone.lattitude = location["latitude"]
        drone.longtitude = location["longitude"]
        drone.altitude = location["altitude"]

        drone.speed_x = speed["speed_x"]
        drone.speed_y = speed["speed_y"]
        drone.speed_z = speed["speed_z"]

        drone.accel_x =  accel["accel_x"]
        drone.accel_y = accel["accel_y"]
        drone.accel_z = accel["accel_z"]

        drone.voltage = battery["voltage"]
        drone.consumption = battery["consumption"]
        drone.mAh_remaining = battery["mAh_remaining"]

        drone.connection_type = connection["connection_type"]
        drone.connection_ssid = connection["ssid"]
        drone.connection_rssi = connection["rssi"]

        drone.current_action = current_action



