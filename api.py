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
from job_scheduler import setup_jobs  
from flasgger import Swagger


app = Flask(__name__)


SWAGGER_TEMPLATE = {
     'securityDefinitions': {
        'bearerAuth': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Enter your bearer token in the format **Bearer &lt;token&gt;**'
        }
    }
}

swagger = Swagger(app, template=SWAGGER_TEMPLATE)

# Load Config
app.config.from_object(Config)

# start JWT and DB
db.init_app(app)
jwt = JWTManager(app)

# Create sceduler instance
scheduler = APScheduler()
scheduler.init_app(app)

# OPen app context
with app.app_context():
    db.create_all()  # Create Table
    setup_jobs(scheduler, app)  # Add a Job 
    print("Scheduler jobs set up completed.")  # Debugging-Print
    scheduler.start()  # Start the sceduler
    print("Scheduler started.")  # Debugging-Print



# data manager
user_data_manager = UserDataManager()
campaign_data_manager = CampaignDataManager()



@app.route('/api/user/login', methods=["POST"])
def login():
    """
    Log in a User and returns a JWT token.
    ---
    parameters:
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: The user's username
              example: johndoe
            password:
              type: string
              description: The user's password
              example: securepassword
    responses:
      200:
        description: Login successful, returns a JWT token
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message
              example: Login Success
            access_token:
              type: string
              description: The JWT token
              example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
      401:
        description: Login failed due to invalid credentials
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message
              example: Login Failed
    """
    '''
    Gets a dict as POST in the format {“username”: ..., “password”: ...}. 
    Then calls the method get_user_token from data_manager which returns a jwt token and returns a token in the header.
    '''
    # Fetches the data from the user
    user_data = request.get_json()
    username = user_data["username"]
    password = user_data["password"]
    
    try:
        # Creates a JWT token and return a succesmesage and the JWT Token.
        acces_token = user_data_manager.get_user_token(username, password)
        return jsonify({'message': 'Login Success', 'access_token': acces_token})

    except ValueError:
        # If an error occures return a error message
        return jsonify({'message': 'Login Failed'}), 401
    

@app.route('/api/user/register', methods=["POST"])
def register():
    """
    Register a new User
    ---
    parameters:
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: The user's desired username
              example: johndoe
            password:
              type: string
              description: The user's desired password
              example: securepassword
            email:
              type: string
              description: The user's email address
              example: email@email.com
    responses:
      201:
        description: User successfully registered
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message
              example: User successfully registered
      400:
        description: Bad request, invalid input
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating invalid input
              example: Invalid input data
      409:
        description: Registration failed, user already exists
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message
              example: User already exists
      422:
        description: Unprocessable entity, validation error
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating validation failure
              example: Invalid email format
    """
    '''
    Gets a dict as POST in the format {“username”: ..., “password”: ..., “email”: ...}. 
    Then calls the method create_user from data_manager which creates a new User record.
    '''
    # Fetches the user data in json format
    user_data = request.get_json()

    try:
        #  Create a new User record
        user_data_manager.create_user(user_data)

    except ValueError:
        #  Returns a error message if the username already exist
        return jsonify({'message': 'User already exists'}), 401

    # Returns succes message
    return jsonify({"msg": "User successfilly registered"}), 201


@app.route('/api/user', methods=["PUT"])
@jwt_required()
def update_user():
    """
    Update Userdata for a logged-in User
    ---
    security:
        - bearerAuth: ['Authorization'] 
    parameters:
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: The user's desired username
              example: johndoe
            password:
              type: string
              description: The user's desired password
              example: securepassword
            email:
              type: string
              description: The user's email address
              example: email@email.com 
    responses:
      200:
        description: User data successfully updated
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message
              example: User successfully updated
      400:
        description: Bad request, invalid input
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating invalid input
              example: Invalid input data
      404:
        description: User not found
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating the user was not found
              example: User not found
      422:
        description: Unprocessable entity, validation error
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating validation failure
              example: Invalid email format
    """
    '''
    Gets a dict as POST in the format {“username”: ..., “password”: ..., “email”: ...}. 
    Then calls the method update_user from data_manager which updates a User record.
    '''
    # Fetches data
    user_id = get_jwt_identity()
    user_data = request.get_json()
    try:
        # Update userdata with provided data 
        user_data_manager.update_user(user_id, user_data)

    except ValueError():
        pass
    
    # Return Succes message
    return jsonify({"msg": "User successfilly registeres"}), 201


