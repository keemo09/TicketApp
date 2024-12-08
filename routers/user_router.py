from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserLogIn, UserUpdate, Token, UserResponse
from crud.user import create_user, update_user, delete_user
from database import get_db
from utils.auth import authenticate_user, create_access_token, get_current_user
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
import pdb
from typing import Annotated
from models.user import User
from services.user_service import get_ticket_dict
from fastapi.security import OAuth2PasswordRequestForm




user_router = APIRouter()


@user_router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new User
    """
    try:
        new_user =  create_user(db, user)
    except Exception as e:
        return {"error": e}
    
    return {"message": f"User {user.username} created successfully!", "email": user.email}


# @user_router.post("/login")
# def login_for_access_token(user_data: UserLogIn, db: Session = Depends(get_db)):
#     """
#     Log in and create a new acces token.
#     """
#     user = authenticate_user(user_data.username, user_data.password, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.id}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")

@user_router.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Log in and create a new access token.
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.post("/")
def upate_existing_user(user_data: UserUpdate, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    """
    Update an User Record.
    """
    try:
        update_user(db, current_user.id, user_data)
    except Exception as e: 
        import traceback
        error_message = traceback.format_exc()  # Dies gibt dir die vollständige Fehlernachricht
        print(f"Error during user update: {error_message}")
        return {"error": error_message}  # Gibt die vollständige Fehlernachricht zurück 
    
    return {"message": f"User {current_user.username} updated successfully!", "email": current_user.email}
  

@user_router.delete("/")
def delete_existing_user(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    """
    Delete an User Record.
    """
    try:
        delete_user(db, current_user.id)
    except Exception as e:
        return {"error": e}
    
    return {"message": f"User {current_user.username} deleted successfully!"}


@user_router.get("/tickets")
def get_user_tickets(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    """
    Return all the tickets from a User
    """
    tickets_dict = get_ticket_dict(db, current_user.id)
    return tickets_dict


# def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user




# @router.get("/users/me/")
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     return current_user



# @router.post("/login")
# def login_for_access_token(user_data: UserLogIn):
#     user = authenticate_user(user_data.username, user_data.password)
#     return user