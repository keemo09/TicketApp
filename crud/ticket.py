from sqlalchemy.orm import Session
from models.ticket import Ticket



def create_ticket(db: Session, user_id: int, campaign_id: int):
    """
    Create a new Ticket record.
    """
    # Create new Ticket Model
    db_ticket = Ticket(
        user_id=user_id,
        campaign_id=campaign_id
    )

    # Save changes to db
    db.add(db_ticket)
    db.commit()  
    #db.refresh(db_campaign)  
    return db_ticket


def get_ticket(db: Session, ticket_id: int):
    """
    Get an speciffic ticket record
    """
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    return db_ticket


def get_tickets(db: Session):
    """
    Get all ticket records
    """
    db_tickets = db.query(Ticket).all()
    return db_tickets


def get_tickets_by_user(db: Session, user_id: int):
    """
    Get all ticket records of an speciffic user
    """
    tickets_in_db = db.query(Ticket).filter(Ticket.user_id == user_id).all()
    return tickets_in_db


def get_tickets_by_campaign(db: Session, campaign_id: int):
    """
    Get all ticket records of an speciffic campaign
    """
    tickets_in_db = db.query(Ticket).filter(Ticket.campaign_id == campaign_id).all()
    return tickets_in_db
   

def get_tickets_by_user_and_campaign(db: Session, user_id: int, campaign_id: int):
    """
    Get all ticket records of an speciffic user
    """
    tickets_in_db = db.query(Ticket).filter(Ticket.user_id == user_id,
                                            Ticket.campaign_id == campaign_id
                                            ).all()
    return tickets_in_db


# def update_ticket(db: Session, ticket_id: int, ticket_data: TicketUpdate):
#     """
#     Update an speciffic ticket record
#     """
#     ticket_in_db = db.query(Ticket).filter(Ticket.id == ticket_id)
#     if not ticket_in_db:
#         raise ValueError("Ticket dont exists!")
#     ticket_data_dict = ticket_data.model_dump(exclude_unset=True)

#     # Set the Values which are for change
#     for key, value in ticket_data_dict.items():
#             if hasattr(ticket_in_db, key):
#                 setattr(ticket_in_db, key, value)

#     db.refresh(ticket_in_db)
#     db.commit()


def delete_ticket(db: Session, ticket_id: int):
     """
     Delete an existing Ticket record
     """
     ticket_in_db = db.query(Ticket).filter(Ticket.id == ticket_id)
     if not ticket_in_db:
          raise ValueError("Ticket dont exists!")
     db.delete(ticket_in_db)
     db.commit()
         
    