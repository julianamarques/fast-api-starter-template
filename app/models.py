import uuid

from sqlalchemy import Column, Uuid, String, Boolean
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id: Uuid = Column(Uuid, default=uuid.uuid4(), primary_key=True)
    name: str = Column(String(255), nullable=False)
    password: str = Column(String(255), nullable=False)
    email: str = Column(String(255), nullable=False, unique=True)
    active: bool = Column(Boolean, nullable=False, default=True)
    admin: bool = Column(Boolean, nullable=False, default=False)
