# imports from third-party libraries
from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

# required imports from package models 
from models import _crud 
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
    dependencies=[Depends(auth.api_token)],
)
async def read_organizations(token: str = None, skip: int = 0, limit: int = 100,
                            db: Session = Depends(get_db)):
    """
    Returns an organization list from movidesk stage
    """
    organizations = _crud.get_organizations(db, skip=skip, limit=limit)
    return organizations


@router.get(
    "/organization/{client_id}",
    tags=TAGS,
    response_model=schemas.Organization,
    dependencies=[Depends(auth.api_token)],
)
async def read_organization(client_id, token: str = None,
                            db: Session = Depends(get_db)):
    """
    Returns an organization object from movidesk stage
    """
    organization = _crud.get_customer_by_id(db, id=client_id)
    if not organization:
        raise HTTPException(
            status_code=400,
            detail="Organization does not exists"
        )
    return organization


@router.post(
    "/organization",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    # response_model=schemas.Organization,
    dependencies=[Depends(auth.api_token)],
)
async def create_organization(organization: schemas.Organization,
                            token: str = None, db: Session=Depends(get_db)):
    """
    Create an organization in movidesk stage
    """
    customer = _crud.get_customer_by_id(db, id=organization.client_id)
    if customer:
        raise HTTPException(
            status_code=400,
            detail="Organization already registered"
        )
    # return crud.create_organization(db=db, organization=organization)
    _crud.create_organization(db=db, organization=organization)


@router.patch(
    "/organization/{client_id}",
    tags=TAGS,
    status_code=status.HTTP_204_NO_CONTENT, 
    # response_model=schemas.Organization,
    dependencies=[Depends(auth.api_token)],
)
async def update_organization(client_id: str,
                            organization: schemas.Organization,
                            token : str = None, db: Session = Depends(get_db)):
    """
    Partial update from an organization object
    """
    stored_organization = _crud.get_customer_by_id(db, id=client_id)
    if not stored_organization:
        raise HTTPException(status_code=404, detail="Organization Not Found")
    
    _crud.partial_update_organization(
        db,
        id=client_id,
        organization=organization
    )


@router.delete(
    "/organization/{client_id}",
    tags=TAGS,
    response_model=schemas.Organization,
    dependencies=[Depends(auth.api_token)],
)
async def delete_organization(client_id = str, token: str = None,
                                db: Session = Depends(get_db)):
    """
    Option to delete an object organization from movidesk stage
    """
    stored_organization = _crud.get_customer_by_id(db, id=client_id)
    if not stored_organization:
        raise HTTPException(status_code=404, detail="Organization Not Found")
    
    deleted_organization = _crud.delete_organization(db, id=client_id)
    
    if not deleted_organization:
        raise HTTPException(
            status_code=400,
            detail="Could Not Possible Delete Organization"
        )
    
    return stored_organization