@app.route('/api/user', methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    """
    Delete a logged-in User
    ---
    responses:
      200:
        description: User successfully deleted
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message
              example: User successfully deleted
      404:
        description: User not found
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating the user was not found
              example: User not found
      403:
        description: Forbidden, user does not have permission
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating insufficient permissions
              example: You do not have permission to delete this user
    """
    '''
    Calls the method delete_user from data_manager which deletes a User record.
    '''
    try:
        # Delete a User record
        user_data_manager.delete_user(user_id)
    except ValueError():
        pass

    # Return succes message
    return jsonify({"msg": "User successfilly registeres"}), 201


@app.route('/api/campaign/new', methods=["POST"])
@jwt_required()
def create_campaign():
    """
    Create a new campaign.
    ---
    parameters:
      - name: campaign
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name of the campaign
              example: Summer Giveaway
            end_date:
              type: string
              format: date-time
              description: The end date of the campaign
              example: 2024-12-31T23:59:59
            max_ticket:
              type: integer
              description: Maximum number of tickets allowed
              example: 100
            prizes:
              type: array
              items:
                type: object
                properties:
                  product_name:
                    type: string
                    description: Name of the prize
                    example: iPhone 14
                  product_description:
                    type: string
                    description: Description of the prize
                    example: Latest model of iPhone
    responses:
      201:
        description: Campaign successfully created
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message
              example: Campaign successfully created
      400:
        description: Bad request, invalid input
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating invalid input
              example: Invalid input data
      401:
        description: Error while creating the campaign
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message
              example: Error while creating Campaign
    """
    '''
    Gets a dict as POST in the format:
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

     }.
    Then calls the method update_user from data_manager which updates a User record.
    '''
    # Create Instance of CampaignSchema
    campaign_schema = CampaignSchema()

    try:
        # Fetches the data from body and extract user identity from JWT token.
        user_id = get_jwt_identity()
        user = user_data_manager.get_user_by_id(user_id)

    except ValueError as e:
        return jsonify({'message': 'Login Failed'}), 401


    try:
        # validate the data
        validated_data = campaign_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    try:
        # Reload data in one dimensional dict and create new campaign record
        campaign_data = {"name": validated_data["name"], "max_ticket": validated_data["max_ticket"], "end_date": validated_data["end_date"]}
        new_campaign = campaign_data_manager.create_campaign(user_id, campaign_data)

        # Iterates thought the prizes data and create new price record
        for prize_data in validated_data["prizes"]:
            campaign_data_manager.add_price(new_campaign.id, prize_data)

        return jsonify({"msg": "Campaign successfilly created"}), 201
    except ValueError:
        return jsonify({'message': ' Error while creating Campaign'}), 401


@app.route('/api/campaign/<int:campaign_id>', methods=["PUT"])
@jwt_required()
def update_campaign(campaign_id):
    """
    Update an existing campaign.
    ---
    parameters:
      - name: campaign
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: The updated name of the campaign
              example: Summer Giveaway
            end_date:
              type: string
              format: date-time
              description: Updated end date of the campaign
              example: 2024-12-31T23:59:59
            active:
              type: boolean
              description: Indicates if campaign is active
              example: True
    responses:
      200:
        description: Campaign successfully updated
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message
              example: Campaign successfully updated
      400:
        description: Bad request, invalid input
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message for invalid input
              example: Invalid input data
      401:
        description: Unauthorized or campaign does not exist for user
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating unauthorized access
              example: Campaign doesn’t exist for user
    """
    '''
    Gets a dict as POST in the format:
    {
    "name": ...,
    "end_date": ...,
    "active": ...,
    }.
    Then calls the method update_user from data_manager which updates a User record.
    '''
    # Fetch data and extract user from JWT token
    campaign_data = request.get_json()
    user_id = get_jwt_identity()

    # Checks if user is owner of the campaign
    if not user_data_manager.user_has_campaign(user_id, campaign_id):
        return jsonify({'message': 'Campaign didn´t exists'}), 401
    
    try:
        # Update an existing Campaign record
        campaign_data_manager.update_campaign(campaign_id, campaign_data)

    except ValueError:
        return jsonify({'message': 'Updating Campaign failed'}), 401


@app.route('/api/campaign/<int:campaign_id>', methods=["DELETE"])
@jwt_required()
def delete_campaign(campaign_id):
    """
    Delete an existing campaign.
    ---
    parameters:
      - name: campaign_id
        in: path
        required: true
        type: integer
        description: The ID of the campaign to delete.
    responses:
      200:
        description: Campaign successfully deleted
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message
              example: Campaign successfully deleted
      400:
        description: Bad request, invalid input
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message for invalid input
              example: Invalid input data
      401:
        description: Unauthorized or campaign does not exist for user
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating unauthorized access
              example: Campaign doesn’t exist for user
      500:
        description: Server error during campaign deletion
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message for server error
              example: An error occurred while deleting the campaign
    """
    # Extract user from JWT token
    user_id = get_jwt_identity()

    # Checks if user is owner of the campaign
    if not user_data_manager.user_has_campaign(user_id, campaign_id):
        return jsonify({'message': 'Campaign didn´t exists'}), 401
    
    try:
        # Delete Campaign record
        campaign_data_manager.delete_campaign(campaign_id)
    except ValueError:
        return jsonify({'message': 'Deleting Campaign failed'}), 401
    
@app.route('/api/campaign/<int:campaign_id>/ticket')
@jwt_required()
def get_ticket(campaign_id):
    """
    Gain a Ticket.
    ---
    parameters:
      - name: campaign_id
        in: path
        required: true
        type: integer
        description: The ID of the campaign to delete.
    responses:
      200:
        description: Campaign successfully deleted
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message
              example: Campaign successfully deleted
      400:
        description: Bad request, invalid input
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message for invalid input
              example: Invalid input data
      401:
        description: Unauthorized or campaign does not exist for user
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating unauthorized access
              example: Campaign doesn’t exist for user
      500:
        description: Server error during campaign deletion
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message for server error
              example: An error occurred while deleting the campaign
    """
    user_id = get_jwt_identity()
    try:
        campaign_data_manager.add_ticket(campaign_id, user_id)
        return jsonify({'message': 'Ticket ordered'})
    except ValueError:
        return jsonify({'message': 'Failed gaining a ticket'}), 401


@app.route('/api/user/tickets')
@jwt_required()
def check_tickets():
    """
    Gain a Ticket for a campaign.
    ---
    parameters:
      - name: campaign_id
        in: path
        required: true
        type: integer
        description: The ID of the campaign for which to gain a ticket.
    responses:
      200:
        description: Ticket successfully gained
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message
              example: Ticket ordered successfully
      400:
        description: Bad request, invalid campaign ID or data format
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating invalid input
              example: Invalid campaign ID or input data
      401:
        description: Unauthorized, user does not have access to this campaign or is not logged in
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating unauthorized access
              example: Campaign doesn’t exist for user or user not authenticated
      500:
        description: Server error during ticket creation
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message for server error
              example: An error occurred while creating the ticket
    """
    # Extract User from JWT Token
    user_id = get_jwt_identity()

    try:
        # CReturn the tickets as dict
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