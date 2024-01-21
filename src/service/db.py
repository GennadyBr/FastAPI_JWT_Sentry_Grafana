from typing import List
from typing import Union

from src.db.dals import UserDAL
from src.db.models import User


async def _get_all_users(session) -> Union[List[User], None]:
    """Get a user with user_id and return user_id"""
    async with session.begin():
        users_dal = UserDAL(session)
        users = await users_dal.get_all_user()
        if users is not None:
            return users
