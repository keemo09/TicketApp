from fastapi_utils.tasks import repeat_every
from fastapi import APIRouter
from sqlalchemy.orm import Session
from database import get_db, SessionLocal  # Stelle sicher, dass du `SessionLocal` importierst
from crud.campaign import get_campaigns
from services.campaign_service import campaign_is_expire, end_campaign
import os
import pdb
import threading
cronjob = APIRouter()


# @cronjob.on_event("startup")
# @repeat_every(seconds=5)
# def check_campaign():
#     print(f"Task started on thread: {threading.current_thread().name}")
#     db: Session = SessionLocal()  
#     try:
#         campaigns_in_db = get_campaigns(db)
#         for campaign in campaigns_in_db:
#             #pdb.set_trace()
#             if campaign_is_expire(db, campaign.id):
#                 #pdb.set_trace()
#                 end_campaign(db, campaign.id)

                
#     finally:
#         db.close()  # Stelle sicher, dass die Session geschlossen wird