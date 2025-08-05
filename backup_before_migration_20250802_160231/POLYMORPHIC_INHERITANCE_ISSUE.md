# SQLAlchemy Polymorphic Inheritance Issue Summary

## Current Status (August 2, 2025)

### What's Working ✅
- **Instrument Creation**: POST `/api/v1/instruments` successfully creates instruments
- **Database Population**: Both `instruments` and `equities` tables are populated with matching IDs
- **FIGI/LEI Integration**: External data enrichment works correctly
- **Basic Data Integrity**: IDs are generated and stored properly in SQL Server

### What's NOT Working ❌
- **Instrument Retrieval**: GET `/api/v1/instruments` returns empty results despite data existing
- **Polymorphic Queries**: SQLAlchemy inheritance queries fail with network/timeout errors
- **API Response Data**: All GET endpoints return empty data or null IDs

## Technical Details

### Database Schema
- **instruments table**: Contains base instrument data (id, isin, type, full_name, etc.)
- **equities table**: Contains equity-specific data with foreign key to instruments.id
- **Relationship**: `equities.id` → `instruments.id` (joined table inheritance)

### SQLAlchemy Model Structure
```python
class Instrument(BaseModel):
    __tablename__ = "instruments"
    __mapper_args__ = {
        'polymorphic_identity': 'instrument',
        'polymorphic_on': 'type'
    }
    id = Column(String(36), primary_key=True)
    type = Column(String(50), nullable=False)
    # ... other fields

class Equity(Instrument):
    __tablename__ = 'equities'
    __mapper_args__ = {'polymorphic_identity': 'equity'}
    id = Column(String(36), ForeignKey('instruments.id'), primary_key=True)
    # ... equity-specific fields
```

### The Core Problem
1. **Direct SQLAlchemy queries work**: `session.query(Instrument).count()` returns correct count
2. **API endpoint queries fail**: Same query in Flask routes returns 0 results
3. **Network errors in logs**: SQL Server connection timeouts during polymorphic queries
4. **Complex JOIN generation**: SQLAlchemy inheritance creates complex queries that timeout

### Error Patterns
- HTTP 500 errors in logs but HTTP 200 responses to clients
- Network errors: `[DBNETLIB]Connection interrupted` 
- Swedish error messages: `Nätverksfel - se dokumentationen för nätverket`
- Precision errors when trying to insert NULL into NUMERIC columns

### Current Workaround
- **Creation**: Use base `Instrument` creation + raw SQL insert for child table
- **Retrieval**: Still broken - needs solution

## What Needs to Be Fixed

### 1. Query Strategy
The polymorphic inheritance queries are too complex for the SQL Server setup. Need to either:
- Simplify the inheritance mapping
- Use direct table queries instead of polymorphic queries
- Fix the SQL Server connection timeout issues

### 2. API Response Format
The GET endpoints return data under `response.data` but may expect different format:
```json
{
  "status": "success",
  "data": [...],     // ← Current format
  "meta": {...}
}
```

### 3. Session Management
Potential issues with SQLAlchemy session handling in Flask routes causing queries to fail.

## Files Modified
- `marketdata_api/models/instrument.py`: Fixed inheritance definitions
- `marketdata_api/services/instrument_service.py`: Added raw SQL insertion for child tables
- `marketdata_api/routes/instrument_routes.py`: Added debug logging (still failing)

## Next Steps for Resolution
1. **Investigate SQL Server connection**: Check why polymorphic queries cause timeouts
2. **Simplify query approach**: Consider using simple table queries instead of inheritance
3. **Test inheritance mapping**: Create minimal test case to isolate the SQLAlchemy issue
4. **Review session handling**: Ensure proper session management in Flask routes
5. **Consider alternative patterns**: May need to abandon polymorphic inheritance for a simpler approach

## Key Insight
The inheritance **creation** works perfectly, but **retrieval** fails due to complex JOIN queries timing out. This suggests the SQLAlchemy polymorphic mapping generates queries that are incompatible with the current SQL Server configuration or connection setup.
