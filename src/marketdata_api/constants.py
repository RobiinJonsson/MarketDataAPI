# Backend Constants - Centralized configuration for all route constants
"""
Backend constants for MarketDataAPI routes.
Centralizes hardcoded values, HTTP status codes, default values, and error messages.
"""


# HTTP Status Codes
class HTTPStatus:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500


# Default Pagination Values
class Pagination:
    DEFAULT_LIMIT = 100
    DEFAULT_OFFSET = 0
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE = 100
    MAX_BATCH_SIZE = 100


# API Version and Info
class API:
    VERSION = "1.0"
    PREFIX = "/api/v1"
    NAME = "MarketDataAPI CRUD API"


# Batch Operations
class BatchOperations:
    CREATE = "create"
    ENRICH = "enrich"
    VALID_OPERATIONS = [CREATE, ENRICH]


# Error Messages
class ErrorMessages:
    NO_DATA_PROVIDED = "No data provided"
    INSTRUMENT_NOT_FOUND = "Instrument not found"
    ENTITY_NOT_FOUND = "Legal entity not found"
    SCHEMA_NOT_FOUND = "Schema not found"
    DATABASE_ERROR = "A database error occurred"
    INVALID_BATCH_OPERATION = (
        f"Invalid operation, must be '{BatchOperations.CREATE}' or '{BatchOperations.ENRICH}'"
    )
    INVALID_DATA_FORMAT = "Invalid data format"
    MISSING_IDENTIFIERS = "Missing or invalid 'identifiers' list"
    ISIN_AND_TYPE_REQUIRED = "ISIN and type are required"
    FAILED_TO_CREATE_ENTITY = "Failed to create or update entity"
    SCHEMA_EXISTS = "Schema already exists"
    NO_SCHEMA_DATA = "No schema data provided"
    SCHEMA_NAME_MISMATCH = "Schema name in data does not match URL param"
    SCHEMA_HAS_DEPENDENTS = "Schema has dependent schemas"
    NO_FILE_PROVIDED = "No file provided"
    FILE_EMPTY = "File is empty"
    NO_FILTERS_PROVIDED = "No filters provided"

    # LEI/GLEIF specific
    LEI_CODE_REQUIRED = "LEI code is required"

    # Search specific
    MISSING_IDENTIFIER = "Missing identifier"
    MISSING_INSTRUMENT_CATEGORY = "Missing instrument category"
    UNABLE_TO_FETCH_OR_CREATE_INSTRUMENT = "Unable to fetch or create instrument"
    QUERY_PARAMETER_REQUIRED = "Query parameter is required"
    NO_FILE_PROVIDED = "No file provided"
    FILE_IS_EMPTY = "File is empty"

    # Schema specific
    SCHEMA_EXAMPLE_NOT_FOUND = "Schema example not found"


# Success Messages
class SuccessMessages:
    INSTRUMENT_CREATED = "Instrument created successfully"
    INSTRUMENT_UPDATED = "Instrument updated successfully"
    INSTRUMENT_DELETED = "Instrument deleted successfully"
    INSTRUMENT_ENRICHED = "Instrument enriched successfully"
    ENTITY_CREATED = "Legal entity created successfully"
    ENTITY_UPDATED = "Legal entity updated successfully"
    ENTITY_DELETED = "Legal entity deleted successfully"
    SCHEMA_CREATED = "Schema created successfully"
    SCHEMA_UPDATED = "Schema updated successfully"
    SCHEMA_DELETED = "Schema deleted successfully"
    INSTRUMENT_PROCESSED = "Successfully processed instrument"
    TEST_SUCCESSFUL = "Test successful"


# Response Field Names
class ResponseFields:
    STATUS = "status"
    DATA = "data"
    META = "meta"
    ERROR = "error"
    MESSAGE = "message"
    RESULTS = "results"
    SUCCESS_STATUS = "success"

    # Pagination fields
    PAGE = "page"
    PER_PAGE = "per_page"
    TOTAL = "total"

    # Batch operation fields
    OPERATION = "operation"
    TYPE = "type"
    SUCCESSFUL = "successful"
    FAILED = "failed"


