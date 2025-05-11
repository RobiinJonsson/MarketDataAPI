# Schema Guide for Market Data API

## Overview
The schema mapping system allows you to define how you want to receive instrument data. It maps database fields to your desired output format using YAML configuration.

## Quick Start
1. Create a schema file (e.g., `my_schema.yaml`):
```yaml
version: "1.0"
name: "demo_equity"
description: "Custom equity schema"
extends: "base"
fields:
  - name: "security_id"     # Your chosen output name
    source: "isin"         # Must match a field in database model
    type: "string"
    required: true
    description: "Security identifier"

  - name: "price"
    source: "price_multiplier"
    type: "number"
    required: false
    description: "Price data"
    transformation: "round(4)"
```

2. Upload the schema:
```bash
curl -X POST http://localhost:5000/api/schema \
  -H "Content-Type: application/x-yaml" \
  --data-binary "@my_schema.yaml"
```

3. Search using the schema:
```bash
curl -X POST http://localhost:5000/api/schema/search \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "identifier": "SE0000108656"
    },
    "schema_type": "demo_equity",
    "format": "json"
  }'
```

## Schema Structure
- `version`: Schema version (starts at "1.0")
- `name`: Unique schema identifier
- `description`: Human-readable description
- `extends`: Parent schema (usually "base")
- `fields`: Array of field mappings

### Field Configuration
- `name`: Your chosen output field name
- `source`: Must match a field in the database model
- `type`: Data type (string, number, date, boolean)
- `required`: Whether field is mandatory
- `description`: Field documentation
- `transformation`: Optional data transformation

### Available Database Fields
Base Instrument fields:
- `isin`: ISIN identifier
- `full_name`: Full instrument name
- `short_name`: Short name/symbol
- `currency`: Trading currency
- `cfi_code`: CFI classification
- `trading_venue`: Trading venue ID

Equity-specific fields:
- `price_multiplier`: Price multiplier
- `market_cap`: Market capitalization
- `shares_outstanding`: Shares outstanding
- `sector`: Business sector
- `industry`: Industry classification

Debt-specific fields:
- `maturity_date`: Maturity date
- `coupon_frequency`: Coupon frequency
- `fixed_interest_rate`: Interest rate
- `nominal_value_per_unit`: Nominal value

### Supported Transformations
- `round(n)`: Round numbers to n decimals
- `format(pattern)`: Format dates (e.g., YYYY-MM-DD)
- `upper`: Convert to uppercase
- `lower`: Convert to lowercase

## Schema Management
Version control:
```bash
# Get version history
curl http://localhost:5000/api/schema/demo_equity/versions

# Get specific version
curl http://localhost:5000/api/schema/demo_equity?version=1.0
```

Update schema:
```bash
curl -X PUT http://localhost:5000/api/schema/demo_equity \
  -H "Content-Type: application/json" \
  -d '{
    "name": "demo_equity",
    "description": "Updated schema",
    "extends": "base",
    "fields": [...]
  }'
```

Delete schema:
```bash
curl -X DELETE http://localhost:5000/api/schema/demo_equity
```

## Best Practices
1. Always extend from "base" schema
2. Use descriptive field names
3. Include proper descriptions
4. Mark required fields appropriately
5. Use transformations for data formatting
