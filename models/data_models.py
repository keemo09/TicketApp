from data_manager.db import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    #Will be created automatically whan User record is created
    created_at = db.Column(db.DateTime, default=func.now())

    #realtionship
    campaigns = db.relationship("Campaign", backref="campaign", lazy=True)
    tickets = db.relationship("Ticket", backref="tickets", lazy=True)

    def set_password(self, password):
        '''
        Set the password as hash
        '''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''
        Checks if password equals to password hash 
        '''
        return check_password_hash(self.password_hash, password)


class Campaign(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    max_ticket = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)

    #Will be created automatically whan User record is created
    created_at = db.Column(db.DateTime, default=func.now())

    #realtionships
    tickets = db.relationship("Ticket", backref="campaign", lazy=True)
    prizes = db.relationship("Prize", backref="campaign", lazy=True)


class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    #realtionships
    prize = db.relationship("Prize", backref="ticket", uselist=False, lazy=True)


    
class Prize(db.Model):
    __tablename__ = "prizes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"), nullable=False)
    winner_ticket_id = db.Column(db.Integer, db.ForeignKey("tickets.id"), nullable=True)
    #product_id = db.Column(db.Integer, db.ForeignKey("products.id"), unique=True, nullable=True)
    product_name = db.Column(db.String, nullable=False)
    product_description = db.Column(db.Text, nullable=True)

    
# class Product(db.Model):
#     __tablename__ = "products"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String, nullable=False)
#     description = db.Column(db.Text, nullable=True)

#     #realtionships
#     prize = db.relationship("Prize", backref="product", uselist=False, lazy=True)
