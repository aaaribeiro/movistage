# built-in libraries
from datetime import datetime

# imports from third-party libraries
from typing import List
from fastapi import Depends, APIRouter, HTTPException, Request, status
from sqlalchemy.orm import Session

# required imports from package models
from models.crud import CRUDTicket
# from models.models import WebhookLogs 
from serializers import schemas

# required imports from packageutils 
from utils import movidesk
from utils import payload
from utils.handlers import get_db

# authentication
from auth import auth

# constants
# it will be used in swagger documentation to organize the endpoints
TAGS = ["listeners",]

router = APIRouter()


@router.post(
    "/listener-ticket",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    response_model=schemas.WebhookLog,
    # dependencies=[Depends(auth.api_token)],
)
async def crud_ticket(request: Request, db: Session=Depends(get_db)):

    response = await request.json()
    ticket = movidesk.get_ticket(response["Id"])
    pload = payload.ticket(ticket)
    crud = CRUDTicket()
    dbticket = crud.read_ticket_by_id(db, pload.ticket_id)
    if not dbticket:
        crud.create_ticket(db, pload)
    else:
        crud.update_ticket(db, pload, dbticket)

# @router.post(
#     "/hook/update/ticket",
#     tags=TAGS,
#     status_code=status.HTTP_201_CREATED, 
#     # response_model=schemas.WebhookLog,
#     dependencies=[Depends(auth.api_token)],
# )
# async def create_hook_for_update_ticket(request: Request, token: str = None,
#                     db: Session=Depends(get_db)):
#     """
#     Write something
#     """
#     response = await request.json()
#     webhook = schemas.WebhookLog(
#         ticket_id = response["Id"],
#         change = "UPDATE TICKET",
#         trigger_date = datetime.now(),
#         was_read = False
#     )
#     _crud.create_hook(db, webhook)
#     # webhook = crud.create_hook(db, webhook)
#     # return webhook



# @router.post(
#     "/hook/new/appointment",
#     tags=TAGS,
#     status_code=status.HTTP_201_CREATED, 
#     # response_model=schemas.WebhookLog,
#     dependencies=[Depends(auth.api_token)],
# )
# async def create_hook_for_appointment(request: Request, token: str = None,
#                     db: Session=Depends(get_db)):
#     """
#     Write something
#     """
#     response = await request.json()
#     webhook = schemas.WebhookLog(
#         ticket_id = response["Id"],
#         change = "NEW APPOINTMENT",
#         trigger_date = datetime.now(),
#         was_read = False
#     )
#     _crud.create_hook(db, webhook)
#     # webhook = crud.create_hook(db, webhook)
#     # return webhook


# @router.get(
#     "/hooks",
#     tags=TAGS,
#     response_model=List[schemas.WebhookLog],
#     dependencies=[Depends(auth.api_token)],
# )
# async def read_hooks(token: str = None, read: bool = None,
#                         skip: int = 0, limit: int = 1000,
#                         db:Session=Depends(get_db)):
#     """
#     Returns a hook list by ticket id
#     """
#     hooks = _crud.get_hook_logs(db, read=read, skip=skip, limit=limit)
#     if not hooks:
#         raise HTTPException(status_code=400, detail="All hooks were read")
#     return hooks


# @router.get(
#     "/hook/{ticket_id}",
#     tags=TAGS,
#     response_model=List[schemas.WebhookLog],
#     dependencies=[Depends(auth.api_token)],
# )
# async def read_hooks_by_ticket_id(ticket_id: int, token: str = None,
#                         skip: int = 0, limit: int = 100,
#                         db:Session=Depends(get_db)):
#     """
#     Returns a hook list by ticket id
#     """
#     hooks = _crud.get_hooks_by_ticket_id(db, ticket_id=ticket_id, skip=skip,
#         limit=limit)
#     return hooks


# @router.patch(
#     "/hook/{hook_id}",
#     tags=TAGS,
#     status_code=status.HTTP_204_NO_CONTENT, 
#     # response_model=schemas.WebhookLog,
#     dependencies=[Depends(auth.api_token)],
# )
# async def update_hook(hook_id: str, hook: schemas.WebhookLog, token:str=None,
#                         db: Session = Depends(get_db)):
#     """
#     Partial update for webhook logs
#     """
#     stored_hook = _crud.get_hook_by_id(db, id=hook_id)
#     if not stored_hook:
#         raise HTTPException(status_code=404, detail="Hook Not Found")
    
#     _crud.partial_update_hook(db, id=hook_id, hook=hook,)
