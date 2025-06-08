from pydantic import BaseModel, Field, EmailStr, field_validator

from app.schemas.user_schema import UserResponseSchema


class UserCreateRequestSchema(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    email: str = EmailStr()
    password: str
    confirm_password: str


    @field_validator('name')
    def validate_name(cls, value):
        if not value:
            raise ValueError('Name is required')
        return value


    @field_validator('email')
    def validate_email(cls, value):
        if not value:
            raise ValueError('Email is required')
        return value


    @field_validator('password')
    def validate_password(cls, value):
        if not value:
            raise ValueError('Password is required')
        return value

    @field_validator('confirm_password')
    def validate_confirm_password(cls, value):
        if not value:
            raise ValueError('Confirm Password is required')
        return value


class LoginRequestSchema(BaseModel):
    email: str = EmailStr()
    password: str


    @field_validator('email')
    def validate_email(cls, value):
        if not value:
            raise ValueError('Email é obrigatório')
        return value


    @field_validator('password')
    def validate_password(cls, value):
        if not value:
            raise ValueError('Senha é obrigatória')
        return value


class AuthUserResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: str
    user_data: UserResponseSchema
