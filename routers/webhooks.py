# built-in libraries
from datetime import datetime

# imports from third-party libraries
# from typing import List
from fastapi import Depends,APIRouter, HTTPException, Request
from sqlalchemy.orm import Session

# required imports from package models
from models import crud 
from serializers import schemas

# required imports from packageutils 
from utils.handlers import get_db

# authentication
from auth import auth

# constants
# it will be used in swagger documentation to organize the endpoints
TAGS = ["Webhook",]

router = APIRouter()

@router.post(
    "/hook/status",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def create_hook(request: Request, token: str = None,
                    db: Session=Depends(get_db)):

    auth.authorization(db, token) 
    response = await request.json()
    webhook = schemas.WebhookLog(
        ticket_id = response["Id"],
        change = "STATUS",
        trigger_date = datetime.now()
    )
    webhook = crud.create_hook(db, webhook)
    return webhook


@router.post(
    "/hook/ticket",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def create_hook(request: Request, token: str = None,
                    db: Session=Depends(get_db)):

    auth.authorization(db, token)
    response = await request.json()
    webhook = schemas.WebhookLog(
        ticket_id = response["Id"],
        change = "TICKET",
        trigger_date = datetime.now()
    )
    webhook = crud.create_hook(db, webhook)
    return webhook


@router.post(
    "/hook/appointment",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def create_hook(request: Request, token: str = None,
                    db: Session=Depends(get_db)):

    auth.authorization(db, token) 
    response = await request.json()
    webhook = schemas.WebhookLog(
        ticket_id = response["Id"],
        change = "APPOINTMENT",
        trigger_date = datetime.now()
    )
    webhook = crud.create_hook(db, webhook)
    return webhook


@router.post(
    "/hook/service",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def create_hook(request: Request, token: str = None,
                    db: Session=Depends(get_db)):

    auth.authorization(db, token) 
    response = await request.json()
    webhook = schemas.WebhookLog(
        ticket_id = response["Id"],
        change = "SERVICE",
        trigger_date = datetime.now()
    )
    webhook = crud.create_hook(db, webhook)
    return webhook


@router.post(
    "/hook/urgency",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def create_hook(request: Request, token: str = None,
                    db: Session=Depends(get_db)):

    auth.authorization(db, token) 
    response = await request.json()
    webhook = schemas.WebhookLog(
        ticket_id = response["Id"],
        change = "URGENCY",
        trigger_date = datetime.now()
    )
    webhook = crud.create_hook(db, webhook)
    return webhook


@router.post(
    "/hook/category",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def create_hook(request: Request, token: str = None,
                    db: Session=Depends(get_db)):

    auth.authorization(db, token) 
    response = await request.json()
    webhook = schemas.WebhookLog(
        ticket_id = response["Id"],
        change = "CATEGORY",
        trigger_date = datetime.now()
    )
    webhook = crud.create_hook(db, webhook)
    return webhook


@router.post(
    "/hook/agent",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def create_hook(request: Request, token: str = None,
                    db: Session=Depends(get_db)):

    auth.authorization(db, token) 
    response = await request.json()
    webhook = schemas.WebhookLog(
        ticket_id = response["Id"],
        change = "AGENT",
        trigger_date = datetime.now()
    )
    webhook = crud.create_hook(db, webhook)
    return webhook


@router.post(
    "/hook/subject",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def create_hook(request: Request, token: str = None,
                    db: Session=Depends(get_db)):

    auth.authorization(db, token) 
    response = await request.json()
    webhook = schemas.WebhookLog(
        ticket_id = response["Id"],
        change = "SUBJECT",
        trigger_date = datetime.now()
    )
    webhook = crud.create_hook(db, webhook)
    return webhook