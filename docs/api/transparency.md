# Transparency Calculations API

The Transparency Calculations API provides access to MiFID II transparency data for financial instruments, including pre-trade and post-trade transparency thresholds, liquidity assessments, and market activity metrics.

## Endpoints

### List All Transparency Calculations

Retrieves a list of transparency calculations with optional filtering.

```http
GET /transparency
```

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| calculation_type | string | Filter by calculation type ("EQUITY", "NON_EQUITY") |
| instrument_type | string | Filter by instrument type ("equity", "debt", "futures") |
| isin | string | Filter by specific ISIN |
| page | integer | Page number for paginated results (default: 1) |
| per_page | integer | Number of records per page (default: 20, max: 100) |

#### Example Request

```http
GET /transparency?calculation_type=EQUITY&isin=NL0000235190
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": [
    {
      "id": "calc_123456",
      "isin": "NL0000235190",
      "calculation_type": "EQUITY",
      "tech_record_id": "TRC_001",
      "from_date": "2023-01-01",
      "to_date": "2023-12-31",
      "liquidity": true,
      "total_transactions_executed": 15420,
      "total_volume_executed": 2547890.50,
      "created_at": "2023-01-15T10:30:00Z",
      "equity_details": {
        "financial_instrument_classification": "SHARES",
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
  "calculation_type": "EQUITY",
  "tech_record_id": "TRC_001",
  "from_date": "2023-01-01",
  "to_date": "2023-12-31",
  "liquidity": true,
  "total_transactions_executed": 15420,
  "total_volume_executed": 2547890.50,
  "statistics": {
    "average_daily_transactions": 42.3,
    "peak_trading_volume": 45670.25
  },
  "created_at": "2023-01-15T10:30:00Z",
  "updated_at": "2023-01-15T10:30:00Z",
  "equity_transparency": {
    "financial_instrument_classification": "SHARES",
    "methodology": "ADF_METHOD",
    "average_daily_turnover": 12500.75,
    "large_in_scale": 25000.00,
    "average_daily_number_of_transactions": 42.3,
    "average_transaction_value": 165.27,
    "standard_market_size": 7500.00
  }
}
```

### Create Transparency Calculation

Creates a new transparency calculation.

```http
POST /transparency
```

#### Request Body

| Field | Type | Description |
|-------|------|-------------|
| ISIN | string | International Securities Identification Number |
| TechRcrdId | string | Technical record identifier |
| calculation_type | string | Type of calculation ("EQUITY", "NON_EQUITY") |
| FrDt | string | From date (YYYY-MM-DD) |
| ToDt | string | To date (YYYY-MM-DD) |
| Lqdty | string | Liquidity indicator ("true"/"false") |
| TtlNbOfTxsExctd | integer | Total number of transactions executed |
| TtlVolOfTxsExctd | number | Total volume of transactions executed |

#### Example Request

```http
POST /transparency
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "ISIN": "NL0000235190",
  "TechRcrdId": "TRC_002",
  "calculation_type": "EQUITY",
  "FrDt": "2023-01-01",
  "ToDt": "2023-12-31",
  "Lqdty": "true",
  "TtlNbOfTxsExctd": 15420,
  "TtlVolOfTxsExctd": 2547890.50
}
```

#### Example Response

```json
{
  "message": "Transparency calculation created successfully",
  "id": "calc_789012",
  "isin": "NL0000235190",
  "calculation_type": "EQUITY"
}
```

### Get Transparency by ISIN

Retrieves transparency calculations for a specific ISIN.

