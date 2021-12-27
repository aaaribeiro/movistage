# built-in libraries
# from datetime import datetime

# imports from third-party libraries
# from typing import List
# from fastapi import Depends, APIRouter, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session

# required imports from package models
# from models import crud 
# from serializers import schemas

# required imports from packageutils 
# from utils.handlers import get_db
# from auth import auth

# constants
# it will be used in swagger documentation to organize the endpoints
# TAGS = ["Authentication",]

# router = APIRouter()

# @router.post(
#     "/user",
#     tags=TAGS,
#     response_model=schemas.CreatedUser
# )
# async def register_user(user: schemas.User, token:str=None,
#                             db: Session=Depends(get_db)):
#     """
#     Create an user in movidesk stage
#     """

#     auth.admin_authorization(db, token)
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(
#             status_code=400,
#             detail="User already registered"
#         )
#     return crud.register_user(db=db, user=user)


# @router.post(
#     "/token",
#     tags=TAGS,
#     response_model=schemas.AccessToken
# )
# async def create_token(form_data: OAuth2PasswordRequestForm=Depends(OAuth2PasswordRequestForm),
#                     db: Session=Depends(get_db)):
#     email = form_data.username
#     password = form_data.password
#     user = crud.authenticate_user(db, user=email, password=password)
    
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

#     token = crud.get_access_token(db, user=user)
#     if not token:
#         token = crud.create_access_token(db, user=user)
    
#     return token