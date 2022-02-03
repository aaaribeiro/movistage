# built-in libraries

# imports from third-party libraries
from fastapi import Depends, APIRouter, Request, status
from sqlalchemy.orm import Session

# required imports from package models
from models.crud import CRUDTicket, CRUDTimeAppointment
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
    # response_model=schemas.WebhookLog,
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



@router.post(
    "/delete-ticket",
    tags=TAGS,
    status_code=status.HTTP_204_NO_CONTENT, 
    # response_model=schemas.WebhookLog,
    # dependencies=[Depends(auth.api_token)],
)
async def delete_ticket(request: Request, db: Session=Depends(get_db)):

    response = await request.json()
    ticket_id = response["Id"]
    crud = CRUDTicket()
    crud.delete_ticket(db, ticket_id)



@router.post(
    "/listener-appointment",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    # response_model=schemas.WebhookLog,
    # dependencies=[Depends(auth.api_token)],
)
async def crud_appointment(request: Request, db: Session=Depends(get_db)):

    response = await request.json()
    ticket = movidesk.get_ticket(response["Id"])
    pload = payload.appointments(ticket)
    crud = CRUDTimeAppointment()
    for appointment in pload:
        dbappointment = crud.read_time_appointment_by_id(db,
                                                    appointment.time_appointment_id)
        if not dbappointment:
            crud.create_time_appointment(db, appointment)
