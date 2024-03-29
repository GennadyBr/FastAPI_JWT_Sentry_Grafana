from datetime import datetime
from datetime import timedelta
from typing import Optional

from jose import jwt

from src.settings import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> jwt:
    """Creates an access token for router login_for_access_token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
