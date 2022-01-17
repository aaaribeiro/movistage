# imports from third-party libraries
from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

# required imports from models package
from models import crud 
from serializers import schemas

# required imports from utils package
from utils.handlers import get_db

# authentication
from auth import auth

# constants
# it will be used in swagger documentation to organize the endpoints
TAGS = ["Time Appointments",]

router = APIRouter()

@router.post(
    "/timeappointment",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    # response_model=schemas.TimeAppointment,
    dependencies=[Depends(auth.api_token)],
)
async def create_time_appointment(time_appointment: schemas.TimeAppointment,
                                token: str = None,
                                db: Session=Depends(get_db)):
    """
    Write something
    """
    # return crud.create_time_appointment(
    #     db=db,
    #     time_appointment=time_appointment
    # )
    
    crud.create_time_appointment(
        db=db,
        time_appointment=time_appointment
    )


@router.get(
    "/timeappointment",
    tags=TAGS,
    response_model=List[schemas.TimeAppointment],
    dependencies=[Depends(auth.api_token)],
)
def read_time_appointments(token: str = None, skip: int = 0, limit: int = 100,
                        db: Session = Depends(get_db)):
    """
    Write something
    """
    time_appointments = crud.get_time_appointments(db, skip=skip, limit=limit)
    return time_appointments
