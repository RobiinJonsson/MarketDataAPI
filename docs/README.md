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
│   ├── schemas.md              # Schema management API
│   ├── transparency.md         # Transparency calculations API
│   └── file_management_endpoints.md # **File management API** (comprehensive guide)
├── openapi/                    # Generated OpenAPI specifications
│   └── openapi.yaml           # Auto-generated from swagger.py
├── postman/                   # Generated Postman collections
│   └── MarketDataAPI.postman_collection.json
└── development/               # Development guides and examples
    └── README.md             # Development documentation index
```

## API Overview

The MarketDataAPI provides access to:

- **Financial Instruments**: ISIN-based instrument data from FIRDS
- **Legal Entities**: LEI-based entity information from GLEIF
- **Entity Relationships**: Parent-child relationships between entities  
- **Schema Management**: Custom data transformation schemas
- **Transparency Calculations**: MiFID II transparency data from FITRS
- **File Management**: Advanced file operations for ESMA data
- **CFI Code Decoding**: Classification of Financial Instruments decoding

### Core Endpoints

- `GET /instruments` - List financial instruments
- `GET /instruments/{isin}` - Get instrument details
- `GET /legal-entities` - List legal entities
- `GET /legal-entities/{lei}` - Get entity details
- `GET /transparency` - List transparency calculations
- `GET /transparency/isin/{isin}` - Get transparency data for instrument

### File Management Endpoints

- `POST /files/download-by-criteria` - **Primary endpoint** for downloading by date, type, and dataset
- `GET /files` - List files with advanced filtering capabilities
- `GET /esma-files` - Browse available ESMA registry files
- `GET /files/stats` - Storage statistics and monitoring
- `POST /files/cleanup` - Automated file cleanup and retention

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
