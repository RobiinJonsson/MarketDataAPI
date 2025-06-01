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

# CFI Code Validation
class CFI:
    REQUIRED_LENGTH = 6

# API Version and Info
class API:
    VERSION = "1.0"
    PREFIX = "/api/v1"
    NAME = "MarketDataAPI CRUD API"

# Instrument Types
class InstrumentTypes:
    EQUITY = "equity"
    DEBT = "debt"
    FUTURE = "future"
    VALID_TYPES = [EQUITY, DEBT, FUTURE]

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
    INVALID_CFI_LENGTH = "CFI code must be 6 characters"
    INVALID_INSTRUMENT_TYPE = f"Invalid instrument type. Must be one of: {', '.join(InstrumentTypes.VALID_TYPES)}"
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
    CFI = "/cfi"
    BATCH_INSTRUMENTS = "/batch/instruments"
    FIRDS = "/firds"
    SEARCH = "/api/search"
    FETCH = "/api/fetch"
    GLEIF = "/api/gleif"
    ADMIN = "/admin"
    
    # Schema endpoints
    SCHEMA_SEARCH = "/api/schema/search"
    SCHEMA_VALIDATE = "/api/schema/validate"
    SCHEMA_EXAMPLES = "/api/schema/examples"
    SCHEMA_BASE = "/api/schema"

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
