# MarketDataAPI Project Structure 📁

This project follows modern Python packaging best practices with a clean, organized directory structure.

**📋 Documentation Rule**: Before creating new .md files, update existing ones. Target: <10 total .md files.

## Directory Overview

```
MarketDataAPI/
├── 📁 src/                          # Source code
│   └── marketdata_api/              # Main package
│       ├── api/                     # Unified Flask-RESTX API (formerly swagger/)
│       │   ├── resources/           # API endpoint implementations
│       │   ├── utils/               # Shared API utilities including:
│       │   │   ├── type_specific_responses.py  # 🎯 Type-specific attribute extractors (10 CFI types)
│       │   │   ├── instrument_utils.py         # Instrument processing utilities
│       │   │   ├── mic_utils.py               # MIC code operations
│       │   │   └── response_builders.py       # Response formatting utilities
│       │   ├── models/              # API response models
│       │   └── config.py            # API configuration
│       ├── models/                  # Database models
│       ├── services/                # Business logic layer  
│       └── database/                # Database configuration
├── 📁 config/                       # Configuration files
│   ├── alembic.ini                  # Database migrations config
│   ├── pytest.ini                  # Testing configuration  
│   └── .env.example                 # Environment variables template
├── 📁 deployment/                   # Deployment files
│   ├── Dockerfile                   # Docker container definition
│   ├── docker-compose.yml          # Multi-container setup
│   ├── install.bat/.sh              # Installation scripts
│   └── upgrade.bat                  # Package upgrade script
├── 📁 data/                         # Data storage (gitignored)
│   ├── downloads/                   # ESMA data downloads
│   ├── database_backups/            # Database backup files
│   └── logs/                        # Application logs
├── 📁 build/                        # Build artifacts (gitignored)
│   └── dist/                        # Distribution packages (.whl, .tar.gz)
├── 📁 docs/                         # Documentation
├── 📁 tests/                        # Test files  
├── 📁 scripts/                      # Utility scripts
├── 📁 frontend/                     # Web frontend files
├── 📁 alembic/                      # Database migration files
└── Core files (README.md, LICENSE, etc.)
```

## Key Benefits of This Structure

✅ **Clean Root Directory**: Essential files only at project root  
✅ **Standard Python Layout**: Follows PEP 518 and modern packaging standards  
✅ **Clear Separation**: Code, config, deployment, and data are separated  
✅ **Build Isolation**: All build artifacts contained in `build/` directory  
✅ **Easy Deployment**: All deployment files organized in `deployment/`  
✅ **Data Management**: Centralized data storage in `data/`
✅ **Unified API**: Single Flask-RESTX implementation with shared utilities (eliminated duplicate `routes/` system)  

## Development Workflow

### Building the Package
```bash
python -m build
# Creates wheel and source distribution in build/dist/
```

### Upgrading Package Version
```bash
# 1. Update version in setup.py and pyproject.toml
# 2. Run upgrade script:
deployment\upgrade.bat 1.0.1
```

### 🚀 Release Workflow (Order of Operations)
```bash
# Step 1: Version upgrade on dev branch
deployment\upgrade.bat 1.0.4
# (Script will pause - manually update setup.py and pyproject.toml versions)

# Step 2: Commit version changes
git add setup.py pyproject.toml build/dist/
git commit -m "Release version 1.0.2"

# Step 3: Create tag
git tag v1.0.2

# Step 4: Push dev with tags
git push origin dev --tags

# Step 5: Merge to main
git checkout main
git pull origin main          # Ensure main is up to date  
git merge dev                 # Merge dev into main

# Step 6: Push main with all tags
git push origin main --tags

# Step 7: Return to dev for continued development
git checkout dev
```

**Key Points:**
- ✅ Always upgrade version on `dev` branch first
- ✅ `upgrade.bat` is semi-manual - you handle git operations
- ✅ Main branch becomes the "release" branch
- ✅ Tags move with the merge from dev to main

