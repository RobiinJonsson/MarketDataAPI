import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

# Load .env file from project root, regardless of current working directory
# Handle both development (source) and installed package scenarios
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# For installed packages, we need to look for the .env in common project locations
possible_env_locations = [
    os.path.join(PROJECT_ROOT, ".env"),  # Development: from source
    os.path.join(os.getcwd(), ".env"),  # Current working directory
    "C:\\Users\\robin\\Projects\\MarketDataAPI\\.env",  # Hardcoded fallback for this project
]

# Try to load from the first available location
for env_path in possible_env_locations:
    if os.path.exists(env_path):
        load_dotenv(env_path, override=True)  # Override existing env vars
        break
else:
    # No .env found, proceed with system environment variables only
    load_dotenv()

OPENFIGI_API_KEY = os.getenv("OPENFIGI_API_KEY")
FLASK_ENV = os.getenv("FLASK_ENV", "production")
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "1"))  # hours
JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "168"))  # hours (7 days)
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Database configuration
# Note: DATABASE_TYPE is dynamically evaluated to allow runtime changes
def get_database_type_from_env():
    """Get database type from environment, allowing runtime changes."""
    return os.getenv("DATABASE_TYPE", "sqlite").lower()

# SQLite Database configuration
SQLITE_DB_FILE = os.getenv("SQLITE_DB_FILE", "marketdata-sqlite-dev.db")
SQLITE_DB_PATH = os.getenv(
    "SQLITE_DB_PATH",
    os.path.join(PROJECT_ROOT, "src", "marketdata_api", "database", SQLITE_DB_FILE),
)

# Azure SQL Database configuration
AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER")
AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE")
AZURE_SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME")
AZURE_SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD")
AZURE_SQL_PORT = int(os.getenv("AZURE_SQL_PORT", "1433"))
AZURE_SQL_AUTH_METHOD = os.getenv("AZURE_SQL_AUTH_METHOD", "sql")  # "sql" or "entra"


class Config:
    # Use environment variables with fallback defaults
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ROOT_PATH = PROJECT_ROOT  # Use the same project root calculation

    # Make database path absolute and relative to project root
    _db_path = os.getenv("SQLITE_DB_PATH", "src/marketdata_api/database/marketdata-sqlite-dev.db")
    DATABASE_PATH = _db_path if os.path.isabs(_db_path) else os.path.join(ROOT_PATH, _db_path)

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH = (
        int(os.getenv("MAX_UPLOAD_SIZE", "500")) * 1024 * 1024
    )  # Convert MB to bytes


class esmaConfig:
    # Use environment variables with fallback defaults
    # Updated to point to the actual downloads folder structure
    downloads_path = Path(
        os.getenv("DOWNLOADS_PATH", r"C:\Users\robin\Projects\MarketDataAPI\data\downloads")
    )
    firds_path = downloads_path / "firds"  # For FIRDS files
    fitrs_path = downloads_path / "fitrs"  # For FITRS files

    # Backward compatibility - some code might still reference file_path
    file_path = firds_path

    start_date = os.getenv("ESMA_START_DATE", "2025-04-26")  # Start date for data processing
    end_date = os.getenv("ESMA_END_DATE", "2025-04-26")  # End date for data processing

    # File management settings
    retention_days = int(os.getenv("ESMA_RETENTION_DAYS", "30"))  # Days to keep files
    max_files_per_type = int(os.getenv("ESMA_MAX_FILES_PER_TYPE", "100"))  # Max files per type
    auto_cleanup = os.getenv("ESMA_AUTO_CLEANUP", "true").lower() == "true"  # Auto cleanup enabled

    # Azure storage settings for future use
    azure_storage_account = os.getenv("AZURE_STORAGE_ACCOUNT")
    azure_container_name = os.getenv("AZURE_CONTAINER_NAME", "marketdata-files")
    azure_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")


