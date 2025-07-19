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

# Database configuration
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")  # "sqlite" or "azure_sql"

# SQLite Database configuration
SQLITE_DB_FILE = os.getenv("SQLITE_DB_FILE", "marketdata.db")
SQLITE_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", os.path.join(SQLITE_BASE_DIR, 'database', SQLITE_DB_FILE))

# Azure SQL Database configuration
AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER")
AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE")
AZURE_SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME")
AZURE_SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD")
AZURE_SQL_PORT = int(os.getenv("AZURE_SQL_PORT", "1433"))

class Config:
    # Use environment variables with fallback defaults
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ROOT_PATH = os.path.dirname(BASE_DIR)  # Path to project root
    DATABASE_PATH = SQLITE_DB_PATH  # Use the new SQLite configuration

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_UPLOAD_SIZE", "500")) * 1024 * 1024  # Convert MB to bytes

class esmaConfig:
    # Use environment variables with fallback defaults
    file_path = Path(os.getenv("ESMA_DATA_PATH", "downloads/esma"))  # Path to ESMA data directory
    start_date = os.getenv("ESMA_START_DATE", "2025-04-26")  # Start date for data processing
    end_date = os.getenv("ESMA_END_DATE", "2025-04-26")      # End date for data processing

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