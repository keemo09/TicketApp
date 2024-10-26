from flask import Flask  # Importiere Flask für den Typ der App-Instanz
from data_manager.campaign_data_manager import CampaignDataManager
from datetime import datetime
from random import choice

campaign_data_manager = CampaignDataManager()

def setup_jobs(scheduler, app: Flask): 
    print("job started")
    
    @scheduler.task('cron', id='campaign_checker', minute='*')
    def check_expiring_campaigns():
        '''
        Checking every minute if a existing campaign is expired.
        Then set the active status to False and Pick for prices a winner ticket.
        '''
        print("check job")
        with app.app_context():  # Activate app context
            print("app context active")
            campaigns = campaign_data_manager.get_campaigns()

            # Checks if end date of a campaign is reached
            for campaign in campaigns:
                if campaign.end_date <= datetime.now() and campaign.active:
                    print("exp campaign found")
                    campaign_data_manager.update_campaign(campaign.id, {"active": False})
                    print(f"Prizes in campaign {campaign.id}: {len(campaign.prizes)}")

                    all_tickets_id = campaign_data_manager.get_tickets(campaign.id)
                    print(f"Tickets in campaign {campaign.id}: {all_tickets_id}")

                    for prize in campaign.prizes:
                        print(f"Processing prize with ID {prize.id}")
                        if all_tickets_id:
                            random_ticket_id = choice(all_tickets_id)
                            print(f"Assigning Ticket ID {random_ticket_id} to Prize ID {prize.id}")
                            campaign_data_manager.update_price(prize.id, {"winner_ticket_id": random_ticket_id})
                            all_tickets_id.remove(random_ticket_id)
