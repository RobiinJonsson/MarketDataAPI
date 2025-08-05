# Migration Plan: Fresh Start with Dual Database Architecture

## Executive Summary

After 3 days of debugging SQLAlchemy polymorphic inheritance issues with SQL Server, we're implementing a clean architecture with separate database implementations. This document outlines what we've learned and the plan for moving forward.

## What We've Learned (The Good Stuff) ✅

### 1. FIRDS Data Integration
- **Field Mapping**: Successfully mapped FIRDS XML data to database fields
- **Data Validation**: Implemented proper ISIN validation and data cleaning
- **External APIs**: FIGI and LEI enrichment working correctly
- **File Processing**: XML parsing and batch processing established

### 2. Schema Requirements
- **Symbol Column**: Needs 50+ characters (not 20) for complex instrument symbols
- **Numeric Precision**: SQL Server requires DECIMAL/NUMERIC instead of FLOAT for financial data
- **ID Generation**: UUID4 string format works well for cross-system compatibility
- **Constraint Handling**: Foreign key relationships work but need careful session management

### 3. API Patterns
- **POST Endpoints**: Successfully create instruments with proper data validation
- **Error Handling**: Good patterns for validation and error responses established
- **Response Format**: Consistent JSON structure with status/data/meta pattern

### 4. Database Compatibility Issues
- **Polymorphic Inheritance**: Works perfectly with SQLite, fails with SQL Server due to complex JOINs
- **Connection Timeouts**: SQL Server doesn't handle complex inheritance queries well
- **Session Management**: Different behavior between SQLite and SQL Server in Flask context

## Architecture Decision: Dual Implementation

### Current Problem
```
One codebase trying to support both SQLite and SQL Server
├── Polymorphic inheritance (great for SQLite)
├── Complex workarounds for SQL Server
├── Conditional logic scattered everywhere
└── Fragile and hard to debug
```

### New Solution
```
marketdata_api/
├── models/
│   ├── base/                    # Shared interfaces and base classes
│   ├── sqlite/                  # SQLite models (keep polymorphic inheritance)
│   │   ├── __init__.py
│   │   ├── instrument.py        # Polymorphic inheritance model
│   │   └── equity.py
│   └── sqlserver/               # SQL Server models (flattened structure)
│       ├── __init__.py
│       ├── instrument.py        # Single table with instrument_type
│       └── equity_fields.py     # Mixin for equity-specific fields
├── services/
│   ├── base/                    # Shared service interfaces
│   ├── sqlite/                  # SQLite-optimized services
│   └── sqlserver/               # SQL Server-optimized services
├── database/
│   ├── base/                    # Shared database utilities
│   ├── sqlite/                  # SQLite mappers and session handling
│   └── sqlserver/               # SQL Server mappers and session handling
└── config.py                   # Database selection and factory pattern
```

## Recommended SQL Server Model Design

### Instead of Inheritance: Single Table with Type Discrimination

```python
# sqlserver/instrument.py
class Instrument(BaseModel):
    __tablename__ = "instruments"
    
    # Base fields
    id = Column(String(36), primary_key=True)
    isin = Column(String(12), nullable=False, index=True)
    instrument_type = Column(String(50), nullable=False)  # 'equity', 'debt', 'future'
    full_name = Column(String(500))
    symbol = Column(String(50))
    
    # All possible fields (nullable for non-applicable types)
    # Equity fields
    shares_outstanding = Column(DECIMAL(20, 0), nullable=True)
    market_cap = Column(DECIMAL(20, 2), nullable=True)
    voting_rights_per_share = Column(DECIMAL(10, 6), nullable=True)
    
    # Debt fields
    maturity_date = Column(Date, nullable=True)
    coupon_rate = Column(DECIMAL(10, 6), nullable=True)
    
    # Future fields
    expiry_date = Column(Date, nullable=True)
    underlying_asset = Column(String(200), nullable=True)
    
    @property
    def equity_fields(self):
        """Return only equity-relevant fields if this is an equity"""
        if self.instrument_type == 'equity':
            return {
                'shares_outstanding': self.shares_outstanding,
                'market_cap': self.market_cap,
                'voting_rights_per_share': self.voting_rights_per_share
            }
        return {}
```

### Benefits of This Approach
1. **Simple Queries**: No JOINs, no inheritance complexity
2. **Fast Performance**: Single table queries are always fast
3. **Easy Debugging**: Clear SQL queries, easy to understand
4. **Flexible Schema**: Easy to add new instrument types
5. **SQL Server Friendly**: No complex inheritance patterns

## Migration Steps

### Phase 1: Documentation and Backup (Today)
1. ✅ Document current learnings (this file)
2. ✅ Document working FIRDS integration patterns
3. ✅ Backup current database schema and test data
4. ✅ List all working API endpoints and test cases

### Phase 2: New Architecture Setup (Day 1)
1. Create new branch: `feature/dual-database-architecture`
2. Set up new directory structure
3. Create base interfaces and abstract classes
4. Implement database factory pattern in config.py

### Phase 3: SQL Server Implementation (Days 2-3)
1. Design and implement single-table SQL Server models
2. Create SQL Server-specific services
3. Implement SQL Server mappers and session handling
4. Create migration scripts for schema changes

### Phase 4: SQLite Preservation (Day 4)
1. Move current working SQLite code to sqlite/ directory
2. Ensure SQLite functionality remains intact
3. Create SQLite-specific services

### Phase 5: Integration and Testing (Day 5)
1. Implement database selection logic
2. Update API routes to use factory pattern
3. Comprehensive testing of both implementations
4. Performance comparison and optimization

## File Preservation Strategy

### Keep These Working Patterns
```python
# FIRDS data mapping (from model_mapper.py)
def map_firds_to_instrument()  # This works well

# FIGI/LEI integration (from openfigi.py and legal_entity_service.py)
def enrich_with_figi()  # This works perfectly

# API validation patterns (from routes/)
def validate_instrument_data()  # Good patterns established

# Test data samples (from get_test_samples.py)
# These are valuable for testing new implementation
```

### Discard These Problem Areas
```python
# Polymorphic inheritance for SQL Server
# Complex session workarounds
# Conditional database logic scattered throughout
# Band-aid fixes for inheritance issues
```

## Success Metrics for New Implementation

### Performance
- GET `/api/v1/instruments` responds in < 200ms
- POST `/api/v1/instruments` creates records in < 100ms
- No connection timeouts or network errors

### Functionality
- All FIRDS fields correctly mapped and stored
- FIGI/LEI enrichment working for both databases
- Proper error handling and validation
- Comprehensive test coverage

### Maintainability
- Clear separation between database implementations
- No conditional database logic in business code
- Easy to add new instrument types
- Simple debugging and error tracking

## Next Steps

1. **Create backup of current working code**
2. **Set up new branch with clean architecture**
3. **Start with SQL Server single-table implementation**
4. **Gradually migrate working components**

This approach will give you a solid, maintainable foundation that properly handles both SQLite and SQL Server without the complexity and fragility of the current approach.
