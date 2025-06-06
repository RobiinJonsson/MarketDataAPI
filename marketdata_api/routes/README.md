# MarketData API Routes

This directory contains the route definitions for the MarketData API. The routes are organized by functionality:

## Route Files

- **common_routes.py**: Common API routes and utilities, including API info and error handlers
- **instrument_routes.py**: Endpoints for instrument-related operations (create, read, update, delete, enrich)
- **entity_routes.py**: Endpoints for legal entity operations (create, read, update, delete)
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
- `/api/v1/cfi` - CFI code decoding
- `/api/v1/batch` - Batch operations for instruments and entities

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
