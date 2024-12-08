from sqlalchemy.orm import Session
from schemas.campaign_old import CampaignCreate
from models.campaign_old import Campaign



def create_campaign(db: Session, user_id: int, campaign_data: CampaignCreate):
    """
    Create a new campaign record
    """
    # create a new campaign model 
    db_campaign = Campaign (
        user_id = user_id
        **campaign_data
    )

    # save the campaign to db 
    db.add(db_campaign)
    db.commit()


    return db_campaign


def get_campaigns(db: Session):
    """
    Returns all the Campaign records
    """

    campaigns = db.query(Campaign).all()
    return campaigns


def get_campaigns_by_user(db: Session, user_id: int):
    """
    Return all Campaign records from a speciffic user
    """
    campaigns = db.query(Campaign).filter(user_id=user_id)
    return campaigns 


def get_campaign(db: Session, campaign_id: int):
    """
    Return a speciffic Campaign 
    """
    campaigns = db.query(Campaign).filter(id=campaign_id)
    return campaigns


def update_campaign(db: Session, campaign_id: int, campaign_data: CampaignUpdate):
    """
    Update a specific Campaign
    """
    campaign_in_db = get_campaign(db, campaign_id)
    if not campaign_in_db:
        raise ValueError("Campaign dont exist")
    
    campaign_data_dict = campaign_data.model_dump(exclude_unset=True)

    # Set the Values which are for change
    for key, value in campaign_data_dict.items():
            if hasattr(campaign_in_db, key):
                setattr(campaign_in_db, key, value)

    db.commit()


def delete_campaign(db: Session, campaign_id: int):
     """
     Delete an existing campaign record
     """
     campaign_in_db = get_campaign(db, campaign_id)
     if not campaign_in_db:
          raise ValueError("Campaign dont exist")
     
     db.delete(campaign_in_db)
     db.commit()




    





