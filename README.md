# MarketDataAPI

Comprehensive market data management system with CFI-based instrument classification, integrating FIRDS, OpenFIGI, ISO10383 (MIC), and GLEIF data sources.

## Key Features

- **Type-Specific Intelligence**: Comprehensive attribute extractors for all 10 CFI instrument types with intelligent field mapping from 254 FIRDS data elements
- **Rich API Responses**: Enterprise-grade endpoints delivering detailed instrument analysis with contract specifications, risk metrics, and business intelligence
- **Advanced Classification**: CFI-driven smart categorization with automatic sub-type detection (Interest Rate Swaps, Call/Put Options, Government Bonds, etc.)
- **Financial Analytics**: Time-to-maturity calculations, expiration tracking, strike price analysis, yield calculations, and protection level assessment
- **Enhanced Derivatives Support**: Comprehensive swap, future, and option analysis with reference rates, underlying assets, and settlement details
- **MIC Code Integration**: Complete ISO 10383 Market Identification Code system with dual-mode operations
- **CFI-Based Architecture**: ISO 10962 compliant CFI code system as single source of truth for all instrument routing and validation
- **Unified Data Models**: JSON-based architecture supporting all 10 FIRDS instrument types (C,D,E,F,H,I,J,O,R,S) with promoted field optimization
- **Performance Optimized**: CFI-driven file filtering and single-pass FIRDS processing reduces I/O operations by 90%
- **Dual Database Support**: SQLite (development) / Azure SQL (production) with unified transparency calculations
- **Complete Data Integration**: FIRDS/FITRS integration with intelligent type detection and field normalization
- **GLEIF API Integration**: Live LEI data retrieval and entity creation from GLEIF public API
- **Professional CLI**: Modern command-line interface with Rich formatting and type-specific displays
- **Smart File Management**: Precise regex-based pattern matching for FIRDS/FITRS files
- **Complete API Documentation**: Interactive Swagger UI at `/api/v1/swagger` with comprehensive endpoint testing

## Quick Start

```bash
# Clone and setup
git clone [repository-url]
cd MarketDataAPI
python -m venv venv
source venv/bin/activate  # Unix
.\venv\Scripts\activate   # Windows

# Install and initialize
pip install -r requirements.txt
pip install -e .
python -m marketdata_api.database.base

# Verify installation
marketdata --help
marketdata stats

# Start API server
marketdata api start
```

## Recent Major Improvements

### Type-Specific Attribute Extractors (October 2025)
- Complete CFI coverage: Intelligent attribute extraction for all 10 major instrument types with comprehensive FIRDS field analysis
- Rich business logic: Contract specifications, expiration analysis, pricing information, risk attributes, and intelligent classification
- Production-ready API: Enhanced `/api/v1/instruments/{isin}` endpoints returning detailed `{instrument_type}_attributes` objects
- Advanced analytics: Automatic calculations for time-to-maturity, strike analysis, swap classification, fund categorization
- Enterprise intelligence across all major instrument types including swaps, options, futures, debt, equity, structured products, and collective investment

### Flask-RESTX API Consolidation (October 2025)
- Major architecture cleanup: Eliminated dual API systems, consolidated into single `api/` folder
- Massive code reduction: Removed 2,658 lines of duplicate endpoint code across 6 obsolete files
- Clean organization: All API code properly organized with utilities, models, and resources
- Zero breaking changes: All endpoints maintain identical functionality and response formats
- Enhanced utilities: Extracted reusable functions for instrument processing, MIC operations, and response building

### CLI Delete Command & Enrichment Fixes (October 2025)
- New delete command: Complete instrument deletion with `--cascade` and `--force` options
- LEI enrichment fix: Resolved postal_code constraint errors for real-world addresses
- Structured products: Full H-category analysis with 500k+ products and real CFI pattern support
- Database migration: SQLite-compatible table recreation for schema changes

### Comprehensive Swap CLI Enhancement (October 2025)
- Complete swap classification system: Intelligent CFI-driven detection for all 5 major swap types
- Professional display: Enhanced CLI with type-specific indicators and comprehensive FIRDS data integration
- Smart attribute extraction: Reference rates, floating terms, currency pairs, basket ISINs, settlement types
- Real-world validation: Tested with Credit Default and Interest Rate swaps from live data

