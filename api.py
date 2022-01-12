# imports from third-party libraries
from typing import Optional

from sqlalchemy.util.langhelpers import dependencies
from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.security import APIKeyHeader

# required imports from models package
from models import models
from models.database import engine
from models import crud
# required imports from package utils 
from utils.handlers import get_db
from sqlalchemy.orm import Session

# required imports from utils package
from routers import organizations, tickets, time_appointments, webhooks, users
from auth import auth

################## constants ####################
DESCRIPTION = """
"""
PREFIX = "/stage/movidesk/v1"
#################################################

app = FastAPI(
    title="Netcon API",
    description=DESCRIPTION,
)

@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)
    # logger.info("Models created/updated sucessfuly")


@app.get("/test")
def get_test_endpoint(db: Session=Depends(get_db)):
    # if not token:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    # acess_token = crud.get_user_by_token(db, token)
    # if not acess_token:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return {"hello": "world"}


# @app.get("/")
# def get_root():
#     return {"message": "welcome to Stage"}

app.include_router(tickets.router, prefix=PREFIX)
app.include_router(organizations.router, prefix=PREFIX)
app.include_router(time_appointments.router, prefix=PREFIX)
app.include_router(webhooks.router, prefix=PREFIX)
# app.include_router(users.router, prefix=PREFIX)





