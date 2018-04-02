import json
import uuid
from flaskapp import db, app
from flask import request, Response, send_file, send_from_directory, session
from sqlalchemy.dialects.postgresql import JSON
from Models.User_DBModel import User_DBModel
from Models.Drone_DBModel import Drone_DBModel
from Models.Mission_DBModel import Mission_DBModel
from Models.Asset_DBModel import Asset_DBModel
from Models.Drone_Live_DBModel import Drone_Live_DBModel


from sqlalchemy.schema import CreateTable


class Drone():

    @staticmethod
    def register_drone():
        if 'user' in session.keys():
            user = session['user']
            parsed_json = request.get_json()
            owner = user["id"]
            drone_id = str(uuid.uuid4())
            description = parsed_json["description"]

            manufacturer = parsed_json["manufacturer"]
            type = parsed_json["type"]
            color = parsed_json["color"]
            number_of_blades = parsed_json["number_of_blades"]

            drone = Drone_DBModel(drone_id, owner, description, None,
                                  manufacturer=manufacturer, type=type, color=color, number_of_blades=number_of_blades )
            db.session.add(drone)
            db.session.commit()

            dict_local = {'id': drone_id}

            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def get_user_drones():
        if 'user' in session.keys():
            user = session['user']
            owner = user['id']

            responses = Drone_DBModel.query.filter_by(owner=owner).all()

            #print(CreateTable(Drone_DBModel.__table__))


            array_local = []
            for response in responses:
                drone_dict = {}

                drone_dict["description"] = response.description
                drone_dict["id"] = response.id

                drone_dict["manufacturer"] = response.manufacturer
                drone_dict["type"] = response.type
                drone_dict["color"] = response.color
                drone_dict["number_of_blades"] = response.number_of_blades

                array_local.append(drone_dict)

                """
                manufacturer = db.Column(db.Text),
                type = db.Column(db.Text),
                color = db.Column(db.Text),
                number_of_blades = db.Column(db.Integer),
                """

            return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            array_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

app.add_url_rule('/v1_1/get_user_drones', 'get_user_drones', Drone.get_user_drones, methods=['GET'])
app.add_url_rule('/v1_1/register_drone', 'register_drone', Drone.register_drone, methods=['POST'])
