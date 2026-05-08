import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.models import Base
from db.seed import seed_data
from db.session import SessionLocal, engine


def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        seed_data(db)
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
