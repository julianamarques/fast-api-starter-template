import uuid
from datetime import datetime, timezone

import jwt

from app.core.database_config import Session
from app.enums import ApiMessageEnum
from app.models.user import User
from app.schemas.auth_schema import AuthUserResponseSchema, LoginRequestSchema
from app.schemas.user_schema import UserResponseSchema
from app.services.user_service import UserService
from app.utils import token_utils, encrypt_password_utils, exceptions_utils


_DUMMY_PASSWORD_HASH = encrypt_password_utils.hash_password("dummy-password")


class AuthService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.user_service = UserService(db_session)

    def login(self, schema: LoginRequestSchema) -> AuthUserResponseSchema:
        email: str = schema.email.lower().strip()
        user: User | None = self.user_service.find_user_by_email(email)
        hashed_password: str = user.password if user else _DUMMY_PASSWORD_HASH
        is_password_valid: bool = encrypt_password_utils.verify_password(schema.password, hashed_password)

        if not user or not is_password_valid or not user.active:
            exceptions_utils.raise_unauthorized(ApiMessageEnum.INVALID_USER_PASSWORD.value)

        token_data = token_utils.encode(subject=str(user.id))

        return AuthUserResponseSchema(
            access_token=token_data["access_token"],
            expires_in=token_data["expires_in"],
            user_data=UserResponseSchema.from_model(user)
        )

    def get_auth_user(
            self,
            access_token: str
    ) -> AuthUserResponseSchema:
        try:
            token_data = token_utils.decode(access_token)

            try:
                user_id = uuid.UUID(token_data["sub"])
            except (ValueError, TypeError):
                exceptions_utils.raise_unauthorized(ApiMessageEnum.INVALID_TOKEN.value)

            user: User | None = self.user_service.find_user_by_id(user_id)

            if not user:
                exceptions_utils.raise_unauthorized(ApiMessageEnum.INVALID_TOKEN.value)

            if not user.active:
                exceptions_utils.raise_unauthorized(ApiMessageEnum.INACTIVE_USER.value)

            expire_at = datetime.fromtimestamp(token_data["exp"], tz=timezone.utc)

            return AuthUserResponseSchema(
                access_token=access_token,
                expires_in=token_utils.seconds_until(expire_at),
                user_data=UserResponseSchema.from_model(user)
            )
        except jwt.ExpiredSignatureError:
            exceptions_utils.raise_unauthorized(ApiMessageEnum.EXPIRED_TOKEN.value)
        except jwt.InvalidTokenError:
            exceptions_utils.raise_unauthorized(ApiMessageEnum.INVALID_TOKEN.value)
