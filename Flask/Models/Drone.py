import json
import uuid
from flaskapp import db, app
from flask import request, Response, send_file, send_from_directory, session
from sqlalchemy.dialects.postgresql import JSON
from DBModel.User_DBModel import User_DBModel
from DBModel.Drone_DBModel import Drone_DBModel
from DBModel.Mission_DBModel import Mission_DBModel
from DBModel.Asset_DBModel import Asset_DBModel
from DBModel.Drone_Live_DBModel import Drone_Live_DBModel


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

            drone = Drone_DBModel(drone_id, owner, description, None)
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
    def register_drone_v1():
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

            responses = Drone_DBModel.query.join(User_DBModel).filter(Drone_DBModel.owner == owner).all()

            array_local = []
            for response in responses:
                drone_dict = {}
                drone_dict["description"] = response.description
                drone_dict["id"] = response.id
                array_local += [drone_dict]

            return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            array_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def get_user_drones_v1():
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


    @staticmethod
    def delete_drone():
        print (session.keys())
        if 'user' in session.keys():

            user = session['user']
            email = user['email']
            parsed_json = request.get_json()

            drone_id = parsed_json["id"]

            drone = Drone_DBModel.query.filter_by(id=drone_id).first()
            if drone is None:
                dict_local = {'code': 31, 'message': "Bad drone id."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            db.session.delete(drone)
            db.session.commit()

            dict_local = {'code': 200}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def get_drones_past_missions():
        if 'user' in session.keys():

            parsed_json = request.get_json()

            drone_id = parsed_json["drone_id"]
            drone = Drone_DBModel.query.filter_by(id=drone_id).first()
            if drone is None:
                dict_local = {'code': 31, 'message': "Bad drone id."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string

            missions = Mission_DBModel.query.join(Asset_DBModel).filter(Asset_DBModel.drone_id == drone_id,
                                                                        Mission_DBModel.closed_at != None).all()

            mission_array = []
            for mission in missions:
                mission_array += [mission.id]

            return_string = json.dumps(mission_array, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def get_mission_update():
        if 'user' in session.keys():
            user = session['user']

            # in this portion I should make a TCP connection out to the
            # sister server and ask for the in-ram, real-time data coming
            # through to us.

            # so no databasing for this.
            dict_local = {
                "drone1": {
                    "latitude": "0",
                    "longitude": "1"
                },
                "drone2": {
                    "latitude": "2",
                    "longitude": "3"
                }
            }
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    def get_live_drones():
        if 'user' in session.keys():
            user = session['user']
            live_missions = Mission_DBModel.query.filter(Mission_DBModel.closed_at == None).all()
            drones_list = []
            for mission in live_missions:
                assets = Asset_DBModel.query.filter(Asset_DBModel.mission_id == mission.id).all()
                for asset in assets:
                    drones_list += [{'id': asset.drone_id}]
            return_string = json.dumps(drones_list, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string


app.add_url_rule('/get_mission_update', 'get_mission_update', Drone.get_mission_update, methods=['POST'])
app.add_url_rule('/get_user_drones', 'get_user_drones', Drone.get_user_drones, methods=['GET'])
app.add_url_rule('/register_drone', 'register_drone', Drone.register_drone, methods=['POST'])
app.add_url_rule('/get_drones_past_missions', 'get_drones_past_missions', Drone.get_drones_past_missions,
                 methods=['POST'])
app.add_url_rule('/delete_drone', 'delete_drone', Drone.delete_drone, methods=['POST'])


app.add_url_rule('/api/v1/get_user_drones', 'get_user_drones_v1', Drone.get_user_drones_v1, methods=['GET'])
app.add_url_rule('/api/v1/register_drone', 'register_drone_v2', Drone.register_drone_v1, methods=['POST'])

app.add_url_rule('/get_live_drones', 'get_live_drones', Drone.get_live_drones, methods=['GET'])
