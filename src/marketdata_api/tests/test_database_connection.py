#!/usr/bin/env python3
"""
Database Connection Test and Management Utility

This script helps you test database connections and manage database switching
between SQLite and Azure SQL Database.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    """Test the current database connection"""
    try:
        from marketdata_api.config import DATABASE_TYPE
        from marketdata_api.database.base import engine, get_database_url
        from sqlalchemy import text
        
        database_url = get_database_url()
        logger.info(f"Testing connection to: {DATABASE_TYPE} database")
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            
        if test_value == 1:
            logger.info("✅ Database connection successful!")
            return True
        else:
            logger.error("❌ Database connection test failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Database connection failed: {str(e)}")
        return False

def list_tables():
    """List all tables in the current database"""
    try:
        from marketdata_api.database.base import engine
        from marketdata_api.config import DATABASE_TYPE
        from sqlalchemy import text
        
        if DATABASE_TYPE.lower() == "azure_sql":
            # Use direct SQL for Azure SQL to avoid reflection issues
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT TABLE_NAME 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_TYPE = 'BASE TABLE'
                    ORDER BY TABLE_NAME
                """))
                tables = [row[0] for row in result.fetchall()]
        else:
            # Use SQLAlchemy reflection for SQLite
            from sqlalchemy import inspect
            inspector = inspect(engine)
            tables = inspector.get_table_names()
        
        if tables:
            logger.info(f"Found {len(tables)} tables:")
            for table in tables:
                logger.info(f"  - {table}")
        else:
            logger.info("No tables found in database")
            
        return tables
        
    except Exception as e:
        logger.error(f"Failed to list tables: {str(e)}")
        return []

def init_database():
    """Initialize the database with all tables"""
    try:
        from marketdata_api.database.initialize_db import init_database
        init_database()
        logger.info("✅ Database initialized successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        return False

def show_config():
    """Show current database configuration"""
    from marketdata_api.config import (
        DATABASE_TYPE, AZURE_SQL_SERVER, AZURE_SQL_DATABASE, 
        AZURE_SQL_USERNAME, AZURE_SQL_PORT
    )
    
    logger.info("Current Database Configuration:")
    logger.info(f"  Database Type: {DATABASE_TYPE}")
    
    if DATABASE_TYPE.lower() == "azure_sql":
        logger.info(f"  Azure SQL Server: {AZURE_SQL_SERVER}")
        logger.info(f"  Azure SQL Database: {AZURE_SQL_DATABASE}")
        logger.info(f"  Azure SQL Username: {AZURE_SQL_USERNAME}")
        logger.info(f"  Azure SQL Port: {AZURE_SQL_PORT}")
        logger.info(f"  Azure SQL Password: {'Set' if os.getenv('AZURE_SQL_PASSWORD') else 'Not Set'}")
    else:
        logger.info(f"  SQLite Database Path: {os.path.join(project_root, 'marketdata_api', 'database', 'marketdata.db')}")

def main():
    """Main function"""
    print("🗄️  Database Connection Test and Management Utility")
    print("=" * 50)
    
    # Show current configuration
    show_config()
    print()
    
    # Test connection
    print("Testing database connection...")
    if test_connection():
        print()
        
        # List tables
        print("Listing database tables...")
        tables = list_tables()
        print()
        
        if not tables:
            print("No tables found. Would you like to initialize the database? (y/n): ", end="")
            response = input().lower().strip()
            if response in ['y', 'yes']:
                print("Initializing database...")
                init_database()
    
    print("\n" + "=" * 50)
    print("Available environment variables for database switching:")
    print("  DATABASE_TYPE=sqlite     (for local SQLite database)")
    print("  DATABASE_TYPE=azure_sql  (for Azure SQL Database)")
    print("\nTo switch databases, update your .env file or set the environment variable")

if __name__ == "__main__":
    main()
