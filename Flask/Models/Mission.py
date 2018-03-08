import json
import uuid
import datetime

from flaskapp import db, app
from flask import request, Response, send_file, send_from_directory, make_response, session

from Utility.Encryptor import Encryptor
from Utility.color_print import ColorPrint

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import or_
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
            
            parsed_json = request.get_json()

            area = parsed_json["area"]
            description = parsed_json["description"]
            title = parsed_json["title"]
            commander = user['id']
            starts_at = parsed_json['starts_at']
            ends_at = parsed_json['ends_at']

            mission_id = str(uuid.uuid4())
            # mission_id = "e4ca934d-988d-4a45-9139-c719dcfb491a"
            mission = Mission_DBModel(mission_id, title, commander, area, description, starts_at, ends_at)
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

            mission_id = parsed_json['mission_id']
            mission = Mission_DBModel.query.filter(Mission_DBModel.id == mission_id).first()


            drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission_id).all()
            
            drone_list = []
            for drone in drones:
                drone_list += [{'id': drone.id, 'description': drone.description}]

            commander = User_DBModel.query.filter_by(id = mission.commander).first()

            mission_info = {'id': mission_id,'title': mission.title,
            'description': mission.description, 'commander': commander.name,
            'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
            'drones': drone_list, 'num_drones': len(drone_list), 'clearance': mission.clearance,
            'area': mission.area}
            
            return_string = json.dumps(mission_info, sort_keys=True, indent=4, separators=(',', ': '))
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
    def get_missions():
        if 'user' in session.keys():
            user = session['user']
            print('ALMOST!!!')
            if User_DBModel.query.filter_by(id = user["id"]).first().account_type == "government_official":
                print('HERE!!!')
                missions = Mission_DBModel.query.all()

                mission_list = []
                for mission in missions:

                    drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission.id).all()
                    
                    drone_list = []
                    for drone in drones:
                        drone_list += [{'id': drone.id, 'description': drone.description}]

                    commander = User_DBModel.query.filter_by(id = mission.commander).first()

                    mission_list += [{'id': mission.id,'title': mission.title,
                    'description': mission.description, 'commander': commander.name,
                    'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
                    'drones': drone_list, 'num_drones': len(drone_list), 'clearance': mission.clearance,
                    'area': mission.area}]

                return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string

            else:
            
                commanded_missions = Mission_DBModel.query.filter(Mission_DBModel.commander == user['id']).all()

                mission_list = []
                for mission in commanded_missions:

                    drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission.id).all()
                    
                    drone_list = []
                    for drone in drones:
                        drone_list += [{'id': drone.id, 'description': drone.description}]

                    commander = User_DBModel.query.filter_by(id = mission.commander).first()

                    mission_list += [{'id': mission.id,'title': mission.title,
                    'description': mission.description, 'commander': commander.name,
                    'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
                    'drones': drone_list, 'num_drones': len(drone_list), 'clearance': mission.clearance,
                    'area': mission.area}]

                participating_missions = Mission_DBModel.query.join(Asset_DBModel, Mission_DBModel.id == Asset_DBModel.mission_id).filter(Asset_DBModel.operator == user['id'], Mission_DBModel.commander != user['id']).all()
                for mission in participating_missions:
                    drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission.id).all()
                    
                    drone_list = []
                    for drone in drones:
                        drone_list += [{'id': drone.id, 'description': drone.description}]

                    commander = User_DBModel.query.filter_by(id = mission.commander).first()

                    mission_list += [{'id': mission.id,'title': mission.title,
                    'description': mission.description, 'commander': commander.name,
                    'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
                    'drones': drone_list, 'num_drones': len(drone_list), 'clearance': mission.clearance}]

                return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def get_active_missions():
        if 'user' in session.keys():
            user = session['user']
            print('ALMOST!!!')
            if User_DBModel.query.filter_by(id = user["id"]).first().account_type == "government_official":
                print('HERE!!!')
                missions = Mission_DBModel.query.filter(Mission_DBModel.closed_at == None).all()

                mission_list = []
                for mission in missions:

                    drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission.id).all()
                    
                    drone_list = []
                    for drone in drones:
                        drone_list += [{'id': drone.id, 'description': drone.description}]

                    commander = User_DBModel.query.filter_by(id = mission.commander).first()

                    mission_list += [{'id': mission.id,'title': mission.title,
                    'description': mission.description, 'commander': commander.name,
                    'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
                    'drones': drone_list, 'num_drones': len(drone_list), 'clearance': mission.clearance,
                    'area': mission.area}]

                return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string

            else:
            
                commanded_missions = Mission_DBModel.query.filter(Mission_DBModel.commander == user['id']).filter(Mission_DBModel.closed_at == None).all()

                mission_list = []
                for mission in commanded_missions:

                    drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission.id).all()
                    
                    drone_list = []
                    for drone in drones:
                        drone_list += [{'id': drone.id, 'description': drone.description}]

                    commander = User_DBModel.query.filter_by(id = mission.commander).first()

                    mission_list += [{'id': mission.id,'title': mission.title,
                    'description': mission.description, 'commander': commander.name,
                    'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
                    'drones': drone_list, 'num_drones': len(drone_list), 'clearance': mission.clearance,
                    'area': mission.area}]

                participating_missions = Mission_DBModel.query.join(Asset_DBModel, Mission_DBModel.id == Asset_DBModel.mission_id).filter(Asset_DBModel.operator == user['id']).filter(Mission_DBModel.closed_at == None).all()
                for mission in participating_missions:
                    drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission.id).all()
                    
                    drone_list = []
                    for drone in drones:
                        drone_list += [{'id': drone.id, 'description': drone.description}]

                    commander = User_DBModel.query.filter_by(id = mission.commander).first()

                    mission_list += [{'id': mission.id,'title': mission.title,
                    'description': mission.description, 'commander': commander.name,
                    'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
                    'drones': drone_list, 'num_drones': len(drone_list), 'clearance': mission.clearance}]

                return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string


    @staticmethod
    def get_user_missions():
        if 'user' in session.keys():
            user = session['user']

            missions = Mission_DBModel.query.filter_by(commander = user['id']).all()

            dict_local = {}
            commanded_list = []
            for mission in missions:
                commanded_list += [{'id': mission.id,'title': mission.title}]
            dict_local["commanding"] = commanded_list

            participating_missions = Mission_DBModel.query.join(Asset_DBModel).join(User_DBModel).filter(
                Drone_DBModel.owner == user['id']).all()

            participating_list = []
            for mission in participating_missions:
                participating_list += [{'id': mission.id,'title': mission.title}]
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
                drone_dict["description"] = drone.description
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
            uid = user["id"]
            if mission.commander != uid:
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
    def edit_mission_details():
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
            uid = user["id"]
            if mission.commander != uid:
                #then this isn't a user that can do this operation.
                dict_local = {'code': 31, 'message': "This user is not the mission commander."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            
            if 'area' in parsed_json:
                mission.area = parsed_json['area']
            if 'description' in parsed_json:
                mission.description = parsed_json['description']
            if 'title' in parsed_json:
                mission.title = parsed_json['title']

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
            uid = user["id"]
            if mission.commander != uid:
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
            uid = user['id']
            if mission.commander != uid:
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

    @staticmethod
    def get_current_mission():
        if 'user' in session.keys():
            user = session['user']
            
            current_mission = Mission_DBModel.query.filter_by(closed_at = None).first()
            if current_mission is None:
                dict_local = {'code': 200, 'message': "no current missions"}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            dict_local = {}
            # drones_dict = {}
            # drones = Drone_DBModel.query.filter_by(mission_id = current_mission.id).all()
            # for drone in drones:
            #     drone_dict = {}
            #     drone_dict["type"] = drone.type
            #     drones_dict[drone.id] = drone_dict
            dict_local["mission_id"] = current_mission.id
            # dict_local["drones"] = drones_dict

            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    def delete_mission():
        if 'user' in session.keys():
            user = session['user']
            parsed_json = request.get_json()
            mission_id = parsed_json['mission_id']
            mission = Mission_DBModel.query.filter_by(id = mission_id).first()
            if mission is None:
                dict_local = {'code' : 31, 'message': "Bad mission id."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            db.session.delete(mission)
            db.session.commit()
            dict_local = {'code': 200}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def edit_clearance():
        if 'user' in session.keys():
            user = session['user']
            if User_DBModel.query.filter_by(id = user["id"]).first().account_type == "government_official":
                parsed_json = request.get_json()

                mission_id = parsed_json['mission_id']
                mission = Mission_DBModel.query.filter(Mission_DBModel.id == mission_id).first()

                if mission is None:
                    dict_local = {'code': 31, 'message': "Bad mission id."}
                    return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                    return return_string
                new_clearance = {'state': parsed_json['new_clearance_state'],
                'official': user['id']}
                mission.clearance = new_clearance

                db.session.commit()

                dict_local = {'code' : 200}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            dict_local = {'code': 50, 'message': "Not authorized to approve missions."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    # def archive_mission():
    #     if 'user' in session.keys():
    #         user = session['user']
    #         parsed_json = request.get_json()
    #         mission_id = parsed_json['mission_id']
    #         mission = Mission_DBModel.query.filter_by(id = mission_id).first()
    #         if mission is None:
    #             dict_local = {'code': 31, 'message': "Bad mission id."}
    #             return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
    #             return return_string
    #         mission.archived = True
    #         db.session.commit()
    #         dict_local = {'code': 200}
    #         return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
    #         return return_string
    #     else:
    #         dict_local = {'code': 31, 'message': "Auth error."}
    #         return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
    #         return return_string

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
app.add_url_rule('/get_current_mission', 'get_current_mission', Mission.get_current_mission, methods=['GET'])
app.add_url_rule('/edit_mission_details', 'edit_mission_details', Mission.edit_mission_details, methods=['POST'])
app.add_url_rule('/delete_mission', 'delete_mission', Mission.delete_mission, methods=['POST'])
app.add_url_rule('/get_missions', 'get_missions', Mission.get_missions, methods=['GET'])
app.add_url_rule('/edit_clearance', 'edit_clearance', Mission.edit_clearance, methods=['POST'])
app.add_url_rule('/get_active_missions', 'get_active_missions', Mission.get_active_missions, methods=['GET'])
# app.add_url_rule('/archive_mission', 'archive_mission', Mission.archive_mission, methods=['POST'])


