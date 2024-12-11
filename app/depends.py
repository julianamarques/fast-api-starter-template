from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.database_config import Session
from app.schemas import CurrentUserSchema
from app.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db_session() -> Session:
    with Session() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


def get_current_user(
        db_session: Session = Depends(get_db_session),
        token: str = Depends(oauth2_scheme)
) -> CurrentUserSchema:
    auth_service = AuthService(db_session=db_session)

    return auth_service.get_current_user(access_token=token)