### Modular CLI Architecture (October 2025)
- Complete modular refactoring: Transformed monolithic CLI into maintainable modular structure
- 9 focused command modules: Separated instruments, transparency, MIC, FIGI, entities, files into individual modules
- 39% code reduction: From 2000+ line monolith to focused modules (100-300 lines each)
- Standalone package ready: Clean architecture enables independent CLI distribution
- Zero breaking changes: All existing commands, imports, and deployment scripts work identically

### Professional CLI Implementation (September 2025)
- Complete CLI rewrite using Click framework with Rich formatting
- All MarketDataAPI functionality accessible via command-line interface
- Enhanced CFI analysis with multi-level classification and business information
- Professional output with Rich tables, panels, and status indicators

### MIC Code Integration (September 2025)
- Complete ISO 10383 support with 2,794 MIC records
- Dual-mode operations: local database storage + remote real-time validation
- Direct integration with ISO 20022 registry
- Smart caching with 60-minute refresh for remote operations

### CFI-Based Validation System (September 2025)
- Single source of truth: all instrument types derived from CFI codes
- Real-time CFI code validation with comprehensive error handling
- Dynamic instrument type loading with live CFI validation
- CFI first character maps directly to file types for optimal search performance

### Unified Transparency Architecture (August 2025)
- Simplified models: unified JSON-based transparency calculations
- Optimized FITRS file search using instrument types for targeted filtering
- Fixed timeout issues: all instruments complete in 4-6 seconds

### Complete FIRDS Support (August 2025)
- Expanded from 3 to all 10 FIRDS instrument types
- Auto-detection of instrument types from filenames
- Promoted frequently-used fields to dedicated columns for performance

## Installation & Configuration

### Installation Options

**Standard Installation:**
```bash
pip install -r requirements.txt
pip install -e .  # Development mode with global CLI access via 'marketdata' command
pip show marketdata-api #Version checking with packages and license
marketdata --version # Version checking
```

**Alternative Methods:**
```bash
pip install .                                              # Production install
pip install build/dist/marketdata_api-1.0.4-py3-none-any.whl  # From built package
docker-compose -f deployment/docker-compose.yml up        # Docker deployment
```

### Environment Setup

Create a `.env` file in the project root:
```env
FLASK_ENV=development
OPENFIGI_API_KEY=your_openfigi_key
DATABASE_URL=sqlite:///marketdata-sqlite-dev.db
```

**Development Environment:**
```bash
set "PYTHONPATH=%PROJECT_ROOT%\src;%PYTHONPATH%"
set "SQLITE_DB_PATH=%PROJECT_ROOT%\src\marketdata_api\database\marketdata-sqlite-dev.db"
```

### CLI Access Verification

```bash
marketdata --help                   # Primary method (after pip install -e .)
marketdata stats                    # Test with database statistics
deployment\mapi.bat --help          # Alternative: Windows wrapper
python -m marketdata_api.cli stats  # Alternative: Direct module execution
```

## Usage

### API Server

```bash
marketdata api start      # Start Flask server on http://localhost:5000
# Alternative: python -m marketdata_api
```

**API Documentation:**
- Interactive Swagger UI: http://127.0.0.1:5000/api/v1/swagger
- ReDoc Documentation: http://127.0.0.1:5000/api/v1/docs
- Base URL: http://127.0.0.1:5000/api/v1

### Command Line Interface

Modern modular CLI with Rich formatting. Access via:
```bash
marketdata [command]                # Primary method (user-friendly)
deployment\mapi.bat [command]       # Alternative: Windows wrapper
python -m marketdata_api.cli [cmd]  # Alternative: Direct module execution
```

**Command Groups:**
- `instruments` - Create, list, get, delete, enrich with CFI validation
- `transparency` - MiFID II calculations and FITRS data  
- `mic` - Market Identification Code operations with ISO registry
- `entities` - Legal entity operations and LEI handling
- `files` - File management and ESMA integration
- Core utilities: `stats`, `cfi`, `init`

