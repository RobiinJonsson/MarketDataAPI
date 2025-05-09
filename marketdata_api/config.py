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
    # Use an absolute path or relative path
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'marketdata.db')  # Adjust path as needed

    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500 MB max file size

class esmaConfig:
    # Convert string path to Path object
    file_path = Path("C:\\Users\\robin\\Projects\\MarketDataAPI\\downloads\\esma") # Path to ESMA data directory
    start_date = "2025-04-26"  # Start date for data processing
    end_date = "2025-04-26"    # End date for data processing

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
DEFAULT_EXCHANGE_CODE = 'SS'

# Schema configuration for handling different financial instruments as requested by application formats
class FieldType(Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    DATE = "date"
    ENUM = "enum"

@dataclass
class SchemaField:
    name: str
    field_type: FieldType
    required: bool
    description: str
    validation_rules: Optional[Dict[str, Any]] = None
    enum_values: Optional[List[str]] = None

@dataclass
class SchemaDefinition:
    name: str
    description: str
    version: str
    fields: List[SchemaField]
    extends: Optional[str] = None  # Name of schema to extend
    custom_validators: Optional[Dict[str, Any]] = None

# Schema Registry - defines all supported schemas
SCHEMA_REGISTRY = {
    "firds_e": SchemaDefinition(
        name="firds_e",
        description="FIRDS European schema for instrument data",
        version="1.0",
        fields=[
            SchemaField(
                name="identifier",
                field_type=FieldType.STRING,
                required=True,
                description="Unique identifier for the instrument (ISIN, FIGI, etc.)"
            ),
            SchemaField(
                name="full_name",
                field_type=FieldType.STRING,
                required=True,
                description="Full name of the instrument"
            ),
            SchemaField(
                name="short_name",
                field_type=FieldType.STRING,
                required=True,
                description="Short name or ticker symbol"
            ),
            SchemaField(
                name="classification_type",
                field_type=FieldType.STRING,
                required=True,
                description="Classification type (e.g., CFICode)"
            ),
            SchemaField(
                name="currency",
                field_type=FieldType.STRING,
                required=False,
                description="Currency of the instrument"
            ),
            SchemaField(
                name="issuer_lei",
                field_type=FieldType.STRING,
                required=False,
                description="Legal Entity Identifier of the issuer"
            ),
            SchemaField(
                name="trading_venue_id",
                field_type=FieldType.STRING,
                required=False,
                description="Trading venue identifier"
            )
        ]
    ),
    "equity": SchemaDefinition(
        name="equity",
        description="Schema for equity instruments",
        version="1.0",
        extends="firds_e",  # Inherits from firds_e schema
        fields=[
            SchemaField(
                name="market_cap",
                field_type=FieldType.NUMBER,
                required=False,
                description="Market capitalization"
            ),
            SchemaField(
                name="dividend_yield",
                field_type=FieldType.NUMBER,
                required=False,
                description="Dividend yield percentage"
            )
        ]
    ),
    "bond": SchemaDefinition(
        name="bond",
        description="Schema for bond instruments",
        version="1.0",
        extends="firds_e",  # Inherits from firds_e schema
        fields=[
            SchemaField(
                name="coupon_rate",
                field_type=FieldType.NUMBER,
                required=True,
                description="Annual coupon rate"
            ),
            SchemaField(
                name="maturity_date",
                field_type=FieldType.DATE,
                required=True,
                description="Bond maturity date"
            )
        ]
    )
}

# Define mapping between schema fields and database columns
SCHEMA_TO_DB_MAPPING = {
    "identifier": "ISIN",
    "currency": "Currency",
    "full_name": "FullName",
    "short_name": "ShortName",
    "classification_type": "CFICode",
    "issuer_lei": "IssuerLEI",
    "trading_venue_id": "TradingVenueId"
}