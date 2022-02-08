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
TAGS = ["Organizations",]

router = APIRouter()

@router.get(
    "/organizations",
    tags=TAGS,
    response_model=List[schemas.Organization],
    # dependencies=[Depends(auth.api_token)],
)
async def read_organizations(skip: int = 0, limit: int = 100,
                            db: Session = Depends(get_db)):
    crud = CRUDOrganization
    dbOrganizations = crud.readOrganizations(db, skip, limit)
    return dbOrganizations



@router.post(
    "/organization",
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



# @router.delete(
#     "/organization/{client_id}",
#     tags=TAGS,
#     response_model=schemas.Organization,
#     dependencies=[Depends(auth.api_token)],
# )
# async def delete_organization(client_id = str, token: str = None,
#                                 db: Session = Depends(get_db)):
#     """
#     Option to delete an object organization from movidesk stage
#     """
#     stored_organization = _crud.get_customer_by_id(db, id=client_id)
#     if not stored_organization:
#         raise HTTPException(status_code=404, detail="Organization Not Found")
    
#     deleted_organization = _crud.delete_organization(db, id=client_id)
    
#     if not deleted_organization:
#         raise HTTPException(
#             status_code=400,
#             detail="Could Not Possible Delete Organization"
#         )
    
#     return stored_organization