from sqlalchemy.orm import Session
from contextlib import contextmanager
from typing import Generator
from .base import SessionLocal
import logging

logger = logging.getLogger(__name__)

@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Get a database session with automatic commit/rollback.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Session rollback due to error: {str(e)}")
        raise
    finally:
        session.close()