**Key Commands:**
```bash
# Database operations
marketdata stats                     # Database statistics
marketdata init                      # Initialize database

# Instrument operations  
marketdata instruments list --limit 10 --type equity
marketdata instruments get SE0000120784
marketdata instruments delete [ISIN] --cascade --force
marketdata instruments enrich SE0000120784

# Transparency and MIC operations
marketdata transparency create SE0000108656
marketdata mic get XNYS

# API server
marketdata api start                 # Start Flask server
```

See CLI help (`marketdata --help`) for complete command reference.

#### Dual Database Migration Management

**MarketDataAPI supports dual database architecture with separate migration paths for SQLite (development) and SQL Server (production) to prevent version conflicts and maintain environment isolation.**

**Dual Alembic Setup:**
- `alembic-sqlite/` - SQLite migrations for development
- `alembic-sqlserver/` - SQL Server migrations for production  
- Independent version control prevents dev/prod conflicts
- Schema compatibility maintained across both databases

**Migration Commands:**
```bash
# Individual database operations
python scripts\dual_alembic.py sqlite-revision -m "Dev schema changes"
python scripts\dual_alembic.py sqlserver-revision -m "Production schema update"
python scripts\dual_alembic.py sqlite-upgrade      # Apply SQLite migrations
python scripts\dual_alembic.py sqlserver-upgrade   # Apply SQL Server migrations

# Synchronized operations (same logical change to both databases)
python scripts\dual_alembic.py sync -m "Add new instrument field"

# Deployment shortcuts
python scripts\dual_alembic.py deploy-dev          # SQLite upgrade (development)
python scripts\dual_alembic.py deploy-prod         # SQL Server upgrade (production)

# Status and monitoring
python scripts\dual_alembic.py status              # Show migration status for both databases
python scripts\dual_alembic.py sqlite-current      # Current SQLite migration
python scripts\dual_alembic.py sqlserver-history   # SQL Server migration history
```

**Environment Requirements:**
- **SQLite**: No additional configuration required
- **SQL Server**: Requires environment variables:
  - `AZURE_SQL_SERVER`, `AZURE_SQL_DATABASE`, `AZURE_SQL_USERNAME`, `AZURE_SQL_PASSWORD`

**Migration Strategy:**
1. **Development**: Create and test changes using SQLite migrations
2. **Schema Sync**: Use `sync` command to create matching SQL Server migrations
3. **Production Deploy**: Apply SQL Server migrations to production database
4. **Independent Evolution**: Each database maintains separate version history

#### Database Backup & Recovery

**Complete backup system with automated safety backups and recovery capabilities.**

```bash
# Create manual backup
python -m marketdata_api.database.database_backup backup

# Create backup with description
python -m marketdata_api.database.database_backup backup --type manual --description "Before major update"

# List all available backups
python -m marketdata_api.database.database_backup list

# Create daily automated backup
python -m marketdata_api.database.database_backup daily

# Restore from backup
python -m marketdata_api.database.database_backup restore [backup_file]

# Verify backup integrity
python -m marketdata_api.database.database_backup verify [backup_file]

# Clean up old backups
python -m marketdata_api.database.database_backup cleanup --days 30
```

**Features:**
- **Automated Pre-Operation Backups**: System automatically creates safety backups before major operations
- **Smart Configuration**: Uses `Config.DATABASE_PATH` and stores backups in `data/database_backups/`
- **Metadata Tracking**: Each backup includes timestamp, type, and description metadata
- **Size Monitoring**: Track database growth over time (e.g., 1.1MB → 10.2MB progression)
- **Integrity Verification**: Built-in backup validation and corruption detection
- **Retention Management**: Configurable cleanup policies for old backups

**Important Notes:**
- Always run from project root: `C:\Users\robin\Projects\MarketDataAPI`
- Use module syntax for proper import resolution: `python -m marketdata_api.database.database_backup`
- Backup logs are written to `logs/database_backup.log`
- Pre-operation backups are created automatically by the system

#### Terminal Output
The CLI provides professional formatting with organized data display, comprehensive details in bordered sections, and clear status indicators for all operations.

### API Endpoints

