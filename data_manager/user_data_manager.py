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
    
    def get_user_by_id(self, user_id):
        user_in_db = User.query.get(user_id)
        if not user_in_db:
            raise ValueError("No such user in db")
        return user_in_db


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
    
    def user_has_campaign(self, user_id, campaign_id):
        user_in_db = User.query.get(user_id)
        if not user_in_db:
            raise ValueError("User didn´t exist")
        
        # Checks if campaign.id exist in user campaigns
        for campaign in user_in_db.campaigns:
            if campaign.id == campaign_id:
                return True
        
        return False


    def update_user(self, user_id, user_data):
        user_in_db = User.query.get(user_id)
        if not user_in_db:
            raise ValueError("User didn´t exist")
            
        for key, value in user_data.items():
            if hasattr(user_in_db, key):
                setattr(user_in_db, key, value)

        # committ changes
        db.session.commit()

    def delete_user(self, user_id):
        user_in_db = User.query.get(user_id)
        if not user_in_db:
            raise ValueError("User didn´t exist")
        
        # delete record
        db.session.delete(user_in_db)
    
    def get_user_tickets(self, user_id):
        user_in_db = User.query.get(user_id)
        if not user_id:
            raise ValueError("User didnt exists")
        
        user_tickets_data = []
        for ticket in user_in_db.tickets:
            campaign = ticket.campaign
            prize = ticket.prize

            if prize:
                winner_ticket = True
                prize_name = prize.product_name
            else:
                winner_ticket = False
                prize_name = "None"

            ticket_data = {
                "ticket_id": ticket.id, 
                "campaign_name": campaign.name, 
                "campaign_end_date": campaign.end_date,
                "winner_ticket": winner_ticket,
                "prize": prize_name
            }

            user_tickets_data.append(ticket_data)
        return user_tickets_data
        