# API Endpoint Names
class Endpoints:
    ROOT = "/"
    INSTRUMENTS = "/instruments"
    ENTITIES = "/entities"
    TRANSPARENCY = "/transparency"
    BATCH = "/batch"
    BATCH_INSTRUMENTS = "/batch/instruments"
    BATCH_ENTITIES = "/batch/entities"
    HEALTH = "/health"
    INFO = "/info"


# Request Headers
class Headers:
    CONTENT_TYPE = "Content-Type"
    X_REQUESTED_WITH = "X-Requested-With"
    XML_HTTP_REQUEST = "XMLHttpRequest"


# Content Types
class ContentTypes:
    JSON = "application/json"
    XML = "application/xml"
    YAML = "application/x-yaml"


# Query Parameters
class QueryParams:
    TYPE = "type"
    CALCULATION_TYPE = "calculation_type"
    CURRENCY = "currency"
    LIMIT = "limit"
    OFFSET = "offset"
    PAGE = "page"
    PER_PAGE = "per_page"
    STATUS = "status"
    JURISDICTION = "jurisdiction"
    VERSION = "version"
    FORCE = "force"
    FORMAT = "format"
    SCHEMA_TYPE = "schema_type"
    FILTERS = "filters"
    DATE = "date"
    FILE_PREFIX = "file_prefix"


# Form Fields
class FormFields:
    ID = "Id"
    CATEGORY = "Category"
    LEI = "lei"
    IDENTIFIERS = "identifiers"
    OPERATION = "operation"
    FILE = "file"


# Database Field Names (for response building)
class DbFields:
    ID = "id"
    ISIN = "isin"
    TYPE = "type"
    SYMBOL = "symbol"
    FULL_NAME = "full_name"
    CFI_CODE = "cfi_code"
    CURRENCY = "currency"
    LEI = "lei"
    NAME = "name"
    JURISDICTION = "jurisdiction"
    STATUS = "status"
    FIGI = "figi"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


# FIRDS Field Mappings (Column mapping only - instrument types handled by CFI manager)
class FirdsFieldMappings:
    """FIRDS field mappings to database columns."""
    
    # Common FIRDS column mappings to database fields
    COLUMN_MAPPING = {
        # Core identification
        "Id": "isin",
        # General attributes
        "FinInstrmGnlAttrbts_FullNm": "full_name",
        "FinInstrmGnlAttrbts_ShrtNm": "short_name",
        "FinInstrmGnlAttrbts_ClssfctnTp": "cfi_code",
        "FinInstrmGnlAttrbts_NtnlCcy": "currency",
        "FinInstrmGnlAttrbts_CmmdtyDerivInd": "commodity_derivative_indicator",
        "Issr": "lei_id",
        # Technical/regulatory attributes
        "TechAttrbts_PblctnPrd_FrDt": "publication_from_date",
        "TechAttrbts_RlvntCmptntAuthrty": "competent_authority",
        "TechAttrbts_RlvntTradgVn": "relevant_trading_venue",
        # Trading venue related attributes (for TradingVenue model)
        "TradgVnRltdAttrbts_Id": "venue_id",
        "TradgVnRltdAttrbts_IssrReq": "issuer_requested",
        "TradgVnRltdAttrbts_FrstTradDt": "first_trade_date",
        "TradgVnRltdAttrbts_TermntnDt": "termination_date",
        "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "admission_approval_date",
        "TradgVnRltdAttrbts_ReqForAdmssnDt": "request_for_admission_date",
    }


# External API Configuration
class ExternalAPIs:
    """External API endpoints and base URLs."""
    GLEIF_BASE_URL = "https://api.gleif.org/api/v1/lei-records"
    OPENFIGI_BASE_URL = "https://api.openfigi.com/v3/mapping"
    ISO_MIC_CSV_URL = "https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.csv"


# API Timeout Configuration
class APITimeouts:
    """Timeout values for HTTP requests."""
    DEFAULT_CONNECT = 5  # Connection timeout in seconds
    DEFAULT_READ = 30    # Read timeout in seconds
    DEFAULT_SINGLE = 30  # Single timeout value for simple requests
    TUPLE_DEFAULT = (5, 30)  # (connect, read) tuple format