# Exchange code mappings for OpenFIGI
EXCHANGE_CODES = {
    # North America
    "US": "US",  # United States
    "CA": "CN",  # Canada
    # Europe
    "GB": "LN",  # United Kingdom (London)
    "DE": "GR",  # Germany (Xetra)
    "FR": "FP",  # France (Euronext Paris)
    "NL": "NA",  # Netherlands (Euronext Amsterdam)
    "BE": "BR",  # Belgium (Euronext Brussels)
    "IT": "IM",  # Italy (Borsa Italiana)
    "ES": "MC",  # Spain (Madrid)
    "SE": "SS",  # Sweden (Stockholm)
    "CH": "SW",  # Switzerland (SIX)
    "DK": "DC",  # Denmark (Copenhagen)
    "FI": "FH",  # Finland (Helsinki)
    "NO": "OL",  # Norway (Oslo)
    "AT": "VI",  # Austria (Vienna)
    "IE": "IR",  # Ireland (Dublin)
    # Nordics
    "IS": "IC",  # Iceland
    # Other European
    "PT": "LS",  # Portugal (Lisbon)
    "GR": "AT",  # Greece (Athens)
    "PL": "WA",  # Poland (Warsaw)
    "CZ": "PR",  # Czech Republic (Prague)
    "HU": "BU",  # Hungary (Budapest)
    # Other
    "XS": "XS",  # Global (SIX Swiss Exchange)
    "XX": "XX",  # Global (Global Market)
    "OTC": "OTC",  # Over-the-Counter
}

# Default exchange code if no country code is provided
DEFAULT_EXCHANGE_CODE = os.getenv("DEFAULT_EXCHANGE_CODE", "SS")

# Update SCHEMA_REGISTRY to use new mapping system
from .schema.schema_mapper import SchemaMapper

schema_mapper = SchemaMapper()
SCHEMA_REGISTRY = schema_mapper.mappings

# Keep the mapping dictionary for backward compatibility
SCHEMA_TO_DB_MAPPING = {
    "identifier": "isin",
    "full_name": "full_name",
    "short_name": "short_name",
    "currency": "currency",
    "trading_venue": "trading_venue",
    # ...existing mappings...
}


# Database factory configuration for dual database support
class DatabaseConfig:
    """Configuration for database selection and factory pattern."""

    @staticmethod
    def get_database_type() -> str:
        """Get the current database type from environment."""
        return get_database_type_from_env()

    @staticmethod
    def is_sql_server() -> bool:
        """Check if we're using SQL Server/Azure SQL."""
        db_type = DatabaseConfig.get_database_type()
        return db_type in ["azure_sql", "sqlserver", "mssql"]

    @staticmethod
    def is_sqlite() -> bool:
        """Check if we're using SQLite."""
        return DatabaseConfig.get_database_type() == "sqlite"

    @staticmethod
    def get_appropriate_service():
        """Get the appropriate service based on database type."""
        from .interfaces.factory.services_factory import ServicesFactory

        return ServicesFactory.get_instrument_service()

    @staticmethod
    def get_appropriate_database():
        """Get the appropriate database implementation."""
        db_type = DatabaseConfig.get_database_type()

        if db_type == "sqlite":
            from .database.sqlite.sqlite_database import SqliteDatabase

            return SqliteDatabase()
        elif db_type in ["sqlserver", "azure_sql", "mssql"]:
            from .database.sqlserver.sql_server_database import SqlServerDatabase

            return SqlServerDatabase()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")


# Backward compatibility - keep existing database configuration
def get_database_config():
    """Get database configuration for backward compatibility."""
    return {
        "type": get_database_type_from_env(),
        "sqlite_path": SQLITE_DB_PATH,
        "azure_sql": {
            "server": AZURE_SQL_SERVER,
            "database": AZURE_SQL_DATABASE,
            "username": AZURE_SQL_USERNAME,
            "port": AZURE_SQL_PORT,
        },
    }
