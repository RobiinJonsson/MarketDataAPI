# Getting Started with Market Data API Schemas

## Quick Start Example
Let's say you want to get equity data for Ericsson B (ISIN: SE0000108656). Here's how:

1. Create a file `my_schema.yaml`:
```yaml
version: "1.0"
name: "equity"
description: "Get equity data"
extends: "base"
fields:
  - name: "identifier"
    source: "isin"
    type: "string"
    required: true
    description: "ISIN code"

  - name: "price"
    source: "last_price"
    type: "number"
    required: false
    description: "Current price"
    transformation: "round(2)"

  - name: "market_cap"
    source: "market_cap"
    type: "number"
    required: false
    description: "Market capitalization"
    transformation: "round(2)"
```

2. Use the API:
```bash
curl -X POST http://your-api/api/schema/search \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "identifier": "SE0000108656"
    },
    "schema_type": "equity",
    "format": "json"
  }'
```

## Creating Your Schema

1. Choose a Schema Type:
   - `base`: Basic instrument data
   - `equity`: Stocks and shares
   - `debt`: Bonds and fixed income

2. Select Your Fields:
   Common fields:
   - identifier (ISIN/FIGI)
   - full_name
   - short_name
   - currency
   - trading_venue

   Equity-specific:
   - market_cap
   - sector
   - price_multiplier

   Debt-specific:
   - maturity_date
   - coupon_rate
   - total_issued_nominal

3. Add Transformations (Optional):
   - `round(2)` for prices
   - `format(YYYY-MM-DD)` for dates
   - `upper()` for text standardization

## Example Use Cases

### 1. Basic Stock Info
```yaml
version: "1.0"
name: "equity"
extends: "base"
fields:
  - name: "identifier"
    source: "isin"
    type: "string"
    required: true
  - name: "price"
    source: "last_price"
    type: "number"
    transformation: "round(2)"
```

### 2. Bond Details
```yaml
version: "1.0"
name: "debt"
extends: "base"
fields:
  - name: "identifier"
    source: "isin"
    type: "string"
    required: true
  - name: "maturity"
    source: "maturity_date"
    type: "date"
    transformation: "format(YYYY-MM-DD)"
```

Need more help? Check the full [Schema Guide](schema_guide.txt) for detailed documentation.
