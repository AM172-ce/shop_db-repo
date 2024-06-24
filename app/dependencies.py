import logging
from app.database import SessionLocal

logging.basicConfig(level=logging.INFO)

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
