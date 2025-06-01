# Instruments API

The Instruments API provides access to detailed information about financial instruments including equities, bonds, futures, and other securities.

## Endpoints

### Get All Instruments

Retrieves a paginated list of instruments.

```http
GET /instruments
```

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| type | string | Filter by instrument type (e.g., "equity", "bond", "future") |
| status | string | Filter by status (e.g., "active", "inactive") |
| currency | string | Filter by currency code |
| issuer_lei | string | Filter by issuer LEI |
| page | integer | Page number for paginated results (default: 1) |
| per_page | integer | Number of records per page (default: 20, max: 100) |

#### Example Request

```http
GET /instruments?type=equity&status=active&page=1&per_page=10
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
    },
    // Additional instruments...
  ],
  "meta": {
    "page": 1,
    "per_page": 10,
    "total": 120
  }
}
```

### Get Instrument by ISIN

Retrieves detailed information about a specific instrument by its ISIN.

```http
GET /instruments/{isin}
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| isin | string | International Securities Identification Number |

#### Example Request

```http
GET /instruments/US0378331005
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": {
    "isin": "US0378331005",
    "name": "APPLE INC",
    "short_name": "AAPL",
    "type": "equity",
    "currency": "USD",
    "issuer_lei": "HWUPKR0MPOU8FGXBT394",
    "status": "active",
    "first_trading_date": "1980-12-12",
    "termination_date": null,
    "cfi_code": "ESVUFR",
    "figi": "BBG000B9XRY4",
    "market_identifier_code": "XNAS",
    "trading_venues": [
      "XNAS",
      "XNYS"
    ],
    "price_multiplier": "1",
    "classification": {
      "cfi_category": "E",
      "cfi_group": "S",
      "description": "Equity, Shares"
    },
    "issuer": {
      "lei": "HWUPKR0MPOU8FGXBT394",
      "name": "APPLE INC",
      "jurisdiction": "US",
      "legal_form": "CORPORATION"
    }
  }
}
```

### Get Instrument by Identifier

Retrieves an instrument by an alternative identifier such as FIGI, ticker symbol, or other identifiers.

```http
GET /instruments/identify
```

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| id_type | string | Type of identifier (e.g., "figi", "ticker", "cusip") |
| id_value | string | Value of the identifier |

#### Example Request

```http
GET /instruments/identify?id_type=ticker&id_value=AAPL
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": {
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
}
```

### Get Instrument with Custom Schema

Retrieves instrument data formatted according to a custom schema.

```http
GET /instruments/{isin}/schema/{schema_id}
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| isin | string | International Securities Identification Number |
| schema_id | string | ID of the custom schema to use |

#### Example Request

```http
GET /instruments/US0378331005/schema/bloomberg_format
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": {
    "security_id": "US0378331005",
    "ticker": "AAPL",
    "name": "APPLE INC",
    "security_type": "Common Stock",
    "currency": "USD",
    "exchange": "NASDAQ",
    "country": "US"
  },
  "meta": {
    "schema": "bloomberg_format",
    "version": "1.2"
  }
}
```

### Get Instrument Classification

Retrieves classification information for an instrument based on its CFI code.

```http
GET /instruments/{isin}/classification
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| isin | string | International Securities Identification Number |

#### Example Request

```http
GET /instruments/US0378331005/classification
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": {
    "cfi_code": "ESVUFR",
    "category": {
      "code": "E",
      "name": "Equities"
    },
    "group": {
      "code": "S",
      "name": "Shares"
    },
    "attributes": [
      {
        "position": 3,
        "code": "V",
        "name": "Voting",
        "description": "Voting rights"
      },
      {
        "position": 4,
        "code": "U",
        "name": "Unrestricted",
        "description": "Free transferability"
      },
      {
        "position": 5,
        "code": "F",
        "name": "Fully Paid",
        "description": "Fully paid shares"
      },
      {
        "position": 6,
        "code": "R",
        "name": "Registered",
        "description": "Registered form"
      }
    ],
    "description": "Equity, Shares, Voting, Unrestricted, Fully Paid, Registered"
  }
}
```
