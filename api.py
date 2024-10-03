from flask import Flask, jsonify, request
import sys
import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_manager.db import db
from data_manager.user_data_manager import UserDataManager
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models.data_models import User 
from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Load config.py and set the configuration
app.config.from_object(Config)

# Initialisiere SQLAlchemy mit der Flask-App
db.init_app(app)

with app.app_context():
    db.create_all()

# JWT Initialization
jwt = JWTManager(app)

data_manager = UserDataManager()

# @app.route('/api/user/login', methods=["POST"])
# def login():
#    user_data = request.get_json()
#    username = user_data["username"]
#    password = user_data["password"]
#    user = User.query.filter_by(username=username).first()

#    if user and user.check_password_hash(password):
#        acces_token = create_access_token(identity=user.id)
#        return jsonify({'message': 'Login Success', 'access_token': access_token})
#    else:
#        return jsonify({'message': 'Login Failed'}), 401


@app.route('/api/user/login', methods=["POST"])
def login():
    '''
    gets a dict as POST in the format {“username”: ..., “password”: ...}. 
    Then calls the method get_user_token from data_manager which returns a jwt token and returns a token in the header.
    '''
    user_data = request.get_json()
    username = user_data["username"]
    password = user_data["password"]
    
    try:
        acces_token = data_manager.get_user_token(username, password)
        return jsonify({'message': 'Login Success', 'access_token': acces_token})

    except ValueError:
        return jsonify({'message': 'Login Failed'}), 401


# @app.route('/api/user/register', methods=["POST"])
# def register():
#     user_data = request.get_json()
#     username = user_data["username"]
#     email = user_data["email"]
#     password = user_data["password"]

#    #Checks if usernae or email already exists
#    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
#        return jsonify({"msg": "Username or Emailadress alreaddy exists"}), 400

#    new_user = User(username=username, email=email)
#    new_user.set_password(password)
   
#    db.session.add(new_user)
#    db.session.commit()

#   return jsonify({"msg": "User successfilly registeres"}), 201

@app.route('/api/user/register', methods=["POST"])
def register():
    user_data = request.get_json()
    try:
        new_user = data_manager.create_user(user_data)
    except ValueError():
        pass

    return jsonify({"msg": "User successfilly registeres"}), 201



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)