# Retry Configuration
class RetryConfig:
    """Retry logic configuration for API calls."""
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_INITIAL_BACKOFF = 2
    DEFAULT_MAX_BACKOFF = 60
    DEFAULT_BACKOFF_FACTOR = 2
    DEFAULT_JITTER = True
    
    # HTTP status codes that should trigger retries
    RETRYABLE_STATUS_CODES = (429, 500, 502, 503, 504)
    
    # Exception types that should trigger retries
    RETRYABLE_EXCEPTIONS = ("RequestException", "ConnectTimeout", "ReadTimeout")


# Data Validation Limits
class ValidationLimits:
    """Validation constraints for data fields."""
    ISIN_LENGTH = 12
    CFI_CODE_LENGTH = 6
    LEI_CODE_LENGTH = 20
    MIC_CODE_LENGTH = 4
    
    # Maximum values for various operations
    MAX_BATCH_SIZE = 1000
    MAX_BATCH_SIZE_ISIN_LIST = 1000  # Specific for isin_list batch operations
    MAX_FILES_PER_TYPE = 100
    DEFAULT_RETENTION_DAYS = 30


# Database and Service Defaults
class ServiceDefaults:
    """Default values for service operations."""
    DEFAULT_LIMIT = 100
    DEFAULT_OFFSET = 0
    DEFAULT_BATCH_SIZE = 10
    DEFAULT_SEARCH_LIMIT = 100
    
    # Transparency service specific
    TRANSPARENCY_BATCH_SIZE = 10
    
    # File processing
    FILE_PROCESSING_CHUNK_SIZE = 1000


# Business Logic Constants
class BusinessConstants:
    """Business-specific constants and thresholds."""
    
    # Volume and transaction thresholds
    MIN_VOLUME_THRESHOLD = 0
    MIN_TRANSACTIONS_THRESHOLD = 0
    
    # Data quality percentages (for reference/documentation)
    FIRDS_DATA_FILL_RATE = 0.95  # 95% typical fill rate
    TRANSACTION_DATA_FILL_RATE = 0.25  # 25% fill rate
    THRESHOLD_DATA_FILL_RATE = 0.31  # 31% fill rate
    
    # CFI position validation
    CFI_FIRST_POSITION_MIN_LENGTH = 1
    
    # Date format patterns
    FIRDS_DATE_FORMAT = "%Y-%m-%d"
    
    # Boolean value mappings
    BOOLEAN_TRUE_VALUES = ("true", "1", "yes", "on")
    BOOLEAN_FALSE_VALUES = ("false", "0", "no", "off")


# File Pattern Constants
class FilePatterns:
    """Regular expressions and patterns for file processing."""
    
    # FIRDS file patterns
    FIRDS_FILENAME_PATTERN = r"^FULINS_([CDEFHIJORS])_\d{8}_\d+of\d+_firds_data\.csv$"
    
    # FITRS file patterns  
    FITRS_ECR_PATTERN = r"^FULECR_\d{8}_([A-Z])_\d+of\d+_fitrs_data\.csv$"
    FITRS_NCR_PATTERN = r"^FULNCR_\d{8}_([A-Z])_\d+of\d+_fitrs_data\.csv$"
    FITRS_COMBINED_PATTERN = r"^FUL(ECR|NCR)_\d{8}_([A-Z])_\d+of\d+_fitrs_data\.csv$"
    
    # Date extraction from filenames
    DATE_EXTRACTION_PATTERN = r"_(\d{8})_"
    
    # File grouping patterns
    FIRDS_GROUP_PATTERN = r"(FULINS_[CDEFHIJORS])_\d{8}"
    FITRS_GROUP_PATTERN = r"(FUL(?:ECR|NCR)_[A-Z])_\d{8}"


# Updated Instrument Types (expanded from original)
class InstrumentTypes:
    EQUITY = "equity"
    DEBT = "debt"
    FUTURE = "future"
    COLLECTIVE_INVESTMENT = "collective_investment"
    HYBRID = "hybrid"
    INTEREST_RATE = "interest_rate"
    CONVERTIBLE = "convertible"
    OPTION = "option"
    RIGHTS = "rights"
    STRUCTURED = "structured"
    OTHER = "other"

    VALID_TYPES = [
        EQUITY,
        DEBT,
        FUTURE,
        COLLECTIVE_INVESTMENT,
        HYBRID,
        INTEREST_RATE,
        CONVERTIBLE,
        OPTION,
        RIGHTS,
        STRUCTURED,
        OTHER,
    ]
