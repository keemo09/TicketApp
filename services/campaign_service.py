from fastapi import HTTPException, status
from schemas.campaign import CampaignCreate, CampaignUpdate
from sqlalchemy.orm import Session
from crud.campaign import create_campaign, get_campaign_by_id, update_campaign
from crud.ticket import create_ticket, get_tickets_by_campaign, get_tickets_by_user_and_campaign
from crud.user import get_user_by_id
from crud.prize import create_prize, get_prizes_by_campaign, get_prize
from random import choice
from services.prize_service import set_winner_to_prize
from datetime import datetime
import pdb


def campaign_is_expire(db: Session, campaign_id: int):
    """
    Checks if an existing campaign is expired
    """
    campaign_in_db = get_campaign_by_id(db, campaign_id)

    # Checks if campaign is valid
    if not campaign_in_db:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Campaign not found"
        )

    # # Checks if campaign status is active
    # if campaign_in_db.active == False:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="The requested campaign is inactive. Access denied."
    #     )
    
    if campaign_in_db.campaign_end <= datetime.now():
        return True 
    
    return False
    


def start_campaign(db: Session, user_id: int, campaign_data: CampaignCreate):
    campaign_data_excludet_price = campaign_data.model_dump(exclude="prizes")
    prize_data = campaign_data.prizes
    new_campaign = create_campaign(db, user_id, campaign_data_excludet_price)

    # for every prize create a new prize record
    for prize in prize_data:
        create_prize(db, new_campaign.id, prize)

    return new_campaign


# def set_campaign_winner(db: Session, campaign_id: int):
#     campaign_tickets_in_db = get_tickets_by_campaign(db, campaign_id)
#     campaign_prizes_in_db = get_prizes_by_campaign(db, campaign_id)
#     # chose for every prize one ticket 
#     for prize in campaign_prizes_in_db:
#         winner_ticket = choice(campaign_tickets_in_db) # remove from list 
#         campaign_tickets_in_db.remove(winner_ticket) 
#         set_winner_to_prize(db, prize.id, winner_ticket.id)

# def set_campaign_winner(db: Session, campaign_id: int):
#     campaign_tickets_in_db = get_tickets_by_campaign(db, campaign_id)
#     campaign_prizes_in_db = get_prizes_by_campaign(db, campaign_id)

#     # Choose one ticket for each prize
#     for prize in campaign_prizes_in_db:
#         if not campaign_tickets_in_db:  # Wenn keine Tickets vorhanden sind, überspringe die Schleife
#             return

#         winner_ticket = choice(campaign_tickets_in_db)
#         if winner_ticket in campaign_tickets_in_db:
#             campaign_tickets_in_db.remove(winner_ticket)
#         else:
#             print(f"Ticket {winner_ticket.id} not found in the available tickets list.")
#         set_winner_to_prize(db, prize.id, winner_ticket.id)

def set_campaign_winner(db: Session, campaign_id: int):
    """
    Select winners for the given campaign by assigning tickets to prizes.

    Args:
        db (Session): The database session.
        campaign_id (int): The ID of the campaign.

    Returns:
        None
    """
    print("choose winner")

    # Tickets und Preise für die Kampagne holen
    campaign_tickets_in_db = get_tickets_by_campaign(db, campaign_id)
    campaign_prizes_in_db = get_prize(db, campaign_id)  # Verwenden von get_prize

    if not campaign_tickets_in_db:
        print(f"No tickets available for campaign {campaign_id}. Skipping prize selection.")
        return

    if not campaign_prizes_in_db:
        print(f"No prizes available for campaign {campaign_id}. Skipping prize selection.")
        return

    # Falls nur ein Preis zurückgegeben wird, muss keine Schleife verwendet werden
    if isinstance(campaign_prizes_in_db, list):
        for prize in campaign_prizes_in_db:
            if not campaign_tickets_in_db:
                print(f"Ran out of tickets before assigning prize {prize.id}.")
                break

            # Zufälliges Ticket auswählen
            winner_ticket = choice(campaign_tickets_in_db)

            # Den Gewinner dem aktuellen Preis zuweisen
            print(f"Selected winner ticket {winner_ticket.id} for prize {prize.id}")

            try:
                # Setze den Gewinner für den Preis
                set_winner_to_prize(db, prize.id, winner_ticket.id)
            except Exception as e:
                print(f"Error assigning ticket {winner_ticket.id} to prize {prize.id}: {e}")
                continue

            # Entferne das Ticket aus der Liste der verfügbaren Tickets
            if winner_ticket in campaign_tickets_in_db:
                campaign_tickets_in_db.remove(winner_ticket)
            else:
                print(f"Ticket {winner_ticket.id} not found in the available tickets list after assignment.")
    else:
        # Wenn nur ein einzelner Preis zurückgegeben wird
        prize = campaign_prizes_in_db
        if not campaign_tickets_in_db:
            print(f"Ran out of tickets before assigning prize {prize.id}.")
        else:
            # Zufälliges Ticket auswählen
            winner_ticket = choice(campaign_tickets_in_db)

            # Den Gewinner dem aktuellen Preis zuweisen
            print(f"Selected winner ticket {winner_ticket.id} for prize {prize.id}")

            try:
                # Setze den Gewinner für den Preis
                set_winner_to_prize(db, prize.id, winner_ticket.id)
            except Exception as e:
                print(f"Error assigning ticket {winner_ticket.id} to prize {prize.id}: {e}")

            # Entferne das Ticket aus der Liste der verfügbaren Tickets
            if winner_ticket in campaign_tickets_in_db:
                campaign_tickets_in_db.remove(winner_ticket)
            else:
                print(f"Ticket {winner_ticket.id} not found in the available tickets list after assignment.")

    print(f"Winners selected for campaign {campaign_id}.")



def end_campaign(db: Session, campaign_id: int):
    """
    Set the active status to False and start the lottery
    """
    campaign_in_db = get_campaign_by_id(db, campaign_id)
    
    # Checks if campaign is valid
    if not campaign_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    #pdb.set_trace()
    # Start the lottery logic
    set_campaign_winner(db, campaign_in_db.id)

    # Set the status to false
    campaign_data = CampaignUpdate(active=False)


    update_campaign(db, campaign_id, campaign_data)



def generate_ticket(db: Session, user_id: int, campaign_id: int):
    """
    Generate a new ticket and assoiate it to an user and campaign
    """
    user_in_db = get_user_by_id(db, user_id)
    campaign_in_db = get_campaign_by_id(db, campaign_id)
    user_tickets_in_db = get_tickets_by_user_and_campaign(db, user_id, campaign_id)

    # checks if user is valid
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # checks if campagn is valid  
    if not campaign_in_db:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Campaign not found"
        )
    
    # checks if campaign is active
    if not campaign_in_db.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The requested campaign is inactive. Access denied."
        )

    # checks if user reaches the max_ticket_per_user
    if len(user_tickets_in_db) >= campaign_in_db.max_ticket_per_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Max tickets per user count is reached. Access denied."
        )
    
    # create a ticket 
    ticket_in_db = create_ticket(db, user_id, campaign_id)

    # checks if max_ticket in campaign is reached
    if len(get_tickets_by_campaign(db, campaign_id)) >= campaign_in_db.max_ticket:
        end_campaign(db, campaign_id)



        
    




