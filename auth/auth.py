from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyQuery
from sqlalchemy.orm import Session
from models import _crud 
from utils.handlers import get_db

# def authorization(db, token):
#     if not token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     acess_token = crud.get_user_by_token(db, token)
#     if not acess_token:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


# def admin_authorization(db, token):
#     if not token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     acess_token = crud.get_user_by_token(db, token)
#     if not acess_token and acess_token.isadmin:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def api_token(token: str=Depends(APIKeyQuery(name="Token")), 
                db: Session=Depends(get_db)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    acess_token = _crud.get_user_by_token(db, token)
    if not acess_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
