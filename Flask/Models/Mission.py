import json
import uuid
import datetime

from flaskapp import db, app
from flask import request, Response, send_file, send_from_directory, make_response, session

from Utility.Encryptor import Encryptor
from Utility.color_print import ColorPrint

from sqlalchemy.dialects.postgresql import JSON
from DBModel.User_DBModel import User_DBModel
from DBModel.Mission_DBModel import Mission_DBModel
from DBModel.Drone_DBModel import Drone_DBModel
from DBModel.Asset_DBModel import Asset_DBModel
from DBModel.Action_DBModel import Action_DBModel


class Mission():

    @staticmethod
    def register_mission():
        print (session.keys())
        if 'user' in session.keys():
            user = session['user']
            
            commander = user["id"]
            parsed_json = request.get_json()

            area = parsed_json["area"]
            area = json.dumps(area, sort_keys=True, indent=4, separators=(',', ': '))
            description = parsed_json["description"]
            title = parsed_json["title"]

            mission_id = str(uuid.uuid4())
            # mission_id = "e4ca934d-988d-4a45-9139-c719dcfb491a"
            mission = Mission_DBModel(mission_id, title, commander, area, description)
            db.session.add(mission)

            db.session.commit()
            dict_local = {'mission_id' : mission_id, 'code':200}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def get_mission_info():
        if 'user' in session.keys():
            user = session['user']
            parsed_json = request.get_json()

            mission_id = parsed_json["mission_id"]

            mission = Mission_DBModel.query.filter_by(id = mission_id).first()

            if mission is None:
                dict_local = {'code': 31, 'message': "Mission does not exist."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            
            drones = Drone_DBModel.query.join(Asset_DBModel).join(Mission_DBModel).filter(Asset_DBModel.mission_id == mission_id).all()

            dict_local = {}
            drones_dict = {}
            for drone in drones:
                drone_dict = {}
                drone_dict["type"] = drone.type
                drones_dict[drone.id] = drone_dict

            dict_local["drones"] = drones_dict
            dict_local["area"] = mission.area
            dict_local["commander"] = mission.commander
            dict_local["closed_at"] = mission.closed_at.isoformat()

            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def add_drone_to_mission():
        if 'user' in session.keys():
            user = session['user']

            parsed_json = request.get_json()
            mission_id = parsed_json["mission_id"]
            drone_id = parsed_json["drone_id"]
            operator_id = parsed_json["operator_id"]

            mission = Mission_DBModel.query.filter_by(id = mission_id).first()

            if mission is None:
                dict_local = {'code': 31, 'message': "Mission does not exist."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string

            drone = Drone_DBModel.query.filter_by(id = drone_id).first()
            if drone is None:
                dict_local = {'code': 31, 'message': "Drone does not exist."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string

            asset = Asset_DBModel.query.filter(Asset_DBModel.drone_id==drone_id,
                Asset_DBModel.mission_id==mission_id).first()
            if asset is None:
                asset = Asset_DBModel(drone_id, operator_id, mission_id)
                db.session.add(asset)
                db.session.commit()

                dict_local = {'code' : 200}

                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            else:
                dict_local = {'code' : 31, 'message': 'Drone already added to mission.'}

                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string


    @staticmethod
    def remove_drone_from_mission():
        if 'user' in session.keys():
            user = session['user']

            parsed_json = request.get_json()

            mission_id = parsed_json["mission_id"]
            drone_id = parsed_json["drone_id"]

            mission = Mission_DBModel.query.filter_by(id = mission_id).first()

            if mission is None:
                dict_local = {'code': 31, 'message': "Mission does not exist."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string

            drone = Drone_DBModel.query.filter_by(id = drone_id).first()
            if drone is None:
                dict_local = {'code': 31, 'message': "Drone does not exist."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string

            drone.mission = None
            drone.operator = None
            db.session.commit()

            dict_local = {'code' : 200}

            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def end_mission():
        if 'user' in session.keys():
            user = session['user']

            parsed_json = request.get_json()

            mission_id = parsed_json["mission_id"]

            mission = Mission_DBModel.query.filter_by(id = mission_id).first()

            if mission.closed_at is not None:
                dict_local = {'code': 31, 'message': "Mission already closed."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string

            mission.closed_at = datetime.datetime.now()
            db.session.commit()

            dict_local = {'code' : 200}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string


    @staticmethod
    def get_user_missions():
        if 'user' in session.keys():
            user = session['user']

            missions = Mission_DBModel.query.filter_by(commander = user['email']).all()

            dict_local = {}
            commanded_list = []
            for mission in missions:
                commanded_list += [mission.id]
            dict_local["commanding"] = commanded_list

            participating_missions = Mission_DBModel.query.join(Asset_DBModel).join(User_DBModel).filter(
                Drone_DBModel.owner == user['email']).all()

            participating_list = []
            for mission in participating_missions:
                participating_list += [mission.id]
            dict_local["participating"] = participating_list

            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def get_mission_drones():
        if 'user' in session.keys():
            user = session['user']
            parsed_json = request.get_json()

            mission_id = parsed_json["mission_id"]

            mission = Mission_DBModel.query.filter_by(id = mission_id).first()

            if mission is None:
                dict_local = {'code': 31, 'message': "Mission does not exist."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string

            drones = Drone_DBModel.query.join(Asset_DBModel).filter(Asset_DBModel.mission_id == mission_id).all()

            dict_local = {}
            for drone in drones:
                drone_dict = {}
                drone_dict["type"] = drone.type
                dict_local[drone.id] = drone_dict

            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def update_mission_area():
        if 'user' in session.keys():
            user = session['user']
            parsed_json = request.get_json()

            mission_id = parsed_json["mission_id"]
            area = parsed_json["area"]
            area = json.dumps(area, sort_keys=True, indent=4, separators=(',', ': '))

            mission = Mission_DBModel.query.filter_by(id = mission_id).first()

            if mission is None:
                dict_local = {'code': 31, 'message': "Mission does not exist."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string

            #make sure this is the commander
            email = user["email"]
            if mission.commander != email:
                #then this isn't a user that can do this operation.
                dict_local = {'code': 31, 'message': "This user is not the mission commander."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            
            mission.area = area
            db.session.commit()

            dict_local = {'code' : 200}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def is_mission_live():
        if 'user' in session.keys():
            user = session['user']
            parsed_json = request.get_json()

            mission_id = parsed_json["mission_id"]

            mission = Mission_DBModel.query.filter_by(id = mission_id).first()

            if mission is None:
                dict_local = {'code': 31, 'message': "Mission does not exist."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            
            #make sure this is the commander
            email = user["email"]
            if mission.commander != email:
                #then this isn't a user that can do this operation.
                dict_local = {'code': 31, 'message': "This user is not the mission commander."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            
            #now we know it's the correct user.

            #this code isn't done yet because it will be based on the TCP connection.
            # I might add a column to say if a misison is live or nah.

            dict_local = {'code' : 200}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def start_mission():
        if 'user' in session.keys():
            user = session['user']
            parsed_json = request.get_json()

            mission_id = parsed_json["mission_id"]
            print (mission_id)

            mission = Mission_DBModel.query.filter_by(id = mission_id).first()

            if mission is None:
                dict_local = {'code': 31, 'message': "Mission does not exist."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            
            #make sure this is the commander
            email = user['email']
            if mission.commander != email:
                #then this isn't a user that can do this operation.
                dict_local = {'code': 31, 'message': "This user is not the mission commander."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            
            #now we know it's the correct user.

            #this code isn't done yet because it will be based on the TCP connection.
            # I might add a column to say if a misison is live or nah.

            dict_local = {'code' : 200}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def add_area_vertices():
        if 'user' in session.keys():
            user = session['user']
            parsed_json = request.get_json()
            mission_id = parsed_json["mission_id"]
            area = json.dumps(area, sort_keys = True, indent = 4, separators = (',', ': '))
            mission = Mission_DBModel.query.filter_by(id = mission_id).first()
            return_string = area
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string


app.add_url_rule('/register_mission', 'register_mission', Mission.register_mission, methods=['POST'])
app.add_url_rule('/get_mission_drones', 'get_mission_drones', Mission.get_mission_drones, methods=['POST'])
app.add_url_rule('/get_mission_info', 'get_mission_info', Mission.get_mission_info, methods=['POST'])
app.add_url_rule('/get_user_missions', 'get_user_missions', Mission.get_user_missions, methods=['GET'])
app.add_url_rule('/add_drone_to_mission', 'add_drone_to_mission', Mission.add_drone_to_mission, methods=['POST'])
app.add_url_rule('/remove_drone_from_mission', 'remove_drone_from_mission', Mission.remove_drone_from_mission, methods=['POST'])
app.add_url_rule('/end_mission', 'end_mission', Mission.end_mission, methods=['POST'])
app.add_url_rule('/update_mission_area', 'update_mission_area', Mission.update_mission_area, methods=['POST'])
app.add_url_rule('/start_mission', 'start_mission', Mission.start_mission, methods=['POST'])
app.add_url_rule('/is_mission_live', 'is_mission_live', Mission.is_mission_live, methods=['POST'])
app.add_url_rule('/add_area_vertices', 'add_area_vertices', Mission.add_area_vertices, methods=['POST'])


