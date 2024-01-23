from logging import getLogger
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import ShowUser
from src.db.session import get_db
from src.service.db import _delete_all_users
from src.service.db import _generate_fake_users
from src.service.db import _get_all_users
from src.settings import settings
from src.tasks.tasks import send_email_report_dashboard

logger = getLogger(__name__)
db_router = APIRouter()


@db_router.get("/", response_model=List[ShowUser])
@cache(expire=settings.REDIS_EXPIRE_SEC)
async def get_all_users(db: AsyncSession = Depends(get_db)) -> List[ShowUser]:
    """Get ALL users"""
    users = [raw[0] for raw in await _get_all_users(db)]
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found.")
    return users


@db_router.post("/", response_model=List[ShowUser])
async def generate_fake_users(db: AsyncSession = Depends(get_db)) -> List[ShowUser]:
    """Generate fake users"""
    res = await _generate_fake_users(settings.QTY_FAKE_USERS, db)
    return res


@db_router.post("/delete_all", response_model=dict[str, str])
async def delete_all_users(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Delete ALL users"""
    res = await _delete_all_users(db)
    return {"message": f"{res} users deleted"}


@db_router.get("/report", response_model=dict[str, str])
async def report_users(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Sent report to GMAIL"""
    users = [raw[0].__dict__ for raw in await _get_all_users(db)]
    send_email_report_dashboard(value=users)
    return {
        "status": 200,
        "data": f"{len(users)} users sent",
        "details": "GMAIL report sent",
    }
