# built-in libraries

# imports from third-party libraries
from fastapi import HTTPException, Depends, APIRouter, Request, Response, status
from sqlalchemy.orm import Session

# required imports from package models
<<<<<<< HEAD
from models.crud import CRUDOrganization, CRUDTicket, CRUDTimeAppointment, CRUDAgent
=======
from models.crud import CRUDAgent, CRUDOrganization, CRUDTicket, CRUDTimeAppointment
>>>>>>> dde6cd4f59602db4f8c421fc2a41567aa2450c87
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
    crudAgent = CRUDAgent()
    crudOrg = CRUDOrganization()
    
    # ticket/payload movidesk
    ticket = movidesk.get_ticket(resp["Id"])
    ploadTicket, ploadOrg, ploadAgent = payload.ticket(ticket)

    dbOrg = crudOrg.readOrganizationById(db, ploadOrg.organization_id)
    if not dbOrg:
        crudOrg.createOrganization(db, ploadOrg)

    dbAgent = crudAgent.readAgentById(db, ploadAgent.agent_id)
    if not dbAgent:
        crudAgent.createAgent(db, ploadAgent)

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
    crudAgent = CRUDAgent()
    crudAppointment = CRUDTimeAppointment()
    
    # get data from movidesk api
    ticket = movidesk.get_ticket(resp["Id"])
    ploadTicket, ploadOrg, ploadAgent = payload.ticket(ticket)
        
    dbOrganization = crudOrg.readOrganizationById(db, ploadOrg.organization_id)
    if not dbOrganization:
        crudOrg.createOrganization(db, ploadOrg)
    
    dbAgent = crudAgent.readAgentById(db, ploadAgent.agent_id)
    if not dbAgent:
        crudAgent.createAgent(db, ploadAgent)
    
    dbTicket = crudTicket.readTicketById(db, ticketID)
    if not dbTicket:        
        crudTicket.createTicket(db, ploadTicket)

    ploadAppointment = payload.appointment(ticket, actionID)
    if resp['Actions'][0]["CreatedBy"]["ProfileType"] in (1, 3):
        appointmentID = int(f"{ticketID}"+f"{actionID:03}")
        dbAppointment = crudAppointment.readTimeAppointmentById(db,
                                                                appointmentID)
        if not dbAppointment:
<<<<<<< HEAD
            crudAppointment.createTimeAppointment(db, ploadAppointment)
            response.status_code = status.HTTP_201_CREATED
        else:
            crudAppointment.updateTimeAppointment(db, ploadAppointment,
                                                    dbAppointment)
=======
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
>>>>>>> dde6cd4f59602db4f8c421fc2a41567aa2450c87
