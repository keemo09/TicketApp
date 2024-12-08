from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base  # Angenommene Basis-Import für SQLAlchemy
from models.user import User 
from models.ticket import Ticket
from models.prize import Prize




class Campaign(Base):
    __tablename__ = "campaigns"
    

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now())

    # Settings
    max_ticket = Column(Integer, nullable=False)
    min_ticket = Column(Integer, nullable=False)
    max_ticket_per_user = Column(Integer, nullable=False)
    campaign_end = Column(DateTime, nullable=True)

    #realtionships
    tickets = relationship("Ticket", backref="campaign", lazy="select")
    prizes = relationship("Prize", backref="campaign", lazy="select")

    def __repr__(self):
        return f"<campaign(name={self.name}, id={self.id}, user_id={self.user_id}, active={self.active})>"


# from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from database import Base  # Angenommene Basis-Import für SQLAlchemy
# from models.user import User 
# from models.ticket import Ticket
# from models.prize import Prize




# class campaign(Base):
#     __tablename__ = "campaigns"
    

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String, nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
#     active = Column(Boolean, default=True, nullable=False)
#     created_at = Column(DateTime, default=func.now())

#     # Settings
#     max_ticket = Column(Integer, nullable=False)
#     min_ticket = Column(Integer, nullable=False, default=1)
#     max_ticket_per_user = Column(Integer, nullable=False, default=1)
#     campaign_end = Column(DateTime, nullable=True)

#     #realtionships
#     tickets = relationship("Ticket", backref="campaign", lazy=True)
#     prizes = relationship("Prize", backref="campaign", lazy=True)

#     def __repr__(self):
#         return f"<campaign(name={self.name}, id={self.id}, user_id={self.user_id}, active={self.active})>"