import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID as alc_UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# we have three class for User model
# User(BaseModel) SQLAlchemy model for User database migration, user_id as alc_UUID, email as str
# ShowUser(TunedModel) Pydentic model for show User to API in json format, user_id as uuid.UUID, email as EmailStr
# UserCreate(BaseModel) Pydentic model for validation name and surname as LETTERRs and email as EmailStr

class User(Base):
    """User model BaseModel"""
    __tablename__ = "users"

    user_id: alc_UUID = Column(alc_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: str = Column(String, nullable=False)
    surname: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    is_active: bool = Column(Boolean, nullable=False, default=True)
