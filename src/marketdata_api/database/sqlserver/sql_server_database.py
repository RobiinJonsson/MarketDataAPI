"""SQL Server database implementation."""

import logging
import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from ..base import Base  # Import shared Base
from ..factory.database_interface import DatabaseInterface

logger = logging.getLogger(__name__)


class SqlServerDatabase(DatabaseInterface):
    """SQL Server database implementation optimized for Azure SQL."""

    def __init__(self):
        self._engine = None
        self._session_maker = None
        self._base = Base  # Use shared Base instead of creating new one

    def get_engine(self):
        """Get the SQL Server database engine."""
        if self._engine is None:
            self._engine = self._create_engine()
        return self._engine

    def get_session_maker(self):
        """Get the SQL Server session maker."""
        if self._session_maker is None:
            self._session_maker = sessionmaker(
                autocommit=False, autoflush=False, bind=self.get_engine()
            )
        return self._session_maker

    def get_base_model(self):
        """Get the declarative base for SQL Server."""
        return self._base

    def _create_engine(self):
        """Create SQL Server engine with optimized settings."""
        from ...config import (
            AZURE_SQL_DATABASE,
            AZURE_SQL_PASSWORD,
            AZURE_SQL_PORT,
            AZURE_SQL_SERVER,
            AZURE_SQL_USERNAME,
        )

        if not AZURE_SQL_PASSWORD:
            raise ValueError("AZURE_SQL_PASSWORD environment variable is required")

        # URL encode the password to handle special characters
        password_encoded = quote_plus(AZURE_SQL_PASSWORD)

        # Azure SQL Database connection string
        connection_string = (
            f"mssql+pyodbc://{AZURE_SQL_USERNAME}:{password_encoded}@"
            f"{AZURE_SQL_SERVER}:{AZURE_SQL_PORT}/{AZURE_SQL_DATABASE}"
            f"?driver=SQL+Server"
        )

        # SQL Server optimized engine configuration
        engine = create_engine(
            connection_string,
            pool_pre_ping=True,
            pool_recycle=300,
            connect_args={"timeout": 30, "autocommit": True, "fast_executemany": True},
            echo=False,  # Set to True for SQL debugging
        )

        logger.info(f"Created SQL Server engine for {AZURE_SQL_SERVER}/{AZURE_SQL_DATABASE}")
        return engine

    def init_db(self) -> None:
        """Initialize SQL Server database with careful error handling."""
        try:
            # First, check if tables exist
            with self.get_engine().connect() as conn:
                result = conn.execute(
                    text(
                        """
                    SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_TYPE = 'BASE TABLE'
                """
                    )
                )
                table_count = result.fetchone()[0]

                if table_count > 0:
                    logger.info(
                        f"✅ SQL Server database already has {table_count} tables - skipping creation"
                    )
                else:
                    logger.info("Creating SQL Server database tables...")
                    self._base.metadata.create_all(bind=self.get_engine(), checkfirst=True)
                    logger.info("✅ SQL Server database tables created successfully")

        except Exception as e:
            logger.warning(f"SQL Server table verification had issues: {e}")
            # Try to verify database works anyway
            try:
                with self.get_engine().connect() as conn:
                    conn.execute(text("SELECT 1"))
                logger.info("✅ SQL Server database connection verified")
            except Exception as verify_error:
                logger.error(f"❌ SQL Server database verification failed: {verify_error}")
                raise
