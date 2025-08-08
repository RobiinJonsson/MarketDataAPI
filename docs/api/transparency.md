# Unified Transparency Calculations API

The Unified Transparency Calculations API provides access to MiFID II transparency data for financial instruments using a simplified JSON-based architecture. The API integrates with FIRDS reference data and searches FITRS files to create transparency calculations for existing instruments.

## Architecture Overview

- **FIRDS-First Approach**: Only creates transparency data for ISINs that exist in the instruments table
- **Unified Storage**: Single model with JSON storage instead of complex polymorphic inheritance
- **Optimized Search**: Uses instrument type to search only relevant FITRS files for better performance
- **File Type Support**: Handles all FITRS types (FULECR_E, FULNCR_C, FULNCR_D, FULNCR_F)

## Endpoints

### List All Transparency Calculations

Retrieves a list of transparency calculations with optional filtering.

```http
GET /transparency
```

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| file_type | string | Filter by FITRS file type ("FULECR_E", "FULNCR_C", "FULNCR_D", "FULNCR_F") |
| isin | string | Filter by specific ISIN |
| page | integer | Page number for paginated results (default: 1) |
| per_page | integer | Number of records per page (default: 20, max: 100) |

#### Example Request

```http
GET /transparency?file_type=FULECR_E&page=1&per_page=10
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "200 OK",
  "data": [
    {
      "id": "uuid-string",
      "isin": "SE0000242455",
      "file_type": "FULECR_E",
      "tech_record_id": 47849,
      "from_date": "2023-10-01",
      "to_date": "2024-03-31",
      "liquidity": false,
      "total_transactions_executed": 1553700,
      "total_volume_executed": 12559281434.6943,
      "source_file": "FULECR_20250802_E_1of1_fitrs_data.csv",
      "is_equity": true,
      "is_non_equity": false,
      "instrument_classification": "SHRS",
      "description": "Equity transparency calculation",
      "raw_data": {
        "TechRcrdId": 47849,
        "Id": "SE0000242455",
        "FinInstrmClssfctn": "SHRS",
        "FrDt": "2023-10-01",
        "ToDt": "2024-03-31",
        "Mthdlgy": "SINT",
        "TtlNbOfTxsExctd": 1553700,
        "TtlVolOfTxsExctd": 12559281434.6943
      },
      "thresholds": []
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 10,
    "total": 13
  }
}
```

### Get Transparency Calculation by ID

Retrieves detailed information about a specific transparency calculation.

```http
GET /transparency/{transparency_id}
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| transparency_id | string | UUID of the transparency calculation |

#### Example Request

```http
GET /transparency/uuid-string
Authorization: Bearer YOUR_API_KEY
```

### Get Transparency Data by ISIN

Retrieves all transparency calculations for a specific ISIN.

```http
GET /transparency/isin/{isin}
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| isin | string | ISIN of the instrument |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| file_type | string | Filter by FITRS file type |

#### Example Request

```http
GET /transparency/isin/SE0000242455
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "200 OK",
  "data": [
    {
      "id": "uuid-1",
      "isin": "SE0000242455",
      "file_type": "FULECR_E",
      "tech_record_id": 47849,
      "from_date": "2023-10-01",
      "to_date": "2024-03-31",
      "liquidity": false,
      "total_transactions_executed": 1553700,
      "total_volume_executed": 12559281434.6943,
      "source_file": "FULECR_20250802_E_1of1_fitrs_data.csv",
      "instrument_classification": "SHRS",
      "description": "Equity transparency calculation"
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 3
  }
}
```

### Create Transparency Calculation

Creates transparency calculations for an existing ISIN by searching FITRS files.

```http
POST /transparency
```

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| isin | string | Yes | ISIN of the instrument (must exist in instruments table) |
| instrument_type | string | No | Instrument type to optimize FITRS file search ("equity", "debt", "fund", etc.) |

#### Example Request

```http
POST /transparency
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "isin": "SE0000242455",
  "instrument_type": "equity"
}
```

#### Example Response

```json
{
  "status": "201 Created",
  "message": "Successfully created 3 transparency calculation(s)",
  "data": [
    {
      "id": "uuid-1",
      "isin": "SE0000242455",
      "file_type": "FULECR_E",
      "tech_record_id": 47849,
      "from_date": "2023-10-01",
      "to_date": "2024-03-31",
      "liquidity": false,
      "total_transactions_executed": 1553700,
      "total_volume_executed": 12559281434.6943,
      "source_file": "FULECR_20250802_E_1of1_fitrs_data.csv"
    }
  ]
}
```

### Error Responses

