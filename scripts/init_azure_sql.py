#!/usr/bin/env python3
"""
Azure SQL Database Initialization Script

This script creates all the necessary tables for the MarketData API
in your Azure SQL Database if they don't already exist.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def initialize_azure_sql():
    """Initialize Azure SQL Database with all required tables"""
    try:
        from marketdata_api.database.base import engine, Base
        from marketdata_api.config import DATABASE_TYPE
        
        # Import all models to register them with Base
        from marketdata_api.models import instrument, legal_entity
        
        logger.info(f"Initializing {DATABASE_TYPE} database...")
        logger.info("Creating tables...")
        
        # Create all tables (with checkfirst=True to avoid errors if tables exist)
        Base.metadata.create_all(bind=engine, checkfirst=True)
        
        # Verify tables were created
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """))
            
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                logger.info(f"✅ Successfully created {len(tables)} tables:")
                for table in tables:
                    logger.info(f"  - {table}")
                    
                # Get column count for each table
                for table in tables:
                    result = conn.execute(text(f"""
                        SELECT COUNT(*) 
                        FROM INFORMATION_SCHEMA.COLUMNS 
                        WHERE TABLE_NAME = '{table}'
                    """))
                    col_count = result.fetchone()[0]
                    logger.info(f"    ({col_count} columns)")
                    
                return True
            else:
                logger.error("❌ No tables found after creation")
                return False
                
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        return False

def test_database_operations():
    """Test basic database operations"""
    try:
        from marketdata_api.database.session import get_session
        from sqlalchemy import text
        
        logger.info("Testing database operations...")
        
        with get_session() as session:
            # Test basic query
            result = session.execute(text("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"))
            table_count = result.fetchone()[0]
            
            logger.info(f"✅ Database operational with {table_count} tables")
            return True
            
    except Exception as e:
        logger.error(f"❌ Database operations test failed: {str(e)}")
        return False

def show_database_info():
    """Show database information"""
    from marketdata_api.config import (
        DATABASE_TYPE, AZURE_SQL_SERVER, AZURE_SQL_DATABASE, 
        AZURE_SQL_USERNAME
    )
    
    logger.info("Database Configuration:")
    logger.info(f"  Type: {DATABASE_TYPE}")
    logger.info(f"  Server: {AZURE_SQL_SERVER}")
    logger.info(f"  Database: {AZURE_SQL_DATABASE}")
    logger.info(f"  Username: {AZURE_SQL_USERNAME}")

if __name__ == "__main__":
    print("🗄️ Azure SQL Database Initialization")
    print("=" * 50)
    
    # Show configuration
    show_database_info()
    print()
    
    # Initialize database
    if initialize_azure_sql():
        print()
        # Test operations
        test_database_operations()
    
    print("=" * 50)
    print("✅ Your Azure SQL Database is ready to use!")
    print("\nTo switch back to SQLite, change DATABASE_TYPE=sqlite in your .env file")
    print("To use Azure SQL, ensure DATABASE_TYPE=azure_sql in your .env file")
