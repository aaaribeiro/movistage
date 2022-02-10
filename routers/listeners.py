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
    # crud objects
    crudTicket = CRUDTicket()
    crudOrg = CRUDOrganization()
    # crudAppointment = CRUDTimeAppointment()
    
    # ticket/payload movidesk
    ticket = movidesk.get_ticket(resp["Id"])
    ploadTicket = payload.ticket(ticket)
   # organization/paylod movidesk
    organization = movidesk.get_organization(ploadTicket.organization_id)
    ploadOrg = payload.organization(organization)
    
    # if resp['Actions'][0]["CreatedBy"]["ProfileType"] in (1, 3):
    #     appointmentId = int(f"{resp['Id']}{resp['Actions'][0]['Id']}")
    #     dbAppointment = crudAppointment.readTimeAppointmentById(db,
    #                                                             appointmentId)
    #     if not dbAppointment:
    #         print("this function must create a new appointment in db")
    
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



@router.post(
    "/appointments/createupdate",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def create_update_appointment(request: Request, response: Response,
                                db: Session=Depends(get_db)):

    resp = await request.json()
    ticketID = resp["Id"]
    actionID = resp["Actions"][0]["Id"]

    # crud objects
    crudAppointment = CRUDTimeAppointment()
    
    # ticket/payload movidesk
    ticket = movidesk.get_ticket(resp["Id"])
    
    if resp['Actions'][0]["CreatedBy"]["ProfileType"] in (1, 3):
        appointmentId = int(f"{ticketID}"+f"{actionID:03}")
        dbAppointment = crudAppointment.readTimeAppointmentById(db,
                                                                appointmentId)
        if not dbAppointment:
            ploadTicket = payload.appointments(ticket, actionID)
            crudAppointment.createTimeAppointment(db, ploadTicket)
            response.status_code = status.HTTP_201_CREATED