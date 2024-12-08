from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# Create password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    #realtionship
    campaigns = relationship("Campaign", backref="user", lazy=True)
    tickets = relationship("Ticket", backref="user", lazy=True)

    def set_password(self, password: str):
        """Erstellt und speichert den Passwort-Hash."""
        self.password_hash = pwd_context.hash(password)

    def check_password(self, password: str) -> bool:
        """Überprüft das Passwort anhand des gespeicherten Hashes."""
        return pwd_context.verify(password, self.password_hash)