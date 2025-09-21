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
    INVALID_BATCH_OPERATION = f"Invalid operation, must be '{BatchOperations.CREATE}' or '{BatchOperations.ENRICH}'"
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


# FIRDS Instrument Type Mappings
class FirdsTypes:
    """FIRDS instrument type mappings and metadata."""
    
    MAPPING = {
        'C': {
            'instrument_type': 'collective_investment',
            'description': 'Collective Investment Vehicles (CIVs)',
            'cfi_category': 'C',
            'examples': ['Mutual funds', 'ETFs', 'REITs', 'Hedge funds']
        },
        'D': {
            'instrument_type': 'debt',
            'description': 'Debt Securities',
            'cfi_category': 'D', 
            'examples': ['Bonds', 'Notes', 'Commercial paper', 'Asset-backed securities']
        },
        'E': {
            'instrument_type': 'equity',
            'description': 'Equities',
            'cfi_category': 'E',
            'examples': ['Common shares', 'Preferred shares', 'Depository receipts', 'Rights']
        },
        'F': {
            'instrument_type': 'future',
            'description': 'Futures',
            'cfi_category': 'F',
            'examples': ['Commodity futures', 'Financial futures', 'Index futures']
        },
        'H': {
            'instrument_type': 'hybrid',
            'description': 'Hybrid/Structured Instruments',
            'cfi_category': 'M',  # Miscellaneous/Others in CFI
            'examples': ['Structured notes', 'Barrier products', 'Participation certificates']
        },
        'I': {
            'instrument_type': 'interest_rate',
            'description': 'Interest Rate Derivatives',
            'cfi_category': 'H',  # Listed derivatives in CFI
            'examples': ['Interest rate swaps', 'FRAs', 'Interest rate futures']
        },
        'J': {
            'instrument_type': 'convertible',
            'description': 'Convertible Instruments',
            'cfi_category': 'D',  # Often debt with conversion features
            'examples': ['Convertible bonds', 'Convertible preferred shares']
        },
        'O': {
            'instrument_type': 'option',
            'description': 'Options',
            'cfi_category': 'O',  # Options in CFI
            'examples': ['Call options', 'Put options', 'Exotic options']
        },
        'R': {
            'instrument_type': 'rights',
            'description': 'Rights and Warrants',
            'cfi_category': 'R',  # Rights in CFI
            'examples': ['Subscription rights', 'Warrants', 'Purchase rights']
        },
        'S': {
            'instrument_type': 'structured',
            'description': 'Structured Products and Swaps',
            'cfi_category': 'S',  # Swaps in CFI
            'examples': ['Credit default swaps', 'Structured products', 'Total return swaps']
        }
    }
    
    # Common FIRDS column mappings to database fields
    COLUMN_MAPPING = {
        # Core identification
        'Id': 'isin',
        
        # General attributes
        'FinInstrmGnlAttrbts_FullNm': 'full_name',
        'FinInstrmGnlAttrbts_ShrtNm': 'short_name',
        'FinInstrmGnlAttrbts_ClssfctnTp': 'cfi_code',
        'FinInstrmGnlAttrbts_NtnlCcy': 'currency',
        'FinInstrmGnlAttrbts_CmmdtyDerivInd': 'commodity_derivative_indicator',
        'Issr': 'lei_id',
        
        # Technical/regulatory attributes
        'TechAttrbts_PblctnPrd_FrDt': 'publication_from_date',
        'TechAttrbts_RlvntCmptntAuthrty': 'competent_authority',
        'TechAttrbts_RlvntTradgVn': 'relevant_trading_venue',
        
        # Trading venue related attributes (for TradingVenue model)
        'TradgVnRltdAttrbts_Id': 'venue_id',
        'TradgVnRltdAttrbts_IssrReq': 'issuer_requested',
        'TradgVnRltdAttrbts_FrstTradDt': 'first_trade_date',
        'TradgVnRltdAttrbts_TermntnDt': 'termination_date',
        'TradgVnRltdAttrbts_AdmssnApprvlDtByIssr': 'admission_approval_date',
        'TradgVnRltdAttrbts_ReqForAdmssnDt': 'request_for_admission_date',
    }


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
        EQUITY, DEBT, FUTURE, COLLECTIVE_INVESTMENT, HYBRID,
        INTEREST_RATE, CONVERTIBLE, OPTION, RIGHTS, STRUCTURED, OTHER
    ]
