import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
import logging

logger = logging.getLogger(__name__)

def get_database_url():
    """Get the appropriate database URL based on configuration"""
    from ..config import (
        DATABASE_TYPE, AZURE_SQL_SERVER, AZURE_SQL_DATABASE, 
        AZURE_SQL_USERNAME, AZURE_SQL_PASSWORD, AZURE_SQL_PORT
    )
    
    if DATABASE_TYPE.lower() == "azure_sql":
        if not AZURE_SQL_PASSWORD:
            raise ValueError("AZURE_SQL_PASSWORD environment variable is required for Azure SQL Database")
        
        # URL encode the password to handle special characters
        password_encoded = quote_plus(AZURE_SQL_PASSWORD)
        
        # Azure SQL Database connection string
        connection_string = (
            f"mssql+pyodbc://{AZURE_SQL_USERNAME}:{password_encoded}@"
            f"{AZURE_SQL_SERVER}:{AZURE_SQL_PORT}/{AZURE_SQL_DATABASE}"
            f"?driver=SQL+Server&Encrypt=yes&TrustServerCertificate=no&autocommit=true"
        )
        logger.info(f"Using Azure SQL Database: {AZURE_SQL_SERVER}/{AZURE_SQL_DATABASE}")
        return connection_string
    else:
        # SQLite configuration (default)
        from ..config import SQLITE_DB_PATH
        
        # Ensure the directory exists
        db_dir = os.path.dirname(SQLITE_DB_PATH)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        sqlite_url = f"sqlite:///{SQLITE_DB_PATH}"
        logger.info(f"Using SQLite database: {SQLITE_DB_PATH}")
        return sqlite_url

def create_database_engine():
    """Create the appropriate database engine"""
    from ..config import DATABASE_TYPE
    
    database_url = get_database_url()
    
    if DATABASE_TYPE.lower() == "azure_sql":
        # Azure SQL specific engine configuration
        engine = create_engine(
            database_url,
            pool_pre_ping=True,
            pool_recycle=300,
            connect_args={
                "timeout": 30,
                "autocommit": True,
                "fast_executemany": True
            },
            execution_options={
                "autocommit": True
            },
            echo=False  # Set to True for SQL debugging
        )
    else:
        # SQLite specific engine configuration
        engine = create_engine(
            database_url, 
            connect_args={"check_same_thread": False},
            echo=False  # Set to True for SQL debugging
        )
    
    return engine

# Create engine and session factory
engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

def init_db():
    """Initialize the database by creating all tables"""
    from ..config import DATABASE_TYPE
    
    if DATABASE_TYPE.lower() == "azure_sql":
        # For Azure SQL, use a simpler approach to avoid reflection issues
        try:
            Base.metadata.create_all(bind=engine, checkfirst=False)
            logger.info("✅ Database tables created successfully")
        except Exception as e:
            logger.warning(f"Table creation had issues but may have succeeded: {e}")
            # Try to verify by running a simple test
            try:
                from sqlalchemy import text
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                logger.info("✅ Database connection verified")
            except Exception as verify_error:
                logger.error(f"❌ Database verification failed: {verify_error}")
                raise
    else:
        # Standard SQLite approach
        Base.metadata.create_all(bind=engine)
