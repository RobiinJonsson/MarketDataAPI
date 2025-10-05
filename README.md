# MarketDataAPI

Comprehensive market data management system with CFI-based instrument classification, integrating FIRDS, OpenFIGI, ISO10383 (MIC), and GLEIF data sources.

## Key Features

- **Enhanced Derivatives Support**: Comprehensive swap classification with intelligent CFI-driven type detection for all major categories
- **MIC Code Integration**: Complete ISO 10383 Market Identification Code system with dual-mode operations
- **CFI-Based Classification**: ISO 10962 compliant CFI code system as single source of truth for instrument types
- **Unified Architecture**: JSON-based models supporting all 10 FIRDS instrument types (C,D,E,F,H,I,J,O,R,S)
- **Performance Optimized**: CFI-driven file filtering reduces I/O operations by 90%
- **Dual Database Support**: SQLite (development) / Azure SQL (production) with unified transparency calculations
- **Complete Data Integration**: FIRDS/FITRS integration with intelligent type detection
- **RESTful API**: Modular Swagger UI with comprehensive endpoint documentation
- **Professional CLI**: Modern command-line interface with Rich formatting and type-specific displays
- **Smart File Management**: Precise regex-based pattern matching for FIRDS/FITRS files
- **Complete API Documentation**: Available at `/api/v1/swagger` (interactive) and `docs/api/`

## Recent Major Improvements

### CLI Delete Command & Enrichment Fixes (October 2025)
- **New Delete Command**: Complete instrument deletion with `--cascade` and `--force` options
- **LEI Enrichment Fix**: Resolved postal_code constraint errors for real-world addresses (Hong Kong, etc.)
- **Structured Products**: Full H-category analysis with 500k+ products and real CFI pattern support
- **Database Migration**: SQLite-compatible table recreation for schema changes

### Comprehensive Swap CLI Enhancement (October 2025)
- **Complete Swap Classification System**: Intelligent CFI-driven detection for all 5 major swap types
- **Professional Display**: Enhanced CLI with type-specific icons (💳📊📈💱🏦) and comprehensive FIRDS data integration
- **Smart Attribute Extraction**: Reference rates, floating terms, currency pairs, basket ISINs, settlement types
- **Real-World Validation**: Tested with Credit Default and Interest Rate swaps from live data

### Modular CLI Architecture (October 2025)
- **Complete Modular Refactoring**: Transformed monolithic CLI into maintainable modular structure
- **9 Focused Command Modules**: Separated instruments, transparency, MIC, FIGI, entities, files into individual modules
- **39% Code Reduction**: From 2000+ line monolith to focused modules (100-300 lines each)
- **Standalone Package Ready**: Clean architecture enables independent CLI distribution
- **Zero Breaking Changes**: All existing commands, imports, and deployment scripts work identically

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

## Installation

```bash
# Clone the repository
git clone [repository-url]
cd MarketDataAPI

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Unix
.\venv\Scripts\activate  # Windows

# Install all dependencies (includes CLI: click>=8.0.0, rich>=13.0.0)
pip install -r requirements.txt

# Install CLI package for global command access (optional)
pip install -e .

# Initialize database
python -m marketdata_api.database.base
```

### CLI Installation Verification

After installation, test the CLI:

```bash
# Windows: Use batch wrapper (recommended)
deployment\mapi.bat --help
deployment\mapi.bat stats

# Direct Python module execution (cross-platform)
python -m marketdata_api.cli --help
python -m marketdata_api.cli stats

# Package installation (if entry points work)
marketdata --help  # or mapi --help
```

## Configuration

Create a `.env` file in the project root:

```env
FLASK_ENV=development
OPENFIGI_API_KEY=your_openfigi_key
DATABASE_URL=sqlite:///marketdata.db
```

## Usage

### Starting the Server

```bash
python -m marketdata_api
```

### Command Line Interface

Modern modular CLI built with Click framework and Rich formatting for professional terminal output.

**New Modular Architecture**: The CLI has been refactored from a monolithic structure into focused command modules for better maintainability and future standalone packaging capability.

#### Setup

```bash
# Package installation (enables global commands)
pip install -e .

# Windows batch wrapper (recommended)
deployment\mapi.bat [command]

# Direct module execution
python -m marketdata_api.cli [command]

# Verify installation
deployment\mapi.bat --help
deployment\mapi.bat stats
```

#### Available Command Groups
- **Core Utilities**: `stats`, `cfi`, `init` - Database operations and analysis
- **Instruments**: Complete instrument lifecycle management with CFI validation
- **Transparency**: MiFID II transparency calculations and FITRS data
- **MIC**: Market Identification Code operations with ISO registry integration
- **FIGI**: Financial Instrument Global Identifier management
- **Entities**: Legal entity operations and LEI handling
- **Files**: File management operations and ESMA integration

