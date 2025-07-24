import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.core.database_config import Session
from app.enums import ApiMessageEnum
from app.models import User
from app.schemas.auth_schema import UserCreateRequestSchema
from app.schemas.user_schema import UserResponseSchema

from app.utils import encrypt_password_utils


class UserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(
            self,
            schema: UserCreateRequestSchema
    ) -> UserResponseSchema | None:
        try:
            self._validate_password(schema.password, schema.confirm_password)

            encrypted_password: str = encrypt_password_utils.hash_password(schema.password)
            user: User = User(
                name=schema.name.strip(),
                email=schema.email.lower().strip(),
                password=encrypted_password,
            )

            self.db_session.add(user)
            self.db_session.flush()

            return UserResponseSchema.from_model(user)
        except IntegrityError as e:
            error_message = str(e)
            is_email_exists_error: bool = ("unique constraint" in error_message.lower()
                                           and "email" in error_message.lower())

            if is_email_exists_error:
                self._raise_bad_request(
                    ApiMessageEnum.USER_EMAIL_EXISTS.value
                )

                return None

            return None

    def find_user_by_id(self, user_id: str) -> User:
        user: User = self.db_session.query(User).filter_by(id=uuid.UUID(user_id)).first()

        if not user:
            self._raise_not_found()

        return user

    def find_user_by_email(self, email: str) -> User:
        user: User = self.db_session.query(User).filter_by(email=email).first()

        if not user:
            self._raise_not_found()

        return user

    def _validate_password(self, password: str, confirm_password: str) -> None:
        password_is_null: bool = not password and not confirm_password
        invalid_password: bool = not password_is_null and password != confirm_password

        if password_is_null:
            self._raise_bad_request(
                ApiMessageEnum.USER_PASSWORD_MANDATORY.value
            )
        elif invalid_password:
            self._raise_bad_request(
                ApiMessageEnum.USER_PASSWORDS_DO_NOT_MATCH.value
            )

    def _raise_bad_request(self, detail: str) -> HTTPException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )

    def _raise_not_found(self) -> HTTPException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ApiMessageEnum.USER_NOT_FOUND.value,
        )
