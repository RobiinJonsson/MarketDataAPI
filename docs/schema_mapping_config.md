# Schema Mapping Configuration

## Overview
The schema mapping configuration defines how instrument attributes from the front-end application schema are mapped to the corresponding data source fields. This configuration allows for flexible mapping without requiring code changes.

## Configuration Format
The configuration is stored in YAML format for readability and ease of maintenance.

### Basic Structure
```yaml
version: "1.0"
mappings:
  - frontend_schema: "trading_app_v1"
    description: "Mapping for Trading Application v1"
    attributes:
      - frontend_field: "symbol"
        source_field: "ticker"
        data_type: "string"
        required: true
        transformation: null
      - frontend_field: "lastPrice"
        source_field: "last_trade_price"
        data_type: "decimal"
        required: true
        transformation: "round(2)"
      - frontend_field: "volume"
        source_field: "trading_volume"
        data_type: "integer"
        required: false
        transformation: null
```

### Configuration Fields

#### Root Level
- `version`: Schema mapping version
- `mappings`: List of mapping configurations

#### Mapping Configuration
- `frontend_schema`: Identifier for the front-end schema
- `description`: Human-readable description of the mapping
- `attributes`: List of attribute mappings

#### Attribute Mapping
- `frontend_field`: Field name in the front-end schema
- `source_field`: Corresponding field in the data source
- `data_type`: Expected data type (string, integer, decimal, date, etc.)
- `required`: Whether the field is mandatory
- `transformation`: Optional transformation rule to apply to the data

## Example Mappings

### Example 1: Basic Stock Data
```yaml
version: "1.0"
mappings:
  - frontend_schema: "stock_viewer_v1"
    description: "Basic stock information mapping"
    attributes:
      - frontend_field: "ticker"
        source_field: "symbol"
        data_type: "string"
        required: true
      - frontend_field: "companyName"
        source_field: "name"
        data_type: "string"
        required: true
      - frontend_field: "currentPrice"
        source_field: "last_price"
        data_type: "decimal"
        required: true
        transformation: "round(2)"
```

### Example 2: Complex Instrument Data
```yaml
version: "1.0"
mappings:
  - frontend_schema: "derivatives_trader_v1"
    description: "Derivatives trading platform mapping"
    attributes:
      - frontend_field: "underlying"
        source_field: "underlying_symbol"
        data_type: "string"
        required: true
      - frontend_field: "strikePrice"
        source_field: "strike"
        data_type: "decimal"
        required: true
        transformation: "round(2)"
      - frontend_field: "expiryDate"
        source_field: "expiration"
        data_type: "date"
        required: true
        transformation: "format('YYYY-MM-DD')"
      - frontend_field: "optionType"
        source_field: "type"
        data_type: "string"
        required: true
        transformation: "upper()"
```

## Transformation Rules
The `transformation` field supports the following operations:
- `round(n)`: Round numeric values to n decimal places
- `upper()`: Convert string to uppercase
- `lower()`: Convert string to lowercase
- `format(pattern)`: Format dates according to specified pattern
- `null`: No transformation (raw value)

## Validation Rules
1. Each `frontend_schema` must be unique
2. Required fields must have corresponding source fields
3. Data types must be compatible between source and target
4. Transformation rules must be valid for the data type

## Next Steps
1. Create a schema validator for the configuration format
2. Implement the mapping engine to process these configurations
3. Add support for more complex transformations
4. Create a configuration management interface 