from models.data_models import Campaign, User, Ticket
from data_manager.db import db

class CampaignDataManager():
    def create_campaign(user_id, campaign_data):
        # Checks if Campaignname alreaddy exists
        existing_campaign = Campaign.query.filter_by(name=campaign_data["name"]).first()
        if existing_campaign:
            raise ValueError("Campaign in this name already exists") 
        
        # Check if user is valid
        existing_user = User.query.filter_by(id=user_id)
        if not existing_user:
            raise ValueError("User didn´t exists")
         
        # Create a new campaign record
        new_campaign = Campaign(user_id=user_id, **campaign_data)
        try:
            db.session.add(new_campaign)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Fehler beim Hinzufügen des Benutzers: {e}")

    def update_campaign(campaign_id, campaign_data):
        pass
    def delete_campaign(self):
        pass

    def add_ticket(self, campaign_id):
        # Check if campaign is valid
        existing_campaign = Campaign.query.filter_by(id=campaign_id)
        if not existing_campaign:
            raise ValueError("Campaign didn´t exists")
        
        # Create a new Ticket record
        new_ticket = Ticket(campaign_id=campaign_id)
        try:
            db.session.add(new_ticket)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error by adduing a ticket: {e}")

        
    # def add_price_to_campaign(self, campaign_id, price_data):
    #     # Check if campaign is valid
    #     existing_campaign = Campaign.query.filter_by(id=campaign_id)
    #     if not existing_campaign:
    #         raise ValueError("Campaign didn´t exists")

    