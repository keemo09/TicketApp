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
                    campaign_data_manager.update_campaign(campaign.id, {"active": False})
                    all_tickets_id = campaign_data_manager.get_tickets(campaign.id)
                    for prize in campaign.prizes:
                        if all_tickets_id:
                            random_ticket_id = choice(all_tickets_id)
                            campaign_data_manager.update_price(prize.id, {"winner_ticket_id": random_ticket_id})
                            all_tickets_id.remove(random_ticket_id)
