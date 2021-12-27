from fastapi import HTTPException, status
from models import crud 

def authorization(db, token):
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    acess_token = crud.get_user_by_token(db, token)
    if not acess_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def admin_authorization(db, token):
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    acess_token = crud.get_user_by_token(db, token)
    if not acess_token and acess_token.isadmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
