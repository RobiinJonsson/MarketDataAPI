from sqlalchemy.orm import Session
from contextlib import contextmanager
from .base import SessionLocal

@contextmanager
def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