#### MIC Code Operations
- `GET /api/v1/mic/` - List MICs with advanced filtering
- `GET /api/v1/mic/{mic_code}` - Detailed MIC information with trading venues
- `GET /api/v1/mic/{mic_code}/segments` - Get segment MICs for operating MIC
- `GET /api/v1/mic/countries` - Countries with MIC counts and statistics
- `GET /api/v1/mic/search` - Advanced MIC search by name, entity, or code
- `GET /api/v1/mic/statistics` - Registry statistics and data quality metrics
- `POST /api/v1/mic/load-data` - Load from local file or remote source
- `GET /api/v1/mic/enums` - Available enum values for MIC fields

#### Remote MIC Operations (Real-time)
- `GET /api/v1/mic/remote/lookup/{mic_code}` - Direct lookup from ISO registry
- `GET /api/v1/mic/remote/search` - Real-time search in official data
- `GET /api/v1/mic/remote/country/{country_code}` - Country MICs from official source
- `GET /api/v1/mic/remote/validate/{mic_code}` - Official MIC validation
- `POST /api/v1/mic/remote/cache/clear` - Clear remote data cache

#### CFI & Instrument Classification
- `GET /api/v1/instruments/types` - Get valid instrument types from CFI system
- `GET /api/v1/instruments/cfi/{cfi_code}` - Comprehensive CFI decoding with business types
- `GET /api/v1/instruments/{isin}/cfi` - Classify existing instruments using CFI codes
- `POST /api/v1/instruments` - CFI-validated instrument creation with consistency checks

#### Core Operations
- `GET/POST /api/v1/instruments` - Instrument management with CFI validation
- `GET/POST /api/v1/entities` - Legal entity operations  
- `GET/POST /api/v1/transparency` - MiFID II transparency calculations with CFI support
- `POST /api/v1/files/download-by-criteria` - Main endpoint for downloading by date/type/dataset
- `GET /api/v1/files` - List files with advanced filtering
- `POST /api/v1/batch/instruments` - Bulk instrument processing

## Performance Metrics

- **File Search Optimization**: 90% reduction in I/O operations via CFI-based targeting
- **API Response Time**: <5 seconds for complex instruments (previously 70+ seconds)
- **Validation Accuracy**: 100% CFI compliance with real-time frontend feedback
- **Coverage**: All 10 FIRDS instrument types supported (up from 3)
- **Success Rate**: 100% instrument processing (eliminated timeouts)

## Integration Examples

### MIC Code Operations
```bash
# Validate MIC code (real-time from ISO registry)
curl -X GET "http://localhost:5000/api/v1/mic/remote/validate/XNYS"
# Returns: {"valid": true, "mic_code": "XNYS", "market_name": "NEW YORK STOCK EXCHANGE, INC.", "status": "ACTIVE"}

# Search for US exchanges
curl -X GET "http://localhost:5000/api/v1/mic/search?name=New York&country=US"

# Get all segment MICs for an operating MIC
curl -X GET "http://localhost:5000/api/v1/mic/XNYS/segments"

# Load latest MIC data from official source
curl -X POST "http://localhost:5000/api/v1/mic/load-data" \
  -H "Content-Type: application/json" \
  -d '{"source": "remote"}'
```

### CFI Integration Examples
```bash
# Validate CFI Code
curl -X GET "http://localhost:5000/api/v1/instruments/cfi/ESVUFR"
# Returns: Complete CFI breakdown + business type + file patterns

# Classify Existing Instrument
curl -X GET "http://localhost:5000/api/v1/instruments/US0378331005/cfi"
# Returns: CFI classification + consistency check with current type

# Create Instrument with CFI Validation
curl -X POST "http://localhost:5000/api/v1/instruments" \
  -H "Content-Type: application/json" \
  -d '{"isin": "US0378331005", "type": "equity", "cfi_code": "ESVUFR"}'
# Auto-validates CFI matches instrument type
```

## Development

### Development Workflow

**Building and Testing:**
```bash
python -m build                           # Build package (creates wheel/source in build/dist/)
deployment\dev.bat test                   # Full test suite
deployment\dev.bat test-quick             # Quick tests
deployment\dev.bat coverage               # Coverage report
```

**Version Management:**
```bash
deployment\upgrade.bat 1.0.5             # Semi-automated version upgrade
git tag v1.0.4                           # Create version tag
git push origin dev --tags               # Push to dev branch
git checkout main && git merge dev       # Merge to main (release branch)
git push origin main --tags              # Push to main branch
git checkout dev                         # Continue development
```

