# imports from third-party libraries
import time
from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

# required imports from models package
# from models import _crud
from models.crud import CRUDTimeAppointment 
from serializers import schemas

# required imports from utils package
from utils.handlers import get_db

# authentication
from auth import auth

# constants
# it will be used in swagger documentation to organize the endpoints
TAGS = ["appointments",]

router = APIRouter()


@router.get(
    "/appointments",
    tags=TAGS,
    response_model=List[schemas.TimeAppointment],
    # dependencies=[Depends(auth.api_token)],
)
async def read_time_appointments(skip: int = 0, limit: int = 100,
                        db: Session = Depends(get_db)):
    crud = CRUDTimeAppointment()
    return crud.readTimeAppointments(db, skip=skip, limit=limit)



@router.post(
    "/appointments",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    # dependencies=[Depends(auth.api_token)],
)
async def create_time_appointment(payload: schemas.TimeAppointment,
                                db: Session=Depends(get_db)):    
    crud = CRUDTimeAppointment()
    dbAppointment = crud.readTimeAppointmentById(payload.time_appointment_id)
    if dbAppointment:
        raise HTTPException(status_code=400,
                            detail="appointment already registered")
    crud.createTimeAppointment(db, payload)



@router.put(
    "/appointments/{id}",
    tags=TAGS,
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(auth.api_token)],
)
async def update_time_appointment(id: int, payload: schemas.TimeAppointment, 
                                db: Session = Depends(get_db)):
    crud = CRUDTimeAppointment()
    dbAppointment = crud.readTimeAppointmentById(db, id)
    if dbAppointment:
        crud.update(db, payload, dbAppointment)  
    else:
        crud.createTimeAppointment(db, payload)



@router.delete(
    "/appointments/{id}",
    tags=TAGS,
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(auth.api_token)],
)
async def delete_appointments(id: int, db: Session = Depends(get_db)):
    crud = CRUDTimeAppointment()
    dbAppointment = crud.readTimeAppointmentById(db, id)
    if not dbAppointment:
        raise HTTPException(status_code=404, detail="appointment not found")
    crud.deleteTimeAppointment(db, id)
