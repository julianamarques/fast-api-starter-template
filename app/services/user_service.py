import uuid

from sqlalchemy.exc import IntegrityError

from app.core.database_config import Session
from app.enums import ApiMessageEnum
from app.models import User
from app.schemas.auth_schema import UserCreateRequestSchema
from app.schemas.user_schema import UserResponseSchema

from app.utils import encrypt_password_utils, exceptions_utils


def _validate_password(password: str, confirm_password: str) -> None:
    if password != confirm_password:
        exceptions_utils.raise_bad_request(ApiMessageEnum.USER_PASSWORDS_DO_NOT_MATCH.value)


class UserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, schema: UserCreateRequestSchema) -> UserResponseSchema:
        try:
            _validate_password(schema.password, schema.confirm_password)

            encrypted_password: str = encrypt_password_utils.hash_password(schema.password)
            user: User = User(
                name=schema.name.strip(),
                email=schema.email.lower().strip(),
                password=encrypted_password,
            )

            self.db_session.add(user)
            self.db_session.flush()

            return UserResponseSchema.from_model(user)
        except IntegrityError as error:
            error_message = str(error).lower()
            is_email_exists_error: bool = "unique constraint" in error_message and "email" in error_message

            if is_email_exists_error:
                exceptions_utils.raise_bad_request(ApiMessageEnum.USER_EMAIL_EXISTS.value)

            raise

    def find_user_by_id(self, user_id: str) -> User:
        user: User = self.db_session.query(User).filter_by(id=uuid.UUID(user_id)).first()

        if not user:
            exceptions_utils.raise_not_found(ApiMessageEnum.USER_NOT_FOUND.value)

        return user

    def find_user_by_email(self, email: str) -> User | None:
        return self.db_session.query(User).filter_by(email=email).first()
