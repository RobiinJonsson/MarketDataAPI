# MarketDataAPI Testing Guide

## Quick Start

```bash
# Install test dependencies
deployment\dev.bat install

# Run quick tests
deployment\dev.bat test-quick

# Run full test suite  
deployment\dev.bat test

# Test version upgrade compatibility
deployment\dev.bat test-upgrade

# Generate coverage report
deployment\dev.bat coverage
```

## Test Structure

```
src/marketdata_api/tests/
├── conftest.py              # Shared fixtures and configuration
├── test_cli_modern.py       # CLI functionality tests
├── test_version_upgrade.py  # Version compatibility tests
├── test_data_generator.py   # Test data utilities
├── run_tests.py            # Python test runner
└── *.py.bak                # Legacy tests (temporarily disabled)
```

## Test Categories

### 🚀 Unit Tests (`@pytest.mark.unit`)
Test individual components in isolation:
```bash
python -m pytest -m unit -v
```

### 🔗 Integration Tests (`@pytest.mark.integration`)
Test components working together:
```bash
python -m pytest -m integration -v
```

### 💻 CLI Tests (`@pytest.mark.cli`)
Test command-line interface:
```bash
python -m pytest -m cli -v
```

### 🔄 Upgrade Tests (`@pytest.mark.upgrade`)
Test version compatibility:
```bash
python -m pytest -m upgrade -v
```

### 🐌 Performance Tests (`@pytest.mark.slow`)
Test performance and benchmarks:
```bash
python -m pytest -m slow -v
```

## Version Upgrade Testing

### Pre-Upgrade Testing
```bash
# Comprehensive pre-upgrade validation
deployment\test-upgrade.bat pre-upgrade

# Quick validation before upgrade
deployment\test-upgrade.bat quick
```

### Post-Upgrade Validation
```bash
# Verify upgrade success
deployment\test-upgrade.bat post-upgrade

# Full test suite after upgrade
deployment\test-upgrade.bat full
```

### Upgrade Test Report
```bash
# Generate detailed upgrade compatibility report
python src\marketdata_api\tests\run_tests.py --upgrade-report
```

## Development Workflow

### 1. Before Making Changes
```bash
# Ensure current state is working
deployment\dev.bat test-quick

# Create baseline if doing performance work
python -m pytest -m slow --benchmark-save=baseline
```

### 2. During Development
```bash
# Run relevant tests frequently
python -m pytest src\marketdata_api\tests\test_cli_modern.py -v

# Check specific functionality
deployment\mapi.bat stats
deployment\mapi.bat instruments list --limit 3
```

### 3. Before Committing
```bash
# Full validation
deployment\dev.bat test

# Code quality checks
deployment\dev.bat lint

# Format code if needed
deployment\dev.bat format
```

### 4. Before Version Release
```bash
# Complete upgrade test suite
deployment\dev.bat test-upgrade

# Performance regression check
python -m pytest -m slow --benchmark-compare=baseline

# Generate coverage report
deployment\dev.bat coverage
```

## Test Configuration

### pytest.ini Options
Located in `config/pytest.ini` and `pyproject.toml`:
- Test markers for categorization
- Test path configuration  
- Coverage settings
- Output formatting

### Fixtures
Shared fixtures in `conftest.py`:
- `test_session`: Clean database for each test
- `sample_instrument`: Pre-built instrument data
- `sample_legal_entity`: Pre-built entity data
- `mock_external_services`: Mocked external APIs
- `temp_directory`: Temporary file operations

### Test Data
Use `test_data_generator.py` for consistent test data:
```python
from marketdata_api.tests.test_data_generator import TestDataGenerator

generator = TestDataGenerator()
instruments = generator.generate_instrument_data(5)
entities = generator.generate_legal_entity_data(3)
```

## Continuous Integration

### GitHub Actions
Automated testing on push/PR via `.github/workflows/test.yml`:
- Multi-platform testing (Ubuntu, Windows)
- Multiple Python versions (3.8-3.12)
- Coverage reporting
- Upgrade compatibility checks

### Local CI Simulation
```bash
# Test across scenarios like CI
python -m pytest --tb=short -x  # Stop on first failure
python -m pytest -n auto        # Parallel testing (if pytest-xdist installed)
```

## Troubleshooting

### Common Issues

#### Test Collection Errors
```bash
# Check test discovery
python -m pytest --collect-only -q

# Verify imports
python -c "import marketdata_api.cli; print('Imports OK')"
```

#### Database Connection Issues
```bash
# Verify database exists and is accessible
deployment\mapi.bat stats

# Check database path configuration
python -c "from marketdata_api.config import Config; print(Config.DATABASE_PATH)"
```

#### CLI Path Issues
```bash
# Test CLI portability
cd C:\
C:\Users\robin\Projects\MarketDataAPI\deployment\mapi.bat --help
```

### Performance Issues
```bash
# Identify slow tests
python -m pytest --durations=10

# Profile specific tests
python -m pytest --benchmark-only
```

## Test Coverage Goals

- **Unit Tests**: >95% coverage of core functionality
- **Integration Tests**: All major workflows covered
- **CLI Tests**: All commands and error scenarios
- **Upgrade Tests**: Version compatibility verified

### Coverage Reporting
```bash
# Generate HTML coverage report
deployment\dev.bat coverage
# Opens htmlcov/index.html in browser

# Terminal coverage report
python -m pytest --cov=marketdata_api --cov-report=term-missing
```

## Best Practices

### Writing Tests
1. **Use descriptive test names**: `test_instruments_list_with_currency_filter`
2. **Follow AAA pattern**: Arrange, Act, Assert
3. **Mock external services**: Don't hit real APIs in tests
4. **Use fixtures for common setup**: Shared database states, sample data
5. **Test error conditions**: Not just happy paths

### Test Data
1. **Use consistent test data**: `test_data_generator.py` for reproducible results
2. **Isolate tests**: Each test should work independently
3. **Clean up**: Use fixtures that handle cleanup automatically
4. **Realistic data**: Test with data similar to production

### Performance Testing
1. **Establish baselines**: Save benchmark results for comparison
2. **Test realistic scenarios**: Use representative data sizes
3. **Monitor trends**: Track performance over time
4. **Set acceptable thresholds**: Define what constitutes regression

## Version Upgrade Safety

### Critical Success Criteria
- ✅ **Zero Data Loss**: All data accessible after upgrade
- ✅ **CLI Compatibility**: Commands work from any directory
- ✅ **Config Compatibility**: Old configuration files still work
- ✅ **Performance**: No significant regression (>10% slower)
- ✅ **API Stability**: Existing integrations continue working

### Rollback Procedures
If tests fail during upgrade:
1. **Stop immediately**: Don't continue with failed upgrade
2. **Restore database**: From pre-upgrade backup
3. **Revert configuration**: Restore previous config files  
4. **Validate rollback**: Run tests to ensure system works
5. **Investigate issues**: Debug upgrade problems in isolation

## Resources

- **Test Strategy**: `docs/testing/TEST_STRATEGY.md`
- **Upgrade Guide**: `docs/testing/VERSION_UPGRADE_TESTING.md`
- **API Documentation**: `docs/api/`
- **CLI Reference**: `deployment/mapi.bat --help`

## Support

For testing questions or issues:
1. Check test output logs in `test-results/` folder
2. Review test documentation in `docs/testing/`
3. Run diagnostic commands to isolate issues
4. Check GitHub Issues for known problems
