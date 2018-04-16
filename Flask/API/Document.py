import json
import uuid
import datetime

from flaskapp import db, app
from flask import request, Response, send_file, send_from_directory, make_response, session

from Utility.Encryptor import Encryptor
from Utility.color_print import ColorPrint

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import or_

from DBModel.Document_DBModel import Document_DBModel

class Document():

    @staticmethod
    def add_document():
        if 'user' in session.keys():
            user = session['user']
            parsed_json = request.get_json()
            location = parsed_json['location']
            document_type = parsed_json['document_type']
            document_id = str(uuid.uuid4())
            document = Document_DBModel(document_id, user['id'], location, document_type)
            db.session.add(document)
            db.session.commit()

            dict_local = {'id': document_id}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string


    @staticmethod
    def get_user_documents():
        if 'user' in session.keys():
            user = session['user']
            documents = Document_DBModel.query.filter(Document_DBModel.owner == user['id']).all()

            array_local = []
            for document in documents:
                document_dict = {}
                document_dict['id'] = document.id
                document_dict['owner'] = document.owner
                document_dict['location'] = document.location
                document_dict['document_type'] = document.document_type
                array_local += [document_dict]
            return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            array_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def delete_document():
        if 'user' in session.keys():
            user = session['user']
            parsed_json = request.get_json()
            document = Document_DBModel.query.filter(Document_DBModel.id == parsed_json['document_id']).first()
            if document is None:
                dict_local = {'code' : 31, 'message': "Bad document id."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            db.session.delete(document)
            db.session.commit()
            dict_local = {'code': 200}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def get_document_from_id():
        if 'user' in session.keys():
            parsed_json = request.get_json()
            document_id = parsed_json['document_id']
            document = Document_DBModel.query.filter(Document_DBModel.id == document_id).first()
            if document is None:
                dict_local = {'code' : 31, 'message': "Bad document id."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            dict_local = {'id': document.id, 'owner': document.owner, 'location': document.location, 'type': document.document_type}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def get_documents_from_type():
        if 'user' in session.keys():
            parsed_json = request.get_json()
            document_type = parsed_json['document_type']
            documents = Document_DBModel.query.filter(Document_DBModel.document_type == document_type).all()
            array_local = []
            for document in documents:
                document_dict = {}
                document_dict['id'] = document.id
                document_dict['owner'] = document.owner
                document_dict['location'] = document.location
                document_dict['document_type'] = document.document_type
                array_local += [document_dict]
            return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            array_local = {'code': 31, 'message': "Auth error."}
            return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string



app.add_url_rule('/add_document', 'add_document', Document.add_document, methods=['POST'])
app.add_url_rule('/get_user_documents', 'get_user_documents', Document.get_user_documents, methods=['GET'])
app.add_url_rule('/delete_document', 'delete_document', Document.delete_document, methods=['POST'])
app.add_url_rule('/get_document_from_id', 'get_document_from_id', Document.get_document_from_id, methods=['POST'])
app.add_url_rule('/get_documents_from_type', 'get_documents_from_type', Document.get_documents_from_type, methods=['POST'])
