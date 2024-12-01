from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from src.schemas.user import UserResponce


class ContactSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: str = EmailStr
    phone: str = Field(pattern=r"^\+?1?\d{9,15}$", description="Номер телефону")
    birthday: date = Field(description="Дата народження")
    data_add: Optional[str] = Field(max_length=250, description="Додатково")


class ContactResponce(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: date
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponce | None
    data_add: str

    class Config:
        from_attributes = True
