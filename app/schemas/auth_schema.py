from pydantic import BaseModel, EmailStr, Field

from app.schemas.user_schema import UserResponseSchema


class UserCreateRequestSchema(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    confirm_password: str = Field(min_length=8, max_length=72)


class LoginRequestSchema(BaseModel):
    email: str
    password: str


class AuthUserResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: str
    user_data: UserResponseSchema
