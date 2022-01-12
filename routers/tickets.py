# imports from third-party libraries
from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

# required imports from package models 
from models import crud 
from serializers import schemas
from auth import auth

# required imports from package utils 
from utils.handlers import get_db

# constants
# it will be used in swagger documentation to organize the endpoints
TAGS = ["Tickets",]

router = APIRouter()

@router.get(
    "/tickets",
    tags=TAGS,
    response_model=List[schemas.Ticket],
    dependencies=[Depends(auth.api_token)]
)
async def read_tickets(skip: int = 0, limit: int = 100,
                db:Session=Depends(get_db)):
    """
    Returns a tickets list from movidesk stage
    """

    # auth.authorization(db, token)    
    tickets = crud.get_tickets(db, skip=skip, limit=limit)
    return tickets


@router.get(
    "/ticket/{ticket_id}",
    tags=TAGS,
    response_model=schemas.Ticket
)
async def read_ticket(ticket_id, token: str=None, db: Session=Depends(get_db)):
    """
    Returns a ticket object from movidesk stage
    """
    auth.authorization(db, token)
    ticket = crud.get_ticket_by_id(db, id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=400, detail="Ticket does not exists")
    return ticket


@router.post(
    "/ticket",
    tags=TAGS, 
    response_model=schemas.Ticket
)
async def create_ticket(ticket: schemas.Ticket, token: str=None,
                    db: Session=Depends(get_db)):
    """
    Create a ticket on movidesk stage
    """

    auth.authorization(db, token)
    db_ticket = crud.get_ticket_by_id(db, id=ticket.ticket_id)
    if db_ticket:
        raise HTTPException(status_code=400, detail="Ticket already registered")
    return crud.create_ticket(db=db, ticket=ticket)


@router.patch(
    "/ticket/{ticket_id}",
    tags=TAGS,
    response_model=schemas.Ticket
)
async def update_ticket(ticket_id: str, ticket: schemas.Ticket, token:str=None,
                        db: Session = Depends(get_db)):
    """
    Partial update from a ticket object
    """

    auth.authorization(db, token)
    stored_ticket = crud.get_ticket_by_id(db, id=ticket_id)
    if not stored_ticket:
        raise HTTPException(status_code=404, detail="Ticket Not Found")
    
    return crud.partial_update_ticket(
        db,
        id=ticket_id,
        ticket=ticket
    )


@router.delete(
    "/ticket/{ticket_id}",
    tags=TAGS,
    response_model=schemas.Ticket
)
async def delete_ticket(ticket_id = str, token:str=None, db: Session = Depends(get_db)):
    """
    Option to delete a ticket object from movidesk stage
    """
    
    auth.authorization(db, token)
    stored_ticket = crud.get_ticket_by_id(db, id=ticket_id)
    if not stored_ticket:
        raise HTTPException(status_code=404, detail="Ticket Not Found")
    
    deleted_ticket = crud.delete_ticket(db, id=ticket_id)
    
    if not deleted_ticket:
        raise HTTPException(
            status_code=400,
            detail="Could Not Possible Delete Ticket"
        )
    
    return stored_ticket