#### ISIN Not Found

```json
{
  "status": "404 Not Found",
  "error": "ISIN SE0000000000 does not exist in the database"
}
```

#### No Transparency Data

```json
{
  "status": "404 Not Found",
  "error": "No transparency calculations found for ISIN SE0000242455"
}
```

## Data Model

### TransparencyCalculation

The unified transparency calculation model with JSON storage for flexible data representation.

| Field | Type | Description |
|-------|------|-------------|
| id | string | UUID primary key |
| isin | string | ISIN (foreign key to instruments table) |
| tech_record_id | integer | Technical record ID from FITRS |
| file_type | string | FITRS file type (FULECR_E, FULNCR_C, FULNCR_D, FULNCR_F) |
| from_date | date | Calculation period start date |
| to_date | date | Calculation period end date |
| liquidity | boolean | Liquidity assessment |
| total_transactions_executed | integer | Total number of transactions |
| total_volume_executed | float | Total volume executed |
| source_file | string | Original FITRS filename |
| raw_data | json | Complete original FITRS record data |

### Derived Properties

| Property | Type | Description |
|----------|------|-------------|
| is_equity | boolean | True for FULECR_E files |
| is_non_equity | boolean | True for FULNCR_* files |
| instrument_classification | string | Financial instrument classification from FITRS |
| description | string | Human-readable description based on file type |

## FITRS File Type Mapping

| File Type | Instrument Types | Search Optimization |
|-----------|------------------|-------------------|
| FULECR_E | equity, share, stock | Searches only equity FITRS files |
| FULNCR_D | bond, debt, note, debenture | Searches only debt FITRS files |
| FULNCR_F | fund, etf, future, derivative | Searches only funds/futures files |
| FULNCR_C | other instruments | Searches corporate/other files |

## API Integration

### Prerequisites

1. **FIRDS Reference Data**: The ISIN must exist in the instruments table
2. **FITRS Files**: Relevant FITRS files must be available in the downloads/fitrs directory
3. **API Authentication**: Valid API key required

### Workflow

1. **Validate ISIN**: Check if ISIN exists in instruments table
2. **Determine File Type**: Use instrument_type to optimize FITRS file search
3. **Search FITRS Files**: Search only relevant files based on instrument type
4. **Create Calculations**: Parse matching records and create transparency calculations
5. **Return Results**: Formatted unified response with created calculations

### Performance Notes

- **Optimized Search**: Only searches relevant FITRS files based on instrument type
- **Database-First**: Only creates data for existing instruments
- **JSON Storage**: Flexible storage for varying FITRS data structures
- **Indexed Queries**: Core fields indexed for fast retrieval
        "methodology": "ADF_METHOD",
        "average_daily_turnover": 12500.75,
        "large_in_scale": 25000.00,
        "standard_market_size": 7500.00
      }
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 1
  }
}
```

### Get Transparency Calculation Details

Retrieves detailed information about a specific transparency calculation.

```http
GET /transparency/{transparency_id}
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| transparency_id | string | ID of the transparency calculation |

#### Example Request

```http
GET /transparency/calc_123456
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "id": "calc_123456",
  "isin": "NL0000235190",
  "tech_record_id": "TRC_001",
  "from_date": "2023-01-01",
  "to_date": "2023-12-31",
  "liquidity": true,
  "total_transactions_executed": 15420,
  "total_volume_executed": 2547890.50,
  "transparency_fields": {
    "TechRcrdId": "TRC_001",
    "FrDt": "2023-01-01",
    "ToDt": "2023-12-31",
    "Lqdty": "true",
    "TtlNbOfTxsExctd": 15420,
    "TtlVolOfTxsExctd": 2547890.50,
    "FinInstrmClssfctn": "SHARES",
    "Mthdlgy": "ADF_METHOD",
    "AvrgDlyTrnvr": 12500.75,
    "LrgInScale": 25000.00,
    "StdMktSz": 7500.00
  },
  "created_at": "2023-01-15T10:30:00Z",
  "updated_at": "2023-01-15T10:30:00Z"
}
```

## Error Responses

All endpoints return standard error responses:

```json
{
  "error": "Error message description"
}
```

Common error codes:
- **400 Bad Request**: Invalid request data
- **404 Not Found**: Transparency calculation not found
- **500 Internal Server Error**: Server processing error

## Data Sources

Transparency calculations are sourced from:
- **FITRS** (Financial Instruments Transparency System) data
- **Manual submissions** via API endpoints
- **Automated batch processing** from regulatory data feeds

The calculations comply with MiFID II transparency requirements and are updated regularly based on market activity and regulatory changes.
