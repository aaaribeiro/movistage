# built-in libraries

# imports from third-party libraries
from fastapi import HTTPException, Depends, APIRouter, Request, Response, status
from sqlalchemy.orm import Session

# required imports from package models
from models.crud import CRUDOrganization, CRUDTicket, CRUDTimeAppointment
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
    "/tickets/createupdate",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def create_update_ticket(request: Request, response: Response,
                                db: Session=Depends(get_db)):
    resp = await request.json()
    ticket = movidesk.get_ticket(resp["Id"])
    ploadTicket = payload.ticket(ticket)

    organization = movidesk.get_organization(ploadTicket.organization_id)
    ploadOrg = payload.organization(organization)
    
    appointments = [f"{resp['Id']}{x['Id']}" for x in resp["Actions"]]
    print(appointments)

    crudTicket, crudOrg = CRUDTicket(), CRUDOrganization()
    dbOrg = crudOrg.readOrganizationById(db, ploadOrg.organization_id)
    if not dbOrg:
        crudOrg.createOrganization(db, ploadOrg)

    dbticket = crudTicket.readTicketById(db, ploadTicket.ticket_id)
    if not dbticket:
        crudTicket.createTicket(db, ploadTicket)
        response.status_code = status.HTTP_201_CREATED
    else:
        crudTicket.updateTicket(db, ploadTicket, dbticket)



@router.post(
    "/tickets/delete",
    tags=TAGS,
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(auth.api_token)],
)
async def delete_ticket(request: Request, db: Session=Depends(get_db)):
    response = await request.json()
    ticketId = response["Id"]

    crudTicket, crudAppointment = CRUDTicket(), CRUDTimeAppointment()
    dbTicket = crudTicket.readTicketById(db, ticketId)
    if not dbTicket:
        raise HTTPException(status_code=404, detail="ticket not found")
    else:
        crudAppointment.deleteTimeAppointmentsByTicketId(db, ticketId)
        crudTicket.deleteTicket(db, ticketId)


# @router.post(
#     "/createupdate-appointment",
#     tags=TAGS,
#     status_code=status.HTTP_200_OK, 
#     # response_model=schemas.WebhookLog,
#     # dependencies=[Depends(auth.api_token)],
# )
# async def create_update_appointment(request: Request, db: Session=Depends(get_db)):

#     response = await request.json()
#     ticket = movidesk.get_ticket(response["Id"])
#     # pload = payload.ticket(ticket)
#     # crud = CRUDTicket()
#     pload = payload.appointments(ticket)
#     crud = CRUDTimeAppointment()
#     for appointment in pload:
#         dbappointment = crud.read_time_appointment_by_id(db,
#                                                 appointment.time_appointment_id)
#         if not dbappointment:
#             crud.create_time_appointment(db, appointment)
#         else:
#             if appointment.time_appointment != dbappointment.time_appointment:
#                 crud.update_time_appointment(db, appointment, dbappointment)