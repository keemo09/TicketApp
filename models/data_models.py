from data_manager import db
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    #Will be created automatically whan User record is created
    created_at = db.Column(db.DateTime default=func.now())

    #realtionships
    campaigns = db.realtionships("Campaign", backref="campaign", lazy=True)
    tickets = db.realtionships("Ticket", backref="tickets", lazy=True)


class Campaign(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id") nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)

    #Will be created automatically whan User record is created
    created_at = db.Column(db.DateTime default=func.now())

    #realtionships
    tickets = db.realtionships("Ticket", backref="campaign", lazy=True)
    prizes = db.realtionships("Prize", backref="campaign", lazy=True)


class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id") nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id") nullable=False)

    #realtionships
    prize = db.realtionships("Prize", backref="ticket", uselist=False, lazy=True)


    
class Prize(db.Model):
    __tablename__ = "prizes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = (db.Integer, db.ForeignKey("campaign.id"), nullable=False)
    winner_ticket_id = (db.Integer, db.ForeignKey("ticket.id"), unique=True, nullable=True)
    product_id = (db.Integer, db.ForeignKey("product.id"), unique=True, nullable=True)

    
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)

    #realtionships
    prize = db.realtionships("Prize", backref="product", uselist=False, lazy=True)
