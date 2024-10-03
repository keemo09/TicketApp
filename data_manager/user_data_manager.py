import sys
import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_jwt_extended import create_access_token
from models.data_models import User
from data_manager.db import db


class UserDataManager():
    def get_user(self, username, password):
        user_in_db = User.query.filter_by(username=username).first()

        if user_in_db and user_in_db.check_password_hash(password):
            return user_in_db

        else:
            raise ValueError("User and password didnt mact to a record in db")
    
    def get_user_token(self, username, password):
        user_in_db = User.query.filter_by(username=username).first()

        if user_in_db and user_in_db.check_password(password):
            acces_token = create_access_token(identity=user_in_db.id)
            return acces_token
        else:
            raise ValueError("User and password didnt mact to a record in db")

    def create_user(self, user_data):
        #Checks if usernae or email already exists
        if User.query.filter_by(username=user_data["username"]).first() or User.query.filter_by(email=user_data["email"]).first():
            raise ValueError("User alreaddy exist")

        username = user_data["username"]
        email = user_data["email"]
        password = user_data["password"]

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Fehler beim Hinzufügen des Benutzers: {e}")

        return True 

    def update_user(self):
        pass

    def delete_user(self):
        pass