from fastapi import HTTPException, status
from schemas.campaign import CampaignCreate, CampaignUpdate
from sqlalchemy.orm import Session
from crud.campaign import create_campaign, get_campaign_by_id, update_campaign
from crud.prize import update_prize, get_prize
from schemas.prize import PrizeUpdate

def set_winner_to_prize(db: Session, prize_id: int, ticket_id: int):
    prize = get_prize(db, prize_id)
    if not prize:
        raise ValueError(f"Prize with ID {prize_id} not found.")
    
    if prize.winner_ticket_id is not None:
        print(f"Prize {prize_id} already has a winner: Ticket {prize.winner_ticket_id}")
        return

    prize.winner_ticket_id = ticket_id
    db.commit()  # Stelle sicher, dass die Änderungen gespeichert werden
    print(f"Prize {prize_id} successfully assigned to ticket {ticket_id}.")