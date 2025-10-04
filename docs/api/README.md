# API Documentation

## MarketDataAPI REST Endpoints

The MarketDataAPI provides comprehensive REST endpoints for financial market data access and processing.

## Interactive Documentation

- **Swagger UI**: [/api/v1/swagger/](/api/v1/swagger/) - Interactive API explorer
- **OpenAPI Spec**: [/docs/openapi](/docs/openapi) - Machine-readable specification

## Endpoint Categories

### Instruments (`/api/v1/instruments/`)
- List and search financial instruments
- Get detailed instrument information by ISIN
- CFI code analysis and classification
- Trading venue information

### Legal Entities (`/api/v1/legal-entities/`)
- Legal entity information via LEI codes
- Company relationships and hierarchies
- GLEIF data integration

### MIC Codes (`/api/v1/mic/`)
- Market identification codes
- Trading venue details
- Geographic and regulatory information
- Remote ISO 10383 registry access

### Transparency (`/api/v1/transparency/`)
- MiFID II transparency calculations
- FITRS data processing
- Liquidity assessments

### File Management (`/api/v1/files/`)
- ESMA data file processing
- FIRDS/FITRS file management
- Automated data loading

## Authentication

API endpoints require authentication via API key in the Authorization header:

```
Authorization: Bearer YOUR_API_KEY
```

## Rate Limits

- Standard endpoints: 1000 requests/hour
- File processing endpoints: 100 requests/hour
- Remote data endpoints: 500 requests/hour

## Response Formats

All endpoints return JSON with consistent structure:

```json
{
  "success": true,
  "data": { ... },
  "pagination": { ... },
  "timestamp": "2025-10-04T16:45:00Z"
}
```