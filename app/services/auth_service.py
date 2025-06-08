from datetime import datetime

import jwt
from fastapi import HTTPException, status

from app.core.database_config import Session
from app.enums import ApiMessageEnum
from app.models.user import User
from app.schemas.auth_schema import AuthUserResponseSchema, LoginRequestSchema
from app.schemas.user_schema import UserResponseSchema
from app.services.user_service import UserService
from app.utils import token_utils, encrypt_password_utils


class AuthService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.user_service = UserService(db_session)


    def login(self, schema: LoginRequestSchema) -> AuthUserResponseSchema:
        user: User = self.user_service.find_user_by_email(schema.email)

        if not user or not encrypt_password_utils.verify_password(schema.password, user.password):
            self._raise_unauthorized(ApiMessageEnum.INVALID_USER_PASSWORD.value)

        token_data = token_utils.encode(username=schema.email)

        return AuthUserResponseSchema(
            access_token=token_data["access_token"],
            expires_in=token_data["expires_in"],
            user_data=UserResponseSchema.from_model(user)
        )


    def get_auth_user(self, access_token: str) -> AuthUserResponseSchema | None:
        try:
            token_data = token_utils.decode(access_token)
            user: User = self.user_service.find_user_by_email(token_data["sub"])

            if not user:
                self._raise_unauthorized(ApiMessageEnum.INVALID_TOKEN.value)

            return AuthUserResponseSchema(
                access_token=access_token,
                expires_in=datetime.fromtimestamp(token_data["exp"]).isoformat() + "Z",
                user_data=UserResponseSchema.from_model(user)
            )
        except jwt.ExpiredSignatureError:
            self._raise_unauthorized(ApiMessageEnum.EXPIRED_TOKEN.value)

            return None
        except jwt.InvalidTokenError:
            self._raise_unauthorized(ApiMessageEnum.INVALID_TOKEN.value)

            return None


    def _raise_unauthorized(self, detail: str) -> None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )
