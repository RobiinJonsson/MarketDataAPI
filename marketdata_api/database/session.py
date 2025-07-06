from sqlalchemy.orm import Session, sessionmaker
from contextlib import contextmanager
from typing import Generator
from .base import SessionLocal, engine
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

def get_session_with_expiration(expire_on_commit=False):
    """
    Get a SQLAlchemy session with custom expire_on_commit setting.
    
    Args:
        expire_on_commit: If False, doesn't expire objects when committing, useful for detached objects.
        
    Returns:
        A SQLAlchemy Session
    """
    SessionWithExpiration = sessionmaker(bind=engine, expire_on_commit=expire_on_commit)
    return SessionWithExpiration()
