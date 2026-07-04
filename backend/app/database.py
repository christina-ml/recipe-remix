"""
Database connection setup.

Uses SQLAlchemy's declarative ORM against Postgres. The connection string
is read from the DATABASE_URL environment variable so it works both in
local dev (docker-compose) and in CI.
"""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://recipe_user:recipe_pass@localhost:5432/recipe_remix",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
