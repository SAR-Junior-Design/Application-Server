import json
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON


class Permissions_DBModel(db.Model):
    __tablename__ = 'permissions'
    user_id = db.Column(db.Text, primary_key=True)
    permissions = db.Column(db.JSON, nullable=False)

    """
    {
    
         "admin": "False",
         "add_user": "True",
         "Area_admin":"False"
     
    } 
    """

    def __init__(self, id, permissions):
        self.id = id
        self.permissions = permissions

    @staticmethod
    def user_has_permission(user, permission):
        """
        Retrieves the permission value of the given user
        :param user: user_id
        :param permission: the key of the permission.
        :return: permission value.
        """
        permissions_object = Permissions_DBModel.query.filter_by(id=user).first()

        if permissions_object is None:
            return None
        else:
            if permission in permissions_object.permissions:
                # Assume the permission is for that value is false if the key does not exist
                return permissions_object.permissions.get(permission, False)

    @staticmethod
    def set_user_permission(user, permission, value):
        """
        Assigns a certain permission value to the user, if that permission key is new it adds it to the json/
        :param user: user_id of the user
        :param permission: the key of the permission
        :param value: the value of the permission
        :return: nothing
        """
        permissions_object = Permissions_DBModel.query.filter_by(id=user).first()

        if permissions_object is None:
            # Wow wtf this shouldn't have happened
            print("Error, permission does not exist for user")
        else:
            permissions_json = permissions_object.permissions

            permissions_json[permission] = value





