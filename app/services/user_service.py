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
        _validate_password(schema.password, schema.confirm_password)

        email: str = schema.email.lower().strip()

        if self.find_user_by_email(email):
            exceptions_utils.raise_bad_request(ApiMessageEnum.USER_EMAIL_EXISTS.value)

        user: User = User(
            name=schema.name.strip(),
            email=email,
            password=encrypt_password_utils.hash_password(schema.password),
        )

        self.db_session.add(user)

        try:
            self.db_session.flush()
        except IntegrityError:
            exceptions_utils.raise_bad_request(ApiMessageEnum.USER_EMAIL_EXISTS.value)

        return UserResponseSchema.from_model(user)

    def find_user_by_email(self, email: str) -> User | None:
        return self.db_session.query(User).filter_by(email=email).first()
