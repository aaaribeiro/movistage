# imports from third-party libraries
from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

# required imports from package models 
from models.crud import CRUDOrganization 
from serializers import schemas

# required imports from package utils
# it will be used in swagger documentation to organize the endpoints
from utils.handlers import get_db

# authentication
from auth import auth

# constants
TAGS = ["organizations",]

router = APIRouter()

@router.get(
    "/organizations",
    tags=TAGS,
    response_model=List[schemas.Organization],
    # dependencies=[Depends(auth.api_token)],
)
async def read_organizations(skip: int = 0, limit: int = 100,
                            db: Session = Depends(get_db)):
    crud = CRUDOrganization()
    dbOrganizations = crud.readOrganizations(db, skip, limit)
    return dbOrganizations



@router.post(
    "/organizations",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    # dependencies=[Depends(auth.api_token)],
)
async def create_organization(payload: schemas.Organization,
                            db: Session=Depends(get_db)):
    crud = CRUDOrganization()
    dbOrganization = crud.readOrganizationById(db, payload.organization_id)
    if dbOrganization:
        raise HTTPException(status_code=400, detail="organization already exits")
    return crud.createOrganization(db, payload)



@router.put(
    "/organizations/{id}",
    tags=TAGS,
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(auth.api_token)],
)
async def update_organization(id: int, payload: schemas.Organization, 
                        db: Session = Depends(get_db)):
    crud = CRUDOrganization()
    dbOrganization = crud.readOrganizationById(db, id)
    if not dbOrganization:
        raise HTTPException(status_code=404, detail="organization not found")
    crud.updateOrganization(db, payload, dbOrganization) 



@router.delete(
    "/organizations/{id}",
    tags=TAGS,
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(auth.api_token)],
)
async def delete_organization(id: str, db: Session = Depends(get_db)):
    crud = CRUDOrganization()
    dbOrganization = crud.readOrganizationById(db, id)
    if not dbOrganization:
        raise HTTPException(status_code=404, detail="organization not found")
    crud.deleteOrganization(db, id)
