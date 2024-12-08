from sqlalchemy.orm import Session
from models.campaign import Campaign
from schemas.campaign import CampaignCreate, CampaignUpdate
from crud.user import get_user_by_id
from fastapi import HTTPException, status
from models.campaign import Campaign


def create_campaign(db: Session, user_id: int, campaign_data: CampaignCreate):
    """
    Create a new campaign record.
    """
    # Checks if user is in db
    if not get_user_by_id(db, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create a new Campaign Model
    db_campaign = Campaign(
        user_id=user_id,
        **campaign_data
    )

    # Save changes to db
    db.add(db_campaign)
    db.commit()  
    #db.refresh(db_campaign)  
    return db_campaign


def get_campaigns(db: Session):
    """
    Return all Campaigns
    """
    campaigns = db.query(Campaign).all()
    return campaigns

def get_campaigns_by_user(db: Session, user_id: int):
    """
    Returns all Campaigns from a speciffic User
    """
    campaigns = db.query(Campaign).filter(Campaign.user_id==user_id)
    return campaigns

def get_campaign_by_id(db: Session, campaign_id: int):
    """
    Return a speciffic campaign by id 
    """
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    return campaign 


# def update_campaign(db: Session, campaign_id: int, campaign_data: CampaignUpdate):
#     """
#     Update a specific Campaign record
#     """
#     campaign_in_db = db.query(Campaign).filter(Campaign.id == campaign_id).first()
#     if not campaign_in_db:
#         raise ValueError("Campaign does not exist!")
    
#     # turn user_data pydantic model into dict
#     campaign_data_dict = campaign_data.model_dump(exclude_unset=True)

#     # Set the Values which are for change
#     for key, value in campaign_data_dict.items():
#         if hasattr(campaign_in_db, key):
#             setattr(campaign_in_db, key, value)

#     db.commit()  # Commit here
#     print("Database commit successful")  # Debug-Ausgabe
#     db.refresh(campaign_in_db)  # Refresh after commit

def update_campaign(db: Session, campaign_id: int, campaign_data: CampaignUpdate):
    """
    Update a specific Campaign record
    """
    try:
        campaign_in_db = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if not campaign_in_db:
            raise ValueError("Campaign does not exist!")

        campaign_data_dict = campaign_data.model_dump(exclude_unset=True)

        for key, value in campaign_data_dict.items():
            if hasattr(campaign_in_db, key):
                setattr(campaign_in_db, key, value)
                #print(f"Set {key} to {value}")  # Debug-Ausgabe


        # Versuche zuerst flush, um Änderungen in die DB zu schreiben
        db.flush()
        db.commit()  # Commit hier


        # Überprüfen, ob der Status nach dem Commit geändert wurde
        db.refresh(campaign_in_db)

    except Exception as e:
        print(f"Error during update_campaign: {e}")  # Debug-Ausgabe für Fehler
        raise  # Ausnahme erneut werfen, um sie weiter oben abzufangen


# from sqlalchemy.orm import Session
# from models.campaign import Event
# from schemas.campaign import EventCreate


# def create_event(db: Session, event_data: EventCreate):
#     """
#     Create a new event record.
#     """
#     db_event = Event (
#         **event_data
#     )

#     # Save changes to db
#     db.add(db_event)
#     db.commit()  
#     db.refresh(db_event)  
#     return 

# def get_events(db: Session):
#     """
#     Return all events
#     """
#     events = db.query(Event).all()
#     return events

# def get_events_by_user(db: Session, user_id: int):
#     """
#     Returns all events from a speciffic User
#     """
#     events = db.query(Event).filter(user_id=user_id)
#     return events

# def get_event_by_id(db: Session, event_id):
#     """
#     Return a speciffic event by id 
#     """
#     event = db.query(Event).filter(id=event_id)
#     return event 



