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
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def delete_ticket(request: Request, db: Session=Depends(get_db)):
    response = await request.json()
    ticketID = response["Id"]

    crudTicket, crudAppointment = CRUDTicket(), CRUDTimeAppointment()
    dbTicket = crudTicket.readTicketById(db, ticketID)
    if not dbTicket:
        raise HTTPException(status_code=404, detail="ticket not found")
    else:
        crudAppointment.deleteTimeAppointmentsByTicketId(db, ticketID)
        crudTicket.deleteTicket(db, ticketID)



@router.post(
    "/appointments/createupdate",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def create_update_appointment(request: Request, response: Response,
                                db: Session=Depends(get_db)):

    # handle webhook response
    resp = await request.json()
    ticketID = resp["Id"]
    actionID = resp["Actions"][0]["Id"]

    # define crud objects
    crudTicket = CRUDTicket()
    crudOrg = CRUDOrganization()
    crudAppointment = CRUDTimeAppointment()
    
    # get data from movidesk api
    ticket = movidesk.get_ticket(resp["Id"])
    organization = movidesk.get_organization(ticket["clients"][0]["organization"]["id"])
        
    dbOrganization = crudOrg.readOrganizationById(db, ticket["owner"]["id"])
    if not dbOrganization:
        ploadOrg = payload.organization(organization)
        crudOrg.createOrganization(db, ploadOrg)
    
    dbTicket = crudTicket.readTicketById(db, ticketID)
    if not dbTicket:
        ploadTicket = payload.Ticket(ticket)
        crudTicket.createTicket(db, ploadTicket)

    if resp['Actions'][0]["CreatedBy"]["ProfileType"] in (1, 3):
        appointmentID = int(f"{ticketID}"+f"{actionID:03}")
        dbAppointment = crudAppointment.readTimeAppointmentById(db,
                                                                appointmentID)
        if not dbAppointment:
            ploadTicket = payload.appointment(ticket, actionID)
            crudAppointment.createTimeAppointment(db, ploadTicket)
            response.status_code = status.HTTP_201_CREATED


@router.post(
    "/appointments/delete",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def delete_appointments(request: Request, db: Session=Depends(get_db)):
    resp = await request.json()
    ticketID = resp["Id"]
    actionID = resp["Actions"][0]["Id"]
    appointmentID = int(f"{ticketID}"+f"{actionID:03}")

    crudAppointment = CRUDTimeAppointment()
    dbAppointment = crudAppointment.readTimeAppointmentById(db, appointmentID)
    if not dbAppointment:
        raise HTTPException(status_code=404, detail="appointment not found")
    else:
        crudAppointment.deleteTimeAppointment(db, appointmentID)