```http
GET /transparency/isin/{isin}
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| isin | string | The ISIN to search for |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| calculation_type | string | Calculation type to get/create ("EQUITY", "NON_EQUITY") |
| ensure_instrument | boolean | Ensure instrument exists before creating transparency data (default: true) |

#### Example Request

```http
GET /transparency/isin/NL0000235190?calculation_type=EQUITY
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": [
    {
      "id": "calc_123456",
      "isin": "NL0000235190",
      "calculation_type": "EQUITY",
      "tech_record_id": "TRC_001",
      "from_date": "2023-01-01",
      "to_date": "2023-12-31",
      "liquidity": true,
      "total_transactions_executed": 15420,
      "total_volume_executed": 2547890.50
    }
  ],
  "count": 1
}
```

### Batch Source Transparency

Batch source transparency calculations from FITRS data.

```http
POST /transparency/batch
```

#### Request Body

| Field | Type | Description |
|-------|------|-------------|
| calculation_type | string | Type of calculation ("EQUITY", "NON_EQUITY") |
| isin_prefix | string | ISIN prefix filter (e.g., "NL" for Netherlands) |
| limit | integer | Maximum number of calculations to create (default: 10) |
| cfi_type | string | CFI type filter ("D", "F", "E") |

#### Example Request

```http
POST /transparency/batch
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "calculation_type": "NON_EQUITY",
  "isin_prefix": "NL",
  "limit": 50,
  "cfi_type": "D"
}
```

#### Example Response

```json
{
  "message": "Successfully created 45 transparency calculations",
  "created_count": 45,
  "calculations": [
    {
      "id": "calc_345678",
      "isin": "NL0012345678",
      "calculation_type": "NON_EQUITY",
      "tech_record_id": "TRC_003"
    }
  ]
}
```

### Batch Create Transparency

Batch create transparency calculations from provided data.

```http
POST /transparency/batch-create
```

#### Request Body

| Field | Type | Description |
|-------|------|-------------|
| records | array | List of transparency records to create |

Each record should follow the same structure as the single create endpoint.

#### Example Request

```http
POST /transparency/batch-create
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "records": [
    {
      "ISIN": "NL0000235190",
      "TechRcrdId": "TRC_004",
      "calculation_type": "EQUITY",
      "FrDt": "2023-01-01",
      "ToDt": "2023-12-31",
      "Lqdty": "true",
      "TtlNbOfTxsExctd": 8500,
      "TtlVolOfTxsExctd": 1250000.00
    },
    {
      "ISIN": "NL0000654321",
      "TechRcrdId": "TRC_005",
      "calculation_type": "NON_EQUITY",
      "FrDt": "2023-01-01",
      "ToDt": "2023-12-31",
      "Lqdty": "false",
      "TtlNbOfTxsExctd": 250,
      "TtlVolOfTxsExctd": 75000.00
    }
  ]
}
```

#### Example Response

```json
{
  "message": "Successfully created 2 transparency calculations",
  "created_count": 2,
  "total_provided": 2
}
```

## Transparency Data Types

### Equity Transparency

For equity instruments (calculation_type: "EQUITY"), additional fields include:

- **financial_instrument_classification**: Classification of the instrument
- **methodology**: Calculation methodology used
- **average_daily_turnover**: Average daily trading volume
- **large_in_scale**: Large-in-scale threshold
- **standard_market_size**: Standard market size for the instrument

### Non-Equity Transparency  

For non-equity instruments (calculation_type: "NON_EQUITY"), additional fields include:

- **description**: Description of the instrument or calculation
- **criterion_name**: Name of the transparency criterion
- **criterion_value**: Value of the transparency criterion
- **pre_trade_large_in_scale_threshold**: Pre-trade threshold amount
- **post_trade_large_in_scale_threshold**: Post-trade threshold amount

### Debt-Specific Transparency

For debt instruments, additional fields include:

- **bond_type**: Type of bond (Corporate, Government, etc.)
- **is_liquid**: Whether the instrument is considered liquid
- **is_securitised_derivative**: Whether it's a securitised derivative

### Futures-Specific Transparency

For futures instruments, additional fields include:

- **underlying_isin**: ISIN of the underlying instrument
- **is_stock_dividend_future**: Whether it's a stock dividend future
- **pre_trade_large_in_scale_threshold_nb**: Pre-trade threshold (number)
- **post_trade_large_in_scale_threshold_nb**: Post-trade threshold (number)

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
