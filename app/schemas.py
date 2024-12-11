from pydantic import BaseModel, field_validator, Field, EmailStr


class UserCreateSchema(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    email: str = EmailStr()
    password: str


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


class LoginSchema(BaseModel):
    email: str = EmailStr()
    password: str


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


class AuthSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: str


class CurrentUserSchema(BaseModel):
    access_token: str
    name: str
    email: str
