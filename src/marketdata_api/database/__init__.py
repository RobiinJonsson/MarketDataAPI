"""
Database package exports.

This module exports the main database components for easy access.
"""

from .factory.database_interface import DatabaseInterface
from .session import get_session


# Lazy imports to avoid circular dependencies
def _lazy_import():
    from .initialize_db import database_exists, init_database, verify_tables

    return init_database, database_exists, verify_tables


def __getattr__(name):
    """Lazy loading for potentially circular imports."""
    if name in ("init_database", "database_exists", "verify_tables"):
        init_database, database_exists, verify_tables = _lazy_import()
        if name == "init_database":
            return init_database
        elif name == "database_exists":
            return database_exists
        elif name == "verify_tables":
            return verify_tables
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = ["DatabaseInterface", "get_session", "init_database", "database_exists", "verify_tables"]
