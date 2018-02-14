import json
import uuid
from flaskapp import db, app
from flask import request, Response, send_file, send_from_directory, session
from sqlalchemy.dialects.postgresql import JSON
from DBModel.User_DBModel import User_DBModel
from DBModel.Drone_DBModel import Drone_DBModel
from DBModel.Mission_DBModel import Mission_DBModel
from DBModel.Asset_DBModel import Asset_DBModel
from DBModel.Drone_Live_DBModel import drone_live_db

class Drone():

	@staticmethod
	def register_drone():
		if 'user' in session.keys():
			user = session['user']
			parsed_json = request.get_json()
			owner = user["email"]
			drone_id = str(uuid.uuid4())
			type = parsed_json["type"]

			drone = Drone_DBModel(drone_id, owner, type)
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
			print (user)
			email = user['email']

			responses = Drone_DBModel.query.join(User_DBModel).filter(Drone_DBModel.owner == email).all()

			dict_local = {}
			for response in responses:
				drone_dict = {}
				drone_dict["type"] = response.type
				dict_local[response.id] = drone_dict

			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			dict_local = {'code': 31, 'message': "Auth error."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def delete_drone():
		print (session.keys())
		if 'user' in session.keys():
			
			user = session['user']
			email = user['email']
			parsed_json = request.get_json()

			drone_id = parsed_json["id"]

			drone = Drone_DBModel.query.filter_by(id = drone_id).first()
			if drone is None:
				dict_local = {'code': 31, 'message': "Bad drone id."}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
			db.session.delete(drone)
			db.session.commit()

			dict_local = {'code' : 200}
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
			drone = Drone_DBModel.query.filter_by(id = drone_id).first()
			if drone is None:
				dict_local = {'code': 31, 'message': "Bad drone id."}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string

			missions = Mission_DBModel.query.join(Asset_DBModel).filter(Asset_DBModel.drone_id == drone_id, Mission_DBModel.closed_at != None).all()

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

			#in this portion I should make a TCP connection out to the 
			#sister server and ask for the in-ram, real-time data coming
			#through to us.

			#so no databasing for this.
			dict_local = {
				"drone1" : {
					"latitude" : "0",
					"longitude" : "1"
				},
				"drone2" : {
					"latitude" : "2",
					"longitude" : "3"
				}
			}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			dict_local = {'code': 31, 'message': "Auth error."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

app.add_url_rule('/get_mission_update', 'get_mission_update', Drone.get_mission_update, methods=['POST'])
app.add_url_rule('/get_user_drones', 'get_user_drones', Drone.get_user_drones, methods=['GET'])
app.add_url_rule('/register_drone', 'register_drone', Drone.register_drone, methods=['POST'])
app.add_url_rule('/get_drones_past_missions', 'get_drones_past_missions', Drone.get_drones_past_missions, methods=['POST'])
app.add_url_rule('/delete_drone', 'delete_drone', Drone.delete_drone, methods=['POST'])




