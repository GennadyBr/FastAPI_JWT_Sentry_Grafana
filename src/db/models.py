import uuid
from enum import Enum

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PortalRole(str, Enum):
    ROLE_PORTAL_USER = "ROLE_PORTAL_USER"
    ROLE_PORTAL_ADMIN = "ROLE_PORTAL_ADMIN"
    ROLE_PORTAL_SUPERADMIN = "ROLE_PORTAL_SUPERADMIN"


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)
    hashed_password = Column(String, nullable=False)
    roles = Column(ARRAY(String), nullable=False)

    @property
    def is_superadmin(self) -> bool:
        """Determines whether the user is an SuperAdmin or Not"""
        return PortalRole.ROLE_PORTAL_SUPERADMIN in self.roles

    @property
    def is_admin(self) -> bool:
        """Determines whether the user is an Admin or Not"""
        return PortalRole.ROLE_PORTAL_ADMIN in self.roles

    def enrich_admin_roles_by_admin_role(self):
        """Enriches the admin roles by an admin role"""
        if not self.is_admin:
            return {*self.roles, PortalRole.ROLE_PORTAL_ADMIN}

    def remove_admin_privileges_from_model(self):
        """Remove the admin privileges from the model"""
        if self.is_admin:
            return {role for role in self.roles if role != PortalRole.ROLE_PORTAL_ADMIN}
