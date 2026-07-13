import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.depends import get_db_session
from app.main import app
from app.models.base import Base


@pytest.fixture(name="db_session_factory")
def db_session_factory_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    yield sessionmaker(bind=engine)

    engine.dispose()


@pytest.fixture(name="client")
def client_fixture(db_session_factory):
    def override_get_db_session():
        with db_session_factory() as session:
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise

    app.dependency_overrides[get_db_session] = override_get_db_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
