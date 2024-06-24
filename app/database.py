from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import logging

logging.basicConfig(level=logging.INFO)

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@db:5432/shop"

def get_engine():
    try:
        engine = create_engine(DATABASE_URL)
        logging.info("SQLAlchemy engine created successfully!")
        return engine
    except Exception as e:
        logging.error(f"Error creating SQLAlchemy engine: {e}")
        return None

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()