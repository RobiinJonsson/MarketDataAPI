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
    
    Yields:
        Session: SQLAlchemy session
        
    Raises:
        Exception: Re-raises any exception after rollback
    """
    session = SessionLocal()
    try:
        logger.debug("Creating new database session")
        yield session
        session.commit()
        logger.debug("Session committed successfully")
    except Exception as e:
        session.rollback()
        logger.error(f"Session rollback due to error: {str(e)}")
        raise
    finally:
        session.close()
        logger.debug("Session closed")
