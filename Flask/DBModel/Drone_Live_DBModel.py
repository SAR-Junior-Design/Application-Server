from PostgreSQL.declerations import Base
from sqlalchemy import Column, VARCHAR, TEXT, TIMESTAMP, func, FLOAT, Integer, JSON


class drone_live_db(Base):
    """
    This is the main table for live drone data. The tunnel server will update this information.
    """
    __tablename__ = 'live_drone_data'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    username = Column(VARCHAR(66), primary_key=True)
    description = Column(TEXT, nullable=False)
    creation_date = Column(TIMESTAMP(0), server_default=func.now())
    last_update = Column(TIMESTAMP(0))

    owner = Column(VARCHAR(60), nullable=False)

    latitude = Column(FLOAT) # TODO make sure that it doesn't round up!
    longitude = Column(FLOAT)
    altitude = Column(FLOAT)

    speed_x = Column(FLOAT)
    speed_y = Column(FLOAT)
    speed_z = Column(FLOAT)

    accel_x = Column(FLOAT)
    accel_y = Column(FLOAT)
    accel_z = Column(FLOAT)

    voltage = Column(FLOAT)
    consumption = Column(FLOAT)
    mAh_remaining = Column(FLOAT)

    connection_type = Column(VARCHAR(40))
    connection_ssid = Column(VARCHAR(60), default=0)
    connection_rssi = Column(Integer, default=0)

    current_action = Column(JSON)

    def __init__(self, username, description, owner):
        self.username = username
        self.description = description
        self.owner = owner
    
