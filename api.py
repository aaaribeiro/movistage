# imports from third-party libraries
# from typing import Optional

from fastapi import FastAPI #, Depends, HTTPException, status ,Form
# from fastapi.security import APIKeyHeader

# required imports from models package
from models import models
from models.database import engine
# from models import crud

# required imports from package utils 
# from utils.handlers import get_db
# from sqlalchemy.orm import Session

# required imports from utils package
# from routers import agents, appointments, listeners, organizations, tickets, users
from routers import tickets
# from auth import auth

################## constants ####################
DESCRIPTION = """
"""
PREFIX = "/stage/movidesk/v1"

#################################################

app = FastAPI(
    title="NETCON",
    description=DESCRIPTION,
)


# def api_token(token: str=Depends(APIKeyHeader(name="Token")), 
#                 db: Session=Depends(get_db)):
#     if not token:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
#     acess_token = crud.get_user_by_token(db, token)
#     if not acess_token:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)


# @app.get("/test", dependencies=[Depends(auth.api_token)])
# def get_test_endpoint():
    #db: Session=Depends(get_db)):
    # if not token:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    # acess_token = crud.get_user_by_token(db, token)
    # if not acess_token:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    # return {"hello": "world"}


@app.get("/")
def get_root():
    return {"message": "welcome to Stage"}

app.include_router(tickets.router, prefix=PREFIX)
# app.include_router(organizations.router, prefix=PREFIX)
# app.include_router(agents.router, prefix=PREFIX)
# app.include_router(appointments.router, prefix=PREFIX)
# app.include_router(listeners.router, prefix=PREFIX)
# app.include_router(users.router, prefix=PREFIX)