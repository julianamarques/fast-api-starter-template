from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.user_schema import UserResponseSchema
from app.utils.encrypt_password_utils import MAX_PASSWORD_BYTES


class UserCreateRequestSchema(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    confirm_password: str = Field(min_length=8, max_length=72)

    @field_validator("password")
    def validate_password_size(cls, value: str) -> str:
        if len(value.encode("utf-8")) > MAX_PASSWORD_BYTES:
            raise ValueError(f"Password must be at most {MAX_PASSWORD_BYTES} bytes")

        return value


class LoginRequestSchema(BaseModel):
    email: str
    password: str


class AuthUserResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_data: UserResponseSchema
