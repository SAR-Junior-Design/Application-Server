import json
import uuid
import datetime

from flaskapp import db, app, mail
from Utility.API_Helpers import row2dict, login_required, must_be_gov_official
from flask import request, Response, send_file, send_from_directory, make_response, session
from flask_mail import Mail,  Message

from Utility.Encryptor import Encryptor
from Utility.color_print import ColorPrint

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import or_
from Models.User_DBModel import User_DBModel
from Models.Mission_DBModel import Mission_DBModel
from Models.Drone_DBModel import Drone_DBModel
from Models.Asset_DBModel import Asset_DBModel
from Models.Action_DBModel import Action_DBModel

#returns all mission data
def get_mission_data(mission):
    drones = Drone_DBModel.query.join(Asset_DBModel).filter(Drone_DBModel.id == Asset_DBModel.drone_id).filter(Asset_DBModel.mission_id == mission.id).all()
    drone_list = []
    for drone in drones:
        drone_list += [{'id': drone.id, 'description': drone.description}]
    commander = User_DBModel.query.filter_by(id = mission.commander).first()
    clearance = {'official': mission.clearance_official,
    'message': mission.clearance_message,
    'state': mission.clearance_state}
    mission_dict = {'id': mission.id,'title': mission.title,
    'description': mission.description, 'commander': commander.name, 'commander_id': mission.commander,
    'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
    'drones': drone_list, 'num_drones': len(drone_list), 'clearance': clearance, 'area': mission.area, 'type': mission.type}

    return mission_dict


