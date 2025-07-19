import logging
import os
from sqlalchemy import inspect, text
from .base import engine, Base, get_database_url
from ..models import instrument, legal_entity  # Import all your model files

logger = logging.getLogger(__name__)

def database_exists():
    """Check if database exists (works for both SQLite and Azure SQL)"""
    from ..config import DATABASE_TYPE
    
    if DATABASE_TYPE.lower() == "azure_sql":
        try:
            # For Azure SQL, try to connect and run a simple query
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.info(f"Azure SQL database connection failed: {e}")
            return False
    else:
        # For SQLite, check if file exists
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DB_PATH = os.path.join(BASE_DIR, "marketdata.db")
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
    from ..config import DATABASE_TYPE
    
    try:
        # Add environment check to prevent accidental resets
        if force_recreate and os.environ.get('FLASK_ENV') == 'production':
            logger.error("Cannot force recreate database in production environment")
            return False
            
        if force_recreate and database_exists():
            if DATABASE_TYPE.lower() == "azure_sql":
                logger.warning("⚠️ WARNING: About to drop all tables in Azure SQL Database - ALL DATA WILL BE LOST")
                user_input = input("Are you sure you want to reset the Azure SQL database? (yes/no): ")
                if user_input.lower() != 'yes':
                    logger.info("Database reset cancelled")
                    return False
                logger.warning("Dropping all tables in Azure SQL Database")
                Base.metadata.drop_all(bind=engine)
            else:
                logger.warning("⚠️ WARNING: About to drop existing SQLite database - ALL DATA WILL BE LOST")
                user_input = input("Are you sure you want to reset the database? (yes/no): ")
                if user_input.lower() != 'yes':
                    logger.info("Database reset cancelled")
                    return False
                logger.warning("Dropping existing SQLite database")
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                DB_PATH = os.path.join(BASE_DIR, "marketdata.db")
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
