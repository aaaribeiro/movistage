# built-in libraries
from datetime import datetime

# imports from third-party libraries
from typing import List
from fastapi import Depends,APIRouter, HTTPException, Request
from sqlalchemy.orm import Session

# required imports from package models
from models import crud
# from models.models import WebhookLogs 
from serializers import schemas

# required imports from packageutils 
from utils.handlers import get_db

# authentication
from auth import auth

# constants
# it will be used in swagger documentation to organize the endpoints
TAGS = ["Hooks",]

router = APIRouter()

@router.post(
    "/hook/status",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def create_hook_for_status(request: Request, token: str = None,
                    db: Session=Depends(get_db)):

    auth.authorization(db, token) 
    response = await request.json()
    webhook = schemas.WebhookLog(
        ticket_id = response["Id"],
        change = "STATUS",
        trigger_date = datetime.now(),
        was_read = False
    )
    webhook = crud.create_hook(db, webhook)
    return webhook


@router.post(
    "/hook/ticket",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def create_hook_for_ticket(request: Request, token: str = None,
                    db: Session=Depends(get_db)):

    auth.authorization(db, token)
    response = await request.json()
    webhook = schemas.WebhookLog(
        ticket_id = response["Id"],
        change = "TICKET",
        trigger_date = datetime.now(),
        was_read = False
    )
    webhook = crud.create_hook(db, webhook)
    return webhook


@router.post(
    "/hook/appointment",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def create_hook_for_appointment(request: Request, token: str = None,
                    db: Session=Depends(get_db)):

    auth.authorization(db, token) 
    response = await request.json()
    webhook = schemas.WebhookLog(
        ticket_id = response["Id"],
        change = "APPOINTMENT",
        trigger_date = datetime.now(),
        was_read = False
    )
    webhook = crud.create_hook(db, webhook)
    return webhook


@router.post(
    "/hook/service",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def create_hook_for_service(request: Request, token: str = None,
                    db: Session=Depends(get_db)):

    auth.authorization(db, token) 
    response = await request.json()
    webhook = schemas.WebhookLog(
        ticket_id = response["Id"],
        change = "SERVICE",
        trigger_date = datetime.now(),
        was_read = False
    )
    webhook = crud.create_hook(db, webhook)
    return webhook


@router.post(
    "/hook/urgency",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def create_hook_for_urgency(request: Request, token: str = None,
                    db: Session=Depends(get_db)):

    auth.authorization(db, token) 
    response = await request.json()
    webhook = schemas.WebhookLog(
        ticket_id = response["Id"],
        change = "URGENCY",
        trigger_date = datetime.now(),
        was_read = False
    )
    webhook = crud.create_hook(db, webhook)
    return webhook


@router.post(
    "/hook/category",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def create_hook_for_category(request: Request, token: str = None,
                    db: Session=Depends(get_db)):

    auth.authorization(db, token) 
    response = await request.json()
    webhook = schemas.WebhookLog(
        ticket_id = response["Id"],
        change = "CATEGORY",
        trigger_date = datetime.now(),
        was_read = False
    )
    webhook = crud.create_hook(db, webhook)
    return webhook


@router.post(
    "/hook/agent",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def create_hook_for_agent(request: Request, token: str = None,
                    db: Session=Depends(get_db)):

    auth.authorization(db, token) 
    response = await request.json()
    webhook = schemas.WebhookLog(
        ticket_id = response["Id"],
        change = "AGENT",
        trigger_date = datetime.now(),
        was_read = False
    )
    webhook = crud.create_hook(db, webhook)
    return webhook


@router.post(
    "/hook/subject",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def create_hook_for_subject(request: Request, token: str = None,
                    db: Session=Depends(get_db)):

    auth.authorization(db, token) 
    response = await request.json()
    webhook = schemas.WebhookLog(
        ticket_id = response["Id"],
        change = "SUBJECT",
        trigger_date = datetime.now(),
        was_read = False
    )
    webhook = crud.create_hook(db, webhook)
    return webhook


@router.get(
    "/hooks",
    tags=TAGS,
    response_model=List[schemas.WebhookLog]
)
async def read_hooks(token: str = None, read: bool = None,
                        skip: int = 0, limit: int = 100,
                        db:Session=Depends(get_db)):

    """
    Returns a hook list by ticket id
    """

    auth.authorization(db, token)    
    hooks = crud.get_hook_logs(db, read=read, skip=skip, limit=limit)
    return hooks


@router.get(
    "/hook/{ticket_id}",
    tags=TAGS,
    response_model=List[schemas.WebhookLog]
)
async def read_hooks_by_ticket_id(ticket_id: int, token: str = None,
                        skip: int = 0, limit: int = 100,
                        db:Session=Depends(get_db)):

    """
    Returns a hook list by ticket id
    """

    auth.authorization(db, token)    
    hooks = crud.get_hooks_by_ticket_id(db, ticket_id=ticket_id, skip=skip,
        limit=limit)
    return hooks


@router.patch(
    "/hook/{hook_id}",
    tags=TAGS,
    response_model=schemas.WebhookLog
)
async def update_hook(hook_id: str, hook: schemas.WebhookLog, token:str=None,
                        db: Session = Depends(get_db)):

    """
    Partial update for webhook logs
    """

    auth.authorization(db, token)
    stored_hook = crud.get_hook_by_id(db, id=hook_id)
    if not stored_hook:
        raise HTTPException(status_code=404, detail="Hook Not Found")
    
    return crud.partial_update_hook(
        db,
        id=hook_id,
        hook=hook,
    )
