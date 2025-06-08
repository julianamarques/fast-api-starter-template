from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.app_config import settings

engine = create_engine(
    str(settings.get_sqlalchemy_database_uri),
    pool_size=10,
    pool_timeout=60,
    max_overflow=20,
    pool_recycle=1800
)

Session = sessionmaker(bind=engine)
