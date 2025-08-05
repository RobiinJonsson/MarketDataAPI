"""
Database session management with direct database access.

This module provides session management functionality using direct database
configuration without the factory pattern.
"""

from sqlalchemy.orm import Session, sessionmaker
from contextlib import contextmanager
from typing import Generator
from ..config import DatabaseConfig
import logging

logger = logging.getLogger(__name__)

def _get_session_maker():
    """Get session maker based on database configuration."""
    db_type = DatabaseConfig.get_database_type()
    
    if db_type == 'sqlite':
        from .sqlite.sqlite_database import SqliteDatabase
        db = SqliteDatabase()
    elif db_type in ['sqlserver', 'azure_sql', 'mssql']:
        from .sqlserver.sql_server_database import SqlServerDatabase
        db = SqlServerDatabase()
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    return db.get_session_maker()

def _get_engine():
    """Get engine based on database configuration."""
    db_type = DatabaseConfig.get_database_type()
    
    if db_type == 'sqlite':
        from .sqlite.sqlite_database import SqliteDatabase
        db = SqliteDatabase()
    elif db_type in ['sqlserver', 'azure_sql', 'mssql']:
        from .sqlserver.sql_server_database import SqlServerDatabase
        db = SqlServerDatabase()
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    return db.get_engine()

# Backward compatibility - expose SessionLocal 
def __getattr__(name):
    """Module-level attribute access for backward compatibility."""
    if name == 'SessionLocal':
        return _get_session_maker()
    elif name == 'engine':
        return _get_engine()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Get a database session with automatic commit/rollback.
    Uses database configuration to get the appropriate session maker.
    """
    session_maker = _get_session_maker()
    session = session_maker()
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
    engine = _get_engine()
    SessionWithExpiration = sessionmaker(bind=engine, expire_on_commit=expire_on_commit)
    return SessionWithExpiration()
