import uuid

from sqlalchemy import Uuid, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[Uuid] = mapped_column(
        Uuid,
        nullable=False,
        default=uuid.uuid4,
        primary_key=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
