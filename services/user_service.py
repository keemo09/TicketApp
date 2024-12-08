from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from typing import Annotated
import jwt
from config import SECRET_KEY, ALGORITHM
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.user import TokenData
from crud.user import get_user_by_username, get_user_by_id
from crud.ticket import get_tickets_by_user
from database import get_db
from sqlalchemy.orm import Session
from models.user import User
from utils.auth import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def authenticate_user(username: str, password: str, db: Session):
#     user = get_user_by_username(db, username)
#     if not user:
#         return False
#     if not user.check_password(password):
#         return False
#     return user


# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         id: int = payload.get("sub")
#         if id is None:
#             raise credentials_exception
#         token_data = TokenData(id=id)
#     except InvalidTokenError:
#         raise credentials_exception
#     user = get_user_by_id(db, token_data.id)
#     if user is None:
#         raise credentials_exception
#     return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_ticket_dict(db: Session, user_id: int):
    tickets_in_db = get_tickets_by_user(db, user_id)
    tickets = []
    for ticket in tickets_in_db:
        ticket_schema = {"id":ticket.id,
                         "campaign_name": ticket.campaign.name,
                         "campaign_ends": ticket.campaign.campaign_end,
                         "campaign_is_active": ticket.campaign.active
                         }
        tickets.append(ticket_schema)
    return tickets