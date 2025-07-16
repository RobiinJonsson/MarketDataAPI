import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging
from dataclasses import dataclass
from ..config import esmaConfig

logger = logging.getLogger(__name__)

@dataclass
class FileInfo:
    name: str
    path: str
    size: int
    created: datetime
    modified: datetime
    file_type: str  # 'firds' or 'fitrs'
    dataset_type: str  # 'FULINS_E', 'FULINS_D', etc.

@dataclass
class FileManagementConfig:
    base_path: Path
    retention_days: int = 30
    max_files_per_type: int = 100
    auto_cleanup: bool = True

class FileManagementService:
    def __init__(self, config: Optional[FileManagementConfig] = None):
        self.config = config or FileManagementConfig(
            base_path=esmaConfig.file_path,
            retention_days=30,
            max_files_per_type=100
        )
        self.logger = logging.getLogger(__name__)
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure the required directory structure exists."""
        esma_dir = self.config.base_path
        fitrs_dir = esma_dir / "fitrs"
        
        for directory in [esma_dir, fitrs_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def get_files_by_type(self, file_type: str) -> List[FileInfo]:
        """Get all files of a specific type (firds or fitrs)."""
        if file_type == 'firds':
            folder_path = self.config.base_path
        elif file_type == 'fitrs':
            folder_path = self.config.base_path / "fitrs"
        else:
            raise ValueError(f"Unknown file type: {file_type}")

        if not folder_path.exists():
            return []

        files = []
        for file_path in folder_path.iterdir():
            if file_path.is_file() and file_path.suffix in ['.csv', '.pickle']:
                try:
                    stat = file_path.stat()
                    dataset_type = self._extract_dataset_type(file_path.name)
                    
                    files.append(FileInfo(
                        name=file_path.name,
                        path=str(file_path),
                        size=stat.st_size,
                        created=datetime.fromtimestamp(stat.st_ctime),
                        modified=datetime.fromtimestamp(stat.st_mtime),
                        file_type=file_type,
                        dataset_type=dataset_type
                    ))
                except Exception as e:
                    self.logger.warning(f"Error processing file {file_path}: {e}")

        return sorted(files, key=lambda f: f.modified, reverse=True)

    def _extract_dataset_type(self, filename: str) -> str:
        """Extract dataset type from filename."""
        # Map common patterns in cached filenames to dataset types
        if 'FULINS_E' in filename or 'equity' in filename.lower():
            return 'FULINS_E'
        elif 'FULINS_D' in filename or 'debt' in filename.lower():
            return 'FULINS_D'
        elif 'FULINS_F' in filename or 'future' in filename.lower():
            return 'FULINS_F'
        elif 'FITRS' in filename or 'fitrs' in filename.lower():
            return 'FITRS'
        elif 'DVCAP' in filename or 'dvcap' in filename.lower():
            return 'DVCAP'
        else:
            return 'UNKNOWN'

    def get_all_files(self) -> Dict[str, List[FileInfo]]:
        """Get all files organized by type."""
        return {
            'firds': self.get_files_by_type('firds'),
            'fitrs': self.get_files_by_type('fitrs')
        }

    def get_storage_stats(self) -> Dict[str, Dict[str, any]]:
        """Get storage statistics for each file type."""
        stats = {}
        
        for file_type in ['firds', 'fitrs']:
            files = self.get_files_by_type(file_type)
            total_size = sum(f.size for f in files)
            
            stats[file_type] = {
                'count': len(files),
                'total_size': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'oldest_file': min(files, key=lambda f: f.modified) if files else None,
                'newest_file': max(files, key=lambda f: f.modified) if files else None
            }
        
        return stats

    def cleanup_old_files(self, file_type: Optional[str] = None, dry_run: bool = False) -> Dict[str, int]:
        """Remove old files based on retention policy."""
        cutoff_date = datetime.now() - timedelta(days=self.config.retention_days)
        removed_count = {'firds': 0, 'fitrs': 0}
        
        file_types = [file_type] if file_type else ['firds', 'fitrs']
        
        for ftype in file_types:
            files = self.get_files_by_type(ftype)
            
            # Remove files older than retention period
            for file_info in files:
                if file_info.modified < cutoff_date:
                    if not dry_run:
                        try:
                            os.remove(file_info.path)
                            removed_count[ftype] += 1
                            self.logger.info(f"Removed old file: {file_info.name}")
                        except Exception as e:
                            self.logger.error(f"Error removing file {file_info.name}: {e}")
                    else:
                        removed_count[ftype] += 1
            
            # Remove excess files if over limit
            if len(files) > self.config.max_files_per_type:
                excess_files = files[self.config.max_files_per_type:]
                for file_info in excess_files:
                    if not dry_run:
                        try:
                            os.remove(file_info.path)
                            removed_count[ftype] += 1
                            self.logger.info(f"Removed excess file: {file_info.name}")
                        except Exception as e:
                            self.logger.error(f"Error removing excess file {file_info.name}: {e}")
                    else:
                        removed_count[ftype] += 1
        
        return removed_count

    def delete_file(self, file_path: str) -> bool:
        """Delete a specific file."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                self.logger.info(f"Deleted file: {file_path}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error deleting file {file_path}: {e}")
            return False

    def delete_files_by_pattern(self, pattern: str, file_type: Optional[str] = None) -> int:
        """Delete files matching a pattern."""
        deleted_count = 0
        file_types = [file_type] if file_type else ['firds', 'fitrs']
        
        for ftype in file_types:
            files = self.get_files_by_type(ftype)
            for file_info in files:
                if pattern in file_info.name:
                    if self.delete_file(file_info.path):
                        deleted_count += 1
        
        return deleted_count

    def organize_files(self) -> Dict[str, int]:
        """Organize files into proper subdirectories."""
        organized_count = {'firds': 0, 'fitrs': 0}
        
        # Check for misplaced files and move them
        base_path = self.config.base_path
        fitrs_path = base_path / "fitrs"
        
        for file_path in base_path.iterdir():
            if file_path.is_file():
                filename = file_path.name.lower()
                
                # Move FITRS files to fitrs subdirectory
                if 'fitrs' in filename or 'transparency' in filename:
                    target_path = fitrs_path / file_path.name
                    try:
                        shutil.move(str(file_path), str(target_path))
                        organized_count['fitrs'] += 1
                        self.logger.info(f"Moved {file_path.name} to fitrs directory")
                    except Exception as e:
                        self.logger.error(f"Error moving file {file_path.name}: {e}")
        
        return organized_count

    def get_file_management_summary(self) -> Dict[str, any]:
        """Get a comprehensive summary of file management status."""
        stats = self.get_storage_stats()
        
        # Calculate cleanup recommendations
        cutoff_date = datetime.now() - timedelta(days=self.config.retention_days)
        cleanup_candidates = {'firds': 0, 'fitrs': 0}
        
        for file_type in ['firds', 'fitrs']:
            files = self.get_files_by_type(file_type)
            cleanup_candidates[file_type] = len([f for f in files if f.modified < cutoff_date])
        
        return {
            'storage_stats': stats,
            'cleanup_candidates': cleanup_candidates,
            'retention_policy': {
                'retention_days': self.config.retention_days,
                'max_files_per_type': self.config.max_files_per_type,
                'auto_cleanup': self.config.auto_cleanup
            }
        }
