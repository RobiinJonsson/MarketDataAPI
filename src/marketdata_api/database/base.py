"""
Database base module with shared declarative base.

This module provides the shared SQLAlchemy declarative base used by all models.
"""

import logging

from sqlalchemy.orm import declarative_base

from ..config import DatabaseConfig

logger = logging.getLogger(__name__)

# Create a global declarative base
Base = declarative_base()

# Legacy support - initialize globals lazily
_engine = None
_session_local = None


def _get_engine():
    """Get database engine with lazy initialization."""
    global _engine
    if _engine is None:
        # Use singleton database instance to prevent multiple engine creation
        from .session import _get_database_instance
        db = _get_database_instance()
        _engine = db.get_engine()
        logger.debug(f"Database engine initialized")
    return _engine


def _get_session_local():
    """Get session maker with lazy initialization."""
    global _session_local
    if _session_local is None:
        # Use singleton database instance to prevent multiple engine creation
        from .session import _get_database_instance
        db = _get_database_instance()
        _session_local = db.get_session_maker()
        logger.debug(f"Session maker initialized")
    return _session_local


# Functions for backward compatibility
def get_database_url():
    """Get database URL via direct database configuration."""
    from .session import _get_database_instance
    db = _get_database_instance()
    return db.get_url() if hasattr(db, "get_url") else str(db.get_engine().url)


def create_database_engine():
    """Create database engine via direct database configuration."""
    return _get_engine()


def init_db():
    """Initialize database via direct database configuration."""
    from .session import _get_database_instance
    db = _get_database_instance()
    db.init_db()


# Module-level attribute access for backward compatibility
def __getattr__(name):
    """Allow access to engine and SessionLocal as module attributes."""
    if name == "engine":
        return _get_engine()
    elif name == "SessionLocal":
        return _get_session_local()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
