# MarketDataAPI Documentation

## Overview

MarketDataAPI is a comprehensive API for accessing financial market data, instrument details, and legal entity information. This API provides structured data from multiple sources including FIRDS (Financial Instruments Reference Data System), GLEIF (Global Legal Entity Identifier Foundation), and OpenFIGI.

## API Base URL

```
https://api.marketdataapi.com/v1
```

## Authentication

MarketDataAPI uses API key authentication. Include your API key in the request header:

```http
Authorization: Bearer YOUR_API_KEY
```

To obtain an API key, please contact the administrator.

## Rate Limits

- Standard tier: 100 requests per minute
- Premium tier: 1,000 requests per minute

## Data Models

### Instrument

The core data model representing a financial instrument.

| Field | Type | Description |
|-------|------|-------------|
| isin | string | International Securities Identification Number |
| name | string | Full name of the instrument |
| short_name | string | Short name or symbol |
| type | string | Instrument type (Equity, Bond, Future, etc.) |
| currency | string | Currency code (ISO 4217) |
| issuer_lei | string | Legal Entity Identifier of the issuer |
| status | string | Current status (Active, Inactive, Suspended) |
| first_trading_date | date | First trading date |
| termination_date | date | Termination date (if applicable) |

### Legal Entity

Represents a legal entity, typically an issuer of financial instruments.

| Field | Type | Description |
|-------|------|-------------|
| lei | string | Legal Entity Identifier (20 characters) |
| name | string | Legal name of the entity |
| jurisdiction | string | Jurisdiction code (ISO 3166-1) |
| legal_form | string | Legal form of the entity |
| status | string | Current status (Active, Inactive, Pending) |

### Entity Relationship

Represents parent-child relationships between legal entities.

| Field | Type | Description |
|-------|------|-------------|
| parent_lei | string | LEI of the parent entity |
| child_lei | string | LEI of the child entity |
| relationship_type | string | Type of relationship (DIRECT, ULTIMATE) |
| relationship_status | string | Status of the relationship (ACTIVE, INACTIVE) |

## Common Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| page | integer | Page number for paginated results (default: 1) |
| per_page | integer | Number of records per page (default: 20, max: 100) |
| sort | string | Sort field (e.g., "name", "isin") |
| order | string | Sort order ("asc" or "desc", default: "asc") |

## Response Format

All API responses are returned in JSON format with a consistent structure:

### Success Response

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

### Error Response

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message description"
  }
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| INVALID_REQUEST | 400 | The request is invalid or missing required parameters |
| UNAUTHORIZED | 401 | Authentication failed or invalid API key |
| FORBIDDEN | 403 | The request is not allowed |
| NOT_FOUND | 404 | The requested resource was not found |
| TOO_MANY_REQUESTS | 429 | Rate limit exceeded |
| SERVER_ERROR | 500 | Internal server error |
| SERVICE_UNAVAILABLE | 503 | Service temporarily unavailable |

## API Versioning

The API version is included in the URL path (e.g., `/v1/`). When breaking changes are introduced, a new API version will be released.
