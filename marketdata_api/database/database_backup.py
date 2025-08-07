#!/usr/bin/env python3
"""
Database Backup and Recovery System for MarketDataAPI

This script provides automatic database backup functionality with:
- Daily automated backups
- Pre-operation safety backups
- Recovery capabilities
- Backup rotation and cleanup
"""

import os
import shutil
import sqlite3
import subprocess
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatabaseBackupManager:
    def __init__(self, db_path: str, backup_dir: str = "database_backups"):
        self.db_path = Path(db_path)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure database exists
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found: {self.db_path}")
    
    def create_backup(self, backup_type: str = "manual", description: str = "") -> Path:
        """Create a backup of the database."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"marketdata_{backup_type}_{timestamp}.db"
        backup_path = self.backup_dir / backup_name
        
        try:
            # Create SQLite backup using backup API for consistency
            with sqlite3.connect(str(self.db_path)) as source:
                with sqlite3.connect(str(backup_path)) as backup:
                    source.backup(backup)
            
            # Create metadata file
            metadata = {
                'timestamp': timestamp,
                'backup_type': backup_type,
                'description': description,
                'original_db_path': str(self.db_path),
                'backup_size': backup_path.stat().st_size
            }
            
            metadata_path = backup_path.with_suffix('.meta')
            with open(metadata_path, 'w') as f:
                for key, value in metadata.items():
                    f.write(f"{key}: {value}\n")
            
            logger.info(f"Backup created: {backup_path} ({metadata['backup_size']} bytes)")
            return backup_path
            
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            if backup_path.exists():
                backup_path.unlink()
            raise
    
    def create_pre_operation_backup(self, operation_name: str) -> Path:
        """Create a backup before performing risky operations."""
        description = f"Pre-operation backup before: {operation_name}"
        return self.create_backup("pre-op", description)
    
    def list_backups(self) -> List[dict]:
        """List all available backups."""
        backups = []
        for backup_file in self.backup_dir.glob("*.db"):
            metadata_file = backup_file.with_suffix('.meta')
            metadata = {}
            
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    for line in f:
                        key, value = line.strip().split(': ', 1)
                        metadata[key] = value
            
            stat = backup_file.stat()
            backups.append({
                'file': backup_file,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime),
                'metadata': metadata
            })
        
        return sorted(backups, key=lambda x: x['created'], reverse=True)
    
    def restore_backup(self, backup_path: Path, confirm: bool = False) -> bool:
        """Restore database from backup."""
        if not backup_path.exists():
            logger.error(f"Backup file not found: {backup_path}")
            return False
        
        if not confirm:
            response = input(f"Are you sure you want to restore from {backup_path.name}? This will overwrite the current database. (yes/no): ")
            if response.lower() != 'yes':
                logger.info("Restore cancelled by user")
                return False
        
        try:
            # Create backup of current database before restore
            self.create_backup("pre-restore", f"Before restoring from {backup_path.name}")
            
            # Restore the backup
            shutil.copy2(backup_path, self.db_path)
            logger.info(f"Database restored from: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False
    
    def cleanup_old_backups(self, keep_days: int = 30, keep_count: int = 10) -> int:
        """Clean up old backups based on age and count."""
        backups = self.list_backups()
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        removed_count = 0
        
        # Remove backups older than cutoff_date, but keep at least keep_count recent backups
        for i, backup in enumerate(backups):
            if i >= keep_count and backup['created'] < cutoff_date:
                try:
                    backup['file'].unlink()
                    metadata_file = backup['file'].with_suffix('.meta')
                    if metadata_file.exists():
                        metadata_file.unlink()
                    removed_count += 1
                    logger.info(f"Removed old backup: {backup['file'].name}")
                except Exception as e:
                    logger.error(f"Error removing backup {backup['file'].name}: {e}")
        
        return removed_count
    
    def verify_backup(self, backup_path: Path) -> bool:
        """Verify backup integrity."""
        try:
            with sqlite3.connect(str(backup_path)) as conn:
                # Check database integrity
                cursor = conn.cursor()
                cursor.execute("PRAGMA integrity_check")
                result = cursor.fetchone()
                
                if result[0] == 'ok':
                    logger.info(f"Backup verification passed: {backup_path.name}")
                    return True
                else:
                    logger.error(f"Backup verification failed: {backup_path.name} - {result[0]}")
                    return False
                    
        except Exception as e:
            logger.error(f"Backup verification error: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Database Backup Manager")
    parser.add_argument('--db-path', default='marketdata_api/database/marketdata.db', help='Database file path')
    parser.add_argument('--backup-dir', default='database_backups', help='Backup directory')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create backup command
    backup_parser = subparsers.add_parser('backup', help='Create a backup')
    backup_parser.add_argument('--type', default='manual', help='Backup type')
    backup_parser.add_argument('--description', default='', help='Backup description')
    
    # List backups command
    list_parser = subparsers.add_parser('list', help='List available backups')
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore from backup')
    restore_parser.add_argument('backup_file', help='Backup file to restore from')
    restore_parser.add_argument('--confirm', action='store_true', help='Skip confirmation prompt')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Clean up old backups')
    cleanup_parser.add_argument('--keep-days', type=int, default=30, help='Keep backups newer than N days')
    cleanup_parser.add_argument('--keep-count', type=int, default=10, help='Keep at least N most recent backups')
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify backup integrity')
    verify_parser.add_argument('backup_file', help='Backup file to verify')
    
    # Daily backup command
    daily_parser = subparsers.add_parser('daily', help='Create daily automated backup')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    backup_manager = DatabaseBackupManager(args.db_path, args.backup_dir)
    
    if args.command == 'backup':
        backup_manager.create_backup(args.type, args.description)
    
    elif args.command == 'list':
        backups = backup_manager.list_backups()
        if not backups:
            print("No backups found")
        else:
            print(f"{'Backup File':<40} {'Size':<10} {'Created':<20} {'Type':<15}")
            print("-" * 90)
            for backup in backups:
                size_mb = backup['size'] / (1024 * 1024)
                backup_type = backup['metadata'].get('backup_type', 'unknown')
                print(f"{backup['file'].name:<40} {size_mb:>8.1f}MB {backup['created'].strftime('%Y-%m-%d %H:%M'):<20} {backup_type:<15}")
    
    elif args.command == 'restore':
        backup_path = Path(args.backup_file)
        if not backup_path.is_absolute():
            backup_path = backup_manager.backup_dir / backup_path
        backup_manager.restore_backup(backup_path, args.confirm)
    
    elif args.command == 'cleanup':
        removed = backup_manager.cleanup_old_backups(args.keep_days, args.keep_count)
        print(f"Removed {removed} old backups")
    
    elif args.command == 'verify':
        backup_path = Path(args.backup_file)
        if not backup_path.is_absolute():
            backup_path = backup_manager.backup_dir / backup_path
        backup_manager.verify_backup(backup_path)
    
    elif args.command == 'daily':
        backup_manager.create_backup('daily', 'Automated daily backup')
        backup_manager.cleanup_old_backups(30, 10)

if __name__ == "__main__":
    main()
