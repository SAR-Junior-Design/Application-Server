import json
import uuid
from flaskapp import db, app
from Utility.API_Helpers import row2dict, login_required, must_be_gov_official
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
    @login_required
    def get_user_drones():
        user = session['user']
        owner = user['id']
        responses = Drone_DBModel.query.filter_by(owner=owner).all()
        array_local = []
        for response in responses:
            array_local.append(row2dict(response))
        return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
        return return_string


    @staticmethod
    @login_required
    def delete_drone():
        user = session['user']
        email = user['email']
        parsed_array = request.get_json()
        for element in parsed_array:
            if "id" not in element.keys():
                dict_local = {'message': "No id tag in element."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return Response(return_string, status=400, mimetype='application/json')
            
            drone = Drone_DBModel.query.filter(Drone_DBModel.id==element["id"]).first()
            if drone is None:
                dict_local = {'message': "Bad drone id."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return Response(return_string, status=400, mimetype='application/json')
            db.session.delete(drone)
        
        db.session.commit()

        dict_local = {'message': 'Drone has been deleted.'}
        return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
        return return_string


    @staticmethod
    @login_required
    def get_drones_past_missions():
        parsed_json = request.get_json()

        drone_id = parsed_json["drone_id"]
        drone = Drone_DBModel.query.filter_by(id=drone_id).first()
        if drone is None:
            dict_local = {'message': "Bad drone id."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(return_string, status=400, mimetype='application/json')

        missions = Mission_DBModel.query.join(Asset_DBModel).filter(Asset_DBModel.drone_id == drone_id,
                                                                    Mission_DBModel.closed_at != None).all()

        mission_array = []
        for mission in missions:
            mission_array += [mission.id]

        return_string = json.dumps(mission_array, sort_keys=True, indent=4, separators=(',', ': '))
        return return_string

    #V1.1 calls here.

    @staticmethod
    @login_required
    def register_drone():
        user = session['user']
        parsed_json = request.get_json()
        owner = user["id"]
        drone_id = str(uuid.uuid4())

        for key in ['description', 'manufacturer', 'type', 'color', 'number_of_blades']:
            if key not in parsed_json.keys():
                message = "No " + key + " given."
                dict_local = {'message': message}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return Response(return_string, status=400, mimetype='application/json')

        description = parsed_json["description"]
        manufacturer = parsed_json["manufacturer"]
        type = parsed_json["type"]
        color = parsed_json["color"]
        number_of_blades = parsed_json["number_of_blades"]

        drone = Drone_DBModel(drone_id, owner, description, None,
                              manufacturer=manufacturer, type=type, color=color, number_of_blades=number_of_blades )
        db.session.add(drone)
        db.session.commit()

        dict_local = {'message': 'Drone successfully registered.'}

        return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
        return return_string


#V1.0
app.add_url_rule('/v1_0/get_user_drones', '/v1_0/get_user_drones', Drone.get_user_drones, methods=['GET'])
app.add_url_rule('/v1_0/register_drone', '/v1_0/register_drone', Drone.register_drone, methods=['POST'])
app.add_url_rule('/v1_0/get_drones_past_missions', '/v1_0/get_drones_past_missions', Drone.get_drones_past_missions, methods=['POST'])
app.add_url_rule('/v1_0/delete_drone', '/v1_0/delete_drone', Drone.delete_drone, methods=['POST'])



