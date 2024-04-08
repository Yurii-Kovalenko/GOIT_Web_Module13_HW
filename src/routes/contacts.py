from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactUpdate, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from src.database.models import User


router = APIRouter(prefix="/contacts", tags=["contacts"])

contact_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
)


@router.get("/", response_model=List[ContactResponse], description='No more than 5 requests per 30 seconds',
            dependencies=[Depends(RateLimiter(times=5, seconds=30))])
async def read_contacts(
    skip: int = 0,
    limit: int = 20,
    first_name: str = "",
    last_name: str = "",
    email: str = "",
    birthdays: int = 0,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    contacts = await repository_contacts.get_contacts(
        skip, limit, first_name, last_name, email, birthdays, current_user, db
    )
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, description='No more than 5 requests per 30 seconds',
            dependencies=[Depends(RateLimiter(times=5, seconds=30))])
async def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise contact_not_found
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, description='No more than 2 requests per 30 seconds',
            dependencies=[Depends(RateLimiter(times=2, seconds=30))])
async def create_contact(
    body: ContactModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse, description='No more than 5 requests per 30 seconds',
            dependencies=[Depends(RateLimiter(times=5, seconds=30))])
async def update_contact(
    body: ContactModel,
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.update_contact(
        contact_id, body, current_user, db
    )
    if contact is None:
        raise contact_not_found
    return contact


@router.patch("/{contact_id}", response_model=ContactResponse, description='No more than 5 requests per 30 seconds',
            dependencies=[Depends(RateLimiter(times=5, seconds=30))])
async def update_date_of_birth_contact(
    body: ContactUpdate,
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.update_date_of_birth_contact(
        contact_id, body, current_user, db
    )
    if contact is None:
        raise contact_not_found
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse, description='No more than 5 requests per 30 seconds',
            dependencies=[Depends(RateLimiter(times=5, seconds=30))])
async def remove_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise contact_not_found
    return contact
