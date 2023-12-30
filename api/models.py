import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator

# we have three class for User model
# User(BaseModel) SQLAlchemy model for User database migration, user_id as alc_UUID, email as str
# ShowUser(TunedModel) Pydentic model for show User to API in json format, user_id as uuid.UUID, email as EmailStr
# UserCreate(BaseModel) Pydentic model for validation name and surname as LETTERRs and email as EmailStr

class TunedModel(BaseModel):
    """Tune model"""

    class Config:
        """Config class tells pydentic to convert even non dict obj to json"""
        orm_mode = True


class ShowUser(TunedModel):
    """API Show user details tuned from dict to json"""
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


LETTER_MACH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class UserCreate(BaseModel):
    """Validate name and surname with LETTER_MACH_PATTERN"""
    name: str
    surname: str
    email: EmailStr

    @validator("name")
    def validate_name(cls, value: str) -> str:
        """Validate name with LETTER_MACH_PATTERN"""
        if not LETTER_MACH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Name must contain only letters")
        return value

    @validator("surname")
    def validate_surname(cls, value: str) -> str:
        """Validate surname with LETTER_MACH_PATTERN"""
        if not LETTER_MACH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Surname must contain only letters")
        return value
