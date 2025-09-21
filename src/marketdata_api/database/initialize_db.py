"""
Database initialization with direct database access.

This module provides database initialization functionality.
"""

import logging
import os

from sqlalchemy import inspect, text

from ..config import DatabaseConfig

logger = logging.getLogger(__name__)


def _get_database():
    """Get database instance based on configuration."""
    db_type = DatabaseConfig.get_database_type()

    if db_type == "sqlite":
        from .sqlite.sqlite_database import SqliteDatabase

        return SqliteDatabase()
    elif db_type in ["sqlserver", "azure_sql", "mssql"]:
        from .sqlserver.sql_server_database import SqlServerDatabase

        return SqlServerDatabase()
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def database_exists():
    """Check if database exists (works for both SQLite and Azure SQL)"""
    db_type = DatabaseConfig.get_database_type()
    db = _get_database()
    engine = db.get_engine()

    if db_type == "sqlserver":
        try:
            # For SQL Server, try to connect and run a simple query
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.info(f"SQL Server database connection failed: {e}")
            return False
    else:
        # For SQLite, check if file exists
        from ..config import SQLITE_DB_PATH

        return os.path.exists(SQLITE_DB_PATH)


def verify_tables():
    """Verify that all expected tables and columns exist"""
    db = _get_database()
    engine = db.get_engine()
    base = db.get_base_model()

    inspector = inspect(engine)
    model_tables = base.metadata.tables
    db_tables = inspector.get_table_names()

    all_valid = True
    for table_name, table in model_tables.items():
        if table_name not in db_tables:
            logger.error(f"Missing table: {table_name}")
            all_valid = False
            continue

        model_columns = {c.name for c in table.columns}
        db_columns = {c["name"] for c in inspector.get_columns(table_name)}
        missing_columns = model_columns - db_columns

        if missing_columns:
            logger.error(f"Table {table_name} missing columns: {missing_columns}")
            all_valid = False

    return all_valid


def init_database(force_recreate=False):
    """Initialize database with all models"""
    db_type = DatabaseConfig.get_database_type()
    db = _get_database()
    engine = db.get_engine()
    base = db.get_base_model()

    try:
        # Add environment check to prevent accidental resets
        if force_recreate and os.environ.get("FLASK_ENV") == "production":
            logger.error("Cannot force recreate database in production environment")
            return False

        if force_recreate and database_exists():
            if db_type == "sqlserver":
                logger.warning(
                    "⚠️ WARNING: About to drop all tables in SQL Server Database - ALL DATA WILL BE LOST"
                )
                user_input = input(
                    "Are you sure you want to reset the SQL Server database? (yes/no): "
                )
                if user_input.lower() != "yes":
                    logger.info("Database reset cancelled")
                    return False
                logger.warning("Dropping all tables in SQL Server Database")
                base.metadata.drop_all(bind=engine)
            else:
                logger.warning(
                    "⚠️ WARNING: About to drop existing SQLite database - ALL DATA WILL BE LOST"
                )
                user_input = input("Are you sure you want to reset the database? (yes/no): ")
                if user_input.lower() != "yes":
                    logger.info("Database reset cancelled")
                    return False
                logger.warning("Dropping existing SQLite database")
                from ..config import SQLITE_DB_PATH

                if os.path.exists(SQLITE_DB_PATH):
                    os.remove(SQLITE_DB_PATH)
        elif database_exists():
            logger.info("Database exists, verifying tables...")
            if verify_tables():
                logger.info("Database structure is valid")
                return True
            else:
                logger.warning(
                    "Database structure is invalid but preserve_data=True, skipping recreation"
                )
                return False

        # Create all tables using factory
        db.init_db()
        logger.info("Created new database with all tables via factory")
        return True

    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise
