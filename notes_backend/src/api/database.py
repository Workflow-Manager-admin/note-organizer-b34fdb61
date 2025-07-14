# database.py — DB engine / session configuration for SQLAlchemy

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("NOTES_DB_URL", "sqlite:///./notes.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# PUBLIC_INTERFACE
def get_db():
    """
    DB session dependency for FastAPI routes.
    Yields a session and ensures proper close after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
