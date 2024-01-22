from typing import List
from typing import Union

from faker import Faker

from src.api.schemas import ShowUser
from src.api.schemas import UserCreate
from src.db.dals import UserDAL
from src.db.models import User
from src.service.user import _create_new_user


async def _get_all_users(session) -> Union[List[User], None]:
    """Get a user with user_id and return user_id"""
    async with session.begin():
        users_dal = UserDAL(session)
        users = await users_dal.get_all_user()
        if users is not None:
            return users


async def _delete_all_users(session) -> Union[int, None]:
    # Удаляем все записи из таблицы
    async with session.begin():
        res = await session.execute(User.__table__.delete())
        return res.rowcount


async def _generate_fake_users(num, db) -> Union[List[ShowUser], None]:
    fake = Faker()
    res = []
    for _ in range(num):
        user = UserCreate(
            name=fake.first_name(),
            surname=fake.last_name(),
            email=fake.email(),
            password="123",
        )
        res.append(await _create_new_user(user, db))
    return res
