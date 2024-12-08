from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.campaign import CampaignCreate, CampaignUpdate
from database import get_db
from utils.auth import get_current_user, user_have_campaign
from datetime import timedelta
import pdb
from typing import Annotated
from models.user import User
from services.campaign_service import start_campaign, generate_ticket
from crud.campaign import get_campaign_by_id, update_campaign, get_campaigns_by_user
from fastapi.encoders import jsonable_encoder
from schemas.campaign import CampaignSchema


campaign_router = APIRouter()


@campaign_router.post("/", response_model=None)
def create_campaign(
    current_user: Annotated[User, Depends(get_current_user)], 
    campaign_data: CampaignCreate, 
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    start_campaign(db, user_id, campaign_data)
    return {"message": "Campaign created successfully"}


# @campaign_router.get("/", response_model=None)
# def get_campaigns(
#     current_user: Annotated[User, Depends(get_current_user)],  
#     db: Session = Depends(get_db)
# ):
#     user_id = current_user.id
#     campaigns = get_campaigns_by_user(db, user_id)
#     return campaigns

# @campaign_router.get("/", response_model=list[CampaignSchema])
# def get_campaigns(
#     current_user: Annotated[User, Depends(get_current_user)],
#     db: Session = Depends(get_db)
# ):
#     user_id = current_user.id
#     campaigns = get_campaigns_by_user(db, user_id)

#     return campaigns

@campaign_router.get("/", response_model=None)
def get_campaigns(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    campaigns = get_campaigns_by_user(db, user_id)
    
    campaigns_data = []
    
    for campaign in campaigns:
        # Extrahiere nur die relevanten Felder
        campaign_data = {
        "id": campaign.id,
        "name": campaign.name,
        "user_id": campaign.user_id,
        "active": campaign.active,
        "created_at": campaign.created_at.strftime('%Y-%m-%d %H:%M:%S') if campaign.created_at else None,
        "campaign_end": campaign.campaign_end.strftime('%Y-%m-%d %H:%M:%S') if campaign.campaign_end else None,
        "max_ticket": campaign.max_ticket,
        "min_ticket": campaign.min_ticket,
        "max_ticket_per_user": campaign.max_ticket_per_user,
        # Optional: Für die Beziehungen (z.B. Tickets, Preise) kannst du auch eine Verkürzung oder Details einfügen
        "tickets": [ticket for ticket in campaign.tickets],  # Hier kannst du das Ticket-Objekt oder die ID einfügen
        "prizes": [prize for prize in campaign.prizes],  # Hier kannst du das Prize-Objekt oder die ID einfügen
        }
        
        campaigns_data.append(campaign_data)
    
    return campaigns_data


@campaign_router.get("/{campaign_id}")
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = get_campaign_by_id(db, campaign_id)
    return campaign


@campaign_router.put("/{campaign_id}")
def update_campaign(current_user: Annotated[User, Depends(get_current_user)],
                    campaign_id: int, 
                    campaign_data: CampaignUpdate,
                    db: Session = Depends(get_db)):
    
    if user_have_campaign(db, current_user.id, campaign_id):
        update_campaign(db, campaign_id, campaign_data)
    return {"message": f"User {campaign_id} updated successfully!"}


@campaign_router.delete("/{campaign_id}")
def delete_campaign(current_user: Annotated[User, Depends(get_current_user)],
                    campaign_id: int,
                    db: Session = Depends(get_db)):
    if user_have_campaign(db, current_user.id, campaign_id):
        delete_campaign(db, campaign_id)


@campaign_router.get("/{campaign_id}/ticket")
def get_ticket(current_user: Annotated[User, Depends(get_current_user)],
               campaign_id: int,
               db: Session = Depends(get_db)):
    generate_ticket(db, current_user.id, campaign_id)

    return {"message": f"Ticket createt successfully!"}
    