class Mission():

    @staticmethod
    @login_required
    def add_drone_to_mission():
        user = session['user']
        parsed_json = request.get_json()
        mission_id = parsed_json["mission_id"]
        drone_id = parsed_json["drone_id"]
        operator_id = parsed_json["operator_id"]
        mission = Mission_DBModel.query.filter_by(id = mission_id).first()
        if mission is None:
            dict_local = {'message': "Mission does not exist."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(return_string, status=400, mimetype='application/json')
        drone = Drone_DBModel.query.filter_by(id = drone_id).first()
        if drone is None:
            dict_local = {'message': "Drone does not exist."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(return_string, status=400, mimetype='application/json')
        asset = Asset_DBModel.query.filter(Asset_DBModel.drone_id==drone_id,
            Asset_DBModel.mission_id==mission_id).first()
        if asset is None:
            asset = Asset_DBModel(drone_id, operator_id, mission_id)
            db.session.add(asset)
            db.session.commit()
            dict_local = {'message' : 'Successfully added drone to mission.'}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'message': "Drone already added to mission."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(return_string, status=400, mimetype='application/json')


    @staticmethod
    @login_required
    def remove_drone_from_mission():
        user = session['user']
        parsed_json = request.get_json()
        mission_id = parsed_json["mission_id"]
        drone_id = parsed_json["drone_id"]
        mission = Mission_DBModel.query.filter_by(id = mission_id).first()
        if mission is None:
            dict_local = {'message': "Mission does not exist."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(return_string, status=400, mimetype='application/json')
        drone = Drone_DBModel.query.filter_by(id = drone_id).first()
        if drone is None:
            dict_local = {'message': "Drone does not exist."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(return_string, status=400, mimetype='application/json')
        drone.mission = None
        drone.operator = None
        db.session.commit()
        dict_local = {'message' : 'Successfully removed drone from mission.'}
        return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
        return return_string

    @staticmethod
    @login_required
    def get_user_missions():
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

    @staticmethod
    @login_required
    def get_mission_drones():
        user = session['user']
        parsed_json = request.get_json()
        mission_id = parsed_json["mission_id"]
        mission = Mission_DBModel.query.filter_by(id = mission_id).first()
        if mission is None:
            dict_local = {'message': "Mission doesn't exist."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(return_string, status=400, mimetype='application/json')
        drones = Drone_DBModel.query.join(Asset_DBModel).filter(Asset_DBModel.mission_id == mission_id).all()
        dict_local = {}
        for drone in drones:
            drone_dict = {}
            drone_dict["description"] = drone.description
            dict_local[drone.id] = drone_dict

        return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
        return return_string

    @staticmethod
    @login_required
    def add_area_vertices():
        user = session['user']
        parsed_json = request.get_json()
        mission_id = parsed_json["mission_id"]
        area = json.dumps(area, sort_keys = True, indent = 4, separators = (',', ': '))
        mission = Mission_DBModel.query.filter_by(id = mission_id).first()
        return_string = area
        return return_string

    @staticmethod
    @login_required
    def delete_mission():
        user = session['user']
        parsed_json = request.get_json()
        mission_id = parsed_json['mission_id']
        mission = Mission_DBModel.query.filter_by(id = mission_id).first()
        if mission is None:
            dict_local = {'message': "Bad Mission ID."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(return_string, status=400, mimetype='application/json')
        db.session.delete(mission)
        db.session.commit()
        dict_local = {'message': 'Mission successfully deleted.'}
        return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
        return return_string

    @staticmethod
    @login_required
    @must_be_gov_official
    def edit_clearance():
        user = session['user']
        parsed_json = request.get_json()

        mission_id = parsed_json['mission_id']
        mission = Mission_DBModel.query.filter(Mission_DBModel.id == mission_id).first()

        if mission is None:
            dict_local = {'message': "Bad Mission ID."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(return_string, status=400, mimetype='application/json')

        if 'message' in parsed_json.keys():
            mission.clearance_message = parsed_json['message']

        mission.clearance_state = parsed_json['new_clearance_state']
        mission.clearance_official = user['id']

        db.session.commit()

        dict_local = {'message' : 'successfully updated clearance.'}
        return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
        return return_string

    @staticmethod
    @login_required
    def register_mission_v1_1():
        user = session['user']
        
        parsed_json = request.get_json()

        for _key in ["area", "description", "title", "starts_at", "ends_at", "type"]:
            if _key not in parsed_json.keys():
                dict_local = {'message': "No {0} attribute.".format(_key)}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return Response(return_string, status=400, mimetype='application/json')

        area = parsed_json["area"]
        description = parsed_json["description"]
        title = parsed_json["title"]
        commander = user['id']
        starts_at = parsed_json['starts_at']
        ends_at = parsed_json['ends_at']
        _type = parsed_json['type']

        mission_id = str(uuid.uuid4())
        # mission_id = "e4ca934d-988d-4a45-9139-c719dcfb491a"
        mission = Mission_DBModel(mission_id, title, commander, area, description, starts_at, ends_at, _type)
        db.session.add(mission)

        gov_offs = User_DBModel.query.filter(User_DBModel.account_type=='government_official').all()

        for gov_off in gov_offs:
            #send hunnicutt an email saying that it worked!
            msg = Message(
                '[ICARUS] Drone Mission Registered',
                sender='samcrane8@gmail.com',
                recipients=[gov_off.email]
            )
            msg.body = "A mission has been created by {0}.\n\n ".format(user['name'])
            msg.body += "This mission stars at: {0}\n".format(starts_at)
            msg.body += "this mission ends at: {0}\"\n".format(ends_at)
            msg.body += "Check the mission at: icarusmap.com"
            print(msg)
            mail.send(msg)

        db.session.commit()
        dict_local = {'mission_id' : mission_id}
        return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
        return return_string


    @staticmethod
    @login_required
    def get_missions():
        user = session['user']
        print('started!')

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

        mission_list = []
        
        if User_DBModel.query.filter_by(id = user["id"]).first().account_type == "government_official":
            missions = Mission_DBModel.query.filter(starts_at < Mission_DBModel.starts_at, Mission_DBModel.ends_at < ends_at).all()
            for mission in missions:
                mission_list += [get_mission_data(mission)]
            
        else:
            commanded_missions = Mission_DBModel.query.filter(Mission_DBModel.commander == user['id'], starts_at < Mission_DBModel.starts_at, Mission_DBModel.ends_at < ends_at).all()
            mission_list = []
            for mission in commanded_missions:
                mission_list += [get_mission_data(mission)]
            participating_missions = Mission_DBModel.query.join(Asset_DBModel, Mission_DBModel.id == Asset_DBModel.mission_id).filter(Asset_DBModel.operator == user['id'], Mission_DBModel.commander != user['id'], starts_at < Mission_DBModel.starts_at, ends_at > Mission_DBModel.ends_at).all()
            for mission in participating_missions:    
                mission_list += [get_mission_data(mission)]
        
        return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
        return return_string

    @staticmethod
    @login_required
    def get_active_missions_v1_1():
        user = session['user']
        current_time = datetime.datetime.now()
        if User_DBModel.query.filter_by(id = user["id"]).first().account_type == "government_official":
            missions = Mission_DBModel.query.filter(Mission_DBModel.starts_at < current_time, current_time < Mission_DBModel.ends_at).all()
            mission_list = []
            for mission in missions:
                mission_list += [get_mission_data(mission)]
            return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            commanded_missions = Mission_DBModel.query.filter(Mission_DBModel.commander == user['id'], Mission_DBModel.starts_at < current_time, current_time < Mission_DBModel.ends_at).all()
            mission_list = []
            for mission in commanded_missions:
                mission_list += [get_mission_data(mission)]
            participating_missions = Mission_DBModel.query.join(Asset_DBModel, Mission_DBModel.id == Asset_DBModel.mission_id).filter(Asset_DBModel.operator == user['id'], Mission_DBModel.commander != user['id'], Mission_DBModel.starts_at < current_time, current_time < Mission_DBModel.ends_at).all()
            for mission in participating_missions:
                mission_list += [get_mission_data(mission)]
            return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    @login_required
    def get_upcoming_missions_v1_1():
        user = session['user']
        current_time = datetime.datetime.now()
        if User_DBModel.query.filter_by(id = user["id"]).first().account_type == "government_official":
            missions = Mission_DBModel.query.filter(Mission_DBModel.starts_at > current_time).all()
            mission_list = []
            for mission in missions:
                mission_list += [get_mission_data(mission)]
            return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            commanded_missions = Mission_DBModel.query.filter(Mission_DBModel.commander == user['id'], Mission_DBModel.starts_at > current_time).all()
            mission_list = []
            for mission in commanded_missions:
                mission_list += [get_mission_data(mission)]
            participating_missions = Mission_DBModel.query.join(Asset_DBModel, Mission_DBModel.id == Asset_DBModel.mission_id).filter(Asset_DBModel.operator == user['id'], Mission_DBModel.commander != user['id'], Mission_DBModel.starts_at > current_time).all()
            for mission in participating_missions: 
                mission_list += [get_mission_data(mission)]
            return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    @login_required
    def get_past_missions_v1_1():
        user = session['user']
        current_time = datetime.datetime.now()

        if User_DBModel.query.filter_by(id = user["id"]).first().account_type == "government_official":

            missions = Mission_DBModel.query.filter(current_time > Mission_DBModel.ends_at).all()

            mission_list = []
            for mission in missions:

                mission_list += [get_mission_data(mission)]

            return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

        else:
        
            commanded_missions = Mission_DBModel.query.filter(Mission_DBModel.commander == user['id'], current_time > Mission_DBModel.ends_at).all()

            mission_list = []
            for mission in commanded_missions:

                mission_list += [get_mission_data(mission)]

            participating_missions = Mission_DBModel.query.join(Asset_DBModel, Mission_DBModel.id == Asset_DBModel.mission_id).filter(Asset_DBModel.operator == user['id'], Mission_DBModel.commander != user['id'], current_time > Mission_DBModel.ends_at).all()
            for mission in participating_missions:
                
                mission_list += [get_mission_data(mission)]

            return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string


    @staticmethod
    @login_required
    def get_possible_mission_conflicts():
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

        missions = Mission_DBModel.query.filter(starts_at < Mission_DBModel.starts_at, Mission_DBModel.ends_at < ends_at).all()

        mission_list = []
        for mission in missions:

            mission_list += [{'starts_at': str(mission.starts_at), 'ends_at': str(mission.ends_at),
            'area': mission.area}]

        return_string = json.dumps(mission_list, sort_keys=True, indent=4, separators=(',', ': '))
        return return_string


    @staticmethod
    @login_required
    def get_mission_info_v1_1():
        user = session['user']
        parsed_json = request.get_json()

        mission_id = parsed_json['mission_id']
        mission = Mission_DBModel.query.filter(Mission_DBModel.id == mission_id).first()

        if mission is None:
            dict_local = {'message': "Bad mission id."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(return_string, status=400, mimetype='application/json')

        mission_info = get_mission_data(mission)
        
        return_string = json.dumps(mission_info, sort_keys=True, indent=4, separators=(',', ': '))
        return return_string

    @staticmethod
    @login_required
    def edit_mission_details_v1_1():
        user = session['user']
        parsed_json = request.get_json()

        if "mission_id" not in parsed_json.keys():
            dict_local = {'message': "No mission id has been given."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(return_string, status=400, mimetype='application/json')

        mission_id = parsed_json["mission_id"]

        mission = Mission_DBModel.query.filter_by(id = mission_id).first()

        if mission is None:
            dict_local = {'message': "Bad mission id."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(return_string, status=400, mimetype='application/json')

        #make sure this is the commander
        uid = user["id"]
        if mission.commander != uid:
            #then this isn't a user that can do this operation.
            dict_local = {'message': "This user is not the mission commander."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(return_string, status=400, mimetype='application/json')

        if 'area' in parsed_json:
            mission.area = parsed_json['area']
        if 'description' in parsed_json:
            mission.description = parsed_json['description']
        if 'title' in parsed_json:
            mission.title = parsed_json['title']
        if 'type' in parsed_json:
            mission.type = parsed_json['type']
        if 'starts_at' in parsed_json:
            mission.starts_at = parsed_json['starts_at']
        if 'ends_at' in parsed_json:
            mission.ends_at = parsed_json['ends_at']

        db.session.commit()

        dict_local = {'message' : 'Mission updated successfully.'}
        return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
        return return_string


#V1_1
app.add_url_rule('/v1_1/register_mission', '/v1_1/register_mission', Mission.register_mission_v1_1, methods=['POST'])
app.add_url_rule('/v1_1/get_missions', '/v1_1/get_missions', Mission.get_missions, methods=['POST'])
app.add_url_rule('/v1_1/get_active_missions', '/v1_1/get_active_missions', Mission.get_active_missions_v1_1, methods=['GET'])
app.add_url_rule('/v1_1/get_past_missions', '/v1_1/get_past_missions', Mission.get_past_missions_v1_1, methods=['GET'])
app.add_url_rule('/v1_1/get_mission_info', '/v1_1/get_mission_info', Mission.get_mission_info_v1_1, methods=['POST'])
app.add_url_rule('/v1_1/edit_mission_details', '/v1_1/edit_mission_details', Mission.edit_mission_details_v1_1, methods=['POST'])
app.add_url_rule('/v1_1/get_upcoming_missions', '/v1_1/get_upcoming_missions', Mission.get_upcoming_missions_v1_1, methods=['GET'])
app.add_url_rule('/v1_1/edit_clearance', '/v1_1/edit_clearance', Mission.edit_clearance, methods=['POST'])


#V1_0
app.add_url_rule('/v1_0/get_possible_mission_conflicts', '/v1_0/get_possible_mission_conflicts', Mission.get_possible_mission_conflicts, methods=['POST'])
app.add_url_rule('/v1_0/get_mission_drones', '/v1_0/get_mission_drones', Mission.get_mission_drones, methods=['POST'])
app.add_url_rule('/v1_0/get_user_missions', '/v1_0/get_user_missions', Mission.get_user_missions, methods=['GET'])
app.add_url_rule('/v1_0/add_drone_to_mission', '/v1_0/add_drone_to_mission', Mission.add_drone_to_mission, methods=['POST'])
app.add_url_rule('/v1_0/remove_drone_from_mission', '/v1_0/remove_drone_from_mission', Mission.remove_drone_from_mission, methods=['POST'])
app.add_url_rule('/v1_0/add_area_vertices', '/v1_0/add_area_vertices', Mission.add_area_vertices, methods=['POST'])
app.add_url_rule('/v1_0/delete_mission', '/v1_0/delete_mission', Mission.delete_mission, methods=['POST'])

