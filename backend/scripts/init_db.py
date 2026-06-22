from db.models import Base
from db.seed import seed_data
from db.session import SessionLocal, engine


def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        seed_data(db)
    except Exception as e:
        db.rollback()
        print(f"Error during data initialization: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
