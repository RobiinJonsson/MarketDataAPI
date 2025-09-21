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
        db_type = DatabaseConfig.get_database_type()

        if db_type == "sqlite":
            from .sqlite.sqlite_database import SqliteDatabase

            db = SqliteDatabase()
        elif db_type in ["sqlserver", "azure_sql", "mssql"]:
            from .sqlserver.sql_server_database import SqlServerDatabase

            db = SqlServerDatabase()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

        _engine = db.get_engine()
        logger.debug(f"Database engine initialized for {db_type}")
    return _engine


def _get_session_local():
    """Get session maker with lazy initialization."""
    global _session_local
    if _session_local is None:
        db_type = DatabaseConfig.get_database_type()

        if db_type == "sqlite":
            from .sqlite.sqlite_database import SqliteDatabase

            db = SqliteDatabase()
        elif db_type in ["sqlserver", "azure_sql", "mssql"]:
            from .sqlserver.sql_server_database import SqlServerDatabase

            db = SqlServerDatabase()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

        _session_local = db.get_session_maker()
        logger.debug(f"Session maker initialized for {db_type}")
    return _session_local


# Functions for backward compatibility
def get_database_url():
    """Get database URL via direct database configuration."""
    db_type = DatabaseConfig.get_database_type()

    if db_type == "sqlite":
        from .sqlite.sqlite_database import SqliteDatabase

        db = SqliteDatabase()
    elif db_type in ["sqlserver", "azure_sql", "mssql"]:
        from .sqlserver.sql_server_database import SqlServerDatabase

        db = SqlServerDatabase()
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

    return db.get_url() if hasattr(db, "get_url") else str(db.get_engine().url)


def create_database_engine():
    """Create database engine via direct database configuration."""
    return _get_engine()


def init_db():
    """Initialize database via direct database configuration."""
    db_type = DatabaseConfig.get_database_type()

    if db_type == "sqlite":
        from .sqlite.sqlite_database import SqliteDatabase

        db = SqliteDatabase()
    elif db_type in ["sqlserver", "azure_sql", "mssql"]:
        from .sqlserver.sql_server_database import SqlServerDatabase

        db = SqlServerDatabase()
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

    db.init_db()


# Module-level attribute access for backward compatibility
def __getattr__(name):
    """Allow access to engine and SessionLocal as module attributes."""
    if name == "engine":
        return _get_engine()
    elif name == "SessionLocal":
        return _get_session_local()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
