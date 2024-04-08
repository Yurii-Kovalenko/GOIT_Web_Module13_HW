from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Field, EmailStr, PastDate


class ContactModel(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    date_of_birth: PastDate
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None, max_length=20)


class ContactUpdate(BaseModel):
    date_of_birth: PastDate


class ContactResponse(ContactModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=50)
    email: EmailStr = Field(min_length=10, max_length=250)
    password: str = Field(min_length=8, max_length=100)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr


class RequestPassword(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
