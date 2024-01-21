from logging import getLogger
from typing import List

from faker import Faker
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import ShowUser
from src.api.schemas import UserCreate
from src.db.session import get_db
from src.service.db import _get_all_users
from src.service.user import _create_new_user

logger = getLogger(__name__)
db_router = APIRouter()


@db_router.get("/", response_model=List[ShowUser])
async def get_all_users(db: AsyncSession = Depends(get_db)) -> List[ShowUser]:
    """Get ALL users"""
    users = [raw[0] for raw in await _get_all_users(db)]
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found.")
    return users


@db_router.post("/", response_model=List[ShowUser])
async def generate_fake_users(db: AsyncSession = Depends(get_db)) -> List[ShowUser]:
    """Generate fake users"""
    QTY_FAKE_USERS = 10
    fake = Faker()
    res = []
    for _ in range(QTY_FAKE_USERS):
        user = UserCreate(
            name=fake.first_name(),
            surname=fake.last_name(),
            email=fake.email(),
            password="123",
        )
        res.append(await _create_new_user(user, db))
    return res
