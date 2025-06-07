# Development Documentation

## Overview

This section contains technical documentation for developers working on the MarketDataAPI.

## Quick Links

- [Development Setup](setup.md) - How to set up the development environment
- [Database Schema](database.md) - Database models and relationships
- [Service Layer](services.md) - Business logic and data access
- [Route Implementation](routes.md) - API route organization and patterns

## Architecture Overview

```
marketdata_api/
├── models/          # SQLAlchemy models (database schema)
├── services/        # Business logic layer
├── routes/          # API endpoints and documentation
├── database/        # Database connection and session management
└── constants/       # Shared constants and configuration
```

## Documentation Maintenance

### When Adding New Endpoints

1. **Update swagger.py**: Add the endpoint with proper documentation
2. **Update route file**: Implement the actual endpoint logic
3. **Update service**: Add business logic if needed
4. **Update models**: Add database models if needed
5. **Generate docs**: Run documentation generation script

### Documentation Generation

```bash
# Generate OpenAPI YAML from swagger.py
python scripts/generate_openapi.py

# Generate API documentation
python scripts/generate_api_docs.py

# Validate all documentation
python scripts/validate_docs.py
```

## Code Organization Patterns

### Route Files
- Keep route files focused on HTTP handling
- Use services for business logic
- Follow consistent error handling patterns
- Document all endpoints in swagger.py

### Service Files  
- Encapsulate database operations
- Handle business logic validation
- Return consistent data structures
- Manage database sessions properly

### Model Files
- Define clear relationships
- Use appropriate constraints
- Include helpful methods for data access
- Document complex relationships
