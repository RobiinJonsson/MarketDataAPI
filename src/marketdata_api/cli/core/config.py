"""
CLI-specific configuration and settings.
"""
import os
from pathlib import Path


class CLIConfig:
    """Configuration settings for the CLI."""
    
    # Database settings
    SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', 'marketdata-sqlite-dev.db')
    
    # Output settings
    DEFAULT_LIMIT = 20
    MAX_DISPLAY_ITEMS = 100
    
    # Formatting settings
    DATE_FORMAT = '%Y-%m-%d'
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    # CLI behavior
    VERBOSE_DEFAULT = False
    FORMAT_DEFAULT = 'table'
    
    @classmethod
    def get_database_path(cls):
        """Get the database path, ensuring directory exists."""
        path = Path(cls.SQLITE_DB_PATH)
        path.parent.mkdir(parents=True, exist_ok=True)
        return str(path)
    
    @classmethod
    def is_test_mode(cls):
        """Check if running in test mode."""
        return bool(os.getenv("MARKETDATA_TEST_MODE"))