

from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdate
import pdb


def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Create a new User record
    """
    db_user = User(
        username=user_data.username,
        email=user_data.email,
    )
    db_user.set_password(user_data.password)  # Setze das Passwort mit der set_password-Methode

    # Save changes to db
    db.add(db_user)
    db.commit()
    return db_user



def get_users(db: Session):
    """
    Reads all the Users from db
    """
    return db.query(User).all()


def get_user_by_id(db: Session, id: int):
    """
    Reads the db and returns a user by id.
    """
    user_in_db = db.query(User).filter(User.id == id).first()
    return user_in_db


def get_user_by_username(db: Session, username: str):
    """
    Reads the db and returns a user by username.
    """
    user_in_db = db.query(User).filter(User.username == username).first()
    return user_in_db


def update_user(db:Session, user_id: int, user_data: UserUpdate):
    """
    Update an existing User record.
    """
    user_in_db = get_user_by_id(db, user_id)
    if not user_in_db:
        raise ValueError("User dont exists!")
    
    # turn user_data pydantic model into dict
    user_data_dict = user_data.model_dump(exclude_unset=True)

    # Set the Values which are for change
    for key, value in user_data_dict.items():
            if hasattr(user_in_db, key):
                setattr(user_in_db, key, value)

    db.commit()


def delete_user(db: Session, user_id):
    """
    Delete an existing User Record
    """
    user_in_db = get_user_by_id(db, user_id)
    if not user_in_db:
      raise ValueError("User dont exists!")
    db.delete(user_in_db)
    db.commit()

    




