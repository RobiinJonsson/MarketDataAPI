# MarketDataAPI Documentation

Welcome to the MarketDataAPI documentation. This API provides access to financial market data, instrument details, and legal entity information.

## Quick Start

### Interactive Documentation
- **Swagger UI**: http://127.0.0.1:5000/api/v1/swagger
- **ReDoc UI**: http://127.0.0.1:5000/api/v1/docs

### API Endpoints
- **Base URL**: `http://127.0.0.1:5000/api/v1`
- **Authentication**: API Key required in `Authorization` header

## Documentation Structure

```
docs/
├── README.md                    # This file - main documentation index
├── api/                         # API reference documentation
│   ├── instruments.md          # Instruments API
│   ├── legal-entities.md       # Legal entities API  
│   ├── relationships.md        # Relationships API
│   └── schemas.md              # Schema management API
├── openapi/                    # Generated OpenAPI specifications
│   └── openapi.yaml           # Auto-generated from swagger.py
└── postman/                   # Generated Postman collections
    └── MarketDataAPI.postman_collection.json
```

## API Overview

### Core Resources

1. **Instruments** (`/instruments`)
   - Financial instruments (stocks, bonds, derivatives)
   - ISIN-based identification
   - Rich metadata including CFI codes, trading venues

2. **Legal Entities** (`/legal-entities`) 
   - Entity information via LEI codes
   - Addresses and registration details
   - Status and jurisdiction data

3. **Relationships** (`/relationships`)
   - Parent-child entity relationships
   - Ownership percentages
   - Direct vs ultimate relationships

4. **Schemas** (`/schemas`)
   - Data transformation schemas
   - Mapping rules for different formats

### Response Format

All API responses follow a consistent format:

```json
{
  "status": "success",
  "data": { ... },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 100
  }
}
```

## Authentication

Include your API key in the Authorization header:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://127.0.0.1:5000/api/v1/instruments
```

## Documentation Maintenance

This documentation is automatically generated from the API implementation:

1. **Primary Source**: `marketdata_api/routes/swagger.py`
2. **Generation Script**: `scripts/generate_docs.py`
3. **Generated Files**: `docs/openapi/` and `docs/postman/`

To regenerate documentation after API changes:

```bash
python scripts/generate_docs.py
```

## Getting Help

- **API Reference**: See the interactive Swagger documentation
- **Examples**: Check the generated Postman collection
- **Issues**: Review the validation output from the generation script
