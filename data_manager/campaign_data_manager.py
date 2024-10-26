from models.data_models import Campaign, User, Ticket, Prize
from data_manager.db import db

class CampaignDataManager():
    def get_campaigns(self):
        campaigns = Campaign.query.all()
        return campaigns
    
    def create_campaign(self, user_id, campaign_data):
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
            raise 
        
        return new_campaign

    def update_campaign(self, campaign_id, campaign_data):
        # Check if campaign is valid
        campaign_in_db = Campaign.query.get(campaign_id)
        if not campaign_in_db:
            raise ValueError("Campaign didn´t exists") 
        
        # Checks with filds are given and update it
        if "name" in campaign_data:
            campaign_in_db.name = campaign_data["name"]
        elif "active" in campaign_data:
            campaign_in_db.active = campaign_data["active"]
        elif "end_date" in campaign_data:
            campaign_in_db.end_date = campaign_data["end_date"]
        
        # committ changes
        db.session.commit()

        

    def delete_campaign(self, campaign_id):
        # Check if campaign is valid
        campaign_in_db = Campaign.query.get(campaign_id)
        if not campaign_in_db:
            raise ValueError("Campaign didn´t exists") 
        
        # Delete record
        db.session.delete(campaign_in_db)
    
    def get_tickets(self, campaign_id):
        # Überprüfe, ob die Kampagne existiert
        campaign_in_db = Campaign.query.get(campaign_id)
        if not campaign_in_db:
            raise ValueError("Campaign doesn’t exist") 

        # Sammle alle Ticket-IDs für die Kampagne
        return [ticket.id for ticket in campaign_in_db.tickets]




    def add_ticket(self, campaign_id, user_id):
        #!!! Change that only ticket creeate if user get one 
        # Check if campaign is valid
        existing_campaign = Campaign.query.get(campaign_id)
        if not existing_campaign:
            raise ValueError("Campaign didn´t exists")
        
        existing_cuser = Campaign.query.get(user_id)
        if not existing_cuser:
            raise ValueError("User didn´t exists")
        
#        tickets_in_db = Ticket.query.filter_by(campaign_id=campaign_id).all()

#        if number_of_tickets > (existing_campaign.max_ticket - len(tickets_in_db)):
#            raise ValueError("No more tickets")

        # Create a new Ticket record
#        tickets = [Ticket(campaign_id=campaign_id, user_id=user_id) for _ in range(number_of_tickets)]
        ticket = Ticket(campaign_id=campaign_id, user_id=user_id)
#        pdb.set_trace()
        try:
            db.session.add(ticket)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise 

    def updtate_ticket(self, ticket_id, ticket_data):
        ticket_in_db = User.query.get(ticket_id)
        if not ticket_in_db:
            raise ValueError("User didn´t exist")
            
        for key, value in ticket_data.items():
            if hasattr(ticket_in_db, key):
                setattr(ticket_in_db, key, value)


    def add_price(self,campaign_id, price_data):
        # Check if campaign is valid
        existing_campaign = Campaign.query.filter_by(id=campaign_id)
        if not existing_campaign:
            raise ValueError("Campaign didn´t exists")
        
        # Create new prize record
        new_price = Prize(campaign_id=campaign_id, **price_data)
        try:
            db.session.add(new_price)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise 
    
    def update_price(self, prize_id, price_data):
        # Prüfe, ob der Preis existiert
        prize_in_db = Prize.query.get(prize_id)
        if not prize_in_db:
            raise ValueError("Prize not found")  # Angepasste Fehlermeldung

        # Aktualisiere die Felder, falls sie im `price_data` enthalten sind
        if "winner_ticket_id" in price_data:
            prize_in_db.winner_ticket_id = price_data["winner_ticket_id"]
        if "product_name" in price_data:
            prize_in_db.product_name = price_data["product_name"]
        if "product_description" in price_data:
            prize_in_db.product_description = price_data["product_description"]

        # Änderungen speichern
        try:
            db.session.commit()
            print(f"Prize {prize_id} updated with {price_data}")  # Debugging-Print
        except Exception as e:
            db.session.rollback()
            print(f"Error updating prize: {e}")
            raise
            
    def delete_prize(self, prize_id):
        # Check if campaign is valid
        prize_in_db = Prize.query.get(prize_id)
        if not prize_in_db:
            raise ValueError("Campaign didn´t exists") 
        
        # delete record
        db.session.delete(prize_in_db)





        
    # def add_price_to_campaign(self, campaign_id, price_data):
    #     # Check if campaign is valid
    #     existing_campaign = Campaign.query.filter_by(id=campaign_id)
    #     if not existing_campaign:
    #         raise ValueError("Campaign didn´t exists")

    