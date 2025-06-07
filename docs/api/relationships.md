# Entity Relationships API

The Entity Relationships API provides access to parent-child relationships between legal entities, based on data from the Global Legal Entity Identifier Foundation (GLEIF). This API allows you to explore corporate ownership structures and hierarchies.

## Endpoints

### Get Entity Relationships

Retrieves all relationships for a specific legal entity, including both parent and child relationships.

```http
GET /relationships/{lei}
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| lei | string | Legal Entity Identifier (20 characters) |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| relationship_type | string | Filter by relationship type ("DIRECT", "ULTIMATE") |
| relationship_status | string | Filter by relationship status ("ACTIVE", "INACTIVE") |
| direction | string | Filter by relationship direction ("PARENT", "CHILD") |
| page | integer | Page number for paginated results (default: 1) |
| per_page | integer | Number of records per page (default: 20, max: 100) |

#### Example Request

```http
GET /relationships/HWUPKR0MPOU8FGXBT394?direction=CHILD&relationship_status=ACTIVE
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": {
    "entity": {
      "lei": "HWUPKR0MPOU8FGXBT394",
      "name": "APPLE INC",
      "jurisdiction": "US",
      "legal_form": "CORPORATION",
      "status": "ACTIVE"
    },
    "relationships": [
      {
        "relationship_type": "DIRECT",
        "relationship_status": "ACTIVE",
        "parent_lei": "529900ODI3047E2LIV03",
        "parent_name": "Apple Operations",
        "child_lei": "HWUPKR0MPOU8FGXBT394",
        "child_name": "APPLE INC",
        "relationship_period_start": "2022-01-15T00:00:00Z",
        "relationship_period_end": null,
        "percentage_ownership": 75.5
      },
      {
        "relationship_type": "ULTIMATE",
        "relationship_status": "ACTIVE",
        "parent_lei": "529900AB12345E67890Z",
        "parent_name": "Apple Holding Corporation",
        "child_lei": "HWUPKR0MPOU8FGXBT394",
        "child_name": "APPLE INC",
        "relationship_period_start": "2020-06-10T00:00:00Z",
        "relationship_period_end": null,
        "percentage_ownership": 100
      }
    ]
  },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 2
  }
}
```

### Get Entity Parents

Retrieves the direct and ultimate parents of a specific legal entity.

```http
GET /relationships/{lei}/parents
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| lei | string | Legal Entity Identifier (20 characters) |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| relationship_type | string | Filter by relationship type ("DIRECT", "ULTIMATE") |
| relationship_status | string | Filter by relationship status ("ACTIVE", "INACTIVE") |
| include_exceptions | boolean | Include relationship reporting exceptions (default: true) |

#### Example Request

```http
GET /relationships/HWUPKR0MPOU8FGXBT394/parents
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": {
    "entity": {
      "lei": "HWUPKR0MPOU8FGXBT394",
      "name": "APPLE INC",
      "jurisdiction": "US",
      "legal_form": "CORPORATION",
      "status": "ACTIVE"
    },
    "direct_parent": {
      "relationship_type": "DIRECT",
      "relationship_status": "ACTIVE",
      "parent_lei": "529900ODI3047E2LIV03",
      "parent_name": "Apple Operations",
      "jurisdiction": "IE",
      "relationship_period_start": "2022-01-15T00:00:00Z",
      "relationship_period_end": null,
      "percentage_ownership": 75.5
    },
    "ultimate_parent": {
      "relationship_type": "ULTIMATE",
      "relationship_status": "ACTIVE",
      "parent_lei": "529900AB12345E67890Z",
      "parent_name": "Apple Holding Corporation",
      "jurisdiction": "US",
      "relationship_period_start": "2020-06-10T00:00:00Z",
      "relationship_period_end": null,
      "percentage_ownership": 100
    }
  }
}
```

### Get Entity Children

Retrieves all child entities of a specific legal entity.

