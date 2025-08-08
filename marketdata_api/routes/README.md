# MarketData API Routes

This directory contains the route definitions for the MarketData API. The routes are organized by functionality:

## Route Files

- **common_routes.py**: Common API routes and utilities, including API info and error handlers
- **instrument_routes.py**: Endpoints for instrument-related operations (create, read, update, delete, enrich)
- **entity_routes.py**: Endpoints for legal entity operations (create, read, update, delete)
- **file_management.py**: Advanced file management endpoints for ESMA data operations
- **transparency_routes.py**: Unified transparency endpoints using JSON-based storage and FITRS file search
- **cfi_routes.py**: Endpoints for CFI code decoding
- **market.py**: Market data related endpoints
- **schema.py**: Schema-related endpoints
- **swagger.py**: Swagger documentation endpoints
- **docs.py**: Documentation-related endpoints

## Route Registration

All routes are registered in the `__init__.py` file, which provides a centralized registration function:

```python
def register_routes(app: Flask) -> None:
    """Register all API route blueprints with the Flask app"""
    app.register_blueprint(common_bp)
    app.register_blueprint(instrument_bp)
    app.register_blueprint(entity_bp)
    app.register_blueprint(cfi_bp)
    # Additional blueprints...
```

## Legacy Files

- **crud.py**: This is a legacy file that contained all CRUD operations for the API. It is being refactored into the modular files listed above. This file will be removed after the refactoring is complete.

## API Structure

The API follows RESTful principles with the following main endpoint groups:

- `/api/v1/instruments` - Financial instrument operations
- `/api/v1/entities` - Legal entity operations
- `/api/v1/files` - File management operations for ESMA data
- `/api/v1/esma-files` - ESMA registry file operations
- `/api/v1/transparency` - Unified transparency calculations with FIRDS validation and FITRS search
- `/api/v1/cfi` - CFI code decoding
- `/api/v1/batch` - Batch operations for instruments and entities

### File Management Operations

The file management system provides comprehensive operations for ESMA data:

- **File Listing**: List downloaded files with advanced filtering
- **ESMA Integration**: Access ESMA registry and download files
- **Download by Criteria**: Download files based on date, type, and dataset
- **Batch Operations**: Download and parse multiple files
- **Statistics**: File storage and usage statistics
- **Cleanup**: Automated file retention and cleanup
- **Organization**: Intelligent file naming and folder structure

### Required Fields for Instrument Creation

When creating an instrument via `POST /api/v1/instruments`, the following fields are required:

```json
{
  "Id": "string",  // Note: Capital 'I' - instrument identifier (ISIN, ticker, etc.)
  "type": "string",  // Instrument type (e.g., "equity", "bond", "derivative")
  "currency": "string",  // Optional but recommended
  "FinInstrmGnlAttrbts_FullNm": "string"  // Optional - full name of instrument
}
```

### Required Fields for Entity Creation

When creating an entity via `POST /api/v1/entities`, the following fields are required:

```json
{
  "lei": "string",  // Legal Entity Identifier (20 characters)
  "name": "string",  // Entity name
  "status": "string"  // Entity status (e.g., "ACTIVE", "INACTIVE")
}
```

See the Swagger documentation (`/swagger`) for complete API details.

## Documentation Sources

The API documentation is maintained in multiple formats:

### 1. Swagger/OpenAPI Documentation
- **swagger.py**: Interactive Swagger UI documentation available at `/api/v1/swagger`
- **docs/openapi.yaml**: OpenAPI 3.0 specification file
- Both provide the same information but swagger.py is the primary source for interactive testing

### 2. Markdown Documentation
- **docs/api/**: Static markdown documentation files
  - **README.md**: API overview and common patterns
  - **instruments.md**: Instruments API documentation
  - **legal_entities.md**: Legal entities API documentation
  - **relationships.md**: Entity relationships API documentation
  - **schemas.md**: Schema management API documentation

### 3. Route Documentation
- **docs.py**: Route for serving static documentation
- **routes/README.md**: This file - technical documentation for developers

## Documentation Synchronization

When updating API endpoints:

1. **Primary**: Update the implementation in swagger.py
2. **Secondary**: Update the corresponding markdown files in docs/api/
3. **Tertiary**: Update the OpenAPI YAML if using external tools

The swagger.py file serves as the source of truth for API behavior and interactive documentation.
