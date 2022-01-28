# imports from third-party libraries
import time
from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

# required imports from models package
# from models import _crud
from models.crud import CRUDAgent, CRUDTicket, CRUDTimeAppointment 
from serializers import schemas

# required imports from utils package
from utils.handlers import get_db

# authentication
from auth import auth

# constants
# it will be used in swagger documentation to organize the endpoints
TAGS = ["time appointments",]

router = APIRouter()


@router.get(
    "/timeappointments",
    tags=TAGS,
    response_model=List[schemas.TimeAppointmentGroupedByAgent],
    dependencies=[Depends(auth.api_token)],
)
def read_time_appointments_by_agent(skip: int = 0, limit: int = 100,
                        db: Session = Depends(get_db)):

    crud = CRUDAgent()
    return crud.read_agents(db, skip=skip, limit=limit)


@router.post(
    "/timeappointments",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    dependencies=[Depends(auth.api_token)],
)
async def create_time_appointment(payload: schemas.TimeAppointment,
                                db: Session=Depends(get_db)):
    """
    Write something
    """

    crud = CRUDTimeAppointment()
    # raise an error HTTP_400 if time already registered
    time = crud.read_time_appointment_by_id(payload.time_appointment_id)
    if time:
        raise HTTPException(status_code=400, detail="time already registered")
        
    crud.create_time_appointment(db, payload)


@router.put(
    "/timeappointments/{timeappointment_id}",
    tags=TAGS,
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth.api_token)],
)
async def update_time_appointment(timeappointment_id: int, 
                                payload: schemas.TimeAppointment, 
                                db: Session = Depends(get_db)):

    crud = CRUDTimeAppointment()
    # read ticket from database and create a new one if not exists
    times = crud.read_time_appointment_by_id(db, timeappointment_id)
    if times:
        crud.update_time_appointment(db, payload, times)  
    else:
        crud.create_time_appointment(db, payload)