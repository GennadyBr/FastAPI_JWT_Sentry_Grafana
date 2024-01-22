from logging import getLogger
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import ShowUser
from src.db.session import get_db
from src.service.db import _delete_all_users
from src.service.db import _generate_fake_users
from src.service.db import _get_all_users

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
    res = await _generate_fake_users(QTY_FAKE_USERS, db)
    return res


@db_router.post("/delete_all", response_model=dict[str, str])
async def delete_all_users(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Delete ALL users"""
    res = await _delete_all_users(db)
    return {"message": f"{res} users deleted"}