#### Core Commands

**Database & Statistics**
```bash
deployment\mapi.bat stats
```

**Instrument Management**
```bash
# List instruments with filtering
mapi.bat instruments list --limit 10 --type equity --currency USD

# Get detailed information
mapi.bat instruments get SE0000120784

# Create from FIRDS data
mapi.bat instruments create US0378331005 equity

# Show trading venues
mapi.bat instruments venues SE0000120784

# Delete instruments with cascade options
mapi.bat instruments delete EZ0F1SLFNWJ8 --force
mapi.bat instruments delete US0378331005 --cascade  # Delete with related data

# Enrich existing instruments with external data
mapi.bat instruments enrich SE0000120784

# Comprehensive derivative support with intelligent type detection
mapi.bat instruments get EZ0XX8PK3511  # Credit Default Swap with full classification
mapi.bat instruments get EZ8SPFL0BM66  # Interest Rate Swap with reference rate details
mapi.bat instruments create [ISIN] swap  # Create swap with automatic CFI classification
```

**CFI Analysis**
```bash
# Enhanced CFI decoding with classification levels
deployment\mapi.bat cfi ESVUFR  # Equity example
deployment\mapi.bat cfi DBFUFR  # Debt example
```

**Market Identification Codes**
```bash
# List MICs with country filtering
deployment\mapi.bat mic list --country US --limit 10

# Get detailed MIC information
deployment\mapi.bat mic get XNYS

# Real-time ISO registry lookup
deployment\mapi.bat mic remote lookup XLON
```

**Transparency Calculations**
```bash
# List transparency calculations with pagination
deployment\mapi.bat transparency list --limit 5 --offset 0

# Get detailed transparency calculation
deployment\mapi.bat transparency get [transparency_id]

# Create transparency calculations from FITRS data
deployment\mapi.bat transparency create SE0000108656
```

**Legal Entities & FIGI Operations**
```bash
# Legal entity lookup
deployment\mapi.bat entities list --country US --limit 10
deployment\mapi.bat entities get [LEI_CODE]

# FIGI operations
deployment\mapi.bat figi get US0378331005
deployment\mapi.bat figi search US0378331005 --mic XNYS
```

**File Management**
```bash
# List processed files
deployment\mapi.bat files list --type FIRDS --limit 20

# Download files from ESMA
deployment\mapi.bat files download [filename]

# File statistics
deployment\mapi.bat files stats
```

#### Rich Terminal Output
The CLI features beautiful formatting with:
- **Rich Tables**: Organized data display with colors and borders
- **Information Panels**: Comprehensive details in bordered sections
- **Status Indicators**: Loading spinners and progress feedback
- **Color Coding**: Cyan headers, green success, red errors
- **Classification Tables**: Clear Yes/No indicators with checkmarks

#### Example Output
```
╭─────────────── Database Statistics ────────────────╮
│ Instruments: 17                                     │
│ Transparency Calculations: 36                       │ 
│ MIC Codes: 2,794                                    │
╰─────────────────────────────────────────────────────╯
```

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

#### File Management
- `POST /api/v1/files/download-by-criteria` - **Main endpoint** for downloading by date/type/dataset
- `GET /api/v1/files` - List files with advanced filtering
- `GET /api/v1/esma-files` - Browse ESMA registry
- `GET /api/v1/files/stats` - Storage statistics and monitoring
- `POST /api/v1/files/cleanup` - Automated file cleanup

#### Batch Operations
- `POST /api/v1/batch/instruments` - Bulk instrument processing
- `POST /api/v1/batch/entities` - Bulk entity processing

**📖 Complete API Documentation**: 
- **Interactive Swagger UI**: http://127.0.0.1:5000/api/v1/swagger
- **ReDoc Documentation**: http://127.0.0.1:5000/api/v1/docs
- **Base URL**: `http://127.0.0.1:5000/api/v1`

## Documentation Policy

**⚠️ Documentation Guidelines**: Keep documentation consolidated. Update existing files rather than creating new ones. The project should have ~10 essential .md files maximum, not 68+.

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

### Quick Test Commands
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

### Development Setup
```bash
# Set PYTHONPATH for development
set "PYTHONPATH=%PROJECT_ROOT%\src;%PYTHONPATH%"

# Set database path for CLI
set "SQLITE_DB_PATH=%PROJECT_ROOT%\src\marketdata_api\database\marketdata.db"

# Use development wrapper
deployment\dev.bat [command]
```

