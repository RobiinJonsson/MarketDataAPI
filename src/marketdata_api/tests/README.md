# MarketDataAPI Test Suite

Comprehensive test infrastructure for MarketDataAPI with real data integration and version upgrade testing.

## Overview

This test suite provides:
- **Real Data Testing**: Uses actual database samples instead of synthetic data for API compatibility
- **Version Upgrade Testing**: Comprehensive migration and compatibility validation
- **CLI Testing**: Modern Click-based CLI testing with mocking
- **Performance Testing**: Memory and query performance regression detection
- **CI/CD Integration**: GitHub Actions workflow and automated testing

## Quick Start

### Running Tests

```bash
# All tests
python -m pytest

# Specific test categories
python -m pytest -m "unit"          # Unit tests only
python -m pytest -m "integration"   # Integration tests only  
python -m pytest -m "cli"           # CLI tests only
python -m pytest -m "upgrade"       # Version upgrade tests
python -m pytest -m "slow"          # Performance/slow tests

# Specific test files
python -m pytest src/marketdata_api/tests/test_cli_modern.py
python -m pytest src/marketdata_api/tests/test_version_upgrade.py

# Development helpers
deployment\dev.bat test                         # Run test suite via dev script
deployment\dev.bat test-unit                    # Unit tests only
deployment\dev.bat test-cli                     # CLI tests only
```

### Version Upgrade Testing

```bash
# Full upgrade test workflow
deployment/test-upgrade.bat

# Manual upgrade testing
python -m pytest -m "upgrade" -v
python src/marketdata_api/tests/run_tests.py upgrade
```

## Test Categories

### Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit` - Fast unit tests, no external dependencies
- `@pytest.mark.integration` - Integration tests with database/services
- `@pytest.mark.cli` - CLI command testing
- `@pytest.mark.upgrade` - Version upgrade and migration tests  
- `@pytest.mark.slow` - Performance tests and large dataset operations

### Test Structure

```
tests/
├── conftest.py                 # Shared fixtures with real data
├── test_data_real.py          # Real test data provider
├── test_cli_modern.py         # Modern CLI testing framework
├── test_version_upgrade.py    # Version upgrade tests
├── test_data_generator.py     # Synthetic data generator (legacy)
└── run_tests.py              # Python test runner
```

## Real Data Approach

### Why Real Data?

We use **real data samples from the production database** instead of synthetic data because:

- **API Compatibility**: External services (ESMA, GLEIF, OpenFIGI) require real identifiers
- **Realistic Testing**: Actual ISINs, MIC codes, and LEI identifiers behave correctly
- **Integration Validation**: Tests work with real external API responses
- **Data Quality**: Ensures production data format compatibility

### Available Real Data

The `test_data_real.py` module provides:

**Real Instruments:**
- `SE0000120784` - Skandinaviska Enskilda Banken AB (SEB)
- `CH0012221716` - ABB Ltd  
- `SE0007100581` - Assa Abloy AB
- `GB0009895292` - AstraZeneca PLC
- `XS2908107019` - ING Groep N.V.

**Real MIC Codes:**
- `XSTO` - NASDAQ STOCKHOLM AB
- `DRSP` - NASDAQ FIRST NORTH GROWTH MARKET (SWEDEN)
- `XCNQ` - CANADIAN NATIONAL STOCK EXCHANGE
- `XNGS` - NASDAQ GLOBAL SELECT MARKET
- `XLON` - LONDON STOCK EXCHANGE

**Real LEI Identifiers:**
- `549300KBQIVNEJEZVL96` - NASDAQ STOCKHOLM AB
- `F3JS33DEI6XQ4ZBPTN86` - Skandinaviska Enskilda Banken AB

### Using Real Data in Tests

```python
from .test_data_real import get_test_instrument, get_test_lei, get_test_mic

# Get real instrument data
instrument = get_test_instrument()  # Returns real SEB data
print(instrument["isin"])          # SE0000120784

# Get real MIC code
mic = get_test_mic()               # Returns real NASDAQ Stockholm
print(mic["mic"])                  # XSTO

# Get real LEI
lei = get_test_lei()               # Returns real LEI identifier
print(lei)                         # 549300KBQIVNEJEZVL96
```

## Test Infrastructure

### Fixtures (conftest.py)

Shared pytest fixtures using real data:

- `sample_instrument()` - Real instrument from database
- `sample_legal_entity()` - Real legal entity data
- `sample_mic_code()` - Real MIC code data
- `sample_transparency_calculation()` - Real transparency data
- `test_session()` - Database session for testing
- `mock_external_services()` - Mocked API responses

