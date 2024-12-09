from app.core.database_config import Session


def get_session() -> Session:
    with Session() as session:
        try:
            yield session
        finally:
            session.close()
