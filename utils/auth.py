from database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from schemas.user import TokenData
import jwt
from typing import Annotated
from jwt.exceptions import InvalidTokenError
from crud.user import get_user_by_username, get_user_by_id
from crud.campaign import get_campaigns_by_user



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login", scheme_name="JWT")



def authenticate_user(username: str, password: str, db: Session):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not user.check_password(password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_id(db, token_data.id)
    if user is None:
        raise credentials_exception
    return user


def user_have_campaign(db: Session, user_id: int, campaign_id: int):
    user_campaigns = get_campaigns_by_user(db, user_id)
    if not campaign_id in user_campaigns:
        return False
    return True