## Project Structure

```
MarketDataAPI/
├── marketdata_api/
│   ├── models/           # SQLAlchemy models
│   │   ├── sqlite/       # Unified SQLite models
│   │   │   ├── instrument.py # Clean instrument models (supports all 10 FIRDS types)
│   │   │   ├── market_identification_code.py # Complete ISO 10383 MIC model
│   │   │   ├── transparency.py # Unified transparency models (JSON-based)
│   │   │   ├── legal_entity.py # Legal Entity models
│   │   │   └── figi.py   # FIGI mapping models
│   │   └── utils/        # Model utilities
│   │       ├── cfi.py    # Complete ISO 10962 CFI decoder
│   │       └── cfi_instrument_manager.py # CFI-based validation & classification system
│   ├── services/         # Business logic & external APIs
│   │   ├── sqlite/       # SQLite service implementations
│   │   │   ├── instrument_service.py # CFI-aware instrument operations (all 10 types)
│   │   │   └── transparency_service.py # Unified transparency with CFI-optimized FITRS search
│   │   ├── mic_data_loader.py # MIC data loading with remote/local support
│   │   ├── file_management_service.py # Advanced file management
│   │   ├── esma_data_loader.py # ESMA data loading and processing
│   │   └── esma_utils.py # ESMA utility functions
│   ├── routes/          # API endpoints
│   │   ├── instrument_routes.py # CFI-enhanced instrument endpoints
│   │   ├── mic_routes.py # Complete MIC API endpoints (8 total)
│   │   ├── entity_routes.py # Legal entity endpoints
│   │   ├── transparency_routes.py # Unified transparency endpoints
│   │   ├── file_management.py # File management endpoints
│   │   └── swagger.py   # API documentation with CFI models
│   ├── database/        # Database configuration
│   ├── config/          # Configuration management
│   └── tests/           # Test suite
├── data/
│   ├── downloads/       # Downloaded ESMA files
│   │   ├── firds/      # FIRDS files (all 10 types: C,D,E,F,H,I,J,O,R,S)
│   │   └── fitrs/      # FITRS files (ECR/NCR pattern support)
│   └── uploads/        # Uploaded files
├── frontend-modern/     # Modern frontend with CFI validation
│   ├── src/
│   │   ├── admin.ts    # CFI-enabled admin interface
│   │   └── utils/api.ts # CFI validation API calls
│   ├── admin.html      # Dynamic instrument type loading
│   └── package.json    # Modern build tooling
├── setup.py            # Package installation with CLI entry points
├── scripts/            # Utility scripts
│   ├── generate_docs.py # OpenAPI documentation generator
│   └── test_firds_fitrs_patterns.py # CFI pattern validation tests
├── docs/               # Documentation
│   ├── api/            # API documentation (auto-generated)
│   ├── CHANGELOG.md    # Detailed project history
│   └── development/    # Development guides
└── alembic/            # Database migrations
```

## Technologies

- **Backend**: Python 3.8+, Flask, SQLAlchemy 2.0+
- **CFI System**: ISO 10962 compliant classification with comprehensive validation
- **Data Sources**: FIRDS (all 10 types), FITRS, OpenFIGI API, GLEIF API
- **Database**: SQLite (with PostgreSQL/Azure SQL support)
- **Frontend**: Modern TypeScript/JavaScript with real-time validation
- **Documentation**: OpenAPI 3.0 with auto-generated Swagger UI
- **Testing**: Pytest with comprehensive CFI pattern validation
- **Migrations**: Alembic for database versioning

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
- **S** - Swaps (Credit Default 💳, Interest Rate 📊, Equity Total Return 📈, Foreign Exchange 💱, OIS 🏦)
- **K** - Commodity derivatives
- **L** - Structured products
- **M** - Financing instruments
- **N** - Referential instruments
- **T** - Other assets

### Business Type Mapping
CFI codes automatically map to business instrument types:
- C → `collective_investment`, D → `debt`, E → `equity`, F → `future`, J → `forward`, O → `option`, R → `rights`, S → `swap`

## Performance Metrics

- File Search Optimization: 90% reduction in I/O operations via CFI-based targeting
- API Response Time: <5 seconds for complex instruments (previously 70+ seconds)
- Validation Accuracy: 100% CFI compliance with real-time frontend feedback
- Coverage: All 10 FIRDS instrument types supported (up from 3)
- Success Rate: 100% instrument processing (eliminated timeouts)

## Requirements

- Python 3.8 or higher
- SQLite 3
- Git
- Virtual environment (recommended)

See `requirements.txt` for complete Python package dependencies.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
