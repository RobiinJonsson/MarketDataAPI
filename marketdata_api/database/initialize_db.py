import logging
import os
from sqlalchemy import inspect
from .base import engine, Base, DB_PATH
from ..models import instrument, legal_entity  # Import all your model files

logger = logging.getLogger(__name__)

def drop_database():
    """Drop the existing database file"""
    try:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            logger.info(f"Removed existing database: {DB_PATH}")
    except Exception as e:
        logger.error(f"Failed to remove database: {str(e)}")
        raise

def verify_tables():
    """Verify that all expected tables and columns exist"""
    inspector = inspect(engine)
    model_tables = Base.metadata.tables
    db_tables = inspector.get_table_names()
    
    all_valid = True
    for table_name, table in model_tables.items():
        if table_name not in db_tables:
            logger.error(f"Missing table: {table_name}")
            all_valid = False
            continue
            
        model_columns = {c.name for c in table.columns}
        db_columns = {c['name'] for c in inspector.get_columns(table_name)}
        missing_columns = model_columns - db_columns
        
        if missing_columns:
            logger.error(f"Table {table_name} missing columns: {missing_columns}")
            all_valid = False
            
    return all_valid

def init_database(force_recreate=True):
    """Initialize database with all models"""
    try:
        if force_recreate:
            drop_database()
            
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Verify tables and columns
        if verify_tables():
            logger.info("Database initialization successful")
        else:
            logger.error("Database verification failed")
            
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise
