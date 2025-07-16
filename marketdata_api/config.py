import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

load_dotenv()  # Load environment variables from .env file

OPENFIGI_API_KEY = os.getenv("OPENFIGI_API_KEY")
FLASK_ENV = os.getenv("FLASK_ENV", "production")
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

class Config:
    # Use environment variables with fallback defaults
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ROOT_PATH = os.path.dirname(BASE_DIR)  # Path to project root
    DATABASE_PATH = os.getenv("DATABASE_PATH", os.path.join(BASE_DIR, 'database', 'marketdata.db'))

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_UPLOAD_SIZE", "500")) * 1024 * 1024  # Convert MB to bytes

class esmaConfig:
    # Use environment variables with fallback defaults
    # Updated to point to the actual downloads folder structure
    downloads_path = Path(os.getenv("DOWNLOADS_PATH", r"C:\Users\robin\Projects\MarketDataAPI\downloads"))
    file_path = downloads_path / "esma"  # For FIRDS files
    fitrs_path = downloads_path / "fitrs"  # For FITRS files
    
    start_date = os.getenv("ESMA_START_DATE", "2025-04-26")  # Start date for data processing
    end_date = os.getenv("ESMA_END_DATE", "2025-04-26")      # End date for data processing
    
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
    'US': 'US',  # United States
    'CA': 'CN',  # Canada
    
    # Europe
    'GB': 'LN',  # United Kingdom (London)
    'DE': 'GR',  # Germany (Xetra)
    'FR': 'FP',  # France (Euronext Paris)
    'NL': 'NA',  # Netherlands (Euronext Amsterdam)
    'BE': 'BR',  # Belgium (Euronext Brussels)
    'IT': 'IM',  # Italy (Borsa Italiana)
    'ES': 'MC',  # Spain (Madrid)
    'SE': 'SS',  # Sweden (Stockholm)
    'CH': 'SW',  # Switzerland (SIX)
    'DK': 'DC',  # Denmark (Copenhagen)
    'FI': 'FH',  # Finland (Helsinki)
    'NO': 'OL',  # Norway (Oslo)
    'AT': 'VI',  # Austria (Vienna)
    'IE': 'IR',  # Ireland (Dublin)
    
    # Nordics
    'IS': 'IC',  # Iceland
    
    # Other European
    'PT': 'LS',  # Portugal (Lisbon)
    'GR': 'AT',  # Greece (Athens)
    'PL': 'WA',  # Poland (Warsaw)
    'CZ': 'PR',  # Czech Republic (Prague)
    'HU': 'BU',  # Hungary (Budapest)

    # Other
    'XS': 'XS',  # Global (SIX Swiss Exchange)
    'XX': 'XX',  # Global (Global Market)
    'OTC': 'OTC',  # Over-the-Counter
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