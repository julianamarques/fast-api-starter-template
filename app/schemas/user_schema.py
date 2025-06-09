from pydantic import BaseModel

from app.models.user import User


class UserResponseSchema(BaseModel):
    name: str
    email: str
    password: str
    active: bool
    admin: bool

    @classmethod
    def from_model(cls, user: User):
        return cls(
            name=user.name,
            email=user.email,
            password=user.password,
            active=user.active,
            admin=user.admin
        )
