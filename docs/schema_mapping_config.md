# Schema Mapping Configuration

## Overview
The schema mapping system defines how instrument data is mapped between different formats using YAML configuration files.

## Configuration Format
Each schema is defined in its own YAML file with the following structure:

```yaml
version: "1.0"
name: "base"  # or "equity" or "debt"
description: "Schema description"
extends: null  # or name of parent schema
fields:
  - name: "identifier"
    source: "isin"
    type: "string"
    required: true
    description: "ISIN identifier"
    transformation: null

  - name: "price"
    source: "last_price"
    type: "number"
    required: false
    description: "Current price"
    transformation: "round(2)"
```

### Field Configuration
- `name`: Output field name
- `source`: Source field in the model
- `type`: Data type (string, number, date, boolean)
- `required`: Whether the field is mandatory
- `description`: Field description
- `transformation`: Optional data transformation

### Supported Transformations
- `round(n)`: Round numbers to n decimal places
- `format(pattern)`: Format dates (e.g., YYYY-MM-DD)
- `upper()`: Convert text to uppercase
- `lower()`: Convert text to lowercase