import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Read database URL from environment, fallback to local SQLite for development.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./palmeras_records.db")

# Build connection arguments only needed for SQLite with FastAPI threads.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Engine: single entry point that manages connections to the database.
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# SessionLocal: factory that creates new database sessions bound to the engine.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base: parent class for all ORM models (RecordLabel, Album, Format, ...).
class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that opens a session per request and closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
