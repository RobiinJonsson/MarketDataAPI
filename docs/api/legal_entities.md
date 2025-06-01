# Legal Entities API

The Legal Entities API provides access to comprehensive information about legal entities, including companies, financial institutions, and other organizations identified through Legal Entity Identifiers (LEIs).

## Endpoints

### Get All Legal Entities

Retrieves a paginated list of legal entities.

```http
GET /legal-entities
```

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| status | string | Filter by entity status (e.g., "ACTIVE", "INACTIVE", "PENDING") |
| jurisdiction | string | Filter by jurisdiction code (ISO 3166-1) |
| page | integer | Page number for paginated results (default: 1) |
| per_page | integer | Number of records per page (default: 20, max: 100) |

#### Example Request

```http
GET /legal-entities?status=ACTIVE&jurisdiction=US&page=1&per_page=10
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": [
    {
      "lei": "HWUPKR0MPOU8FGXBT394",
      "name": "APPLE INC",
      "jurisdiction": "US",
      "legal_form": "CORPORATION",
      "registered_as": "CORPORATION",
      "status": "ACTIVE",
      "registration_status": "ISSUED",
      "managing_lou": "EVK05KS7XY1DEII3R011"
    },
    // Additional entities...
  ],
  "meta": {
    "page": 1,
    "per_page": 10,
    "total": 248
  }
}
```

### Get Legal Entity by LEI

Retrieves detailed information about a specific legal entity by its LEI.

```http
GET /legal-entities/{lei}
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| lei | string | Legal Entity Identifier (20 characters) |

#### Example Request

```http
GET /legal-entities/HWUPKR0MPOU8FGXBT394
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": {
    "lei": "HWUPKR0MPOU8FGXBT394",
    "name": "APPLE INC",
    "jurisdiction": "US",
    "legal_form": "CORPORATION",
    "registered_as": "CORPORATION",
    "status": "ACTIVE",
    "bic": null,
    "next_renewal_date": "2023-12-31T00:00:00Z",
    "registration_status": "ISSUED",
    "managing_lou": "EVK05KS7XY1DEII3R011",
    "addresses": [
      {
        "type": "HEADQUARTERS",
        "line1": "ONE APPLE PARK WAY",
        "line2": null,
        "city": "CUPERTINO",
        "region": "CA",
        "country": "US",
        "postal_code": "95014"
      },
      {
        "type": "LEGAL",
        "line1": "ONE APPLE PARK WAY",
        "line2": null,
        "city": "CUPERTINO",
        "region": "CA",
        "country": "US",
        "postal_code": "95014"
      }
    ],
    "registration": {
      "initial_registration_date": "2012-06-06T00:00:00Z",
      "last_update_date": "2022-12-08T00:00:00Z",
      "registration_status": "ISSUED",
      "next_renewal_date": "2023-12-31T00:00:00Z",
      "managing_lou": "EVK05KS7XY1DEII3R011"
    }
  }
}
```

### Search Legal Entities

Searches for legal entities based on name, registration number, or other identifiers.

```http
GET /legal-entities/search
```

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| q | string | Search query (entity name, registration number) |
| jurisdiction | string | Filter by jurisdiction code (ISO 3166-1) |
| status | string | Filter by entity status |
| page | integer | Page number for paginated results (default: 1) |
| per_page | integer | Number of records per page (default: 20, max: 100) |

#### Example Request

```http
GET /legal-entities/search?q=apple&jurisdiction=US&status=ACTIVE&page=1&per_page=10
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": [
    {
      "lei": "HWUPKR0MPOU8FGXBT394",
      "name": "APPLE INC",
      "jurisdiction": "US",
      "legal_form": "CORPORATION",
      "status": "ACTIVE"
    },
    {
      "lei": "549300EVRK4JBPWJXL51",
      "name": "APPLE OPERATIONS INTERNATIONAL LIMITED",
      "jurisdiction": "IE",
      "legal_form": "PRIVATE COMPANY LIMITED BY SHARES",
      "status": "ACTIVE"
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 10,
    "total": 2,
    "query": "apple"
  }
}
```

### Get Instruments by Legal Entity

Retrieves all financial instruments issued by a specific legal entity.

```http
GET /legal-entities/{lei}/instruments
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| lei | string | Legal Entity Identifier (20 characters) |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| type | string | Filter by instrument type |
| status | string | Filter by instrument status |
| page | integer | Page number for paginated results (default: 1) |
| per_page | integer | Number of records per page (default: 20, max: 100) |

#### Example Request

```http
GET /legal-entities/HWUPKR0MPOU8FGXBT394/instruments?type=equity&status=active&page=1&per_page=10
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": [
    {
      "isin": "US0378331005",
      "name": "APPLE INC",
      "short_name": "AAPL",
      "type": "equity",
      "currency": "USD",
      "issuer_lei": "HWUPKR0MPOU8FGXBT394",
      "status": "active",
      "first_trading_date": "1980-12-12",
      "termination_date": null
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 10,
    "total": 1,
    "entity_lei": "HWUPKR0MPOU8FGXBT394",
    "entity_name": "APPLE INC"
  }
}
```
