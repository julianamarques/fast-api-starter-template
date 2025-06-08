from datetime import datetime, timedelta

import jwt

from app.core.app_config import settings


def encode(username: str) -> dict:
    expire_date = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": username,
        "exp": expire_date,
    }

    return {
        "access_token": jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.TOKEN_ALGORITHM
        ),
        "expires_in": expire_date.isoformat()
    }


def decode(access_token: str) -> dict:
    return jwt.decode(
        jwt=access_token,
        key=settings.SECRET_KEY,
        algorithms=[settings.TOKEN_ALGORITHM]
    )
