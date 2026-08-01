from datetime import datetime, timedelta, timezone

import jwt

from app.core.app_config import settings


def encode(subject: str) -> dict:
    now = datetime.now(timezone.utc)
    expire_date = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": subject,
        "exp": expire_date,
    }

    return {
        "access_token": jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.TOKEN_ALGORITHM
        ),
        "expires_in": seconds_until(expire_date, now=now)
    }


def decode(access_token: str) -> dict:
    return jwt.decode(
        jwt=access_token,
        key=settings.SECRET_KEY,
        algorithms=[settings.TOKEN_ALGORITHM]
    )


def seconds_until(expire_at: datetime, now: datetime | None = None) -> int:
    now = now if now is not None else datetime.now(timezone.utc)

    return max(0, int((expire_at - now).total_seconds()))
