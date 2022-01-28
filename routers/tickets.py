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
    response_model=List[schemas.TicketNestedCompany],
    dependencies=[Depends(auth.api_token)]
)
async def read_tickets(skip: int = 0, limit: int = 100,
                    db:Session=Depends(get_db)):
    """
    Returns a tickets list from movidesk stage
    """
    crud = CRUDTicket()
    return crud.read_tickets(db, skip=skip, limit=limit)


@router.post(
    "/tickets",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    dependencies=[Depends(auth.api_token)]
)
async def create_ticket(payload: schemas.TicketNestedCompany,
                        db: Session=Depends(get_db)):
    """
    Create a ticket in movidesk stage
    """

    crud = CRUDTicket()
    # read ticket from database and raise an error if ticket exist
    dbticket = crud.read_ticket_by_id(db, payload.ticket_id) 
    if dbticket:
        raise HTTPException(status_code=400, detail="ticket already exists")

    crud.create_ticket(db, payload)


@router.put(
    "/tickets/{ticket_id}",
    tags=TAGS,
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth.api_token)],
)
async def update_ticket(ticket_id: int, payload: schemas.TicketNestedCompany, 
                        db: Session = Depends(get_db), ):

    """
    Delete a ticket in movidesk stage
    """

    crud = CRUDTicket()
    # read ticket from database and create a new one if not exists
    ticket = crud.read_ticket_by_id(db, ticket_id)
    if ticket:
        crud.update_ticket(db, payload)  
    else:
        crud.create_ticket(db, payload, ticket)


@router.delete(
    "/tickets/{ticket_id}",
    tags=TAGS,
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth.api_token)],
)
async def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):

    crud = CRUDTicket()
    dbticket = crud.read_ticket_by_id(db, ticket_id)
    if not dbticket:
        raise HTTPException(status_code=404, detail="ticket not found")
    
    crud.delete_ticket(db, ticket_id)
    

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
        