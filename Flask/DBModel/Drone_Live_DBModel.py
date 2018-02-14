from sqlalchemy import Column, VARCHAR, TEXT, TIMESTAMP, func, FLOAT, Integer, JSON
from flaskapp import db, app


class Drone_Live_DBModel(db.Model):
    """
    This is the main table for live drone data. The tunnel server will update this information.
    """
    __tablename__ = 'live_drone_data'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(db.TEXT, primary_key=True)
    description = Column(db.TEXT, nullable=False)
    creation_date = Column(db.TIMESTAMP(0), server_default=func.now())
    last_update = Column(db.TIMESTAMP(0))

    owner = Column(db.VARCHAR(60), nullable=False)
    # latitude = Column(FLOAT)
    # longitude = Column(FLOAT)
    # altitude = Column(FLOAT)

    speed = Column(db.JSON)

    #
    # speed_x = Column(FLOAT)
    # speed_y = Column(FLOAT)
    # speed_z = Column(FLOAT)

    accel = Column(db.JSON)

    #
    # accel_x = Column(FLOAT)
    # accel_y = Column(FLOAT)
    # accel_z = Column(FLOAT)

    battery = Column(db.JSON)
    # voltage = Column(FLOAT)
    # consumption = Column(FLOAT)
    # mAh_remaining = Column(FLOAT)

    connection = Column(db.JSON)
    # connection_type = Column(VARCHAR(40))
    # connection_ssid = Column(VARCHAR(60), default=0)
    # connection_rssi = Column(Integer, default=0)

    current_action = Column(db.JSON)

    def __init__(self, username, description, owner):
        self.username = username
        self.description = description
        self.owner = owner

