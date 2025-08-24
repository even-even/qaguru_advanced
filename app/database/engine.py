import os

from loguru import logger
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from sqlmodel import SQLModel, create_engine, text

engine = create_engine(os.getenv("DATABASE_ENGINE"))


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def check_availability() -> bool:
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
            return True
    except OperationalError as e:
        logger.exception(f"Database connection error: {e}")
        return False
