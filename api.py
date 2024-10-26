from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from data_manager.db import db
from data_manager.user_data_manager import UserDataManager
from data_manager.campaign_data_manager import CampaignDataManager
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from config import Config
from models.data_models import User
from validators.campaign_validators import CampaignSchema
from marshmallow import ValidationError
from job_scheduler import setup_jobs  # Stelle sicher, dass `setup_jobs` importiert ist

app = Flask(__name__)

# Konfiguration laden
app.config.from_object(Config)

# Initialisierung der Datenbank und JWT
db.init_app(app)
jwt = JWTManager(app)

# Scheduler-Instanz erstellen und zur App hinzufügen
scheduler = APScheduler()
scheduler.init_app(app)

# Einmaligen Anwendungskontext öffnen
with app.app_context():
    db.create_all()  # Tabellen erstellen
    setup_jobs(scheduler, app)  # Geplante Jobs hinzufügen
    print("Scheduler jobs set up completed.")  # Debugging-Print
    scheduler.start()  # Scheduler starten, nachdem Jobs hinzugefügt wurden
    print("Scheduler started.")  # Debugging-Print



# data manager
user_data_manager = UserDataManager()
campaign_data_manager = CampaignDataManager()



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
        acces_token = user_data_manager.get_user_token(username, password)
        return jsonify({'message': 'Login Success', 'access_token': acces_token})

    except ValueError:
        return jsonify({'message': 'Login Failed'}), 401
    

@app.route('/api/user/register', methods=["POST"])
def register():
    user_data = request.get_json()
    try:
        new_user = user_data_manager.create_user(user_data)
    except ValueError():
        return jsonify({'message': 'User already exists'}), 401

    return jsonify({"msg": "User successfilly registeres"}), 201


@app.route('/api/user/<int:user_id>', methods=["PUT"])
@jwt_required()
def update_user(user_id):
    user_data = request.get_json()
    try:
        user_data_manager.update_user(user_id, user_data)
    except ValueError():
        pass

    return jsonify({"msg": "User successfilly registeres"}), 201


@app.route('/api/user/<int:user_id>', methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    try:
        user_data_manager.delete_user(user_id)
    except ValueError():
        pass

    return jsonify({"msg": "User successfilly registeres"}), 201


@app.route('/api/campaign/new', methods=["POST"])
@jwt_required()
def create_campaign():
    '''
    args:
    {
    "name": ...,
    "end_date": ...,
    "max_ticket": ...,
    "prizes": [
                {
                "product_name": ...,
                "product_description"(optimal): ...,
                },
                {...}
              ]

     }
    '''
    # Create Instance of CampaignSchema
    campaign_schema = CampaignSchema()

    try:
        user_id = get_jwt_identity()
        user = user_data_manager.get_user_by_id(user_id)
    except ValueError as e:
        return jsonify({'message': 'Login Failed'}), 401

    # Try to load the user data into the CampaignSchema valitator
    try:
        # loads the data and give it back if no eerror
        validated_data = campaign_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    try:
        #!!! implement deleting the created record if an error !!!
        campaign_data = {"name": validated_data["name"], "max_ticket": validated_data["max_ticket"], "end_date": validated_data["end_date"]}
        new_campaign = campaign_data_manager.create_campaign(user_id, campaign_data)
        #campaign_data_manager.add_ticket(new_campaign.id, validated_data["ticket_count"])
        for prize_data in validated_data["prizes"]:
            campaign_data_manager.add_price(new_campaign.id, prize_data)
        return jsonify({"msg": "Campaign successfilly created"}), 201
    except ValueError:
        return jsonify({'message': ' Error while creating Campaign'}), 401


@app.route('/api/campaign/<int:campaign_id>', methods=["PUT"])
@jwt_required()
def update_campaign(campaign_id):
    campaign_data = request.get_json()
    user_id = get_jwt_identity()
    if not user_data_manager.user_has_campaign(user_id, campaign_id):
        return jsonify({'message': 'Campaign didn´t exists'}), 401
    
    try:
        campaign_data_manager.update_campaign(campaign_id, campaign_data)
    except ValueError:
        return jsonify({'message': 'Updating Campaign failed'}), 401


@app.route('/api/campaign/<int:campaign_id>', methods=["DELETE"])
@jwt_required()
def delete_campaign(campaign_id):
    user_id = get_jwt_identity()
    if not user_data_manager.user_has_campaign(user_id, campaign_id):
        return jsonify({'message': 'Campaign didn´t exists'}), 401
    try:
        campaign_data_manager.delete_campaign_campaign(campaign_id)
    except ValueError:
        return jsonify({'message': 'Deleting Campaign failed'}), 401
    
@app.route('/api/campaign/<int:campaign_id>/ticket')
@jwt_required()
def get_ticket(campaign_id):
    user_id = get_jwt_identity()
    try:
        campaign_data_manager.add_ticket(campaign_id, user_id)
        return jsonify({'message': 'Ticket ordered'})
    except ValueError:
        return jsonify({'message': 'Failed gaining a ticket'}), 401


@app.route('/api/user/tickets')
@jwt_required()
def check_tickets():
    user_id = get_jwt_identity()
    try:
        ticket_dict = user_data_manager.get_user_tickets(user_id)
        return jsonify(ticket_dict)
    except ValueError:
        return jsonify({'message': 'Failed fetch ticket data for speciffic user'}), 401


@app.route('/protected', methods=["POST"])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    # Check if user exists
    if user: 
        return jsonify({'message': 'User found', 'name': user.username})
    else:
        return jsonify({'message': 'User not found'}), 404
    

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=5002)

#if __name__ == "__main__":
#    app.run()