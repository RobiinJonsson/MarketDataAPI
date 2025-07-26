#!/usr/bin/env python3
"""
Production Database Upgrade Script

This script safely upgrades your production database to match your dev schema
using Alembic migrations.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import logging
from sqlalchemy import text

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def check_current_state():
    """Check the current state of the production database"""
    print("🔍 Checking Current Database State")
    print("=" * 50)
    
    try:
        from marketdata_api.database.base import engine
        from marketdata_api.config import DATABASE_TYPE, AZURE_SQL_SERVER, AZURE_SQL_DATABASE
        
        logger.info(f"Database Type: {DATABASE_TYPE}")
        logger.info(f"Server: {AZURE_SQL_SERVER}")
        logger.info(f"Database: {AZURE_SQL_DATABASE}")
        
        with engine.connect() as conn:
            # Check if alembic_version table exists
            result = conn.execute(text("""
                SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'alembic_version'
            """))
            
            has_alembic = result.fetchone()[0] > 0
            
            if has_alembic:
                version_result = conn.execute(text("SELECT version_num FROM alembic_version"))
                current_version = version_result.fetchone()
                if current_version:
                    logger.info(f"✅ Alembic version table exists, current version: {current_version[0]}")
                    return current_version[0]
                else:
                    logger.info("⚠️  Alembic version table exists but no version recorded")
                    return None
            else:
                logger.info("❌ No alembic_version table found")
                
                # List existing tables
                tables_result = conn.execute(text("""
                    SELECT TABLE_NAME 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_TYPE = 'BASE TABLE'
                    ORDER BY TABLE_NAME
                """))
                tables = [row[0] for row in tables_result.fetchall()]
                
                logger.info(f"Found {len(tables)} existing tables:")
                for table in tables:
                    logger.info(f"  - {table}")
                
                return None
                
    except Exception as e:
        logger.error(f"Failed to check database state: {e}")
        return False

def initialize_alembic_version():
    """Initialize alembic_version table and set to appropriate version"""
    print("\n🔧 Initializing Alembic Version Tracking")
    print("=" * 50)
    
    try:
        from marketdata_api.database.base import engine
        
        with engine.connect() as conn:
            # Create alembic_version table
            logger.info("Creating alembic_version table...")
            conn.execute(text("""
                CREATE TABLE alembic_version (
                    version_num VARCHAR(32) NOT NULL,
                    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
                )
            """))
            
            # Determine which version to set based on existing tables
            tables_result = conn.execute(text("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """))
            tables = {row[0] for row in tables_result.fetchall()}
            
            # Determine migration level based on existing tables
            if 'transparency_calculations' in tables:
                # Has transparency tables - set to latest
                target_version = '20250601_120000_add_transparency_tables'
                logger.info("Transparency tables found - setting to latest migration")
            elif 'entity_relationships' in tables:
                # Has entity relationships but no transparency
                target_version = '20250530_parent_child'
                logger.info("Entity relationships found - setting to parent_child migration")
            else:
                # Basic schema only
                target_version = '20250517_initial_schema'
                logger.info("Basic schema found - setting to initial migration")
            
            # Insert the version
            conn.execute(text(f"INSERT INTO alembic_version (version_num) VALUES ('{target_version}')"))
            conn.commit()
            
            logger.info(f"✅ Alembic version set to: {target_version}")
            return target_version
            
    except Exception as e:
        logger.error(f"Failed to initialize alembic version: {e}")
        return None

def run_alembic_upgrade():
    """Run alembic upgrade to latest version"""
    print("\n🚀 Running Alembic Upgrade")
    print("=" * 50)
    
    try:
        import subprocess
        
        logger.info("Running: alembic upgrade head")
        
        # Change to project directory
        os.chdir(project_root)
        
        # Run alembic upgrade
        result = subprocess.run(
            ['alembic', 'upgrade', 'head'],
            capture_output=True,
            text=True,
            check=True
        )
        
        logger.info("✅ Alembic upgrade completed successfully!")
        
        if result.stdout:
            logger.info("Upgrade output:")
            for line in result.stdout.split('\n'):
                if line.strip():
                    logger.info(f"  {line}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Alembic upgrade failed: {e}")
        if e.stdout:
            logger.error("STDOUT:")
            logger.error(e.stdout)
        if e.stderr:
            logger.error("STDERR:")
            logger.error(e.stderr)
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error during upgrade: {e}")
        return False

def verify_upgrade():
    """Verify the upgrade was successful"""
    print("\n✅ Verifying Upgrade")
    print("=" * 50)
    
    try:
        from marketdata_api.database.base import engine
        
        with engine.connect() as conn:
            # Check final version
            version_result = conn.execute(text("SELECT version_num FROM alembic_version"))
            final_version = version_result.fetchone()[0]
            logger.info(f"Final migration version: {final_version}")
            
            # Check for transparency tables
            transparency_check = conn.execute(text("""
                SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'transparency_calculations'
            """))
            
            has_transparency = transparency_check.fetchone()[0] > 0
            
            if has_transparency:
                logger.info("✅ Transparency tables now available")
            else:
                logger.warning("⚠️  Transparency tables still missing")
            
            # List all tables
            tables_result = conn.execute(text("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """))
            tables = [row[0] for row in tables_result.fetchall()]
            
            logger.info(f"Final table count: {len(tables)}")
            logger.info("Tables:")
            for table in tables:
                logger.info(f"  - {table}")
            
            return True
            
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        return False

def main():
    """Main upgrade process"""
    print("🔄 Production Database Upgrade to Dev Schema")
    print("=" * 60)
    
    # Step 1: Check current state
    current_version = check_current_state()
    
    if current_version is False:
        print("\n❌ Cannot proceed - database connection failed")
        return
    
    # Step 2: Initialize alembic if needed
    if current_version is None:
        logger.info("\n⚠️  Alembic version tracking not set up")
        response = input("Initialize alembic version tracking? (y/n): ").lower().strip()
        
        if response not in ['y', 'yes']:
            print("Upgrade cancelled by user")
            return
            
        current_version = initialize_alembic_version()
        if not current_version:
            print("\n❌ Failed to initialize alembic version")
            return
    
    # Step 3: Run upgrade
    print(f"\n📋 Current version: {current_version}")
    print("🎯 Target: Latest (head)")
    
    response = input("Proceed with upgrade? (y/n): ").lower().strip()
    
    if response not in ['y', 'yes']:
        print("Upgrade cancelled by user")
        return
    
    if run_alembic_upgrade():
        verify_upgrade()
        print("\n🎉 Production database successfully upgraded!")
        print("Your production database now matches your dev schema.")
        print("\n✅ You can now:")
        print("  - Use all transparency features")
        print("  - Run your Flask app without compatibility issues")
        print("  - Use your full dev codebase in production")
    else:
        print("\n❌ Upgrade failed. Check logs above for details.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Upgrade cancelled by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
