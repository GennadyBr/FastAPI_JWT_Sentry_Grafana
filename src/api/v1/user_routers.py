from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import DeleteUserResponse
from src.api.schemas import ShowUser
from src.api.schemas import UpdatedUserResponse
from src.api.schemas import UpdateUserRequest
from src.api.schemas import UserCreate
from src.db.models import User
from src.db.session import get_db
from src.service.auth import get_current_user_from_token
from src.service.user import _create_new_user
from src.service.user import _delete_user
from src.service.user import _get_user_by_id
from src.service.user import _update_user
from src.service.user import check_user_permissions
from src.settings import settings

LOGGER = getLogger(__name__)

user_router = APIRouter()


@user_router.get("/", response_model=ShowUser)
@cache(expire=settings.REDIS_EXPIRE_SEC)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    """Get user by id and return ShowUser object"""
    LOGGER.info(f"def get_user_by_id({user_id=}, {current_user=}):")
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return user


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    LOGGER.info(f"def create_user({body=}):")
    """Creates a new user with UserCreate body and return ShowUser object"""
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        LOGGER.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> DeleteUserResponse:
    """Deletes a user with user_id and return DeleteUserResponse object"""
    LOGGER.info(f"def delete_user({user_id=}, {current_user=}):")
    user_for_deletion = await _get_user_by_id(user_id, db)
    if user_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    if not check_user_permissions(
        target_user=user_for_deletion,
        current_user=current_user,
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
    user_id: UUID,
    body: UpdateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UpdatedUserResponse:
    """Update user by user_id and UpdateUserRequest body and return UpdatedUserResponse object"""
    LOGGER.info(f"def update_user_by_id({user_id=}, {body=}, {current_user=}):")
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    user_for_update = await _get_user_by_id(user_id, db)
    if user_for_update is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    if user_id != current_user.user_id:
        if check_user_permissions(
            target_user=user_for_update, current_user=current_user
        ):
            raise HTTPException(status_code=403, detail="Forbidden.")
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=db, user_id=user_id
        )
    except IntegrityError as err:
        LOGGER.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)