### CLI Testing (test_cli_modern.py)

Modern CLI testing framework:

```python
class TestCLIBasics:
    def test_cli_help(self):
        """Test CLI help output."""
        
class TestInstrumentsCommands:
    def test_instruments_get_success(self, mock_service):
        """Test successful instrument retrieval."""
```

### Version Upgrade Testing (test_version_upgrade.py)

Comprehensive upgrade validation:

```python
class TestDatabaseMigrations:
    def test_database_migration_forward(self):
        """Test forward database migrations."""
        
class TestCLICompatibility:
    def test_cli_command_stability(self):
        """Ensure CLI commands remain stable across versions."""
```

## Development Workflow

### Pre-Commit Testing

```bash
# Quick validation before commits
python -m pytest -m "unit" --maxfail=1
deployment\dev.bat test-unit
```

### Integration Testing

```bash
# Full integration test suite
python -m pytest -m "integration" -v
deployment\dev.bat test-integration
```

### Performance Monitoring

```bash
# Performance regression tests
python -m pytest -m "slow" -v --durations=10
```

### Upgrade Testing Workflow

```bash
# 1. Pre-upgrade validation
python -m pytest -m "upgrade" --tb=short

# 2. Run upgrade script
deployment/test-upgrade.bat

# 3. Post-upgrade validation
python -m pytest -m "integration" --maxfail=5
```

## Configuration

### pytest.ini / pyproject.toml

```toml
[tool.pytest.ini_options]
minversion = "6.0"
testpaths = ["src/marketdata_api/tests"]
markers = [
    "unit: Fast unit tests",
    "integration: Integration tests", 
    "cli: CLI command tests",
    "upgrade: Version upgrade tests",
    "slow: Performance and slow tests"
]
```

### Test Environment Setup

```bash
# Install test dependencies
pip install pytest pytest-mock click

# Configure Python environment
python src/marketdata_api/tests/conftest.py

# Verify test data
python -c "from src.marketdata_api.tests.test_data_real import *; print('Real data OK')"
```

## Continuous Integration

### GitHub Actions

The `.github/workflows/test.yml` workflow runs:

1. **Unit Tests** - Fast validation on every push
2. **Integration Tests** - Database and API integration  
3. **CLI Tests** - Command-line interface validation
4. **Upgrade Tests** - Migration safety validation

### Local CI Simulation

```bash
# Simulate CI pipeline locally
deployment\dev.bat test-all
deployment/test-upgrade.bat --ci-mode
```

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure Python path is correct
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python -c "import marketdata_api; print('Import OK')"
```

**Database Issues:**
```bash
# Reset test database
python scripts/init_azure_sql.py --test-mode
python -m pytest src/marketdata_api/tests/test_database_connection.py
```

**Real Data Problems:**
```bash
# Verify real data availability
python -c "from src.marketdata_api.tests.test_data_real import *; print(get_test_instrument())"
```

### Test Performance

**Slow Tests:**
```bash
# Profile slow tests
python -m pytest --durations=10 -v

# Run only fast tests
python -m pytest -m "not slow"
```

**Memory Issues:**
```bash
# Monitor memory usage during tests
python -m pytest -m "upgrade" --tb=short --maxfail=1
```

## Best Practices

### Writing New Tests

1. **Use Real Data**: Import from `test_data_real.py` 
2. **Mark Tests**: Add appropriate `@pytest.mark.{category}` markers
3. **Mock External APIs**: Use fixtures from `conftest.py`
4. **Test CLI Commands**: Use `CliRunner` for CLI testing
5. **Validate Upgrades**: Add upgrade compatibility tests

### Test Organization

```python
# Good: Organized by functionality
class TestInstrumentsAPI:
    def test_create_instrument(self):
        pass
    
    def test_update_instrument(self):
        pass

# Good: Clear test names
def test_cli_instruments_get_returns_correct_format(self):
    pass
```

### Performance Considerations

- Mark slow tests with `@pytest.mark.slow`
- Use real data sparingly in performance tests
- Profile database queries in upgrade tests
- Monitor memory usage in large dataset tests

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python -m pytest` | Run all tests |
| `python -m pytest -m "unit"` | Unit tests only |
| `deployment\dev.bat test` | Development test runner |
| `deployment/test-upgrade.bat` | Full upgrade testing |
| `python -m pytest --collect-only` | List all available tests |
| `python -m pytest -k "cli"` | Tests matching pattern |
| `python -m pytest --lf` | Run last failed tests |
| `python -m pytest --tb=short` | Short traceback format |

For more details, see the individual test files and the `docs/testing/` directory.
