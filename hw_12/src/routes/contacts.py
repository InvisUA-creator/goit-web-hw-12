from typing import Optional, List
from fastapi import APIRouter, FastAPI, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.dbase.dbase import get_db
from src.dbase.models import User
from src.repo import contacts as repo_contact

from src.schemas.contact import ContactSchema, ContactResponce
from src.services.auth import auth_service

router = APIRouter(prefix="/contact", tags=["contact"])


@router.get("/search", responce_model=list[ContactResponce])
async def search_contacts(
    first_name: Optional[str] = Query(None, min_length=1),
    last_name: Optional[str] = Query(None, min_length=1),
    email: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    contacts = await repo_contact.search_contacts(
        db=db, first_name=first_name, last_name=last_name, email=email
    )
    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found"
        )
    return contacts


@router.get("/upcoming_birthdays", response_model=List[dict])
async def upcoming_birthdays(
    days: int = 7,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):

    contacts = await repo_contact.get_upcoming_birthdays(db, user, days)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponce)
async def get_contact(
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    contact = await repo_contact.get_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.get("/", response_model=list[ContactResponce])
async def get_contacts(
    limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    contacts = await repo_contact.get_contacts(limit, offset, db, user)
    return contacts


@router.post("/", response_model=ContactResponce, status_code=status.HTTP_201_CREATED)
async def create_contact(
    body: ContactSchema,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    contact = await repo_contact.create_contact(body, db, user)
    return contact


@router.put("/{contact_id}")
async def update_contact(
    body: ContactSchema,
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    contact = await repo_contact.update_contact(contact_id, body, db, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user)
):
    contact = await repo_contact.delete_contact(contact_id, db, user)
    return contact
