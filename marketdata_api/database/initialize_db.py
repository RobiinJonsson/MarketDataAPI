import logging
import os
from sqlalchemy import inspect
from .base import engine, Base, DB_PATH
from ..models import instrument, legal_entity  # Import all your model files

logger = logging.getLogger(__name__)

def database_exists():
    """Check if database file exists"""
    return os.path.exists(DB_PATH)

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

def init_database(force_recreate=False):
    """Initialize database with all models"""
    try:
        if force_recreate and database_exists():
            logger.warning("Dropping existing database - ALL DATA WILL BE LOST")
            os.remove(DB_PATH)
        elif database_exists():
            logger.info("Database exists, verifying tables...")
            if verify_tables():
                logger.info("Database structure is valid")
                return
            else:
                logger.warning("Database structure is invalid but preserve_data=True, skipping recreation")
                return
            
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Created new database with all tables")
            
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise
