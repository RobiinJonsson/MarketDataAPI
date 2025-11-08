#!/usr/bin/env python3
"""
Dual Alembic Migration Manager

This script manages migrations for both SQLite (dev) and SQL Server (prod) databases.
It ensures schema compatibility while maintaining separate version control.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {cmd}")
            print(f"Error output: {result.stderr}")
            return False
        print(result.stdout)
        return True
    except Exception as e:
        print(f"Exception running command: {cmd}")
        print(f"Exception: {e}")
        return False

def sqlite_migration(action, message=None):
    """Handle SQLite migrations."""
    print(f"\n🔸 SQLite Migration: {action}")
    
    if action == "init":
        return run_command("alembic -c alembic-sqlite/alembic.ini init alembic-sqlite")
    elif action == "revision":
        if not message:
            message = input("Enter migration message: ")
        return run_command(f"alembic -c alembic-sqlite/alembic.ini revision --autogenerate -m '{message}'")
    elif action == "upgrade":
        return run_command("alembic -c alembic-sqlite/alembic.ini upgrade head")
    elif action == "downgrade":
        return run_command("alembic -c alembic-sqlite/alembic.ini downgrade -1")
    elif action == "current":
        return run_command("alembic -c alembic-sqlite/alembic.ini current")
    elif action == "history":
        return run_command("alembic -c alembic-sqlite/alembic.ini history")
    else:
        print(f"Unknown SQLite action: {action}")
        return False

def sqlserver_migration(action, message=None):
    """Handle SQL Server migrations."""
    print(f"\n🔹 SQL Server Migration: {action}")
    
    # Check environment variables
    required_vars = ["AZURE_SQL_SERVER", "AZURE_SQL_DATABASE", "AZURE_SQL_USERNAME", "AZURE_SQL_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing environment variables: {', '.join(missing_vars)}")
        print("Please set all Azure SQL environment variables before running SQL Server migrations.")
        return False
    
    if action == "init":
        return run_command("alembic -c alembic-sqlserver/alembic.ini init alembic-sqlserver")
    elif action == "revision":
        if not message:
            message = input("Enter migration message: ")
        return run_command(f"alembic -c alembic-sqlserver/alembic.ini revision --autogenerate -m '{message}'")
    elif action == "upgrade":
        return run_command("alembic -c alembic-sqlserver/alembic.ini upgrade head")
    elif action == "downgrade":
        return run_command("alembic -c alembic-sqlserver/alembic.ini downgrade -1")
    elif action == "current":
        return run_command("alembic -c alembic-sqlserver/alembic.ini current")
    elif action == "history":
        return run_command("alembic -c alembic-sqlserver/alembic.ini history")
    else:
        print(f"Unknown SQL Server action: {action}")
        return False

def sync_schemas(message):
    """Create matching migrations for both databases."""
    print(f"\n🔄 Syncing schemas: {message}")
    
    print("Creating SQLite migration...")
    if not sqlite_migration("revision", message):
        return False
    
    print("Creating SQL Server migration...")
    if not sqlserver_migration("revision", message):
        return False
    
    print("✅ Schema sync complete!")
    return True

def deploy_dev():
    """Deploy to development (SQLite)."""
    print("\n🚀 Deploying to Development (SQLite)")
    return sqlite_migration("upgrade")

def deploy_prod():
    """Deploy to production (SQL Server)."""
    print("\n🚀 Deploying to Production (SQL Server)")
    return sqlserver_migration("upgrade")

def status():
    """Show migration status for both databases."""
    print("\n📊 Migration Status")
    print("=" * 50)
    
    print("SQLite (Development):")
    sqlite_migration("current")
    
    print("\nSQL Server (Production):")  
    sqlserver_migration("current")

def main():
    parser = argparse.ArgumentParser(description="Dual Alembic Migration Manager")
    parser.add_argument("action", choices=[
        "sqlite-init", "sqlite-revision", "sqlite-upgrade", "sqlite-downgrade", "sqlite-current", "sqlite-history",
        "sqlserver-init", "sqlserver-revision", "sqlserver-upgrade", "sqlserver-downgrade", "sqlserver-current", "sqlserver-history",
        "sync", "deploy-dev", "deploy-prod", "status"
    ], help="Migration action to perform")
    parser.add_argument("-m", "--message", help="Migration message")
    
    args = parser.parse_args()
    
    if args.action.startswith("sqlite-"):
        action = args.action.replace("sqlite-", "")
        success = sqlite_migration(action, args.message)
    elif args.action.startswith("sqlserver-"):
        action = args.action.replace("sqlserver-", "")
        success = sqlserver_migration(action, args.message)
    elif args.action == "sync":
        if not args.message:
            args.message = input("Enter migration message for schema sync: ")
        success = sync_schemas(args.message)
    elif args.action == "deploy-dev":
        success = deploy_dev()
    elif args.action == "deploy-prod":
        success = deploy_prod()
    elif args.action == "status":
        success = status()
    else:
        print(f"Unknown action: {args.action}")
        success = False
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()