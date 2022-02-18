# built-in libraries
# from datetime import datetime

# imports from third-party libraries
# from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

# required imports from package models
from models.crud import CRUDUser 
from serializers import schemas

# required imports from packageutils 
from utils.handlers import get_db
# from auth import auth

# constants
# it will be used in swagger documentation to organize the endpoints
TAGS = ["users",]

router = APIRouter()

@router.post(
    "/token",
    tags=TAGS,
    response_model=schemas.CreatedUser
)
async def login(formData: OAuth2PasswordRequestForm=Depends(),
                            db: Session=Depends(get_db)):
    dbUser = CRUDUser.readUserByEmail(db, formData.username)
    if not dbUser:
        raise HTTPException(status_code=400,
                            detail="incorrect username or password")
    if dbUser.password != formData.password:
        raise HTTPException(status_code=400,
                            detail="incorrect username or password")
    return dbUser


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