# imports from third-party libraries
from typing import List

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

# required imports from package models 
from models.crud import CRUDTicket
from serializers import schemas
from auth import auth

# required imports from package utils 
from utils.handlers import get_db

# constants
# it will be used in swagger documentation to organize the endpoints
TAGS = ["tickets",]

router = APIRouter()

@router.get(
    "/tickets",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.TicketNestedCompany],
    # dependencies=[Depends(auth.api_token)]
)
async def read_tickets(skip: int = 0, limit: int = 100,
                    db:Session=Depends(get_db)):
    crud = CRUDTicket()
    return crud.readTickets(db, skip, limit)


@router.post(
    "/tickets",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    # dependencies=[Depends(auth.api_token)]
)
async def create_ticket(payload: schemas.Ticket, db: Session=Depends(get_db)):
    crud = CRUDTicket()    
    dbTicket = crud.readTicketById(db, payload.ticket_id)  
    if dbTicket:
        raise HTTPException(status_code=400, detail="ticket already exists")
    crud.createTicket(db, payload)


@router.put(
    "/tickets/{id}",
    tags=TAGS,
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(auth.api_token)],
)
async def update_ticket(id: int, payload: schemas.Ticket, 
                        db: Session = Depends(get_db), ):
    crud = CRUDTicket()
    dbTicket = crud.readTicketById(db, id)
    if not dbTicket:
        raise HTTPException(status_code=400, detail="ticket does not exist")
    crud.updateTicket(db, payload, dbTicket)  
    


@router.delete(
    "/tickets/{id}",
    tags=TAGS,
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(auth.api_token)],
)
async def delete_ticket(id: int, db: Session = Depends(get_db)):

    crud = CRUDTicket()
    dbTicket = crud.readTicketById(db, id)
    if not dbTicket:
        raise HTTPException(status_code=404, detail="ticket not found")
    crud.deleteTicket(db, id)
    

# @router.get(
#     "/tickets/{ticket_id}",
#     tags=TAGS,
#     response_model=schemas.TicketNestedCompany,
#     dependencies=[Depends(auth.api_token)]
# )
# async def read_ticket(ticket_id, db: Session=Depends(get_db)):
#     """
#     Returns a ticket object from movidesk stage
#     """
#     ticket = crud.get_ticket_by_id(db, id=ticket_id)
#     if not ticket:
#         raise HTTPException(status_code=400, detail="Ticket does not exists")
#     return ticket

# @router.patch(
#     "/tickets/{ticket_id}",
#     tags=TAGS,
#     status_code=status.HTTP_204_NO_CONTENT, 
#     dependencies=[Depends(auth.api_token)],
# )
# async def update_ticket(ticket_id: str, ticket: schemas.Ticket, token:str=None,
#                         db: Session = Depends(get_db)):
#     """
#     Partial update from a ticket object
#     """
#     stored_ticket = crud.get_ticket_by_id(db, id=ticket_id)
#     if not stored_ticket:
#         raise HTTPException(status_code=404, detail="Ticket Not Found")
    
#     crud.partial_update_ticket(
#         db,
#         id=ticket_id,
#         ticket=ticket
#     )
        