from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from app.core.app_config import settings
from app.schemas import UserCreateSchema, LoginSchema, CurrentUserSchema, AuthSchema
from app.core.database_config import Session
from app.models import User

security = HTTPBearer()
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return crypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt_context.verify(plain_password, hashed_password)


def decode_token(access_token: str) -> dict:
    return jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])


def encode_token(username: str) -> dict:
    expire_date = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": username,
        "exp": expire_date,
    }

    return {
        "access_token": jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM),
        "expires_in": expire_date.isoformat()
    }

class AuthService:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def create(self, schema: UserCreateSchema) -> None:
        try:
            user = User(
                name=schema.name,
                email=schema.email,
                password=hash_password(schema.password),
            )

            self.db_session.add(user)

        except IntegrityError:
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )


    def login(self, schema: LoginSchema) -> AuthSchema:
        user: User = self._find_by_email(schema.email)

        if not user or not verify_password(schema.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User or password invalid",
            )

        token_data = encode_token(username=schema.email)

        return AuthSchema(
            access_token=token_data["access_token"],
            expires_in=token_data["expires_in"]
        )


    def get_current_user(self, access_token: str) -> CurrentUserSchema:
        try:
            token_data = decode_token(access_token)
            user: User = self._find_by_email(token_data["sub"])

            if not user:
                self._raise_unauthorized("Invalid access token")
            return CurrentUserSchema(
                access_token=access_token,
                name=user.name,
                email=user.email
            )
        except jwt.ExpiredSignatureError:
            self._raise_unauthorized("Expired token")
        except jwt.InvalidTokenError:
            self._raise_unauthorized("Invalid access token")


    def _find_by_email(self, email: str) -> User:
        return self.db_session.query(User).filter_by(email=email).first()


    def _raise_unauthorized(self, detail: str) -> None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )
