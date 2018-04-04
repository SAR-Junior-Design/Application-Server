import json
import uuid
import datetime

from flaskapp import db, app, mail
from flask import request, Response, send_file, send_from_directory, make_response, session

from Utility.Encryptor import Encryptor
from Utility.color_print import ColorPrint
from flask_mail import Mail,  Message

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import or_
from Models.User_DBModel import User_DBModel
from Models.Mission_DBModel import Mission_DBModel
from Models.Drone_DBModel import Drone_DBModel
from Models.Asset_DBModel import Asset_DBModel
from Models.Action_DBModel import Action_DBModel


class Mission():

    @staticmethod
    def get_missions():
        if 'user' in session.keys():
            user = session['user']

            parsed_json = request.get_json()

            if "starts_at" not in parsed_json.keys():
                dict_local = {'message': "No starts_at attribute."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return Response(return_string, status=400, mimetype='application/json')

            if "ends_at" not in parsed_json.keys():
                dict_local = {'message': "No ends_at attribute."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return Response(return_string, status=400, mimetype='application/json')

            starts_at = parsed_json["starts_at"]
            starts_at = datetime.datetime.strptime(starts_at, "%Y-%m-%d %H:%M:%S")
            ends_at = parsed_json["ends_at"]
            ends_at = datetime.datetime.strptime(ends_at, "%Y-%m-%d %H:%M:%S")

            if User_DBModel.query.filter_by(id = user["id"]).first().account_type == "government_official":
                missions = Mission_DBModel.query.filter(starts_at < Mission_DBModel.starts_at, Mission_DBModel.ends_at < ends_at).all()

                mission_list = []
                for mission in missions:

                    drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission.id).all()
                    
                    drone_list = []
                    for drone in drones:
                        drone_list += [{'id': drone.id, 'description': drone.description}]

                    commander = User_DBModel.query.filter_by(id = mission.commander).first()

                    mission_list += [{'id': mission.id,'title': mission.title,
                    'description': mission.description, 'commander': commander.name, 'commander_id': mission.commander,
                    'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
                    'drones': drone_list, 'num_drones': len(drone_list), 'clearance': mission.clearance,
                    'area': mission.area}]

                return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string

            else:
            
                commanded_missions = Mission_DBModel.query.filter(Mission_DBModel.commander == user['id'], starts_at < Mission_DBModel.starts_at, Mission_DBModel.ends_at < ends_at).all()

                mission_list = []
                for mission in commanded_missions:

                    drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission.id).all()
                    
                    drone_list = []
                    for drone in drones:
                        drone_list += [{'id': drone.id, 'description': drone.description}]

                    commander = User_DBModel.query.filter_by(id = mission.commander).first()

                    mission_list += [{'id': mission.id,'title': mission.title,
                    'description': mission.description, 'commander': commander.name, 'commander_id': mission.commander,
                    'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
                    'drones': drone_list, 'num_drones': len(drone_list), 'clearance': mission.clearance,
                    'area': mission.area}]

                participating_missions = Mission_DBModel.query.join(Asset_DBModel, Mission_DBModel.id == Asset_DBModel.mission_id).filter(Asset_DBModel.operator == user['id'], Mission_DBModel.commander != user['id'], starts_at < Mission_DBModel.starts_at, ends_at > Mission_DBModel.ends_at).all()
                for mission in participating_missions:
                    drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission.id).all()
                    
                    drone_list = []
                    for drone in drones:
                        drone_list += [{'id': drone.id, 'description': drone.description}]

                    commander = User_DBModel.query.filter_by(id = mission.commander).first()

                    mission_list += [{'id': mission.id,'title': mission.title,
                    'description': mission.description, 'commander': commander.name, 'commander_id': mission.commander,
                    'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
                    'drones': drone_list, 'num_drones': len(drone_list), 'clearance': mission.clearance}]

                return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            dict_local = {'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(return_string, status=400, mimetype='application/json')

    @staticmethod
    def get_active_missions():
        if 'user' in session.keys():
            user = session['user']
            current_time = datetime.datetime.now()

            if User_DBModel.query.filter_by(id = user["id"]).first().account_type == "government_official":

                missions = Mission_DBModel.query.filter(Mission_DBModel.starts_at < current_time, current_time < Mission_DBModel.ends_at).all()

                mission_list = []
                for mission in missions:

                    drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission.id).all()
                    
                    drone_list = []
                    for drone in drones:
                        drone_list += [{'id': drone.id, 'description': drone.description}]

                    commander = User_DBModel.query.filter_by(id = mission.commander).first()

                    mission_list += [{'id': mission.id,'title': mission.title,
                    'description': mission.description, 'commander': commander.name, 'commander_id': mission.commander,
                    'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
                    'drones': drone_list, 'num_drones': len(drone_list), 'clearance': mission.clearance,
                    'area': mission.area}]

                return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string

            else:
            
                commanded_missions = Mission_DBModel.query.filter(Mission_DBModel.commander == user['id'], Mission_DBModel.starts_at < current_time, current_time < Mission_DBModel.ends_at).all()

                mission_list = []
                for mission in commanded_missions:

                    drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission.id).all()
                    
                    drone_list = []
                    for drone in drones:
                        drone_list += [{'id': drone.id, 'description': drone.description}]

                    commander = User_DBModel.query.filter_by(id = mission.commander).first()

                    mission_list += [{'id': mission.id,'title': mission.title,
                    'description': mission.description, 'commander': commander.name, 'commander_id': mission.commander,
                    'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
                    'drones': drone_list, 'num_drones': len(drone_list), 'clearance': mission.clearance,
                    'area': mission.area}]

                participating_missions = Mission_DBModel.query.join(Asset_DBModel, Mission_DBModel.id == Asset_DBModel.mission_id).filter(Asset_DBModel.operator == user['id'], Mission_DBModel.commander != user['id'], Mission_DBModel.starts_at < current_time, current_time < Mission_DBModel.ends_at).all()
                for mission in participating_missions:
                    drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission.id).all()
                    
                    drone_list = []
                    for drone in drones:
                        drone_list += [{'id': drone.id, 'description': drone.description}]

                    commander = User_DBModel.query.filter_by(id = mission.commander).first()

                    mission_list += [{'id': mission.id,'title': mission.title,
                    'description': mission.description, 'commander': commander.name, 'commander_id': mission.commander,
                    'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
                    'drones': drone_list, 'num_drones': len(drone_list), 'clearance': mission.clearance}]

                return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            dict_local = {'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(return_string, status=400, mimetype='application/json')

    @staticmethod
    def get_past_missions():
        if 'user' in session.keys():
            user = session['user']
            current_time = datetime.datetime.now()

            if User_DBModel.query.filter_by(id = user["id"]).first().account_type == "government_official":

                missions = Mission_DBModel.query.filter(current_time > Mission_DBModel.ends_at).all()

                mission_list = []
                for mission in missions:

                    drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission.id).all()
                    
                    drone_list = []
                    for drone in drones:
                        drone_list += [{'id': drone.id, 'description': drone.description}]

                    commander = User_DBModel.query.filter_by(id = mission.commander).first()

                    mission_list += [{'id': mission.id,'title': mission.title,
                    'description': mission.description, 'commander': commander.name, 'commander_id': mission.commander,
                    'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
                    'drones': drone_list, 'num_drones': len(drone_list), 'clearance': mission.clearance,
                    'area': mission.area}]

                return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string

            else:
            
                commanded_missions = Mission_DBModel.query.filter(Mission_DBModel.commander == user['id'], current_time > Mission_DBModel.ends_at).all()

                mission_list = []
                for mission in commanded_missions:

                    drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission.id).all()
                    
                    drone_list = []
                    for drone in drones:
                        drone_list += [{'id': drone.id, 'description': drone.description}]

                    commander = User_DBModel.query.filter_by(id = mission.commander).first()

                    mission_list += [{'id': mission.id,'title': mission.title,
                    'description': mission.description, 'commander': commander.name, 'commander_id': mission.commander,
                    'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
                    'drones': drone_list, 'num_drones': len(drone_list), 'clearance': mission.clearance,
                    'area': mission.area}]

                participating_missions = Mission_DBModel.query.join(Asset_DBModel, Mission_DBModel.id == Asset_DBModel.mission_id).filter(Asset_DBModel.operator == user['id'], Mission_DBModel.commander != user['id'], current_time > Mission_DBModel.ends_at).all()
                for mission in participating_missions:
                    drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission.id).all()
                    
                    drone_list = []
                    for drone in drones:
                        drone_list += [{'id': drone.id, 'description': drone.description}]

                    commander = User_DBModel.query.filter_by(id = mission.commander).first()

                    mission_list += [{'id': mission.id,'title': mission.title,
                    'description': mission.description, 'commander': commander.name, 'commander_id': mission.commander,
                    'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
                    'drones': drone_list, 'num_drones': len(drone_list), 'clearance': mission.clearance}]

                return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            dict_local = {'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(return_string, status=400, mimetype='application/json')


app.add_url_rule('/v1_1/get_missions', '/v1_1/get_missions', Mission.get_missions, methods=['POST'])
app.add_url_rule('/v1_1/get_active_missions', '/v1_1/get_active_missions', Mission.get_active_missions, methods=['GET'])
app.add_url_rule('/v1_1/get_past_missions', '/v1_1/get_past_missions', Mission.get_past_missions, methods=['GET'])



