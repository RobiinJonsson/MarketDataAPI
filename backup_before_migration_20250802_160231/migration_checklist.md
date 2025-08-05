# Migration Checklist

## Phase 1: Setup (Day 1)
- [ ] Create new branch: `feature/dual-database-architecture`
- [ ] Set up directory structure:
  - [ ] `marketdata_api/models/base/`
  - [ ] `marketdata_api/models/sqlite/`
  - [ ] `marketdata_api/models/sqlserver/`
  - [ ] `marketdata_api/services/base/`
  - [ ] `marketdata_api/services/sqlite/`
  - [ ] `marketdata_api/services/sqlserver/`
  - [ ] `marketdata_api/database/base/`
  - [ ] `marketdata_api/database/sqlite/`
  - [ ] `marketdata_api/database/sqlserver/`

## Phase 2: Base Interfaces (Day 1-2)
- [ ] Create `models/base/instrument_interface.py`
- [ ] Create `services/base/instrument_service_interface.py`
- [ ] Create `database/base/database_factory.py`
- [ ] Update `config.py` with database selection logic

## Phase 3: SQL Server Implementation (Days 2-4)
- [ ] Design single-table SQL Server model
- [ ] Implement SQL Server instrument service
- [ ] Create SQL Server data mapper
- [ ] Test basic CRUD operations
- [ ] Integrate FIRDS data mapping
- [ ] Test FIGI/LEI enrichment

## Phase 4: SQLite Preservation (Day 4)
- [ ] Move current models to `sqlite/` directory
- [ ] Ensure SQLite functionality intact
- [ ] Update imports and references

## Phase 5: Integration (Day 5)
- [ ] Update API routes to use factory pattern
- [ ] Comprehensive testing
- [ ] Performance benchmarks
- [ ] Documentation updates

## Success Criteria
- [ ] GET `/api/v1/instruments` responds < 200ms
- [ ] POST `/api/v1/instruments` creates in < 100ms
- [ ] No connection timeouts
- [ ] All FIRDS fields correctly mapped
- [ ] FIGI/LEI enrichment working
- [ ] Both SQLite and SQL Server working
