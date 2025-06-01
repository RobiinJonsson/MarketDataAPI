# Schema Management API

The Schema Management API allows you to create, manage, and apply custom data schemas for instruments and legal entities. This enables you to transform the standard MarketDataAPI data models into specific formats that match your organization's requirements.

## Endpoints

### List All Schemas

Retrieves a list of all available schemas.

```http
GET /schemas
```

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| type | string | Filter by schema type ("instrument", "legal_entity", "relationship") |
| status | string | Filter by schema status ("active", "draft", "deprecated") |
| page | integer | Page number for paginated results (default: 1) |
| per_page | integer | Number of records per page (default: 20, max: 100) |

#### Example Request

```http
GET /schemas?type=instrument&status=active
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": [
    {
      "id": "bloomberg_format",
      "name": "Bloomberg Format",
      "description": "Schema for mapping instrument data to Bloomberg format",
      "type": "instrument",
      "status": "active",
      "version": "1.2",
      "created_at": "2022-03-15T10:30:00Z",
      "updated_at": "2022-09-22T14:45:00Z"
    },
    {
      "id": "refinitiv_format",
      "name": "Refinitiv Format",
      "description": "Schema for mapping instrument data to Refinitiv format",
      "type": "instrument",
      "status": "active",
      "version": "2.1",
      "created_at": "2022-04-10T09:15:00Z",
      "updated_at": "2022-10-05T11:20:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 2
  }
}
```

### Get Schema Details

Retrieves detailed information about a specific schema, including its mapping rules.

```http
GET /schemas/{schema_id}
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| schema_id | string | ID of the schema |

#### Example Request

```http
GET /schemas/bloomberg_format
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": {
    "id": "bloomberg_format",
    "name": "Bloomberg Format",
    "description": "Schema for mapping instrument data to Bloomberg format",
    "type": "instrument",
    "status": "active",
    "version": "1.2",
    "created_at": "2022-03-15T10:30:00Z",
    "updated_at": "2022-09-22T14:45:00Z",
    "mapping_rules": [
      {
        "source_field": "isin",
        "target_field": "security_id",
        "transformation": null
      },
      {
        "source_field": "short_name",
        "target_field": "ticker",
        "transformation": null
      },
      {
        "source_field": "name",
        "target_field": "name",
        "transformation": null
      },
      {
        "source_field": "type",
        "target_field": "security_type",
        "transformation": {
          "type": "map",
          "mapping": {
            "equity": "Common Stock",
            "debt": "Bond",
            "derivative": "Derivative"
          },
          "default_value": "Other"
        }
      }
    ]
  }
}
```

### Create Schema

Creates a new custom schema.

```http
POST /schemas
```

#### Request Body

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier for the schema |
| name | string | Display name for the schema |
| description | string | Description of the schema and its purpose |
| type | string | Type of the schema ("instrument", "legal_entity", "relationship") |
| mapping_rules | array | Array of field mapping rules |

#### Example Request

```http
POST /schemas
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "id": "custom_investor_format",
  "name": "Custom Investor Format",
  "description": "Schema for mapping instrument data to our investor portal format",
  "type": "instrument",
  "mapping_rules": [
    {
      "source_field": "isin",
      "target_field": "identifier",
      "transformation": null
    },
    {
      "source_field": "name",
      "target_field": "security_name",
      "transformation": null
    },
    {
      "source_field": "currency",
      "target_field": "trading_currency",
      "transformation": null
    },
    {
      "source_field": "type",
      "target_field": "asset_class",
      "transformation": {
        "type": "map",
        "mapping": {
          "equity": "Stocks",
          "debt": "Fixed Income",
          "derivative": "Derivatives"
        },
        "default_value": "Other Assets"
      }
    }
  ]
}
```

#### Example Response

```json
{
  "status": "success",
  "data": {
    "id": "custom_investor_format",
    "name": "Custom Investor Format",
    "description": "Schema for mapping instrument data to our investor portal format",
    "type": "instrument",
    "status": "active",
    "version": "1.0",
    "created_at": "2023-05-30T15:20:30Z",
    "updated_at": "2023-05-30T15:20:30Z"
  }
}
```

### Update Schema

Updates an existing schema.

```http
PUT /schemas/{schema_id}
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| schema_id | string | ID of the schema to update |

#### Request Body

| Field | Type | Description |
|-------|------|-------------|
| name | string | Display name for the schema |
| description | string | Description of the schema and its purpose |
| status | string | Status of the schema ("active", "draft", "deprecated") |
| mapping_rules | array | Array of field mapping rules |

#### Example Request

```http
PUT /schemas/custom_investor_format
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "name": "Custom Investor Format",
  "description": "Updated schema for mapping instrument data to our investor portal",
  "status": "active",
  "mapping_rules": [
    {
      "source_field": "isin",
      "target_field": "identifier",
      "transformation": null
    },
    {
      "source_field": "name",
      "target_field": "security_name",
      "transformation": null
    },
    {
      "source_field": "currency",
      "target_field": "trading_currency",
      "transformation": null
    },
    {
      "source_field": "type",
      "target_field": "asset_class",
      "transformation": {
        "type": "map",
        "mapping": {
          "equity": "Stocks",
          "debt": "Fixed Income",
          "derivative": "Derivatives",
          "commodity": "Commodities"
        },
        "default_value": "Other Assets"
      }
    },
    {
      "source_field": "issuer_lei",
      "target_field": "issuer_id",
      "transformation": null
    }
  ]
}
```

#### Example Response

```json
{
  "status": "success",
  "data": {
    "id": "custom_investor_format",
    "name": "Custom Investor Format",
    "description": "Updated schema for mapping instrument data to our investor portal",
    "type": "instrument",
    "status": "active",
    "version": "1.1",
    "created_at": "2023-05-30T15:20:30Z",
    "updated_at": "2023-05-30T16:45:15Z"
  }
}
```

### Delete Schema

Deletes a schema.

```http
DELETE /schemas/{schema_id}
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| schema_id | string | ID of the schema to delete |

#### Example Request

```http
DELETE /schemas/custom_investor_format
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": {
    "message": "Schema 'custom_investor_format' successfully deleted"
  }
}
```

### Apply Schema to Data

Applies a schema to transform data from a specific endpoint.

```http
GET /{resource_type}/{resource_id}/schema/{schema_id}
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| resource_type | string | Type of resource ("instruments", "legal-entities", "relationships") |
| resource_id | string | ID of the resource (e.g., ISIN for instruments, LEI for legal entities) |
| schema_id | string | ID of the schema to apply |

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
    "version": "1.2",
    "source": "instruments/US0378331005"
  }
}
```

### Validate Data Against Schema

Validates a data payload against a schema without transforming it.

```http
POST /schemas/{schema_id}/validate
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| schema_id | string | ID of the schema to validate against |

#### Request Body

The data to validate against the schema.

#### Example Request

```http
POST /schemas/bloomberg_format/validate
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "isin": "US0378331005",
  "name": "APPLE INC",
  "short_name": "AAPL",
  "type": "equity",
  "currency": "USD",
  "issuer_lei": "HWUPKR0MPOU8FGXBT394"
}
```

#### Example Response

```json
{
  "status": "success",
  "data": {
    "is_valid": true,
    "mapped_fields": ["isin", "name", "short_name", "type"],
    "unmapped_fields": ["currency", "issuer_lei"],
    "missing_required_fields": []
  }
}
```
