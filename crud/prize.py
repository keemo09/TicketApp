from sqlalchemy.orm import Session
from models.prize import Prize
from schemas.prize import PrizeCreate, PrizeUpdate


def create_prize(db: Session, campaign_id: int,  prize_data: PrizeCreate):
    """
    Create a new Prize Record
    """
    prize_data_dict = prize_data.model_dump(exclude_unset=True)

    db_prize = Prize(
        campaign_id = campaign_id,
        **prize_data_dict
    )

    # save changes to db 
    db.add(db_prize)
    db.commit()
    return db_prize


def get_prizes_by_campaign(db: Session, campaign_id: int):
    """
    Return all Prize records of a Campaign
    """
    prizes = db.query(Prize).filter(id=campaign_id).all()
    return prizes


def get_prizes_by_campaign(db: Session, campaign_id: int):
    """
    Return all Prize records of a Campaign
    """
    prizes = db.query(Prize).filter(Prize.campaign_id == campaign_id).all()
    return prizes


def get_prize(db: Session, prize_id: int):
    """
    Return Prize records
    """
    prize = db.query(Prize).filter(Prize.campaign_id == prize_id).first()  
    return prize

def update_prize(db: Session, prize_id: int, prize_data: PrizeUpdate):
    """
    Update a peciffic Campaign record
    """
    prize_in_db = get_prize(db, prize_id)
    if not prize_in_db:
        raise ValueError("Campaign dont exists!")
    
    # turn user_data pydantic model into dict
    prize_data_dict = prize_data.model_dump(exclude_unset=True)

    # Set the Values which are for change
    for key, value in prize_data_dict.items():
            if hasattr(prize_in_db, key):
                setattr(prize_in_db, key, value)

    db.commit()


def delete_prize(db: Session, prize_id):
    """
    Delete a peciffic Prize record
    """
    prize_in_db = get_prize(db, prize_id)
    if not prize_in_db:
        raise ValueError("Campaign dont exists!")
    
    db.delete(prize_in_db)
    db.commit()
    
     



