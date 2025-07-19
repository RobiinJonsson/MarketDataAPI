import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging
from dataclasses import dataclass
import pandas as pd
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
class ESMAFileInfo:
    """Extended file info for ESMA files from the registry."""
    file_name: str
    download_link: str
    file_type: str
    publication_date: str
    creation_date: str
    instrument_type: Optional[str] = None
    file_size: Optional[int] = None
    
@dataclass
class FileManagementConfig:
    base_path: Path
    retention_days: int = 30
    max_files_per_type: int = 100
    auto_cleanup: bool = True

class FileManagementService:
    def __init__(self, config: Optional[FileManagementConfig] = None):
        self.config = config or FileManagementConfig(
            base_path=esmaConfig.firds_path,
            retention_days=esmaConfig.retention_days,
            max_files_per_type=esmaConfig.max_files_per_type
        )
        self.logger = logging.getLogger(__name__)
        self._ensure_directories()
        self._esma_loader = None
        
    def _get_esma_loader(self):
        """Lazy initialization of ESMA data loader."""
        if self._esma_loader is None:
            from .esma_data_loader import EsmaDataLoader
            self._esma_loader = EsmaDataLoader()
        return self._esma_loader

    def _ensure_directories(self):
        """Ensure the required directory structure exists."""
        firds_dir = self.config.base_path
        fitrs_dir = esmaConfig.fitrs_path
        
        for directory in [firds_dir, fitrs_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def get_files_by_type(self, file_type: str) -> List[FileInfo]:
        """Get all files of a specific type (firds or fitrs)."""
        if file_type == 'firds':
            folder_path = self.config.base_path
        elif file_type == 'fitrs':
            folder_path = esmaConfig.fitrs_path
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
        filename_upper = filename.upper()
        
        # Check for specific patterns in cached filenames
        if 'FULINS_E' in filename_upper or 'EQUITY' in filename_upper:
            return 'FULINS_E'
        elif 'FULINS_D' in filename_upper or 'DEBT' in filename_upper:
            return 'FULINS_D'
        elif 'FULINS_F' in filename_upper or 'FUTURE' in filename_upper:
            return 'FULINS_F'
        elif 'FULINS_C' in filename_upper:
            return 'FULINS_C'
        elif 'DELVINS' in filename_upper or 'DELTA' in filename_upper:
            return 'DELVINS'
        elif 'FITRS' in filename_upper or 'TRANSPARENCY' in filename_upper:
            return 'FITRS'
        elif 'FULNCR' in filename_upper or 'FULECR' in filename_upper:
            return 'FITRS'
        elif 'DVCAP' in filename_upper or 'VOLUME' in filename_upper or 'DVCRES' in filename_upper:
            return 'DVCAP'
        # Check for hash-based cached files by looking at file extension and length
        elif filename.endswith('.csv') and len(filename) == 36:  # MD5 hash + .csv
            # This is likely a cached file, determine type by location and context
            return 'CACHED_DATA'
        elif filename.endswith('.pickle'):
            return 'CACHED_DATA'
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
        fitrs_path = esmaConfig.fitrs_path
        
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

    def get_files_with_filters(self, 
                              file_type: Optional[str] = None,
                              dataset_type: Optional[str] = None,
                              date_from: Optional[str] = None,
                              date_to: Optional[str] = None,
                              limit: Optional[int] = None) -> List[FileInfo]:
        """Get files with conditional filters."""
        
        # Get all files or specific type
        if file_type:
            all_files = self.get_files_by_type(file_type)
        else:
            all_files_dict = self.get_all_files()
            all_files = []
            for files in all_files_dict.values():
                all_files.extend(files)
        
        # Apply filters
        filtered_files = all_files
        
        if dataset_type:
            filtered_files = [f for f in filtered_files if f.dataset_type == dataset_type]
        
        if date_from:
            date_from_dt = datetime.strptime(date_from, '%Y-%m-%d')
            filtered_files = [f for f in filtered_files if f.modified >= date_from_dt]
        
        if date_to:
            date_to_dt = datetime.strptime(date_to, '%Y-%m-%d')
            filtered_files = [f for f in filtered_files if f.modified <= date_to_dt]
        
        # Sort by modification date (newest first)
        filtered_files.sort(key=lambda x: x.modified, reverse=True)
        
        if limit:
            filtered_files = filtered_files[:limit]
            
        return filtered_files
    
    def get_available_esma_files(self,
                                datasets: List[str] = ['firds', 'fitrs'],
                                date_from: Optional[str] = None,
                                date_to: Optional[str] = None,
                                file_type: Optional[str] = None) -> List[ESMAFileInfo]:
        """Get list of available ESMA files from the registry."""
        
        try:
            loader = self._get_esma_loader()
            
            # Set date range if provided
            if date_from:
                loader.creation_date_from = date_from
            if date_to:
                loader.creation_date_to = date_to
                
            # Load file list from ESMA
            files_df = loader.load_mifid_file_list(datasets)
            
            if files_df.empty:
                return []
            
            # Apply additional filters
            if file_type:
                files_df = files_df[files_df['file_name'].str.contains(file_type, case=False, na=False)]
                
            # Convert to ESMAFileInfo objects
            esma_files = []
            for _, row in files_df.iterrows():
                esma_file = ESMAFileInfo(
                    file_name=row.get('file_name', ''),
                    download_link=row.get('download_link', ''),
                    file_type=self._determine_esma_file_type(row.get('file_name', '')),
                    publication_date=row.get('publication_date', ''),
                    creation_date=row.get('creation_date', ''),
                    instrument_type=row.get('instrument_type', None),
                    file_size=row.get('file_size', None)
                )
                esma_files.append(esma_file)
                
            return esma_files
            
        except Exception as e:
            self.logger.error(f"Error getting ESMA files: {e}")
            return []
    
    def _determine_esma_file_type(self, filename: str) -> str:
        """Determine ESMA file type from filename."""
        filename_upper = filename.upper()
        
        if any(pattern in filename_upper for pattern in ['FULINS', 'DELVINS']):
            return 'firds'
        elif any(pattern in filename_upper for pattern in ['FULNCR', 'FULECR']):
            return 'fitrs'
        elif 'DVCAP' in filename_upper or 'DVCRES' in filename_upper:
            return 'firds'  # DVCAP goes to firds folder
        else:
            return 'unknown'
    
    def download_and_parse_files(self, urls: List[str], force_update: bool = False) -> Dict[str, any]:
        """Download and parse multiple ESMA files."""
        
        results = {
            'success': [],
            'failed': [],
            'skipped': []
        }
        
        loader = self._get_esma_loader()
        
        for url in urls:
            try:
                self.logger.info(f"Processing URL: {url}")
                
                # Check if file already exists (unless force_update)
                from .esma_utils import Utils
                filename = Utils.extract_file_name_from_url(url)
                file_type = self._determine_esma_file_type(filename)
                
                if file_type == 'firds':
                    expected_path = esmaConfig.firds_path / f"{filename}_firds_data.csv"
                elif file_type == 'fitrs':
                    expected_path = esmaConfig.fitrs_path / f"{filename}_fitrs_data.csv"
                else:
                    expected_path = esmaConfig.firds_path / f"{filename}_data.csv"
                
                if expected_path.exists() and not force_update:
                    results['skipped'].append({
                        'url': url,
                        'filename': filename,
                        'reason': 'File already exists',
                        'path': str(expected_path)
                    })
                    continue
                
                # Download and parse
                df = loader.download_file(url, update=force_update)
                
                if df is not None and not df.empty:
                    results['success'].append({
                        'url': url,
                        'filename': filename,
                        'records': len(df),
                        'path': str(expected_path),
                        'size_mb': round(expected_path.stat().st_size / (1024*1024), 2) if expected_path.exists() else 0
                    })
                else:
                    results['failed'].append({
                        'url': url,
                        'filename': filename,
                        'error': 'Empty or invalid DataFrame'
                    })
                    
            except Exception as e:
                results['failed'].append({
                    'url': url,
                    'filename': filename if 'filename' in locals() else 'unknown',
                    'error': str(e)
                })
                self.logger.error(f"Error processing {url}: {e}")
        
        return results
    
    def get_file_stats_by_criteria(self, 
                                  dataset_types: Optional[List[str]] = None,
                                  file_types: Optional[List[str]] = None) -> Dict[str, any]:
        """Get detailed statistics with filtering criteria."""
        
        all_files = self.get_all_files()
        
        stats = {
            'total_files': 0,
            'total_size_mb': 0,
            'by_dataset_type': {},
            'by_file_type': {},
            'oldest_file': None,
            'newest_file': None,
            'files_by_date': {}
        }
        
        # Flatten all files
        flat_files = []
        for files in all_files.values():
            flat_files.extend(files)
        
        # Apply filters
        if dataset_types:
            flat_files = [f for f in flat_files if f.dataset_type in dataset_types]
        if file_types:
            flat_files = [f for f in flat_files if f.file_type in file_types]
        
        if not flat_files:
            return stats
        
        # Calculate statistics
        stats['total_files'] = len(flat_files)
        stats['total_size_mb'] = round(sum(f.size for f in flat_files) / (1024*1024), 2)
        
        # Group by dataset type
        for file_info in flat_files:
            dataset = file_info.dataset_type
            if dataset not in stats['by_dataset_type']:
                stats['by_dataset_type'][dataset] = {'count': 0, 'size_mb': 0}
            stats['by_dataset_type'][dataset]['count'] += 1
            stats['by_dataset_type'][dataset]['size_mb'] += round(file_info.size / (1024*1024), 2)
        
        # Group by file type
        for file_info in flat_files:
            ftype = file_info.file_type
            if ftype not in stats['by_file_type']:
                stats['by_file_type'][ftype] = {'count': 0, 'size_mb': 0}
            stats['by_file_type'][ftype]['count'] += 1
            stats['by_file_type'][ftype]['size_mb'] += round(file_info.size / (1024*1024), 2)
        
        # Find oldest and newest
        sorted_files = sorted(flat_files, key=lambda x: x.modified)
        stats['oldest_file'] = {
            'name': sorted_files[0].name,
            'modified': sorted_files[0].modified.isoformat(),
            'size_mb': round(sorted_files[0].size / (1024*1024), 2)
        }
        stats['newest_file'] = {
            'name': sorted_files[-1].name,
            'modified': sorted_files[-1].modified.isoformat(),
            'size_mb': round(sorted_files[-1].size / (1024*1024), 2)
        }
        
        # Group by date
        for file_info in flat_files:
            date_str = file_info.modified.strftime('%Y-%m-%d')
            if date_str not in stats['files_by_date']:
                stats['files_by_date'][date_str] = 0
            stats['files_by_date'][date_str] += 1
        
        return stats

    def download_by_criteria(self,
                            file_type: str,  # 'firds' or 'fitrs' - mandatory
                            dataset: Optional[str] = None,  # e.g., 'FULINS_E', 'FULINS_D', etc.
                            date: Optional[str] = None,  # specific date or None for config default
                            date_range: Optional[Tuple[str, str]] = None,  # (start_date, end_date)
                            force_update: bool = False) -> Dict[str, any]:
        """
        Download and parse files based on criteria.
        
        Args:
            file_type: 'firds' or 'fitrs' (mandatory)
            dataset: Dataset type like 'FULINS_E', 'FULINS_D', etc.
            date: Specific date (YYYY-MM-DD) or None for config default
            date_range: Tuple of (start_date, end_date) for range, uses latest if provided
            force_update: Whether to re-download existing files
            
        Returns:
            Dict with download results and file info
        """
        
        try:
            loader = self._get_esma_loader()
            
            # Determine date range for search
            if date_range:
                date_from, date_to = date_range
                use_latest = True  # For ranges, we'll get the latest file
            elif date:
                date_from = date_to = date
                use_latest = False
            else:
                # Use config defaults
                from ..config import esmaConfig
                date_from = esmaConfig.start_date
                date_to = esmaConfig.end_date
                use_latest = False
            
            self.logger.info(f"Searching for {file_type} files from {date_from} to {date_to}")
            
            # Set loader date range
            original_from = loader.creation_date_from
            original_to = loader.creation_date_to
            loader.creation_date_from = date_from
            loader.creation_date_to = date_to
            
            try:
                # Get available files
                if file_type.lower() == 'firds':
                    datasets = ['firds']
                elif file_type.lower() == 'fitrs':
                    datasets = ['fitrs']
                else:
                    raise ValueError(f"Invalid file_type: {file_type}. Must be 'firds' or 'fitrs'")
                
                files_df = loader.load_mifid_file_list(datasets)
                
                if files_df.empty:
                    return {
                        'success': False,
                        'message': f'No {file_type} files found for date range {date_from} to {date_to}',
                        'files_processed': 0,
                        'files_downloaded': [],
                        'files_skipped': []
                    }
                
                # Filter by dataset if specified
                if dataset:
                    dataset_patterns = {
                        'FULINS_E': ['FULINS.*_E_', 'equity'],
                        'FULINS_D': ['FULINS.*_D_', 'debt'], 
                        'FULINS_F': ['FULINS.*_F_', 'future'],
                        'FULINS_C': ['FULINS.*_C_'],
                        'DELVINS': ['DELVINS'],
                        'FITRS': ['FULNCR', 'FULECR'],
                        'DVCAP': ['DVCAP', 'DVCRES']
                    }
                    
                    if dataset in dataset_patterns:
                        pattern_filter = '|'.join(dataset_patterns[dataset])
                        files_df = files_df[files_df['file_name'].str.contains(pattern_filter, case=False, na=False)]
                        
                        if files_df.empty:
                            return {
                                'success': False,
                                'message': f'No {file_type} files found for dataset {dataset} in date range {date_from} to {date_to}',
                                'files_processed': 0,
                                'files_downloaded': [],
                                'files_skipped': []
                            }
                
                # If date_range provided, get only the latest file
                if use_latest and len(files_df) > 1:
                    # Sort by publication_date or creation_date and take the most recent
                    date_col = 'publication_date' if 'publication_date' in files_df.columns else 'creation_date'
                    files_df = files_df.sort_values(date_col, ascending=False).head(1)
                    self.logger.info(f"Using latest file from range: {files_df.iloc[0]['file_name']}")
                
                # Download the selected files
                urls = files_df['download_link'].tolist()
                download_results = self.download_and_parse_files(urls, force_update=force_update)
                
                # Prepare response
                result = {
                    'success': True,
                    'message': f'Processed {len(urls)} {file_type} files',
                    'files_processed': len(urls),
                    'criteria': {
                        'file_type': file_type,
                        'dataset': dataset,
                        'date': date,
                        'date_range': date_range,
                        'force_update': force_update
                    },
                    'date_range_used': {
                        'from': date_from,
                        'to': date_to,
                        'latest_only': use_latest
                    },
                    'files_downloaded': download_results['success'],
                    'files_skipped': download_results['skipped'],
                    'files_failed': download_results['failed']
                }
                
                return result
                
            finally:
                # Restore original date range
                loader.creation_date_from = original_from
                loader.creation_date_to = original_to
                
        except Exception as e:
            self.logger.error(f"Error in download_by_criteria: {e}")
            return {
                'success': False,
                'message': f'Error: {str(e)}',
                'files_processed': 0,
                'files_downloaded': [],
                'files_skipped': []
            }
