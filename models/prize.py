from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from database import Base  # Angenommene Basis-Import für SQLAlchemy
from sqlalchemy.orm import relationship


class Prize(Base):
    __tablename__ = "prizes"
    id = Column(Integer, primary_key=True, autoincrement=True) 
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    winner_ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)
    product_name = Column(String, nullable=False)
    product_description = Column(String, nullable=True)