```http
GET /relationships/{lei}/children
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| lei | string | Legal Entity Identifier (20 characters) |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| relationship_status | string | Filter by relationship status ("ACTIVE", "INACTIVE") |
| jurisdiction | string | Filter children by jurisdiction (ISO 3166-1 code) |
| page | integer | Page number for paginated results (default: 1) |
| per_page | integer | Number of records per page (default: 20, max: 100) |

#### Example Request

```http
GET /relationships/529900AB12345E67890Z/children?relationship_status=ACTIVE&page=1&per_page=10
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": {
    "entity": {
      "lei": "529900AB12345E67890Z",
      "name": "Apple Holding Corporation",
      "jurisdiction": "US"
    },
    "children": [
      {
        "relationship_type": "DIRECT",
        "relationship_status": "ACTIVE",
        "child_lei": "HWUPKR0MPOU8FGXBT394",
        "child_name": "APPLE INC",
        "child_jurisdiction": "US",
        "relationship_period_start": "2022-01-15T00:00:00Z",
        "relationship_period_end": null,
        "percentage_ownership": 75.5
      },
      {
        "relationship_type": "DIRECT",
        "relationship_status": "ACTIVE",
        "child_lei": "549300EVRK4JBPWJXL51",
        "child_name": "APPLE OPERATIONS INTERNATIONAL LIMITED",
        "child_jurisdiction": "IE",
        "relationship_period_start": "2020-03-22T00:00:00Z",
        "relationship_period_end": null,
        "percentage_ownership": 100
      }
    ]
  },
  "meta": {
    "page": 1,
    "per_page": 10,
    "total": 2,
    "entity_lei": "529900AB12345E67890Z"
  }
}
```

### Get Corporate Group

Retrieves the complete corporate group structure for a specific legal entity, including the entity itself, its parents, and all its direct and indirect children.

```http
GET /relationships/{lei}/group
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| lei | string | Legal Entity Identifier (20 characters) |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| max_depth | integer | Maximum depth of the hierarchy to retrieve (default: 3) |
| relationship_status | string | Filter by relationship status ("ACTIVE", "INACTIVE") |
| include_exceptions | boolean | Include relationship reporting exceptions (default: true) |

#### Example Request

```http
GET /relationships/529900AB12345E67890Z/group?max_depth=2&relationship_status=ACTIVE
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": {
    "entity": {
      "lei": "529900AB12345E67890Z",
      "name": "Apple Holding Corporation",
      "jurisdiction": "US",
      "status": "ACTIVE"
    },
    "relationships": {
      "parents": {
        "direct": null,
        "ultimate": null
      },
      "children": [
        {
          "lei": "HWUPKR0MPOU8FGXBT394",
          "name": "APPLE INC",
          "jurisdiction": "US",
          "status": "ACTIVE",
          "relationship": {
            "type": "DIRECT",
            "status": "ACTIVE",
            "period_start": "2022-01-15T00:00:00Z",
            "period_end": null,
            "percentage_ownership": 75.5
          },
          "children": [
            {
              "lei": "549300EVRK4JBPWJXL51",
              "name": "APPLE OPERATIONS INTERNATIONAL LIMITED",
              "jurisdiction": "IE",
              "status": "ACTIVE",
              "relationship": {
                "type": "DIRECT",
                "status": "ACTIVE",
                "period_start": "2021-05-10T00:00:00Z",
                "period_end": null,
                "percentage_ownership": 100
              }
            }
          ]
        },
        {
          "lei": "549300EVRK4JBPWJXL51",
          "name": "APPLE OPERATIONS INTERNATIONAL LIMITED",
          "jurisdiction": "IE",
          "status": "ACTIVE",
          "relationship": {
            "type": "DIRECT",
            "status": "ACTIVE",
            "period_start": "2020-03-22T00:00:00Z",
            "period_end": null,
            "percentage_ownership": 100
          }
        }
      ]
    }
  },
  "meta": {
    "max_depth": 2,
    "entity_lei": "529900AB12345E67890Z",
    "total_entities": 3
  }
}
```

### Get Relationship History

Retrieves the history of a specific relationship between two legal entities.

```http
GET /relationships/history
```

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| parent_lei | string | Legal Entity Identifier of the parent entity |
| child_lei | string | Legal Entity Identifier of the child entity |
| relationship_type | string | Filter by relationship type ("DIRECT", "ULTIMATE") |

#### Example Request

```http
GET /relationships/history?parent_lei=529900AB12345E67890Z&child_lei=HWUPKR0MPOU8FGXBT394
Authorization: Bearer YOUR_API_KEY
```

#### Example Response

```json
{
  "status": "success",
  "data": {
    "parent_entity": {
      "lei": "529900AB12345E67890Z",
      "name": "Apple Holding Corporation",
      "jurisdiction": "US"
    },
    "child_entity": {
      "lei": "HWUPKR0MPOU8FGXBT394",
      "name": "APPLE INC",
      "jurisdiction": "US"
    },
    "history": [
      {
        "relationship_type": "DIRECT",
        "relationship_status": "ACTIVE",
        "period_start": "2022-01-15T00:00:00Z",
        "period_end": null,
        "percentage_ownership": 75.5,
        "last_updated": "2022-01-15T00:00:00Z"
      },
      {
        "relationship_type": "DIRECT",
        "relationship_status": "ACTIVE",
        "period_start": "2020-06-10T00:00:00Z",
        "period_end": "2022-01-15T00:00:00Z",
        "percentage_ownership": 70.2,
        "last_updated": "2020-06-10T00:00:00Z"
      },
      {
        "relationship_type": "DIRECT",
        "relationship_status": "INACTIVE",
        "period_start": "2018-03-05T00:00:00Z",
        "period_end": "2020-06-10T00:00:00Z",
        "percentage_ownership": 65.0,
        "last_updated": "2018-03-05T00:00:00Z"
      }
    ]
  }
}
```
