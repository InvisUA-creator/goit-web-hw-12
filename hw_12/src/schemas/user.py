from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponce(BaseModel):
    id: int = 1
    username: str
    email: EmailStr
    avatar: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field("bearer", constant=True)
