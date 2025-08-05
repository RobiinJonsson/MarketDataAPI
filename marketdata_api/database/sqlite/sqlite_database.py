"""SQLite database implementation preserving existing polymorphic inheritance."""

import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..factory.database_interface import DatabaseInterface
from ..base import Base  # Import shared Base

logger = logging.getLogger(__name__)


class SqliteDatabase(DatabaseInterface):
    """SQLite database implementation with polymorphic inheritance."""
    
    def __init__(self):
        self._engine = None
        self._session_maker = None
        self._base = Base  # Use shared Base instead of creating new one
    
    def get_engine(self):
        """Get the SQLite database engine."""
        if self._engine is None:
            self._engine = self._create_engine()
        return self._engine
    
    def get_session_maker(self):
        """Get the SQLite session maker."""
        if self._session_maker is None:
            self._session_maker = sessionmaker(
                autocommit=False, 
                autoflush=False, 
                bind=self.get_engine()
            )
        return self._session_maker
    
    def get_base_model(self):
        """Get the declarative base for SQLite."""
        return self._base
    
    def _create_engine(self):
        """Create SQLite engine."""
        from ...config import SQLITE_DB_PATH
        
        # Ensure the directory exists
        db_dir = os.path.dirname(SQLITE_DB_PATH)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        sqlite_url = f"sqlite:///{SQLITE_DB_PATH}"
        
        # SQLite specific engine configuration
        engine = create_engine(
            sqlite_url, 
            connect_args={"check_same_thread": False},
            echo=False  # Set to True for SQL debugging
        )
        
        logger.info(f"Created SQLite engine for {SQLITE_DB_PATH}")
        return engine
    
    def init_db(self) -> None:
        """Initialize SQLite database."""
        self._base.metadata.create_all(bind=self.get_engine())
        logger.info("✅ SQLite database tables created successfully")