**Development Environment:**
```bash
deployment\dev.bat [command]             # Development wrapper script
```

### Production Deployment

**Docker (Recommended):**
```bash
docker-compose -f deployment/docker-compose.yml up -d
```

**Production Servers:**
```bash
# Linux/macOS with Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "marketdata_api:create_app()"

# Windows with Waitress  
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 marketdata_api:create_app
```

**Environment Configuration:**
```env
# .env file for production
DATABASE_URL=sqlite:///data/marketdata-sqlite-dev.db
FLASK_ENV=production
FLASK_DEBUG=false
SECRET_KEY=your-production-secret-key
```

**Database Schema Migrations:**
```bash
# SQLite operations
alembic -c alembic-sqlite/alembic.ini current
alembic -c alembic-sqlite/alembic.ini history  
alembic -c alembic-sqlite/alembic.ini revision --autogenerate -m "message"
alembic -c alembic-sqlite/alembic.ini upgrade head

# SQL Server operations  
alembic -c alembic-sqlserver/alembic.ini current
alembic -c alembic-sqlserver/alembic.ini revision --autogenerate -m "message"
alembic -c alembic-sqlserver/alembic.ini upgrade head

# Equivalent operations using the script
python scripts/dual_alembic.py sqlite-current
python scripts/dual_alembic.py sqlite-revision -m "message" 
python scripts/dual_alembic.py sqlserver-current
python scripts/dual_alembic.py status  # Shows both systems at once
´´´
## Project Structure

```
MarketDataAPI/
├── src/marketdata_api/              # Main package
│   ├── api/                         # Unified Flask-RESTX API
│   │   ├── models/                  # API response models (organized by domain)
│   │   ├── resources/               # API endpoint implementations
│   │   ├── utils/                   # Shared API utilities
│   │   │   ├── type_specific_responses.py  # Type-specific attribute extractors (10 CFI types)
│   │   │   ├── instrument_utils.py         # Instrument processing utilities
│   │   │   ├── mic_utils.py               # MIC code operations
│   │   │   ├── response_builders.py       # Response formatting utilities
│   │   │   └── transparency_utils.py      # Rich transparency calculations
│   │   └── config.py                # API configuration
│   ├── cli/                         # Modular CLI implementation
│   ├── models/                      # Database models (dual database support)
│   │   ├── sqlite/                  # SQLite model implementations
│   │   └── sqlserver/               # SQL Server model implementations
│   ├── services/                    # Business logic layer
│   │   ├── sqlite/                  # SQLite service implementations
│   │   └── external APIs            # GLEIF, OpenFIGI, MIC integrations
│   ├── database/                    # Database configuration and initialization
│   ├── interfaces/                  # Service abstractions and factories
│   ├── schema/                      # Database schema utilities
│   ├── tests/                       # Test suite
│   ├── config.py                    # Application configuration
│   └── constants.py                 # Centralized constants and configuration
├── alembic/                         # Database migrations
├── config/                          # Configuration files
│   ├── alembic.ini                  # Database migrations config
│   └── pytest.ini                  # Testing configuration
├── data/                            # Data storage (gitignored)
│   ├── downloads/                   # ESMA data downloads
│   ├── database_backups/            # Database backup files
│   └── logs/                        # Application logs
├── deployment/                      # Deployment files
│   ├── mapi.bat                     # CLI wrapper script
│   ├── install.bat/.sh              # Installation scripts
│   └── upgrade.bat                  # Package upgrade script
├── alembic-sqlite/                  # SQLite migration configuration
│   ├── env.py                       # SQLite-specific migration environment
│   └── versions/                    # SQLite migration history
├── alembic-sqlserver/               # SQL Server migration configuration
│   ├── env.py                       # SQL Server-specific migration environment
│   └── versions/                    # SQL Server migration history
├── docs/                            # Documentation
├── examples/                        # Usage examples
├── frontend-modern/                 # Modern TypeScript frontend
│   ├── src/                         # TypeScript source code
│   ├── dist/                        # Built frontend assets
│   └── package.json                 # Frontend build configuration
├── scripts/                         # Utility scripts
├── setup.py                         # Package installation with CLI entry points
├── pyproject.toml                   # Modern Python packaging
├── requirements.txt                 # Python dependencies
└── README.md, CHANGELOG.md, LICENSE # Documentation
```

### Key Architecture Benefits

- **Clean separation**: Code, config, deployment, and data are properly separated
- **Standard Python layout**: Follows PEP 518 and modern packaging standards
- **Build isolation**: All build artifacts contained in `build/` directory
- **Unified API**: Single Flask-RESTX implementation eliminates duplicate code
- **Modular CLI**: Command groups organized by business functionality
- **CFI-driven design**: All instrument operations use CFI codes as primary classification
- **Rich utilities**: Shared response formatting and business logic extraction
- **Type safety**: Comprehensive models and validation throughout the stack

## Technical Stack

- **Backend**: Python 3.8+, Flask, SQLAlchemy 2.0+, Click CLI, Rich formatting
- **Data Sources**: FIRDS (10 types), FITRS, OpenFIGI API, GLEIF API, ISO 10383 MIC registry
- **Database**: SQLite (development), Azure SQL (production), Alembic migrations
- **Frontend**: Modern TypeScript, Vite, Tailwind CSS
- **API**: Flask-RESTX, OpenAPI 3.0, Swagger UI, comprehensive validation
- **Classification**: ISO 10962 CFI codes, 254 FIRDS field analysis

## Type-Specific Attributes System

The `api/utils/type_specific_responses.py` module implements comprehensive data extraction and enrichment based on CFI classification:

### CFI Type Extractors
- **Swaps (S)**: Reference rates, settlement types, floating terms, swap classifications
- **Futures (F)**: Contract specifications, delivery types, expiration tracking, underlying assets  
- **Options (O)**: Strike prices, exercise styles, barrier features, underlying mapping
- **Debt (D)**: Maturity analysis, interest rate types, convertible bond detection
- **Equity (E)**: Share classifications, voting rights analysis, dividend information
- **Rights (R)**: Exercise price analysis, underlying mapping, expiry status tracking
- **Collective Investment (C)**: Fund strategies, distribution policies, geographic focus
- **Structured Products (I)**: Capital protection analysis, participation rates, barrier classifications
- **Spot (H)**: FX pair detection, commodity categorization, settlement analysis  
- **Forward (J)**: Contract terms, underlying assets, maturity calculations

### Intelligence Features
- **254 FIRDS Fields Analyzed**: Comprehensive categorization into dates, rates, contract specs, underlying assets
- **Business Logic**: Automatic sub-type detection and intelligent naming
- **Time Calculations**: Days-to-expiry, time-to-maturity, term classifications
- **Risk Analysis**: Protection levels, barrier detection, enhanced rights assessment

### API Integration
- **Rich Responses**: `/api/v1/instruments/{isin}` returns detailed `{instrument_type}_attributes`
- **Raw Data Access**: `/api/v1/instruments/{isin}/raw` for development comparison
- **Consistent Structure**: Standardized field normalization across all types
- **Performance Optimized**: Single-pass FIRDS processing with lazy evaluation

## CFI Code Support

Complete ISO 10962 CFI code support:

### Supported Categories
- **C** - Collective Investment Vehicles (Funds, ETFs, etc.)
- **D** - Debt instruments (Bonds, Notes, etc.) 
- **E** - Equities (Common shares, Preferred shares, etc.)
- **F** - Futures (Commodities, Financial, etc.)
- **H** - Non-listed and complex products
- **I** - Others (Interest rate instruments, etc.)
- **J** - Forwards (Forward contracts, Warrants in FIRDS context)
- **O** - Options (Calls, Puts, etc.)
- **R** - Entitlements (Rights, Warrants, etc.)
- **S** - Swaps (Credit Default, Interest Rate, Equity Total Return, Foreign Exchange, OIS)
- **K** - Commodity derivatives
- **L** - Structured products
- **M** - Financing instruments
- **N** - Referential instruments
- **T** - Other assets

### Business Type Mapping
CFI codes automatically map to business instrument types:
- C → `collective_investment`, D → `debt`, E → `equity`, F → `future`, J → `forward`, O → `option`, R → `rights`, S → `swap`

## Requirements

- **Python**: 3.8+ with virtual environment
- **Database**: SQLite 3 (included) or Azure SQL
- **Dependencies**: See `requirements.txt` for complete package list

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
