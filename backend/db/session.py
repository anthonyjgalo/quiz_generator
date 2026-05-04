from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base

engine = create_engine(settings.DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