## API Architecture

### Unified Flask-RESTX Implementation
The project uses a **single, consolidated API system** in `src/marketdata_api/api/`:

```
api/
├── config.py                   # Flask-RESTX app configuration
├── models/                     # Swagger model definitions (organized by domain)
├── resources/                  # API endpoint implementations
│   ├── instruments.py          # Instrument operations
│   ├── entities.py             # Legal entity operations  
│   ├── transparency.py         # MiFID II transparency calculations
│   ├── mic.py                  # MIC code operations
│   └── files.py                # File management
└── utils/                      # Rich response utilities
    ├── instrument_utils.py     # Rich instrument data processing with CLI-quality formatting
    ├── mic_utils.py            # MIC operations with status indicators
    ├── response_builders.py    # Enterprise-grade response formatting
    ├── transparency_utils.py   # Rich transparency calculations with comprehensive analysis
    └── generate_docs.py        # OpenAPI/Postman documentation generation
```

**Key Benefits:**
- **No Code Duplication**: Eliminated previous dual `routes/` + `swagger/` systems
- **Rich Response Architecture**: CLI-quality API responses with status indicators and formatted metrics
- **Shared Utilities**: Common operations extracted to reusable utility functions  
- **Domain Organization**: Resources grouped by business functionality
- **CFI-Driven**: All instrument operations use CFI codes as primary classification
- **Enterprise-Grade Data**: Comprehensive analysis, contextual information, and professional formatting

### Running from Source (Development)
```bash
# Install in development mode
pip install -e .

# Run CLI with wrapper script (recommended - sets environment)
deployment\mapi.bat --help
deployment\mapi.bat instruments --help

# Or run CLI directly  
python -m marketdata_api.cli --help
```

### CLI Command Structure
```
mapi.bat [command-group] [command] [options]

Command Groups:
├── instruments    # Create, list, get, delete, enrich instruments
├── transparency   # MiFID II transparency calculations
├── mic           # Market Identification Code operations
├── figi          # Financial Instrument Global Identifier
├── entities      # Legal entity operations
└── files         # File management operations

New Features:
├── instruments delete [ISIN] [--cascade] [--force]  # Delete with related data
├── instruments enrich [ISIN]                        # External data enrichment
└── Enhanced structured products support (H-category CFI codes)
```

### Running Tests
```bash
pytest -c config/pytest.ini
```

### Docker Deployment
```bash
cd deployment/
docker-compose up
```

## 🎯 Type-Specific Attributes System

### Core Architecture
The `api/utils/type_specific_responses.py` module implements a comprehensive system for extracting and enriching instrument data based on CFI classification:

#### **10 CFI Type Extractors**
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

#### **Intelligence Features**
- **254 FIRDS Fields Analyzed**: Comprehensive categorization into dates, rates, contract specs, underlying assets
- **Business Logic**: Automatic sub-type detection and intelligent naming
- **Time Calculations**: Days-to-expiry, time-to-maturity, term classifications
- **Risk Analysis**: Protection levels, barrier detection, enhanced rights assessment

#### **API Integration**
- **Rich Responses**: `/api/v1/instruments/{isin}` returns detailed `{instrument_type}_attributes`
- **Raw Data Access**: `/api/v1/instruments/{isin}/raw` for development comparison
- **Consistent Structure**: Standardized field normalization across all types
- **Performance Optimized**: Single-pass FIRDS processing with lazy evaluation

## Environment Configuration

Copy `config/.env.example` to `.env` and configure:
- Database paths
- API keys  
- Download directories
- Logging settings

## Installation

**From Source:**
```bash
pip install .
```

**From Built Package:**
```bash
pip install build/dist/marketdata_api-1.0.0-py3-none-any.whl
```

**Docker:**
```bash
docker-compose -f deployment/docker-compose.yml up
```

This structure ensures maintainability, scalability, and follows Python packaging best practices! 🚀
