from typing import Iterator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.app_config import settings
from app.core.database_config import Session
from app.schemas.auth_schema import AuthUserResponseSchema
from app.services.auth_service import AuthService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")


def get_db_session() -> Iterator[Session]:
    with Session() as session:
        yield session


def get_auth_user(
        db_session: Session = Depends(get_db_session),
        token: str = Depends(oauth2_scheme)
) -> AuthUserResponseSchema:
    auth_service = AuthService(db_session=db_session)

    return auth_service.get_auth_user(access_token=token)
