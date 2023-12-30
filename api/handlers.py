from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.dals import UserDAL
from db.session import async_session, get_db
from api.models import ShowUser, UserCreate

user_router = APIRouter()


async def _create_new_user(body: UserCreate, db: AsyncSession) -> ShowUser:
    """Create a new user, flush into DB and return it as tuned ShowUser"""
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
            )
            return ShowUser(
                name=user.name,
                surname=user.surname,
                email=user.email,
            )


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    """Router for creating a new user, flush into DB and return it as tuned ShowUser"""
    return await _create_new_user(body, db)
