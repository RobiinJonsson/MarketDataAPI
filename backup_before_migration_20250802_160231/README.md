# Market Data API

A comprehensive market data management system that integrates FIRDS, OpenFIGI, and GLEIF data sources.

## Features

- **🔧 Database**: SQLite (development) / Azure SQL (production)
- **📊 Data Sources**: FIRDS, OpenFIGI, GLEIF integration with automated enrichment
- **🎯 Instruments**: ISIN-based lookup, equity/debt/futures support, CFI decoding
- **📁 File Management**: Advanced ESMA data operations, automated downloads, intelligent organization
- **🌐 RESTful API**: Comprehensive endpoints for instruments, entities, files, and batch operations
- **🖥️ Web Interface**: Interactive data exploration with real-time updates and filtering
  - Raw JSON data display for debugging

## Installation

```bash
# Clone the repository
git clone [repository-url]
cd MarketDataAPI

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Unix
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -m marketdata_api.database.base
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

```bash
# List all instruments
python scripts/cli.py instrument list

# Get instrument details
python scripts/cli.py instrument detail <ISIN>

# Batch process instruments
python scripts/cli.py batch create isins.txt equity

# Decode a CFI code
python scripts/cli.py cfi ESVUFR

# Batch source from FIRDS
python scripts/cli.py batch batch-source equity SE
```

### API Endpoints

#### Core Operations
- `GET/POST /api/v1/instruments` - Instrument management and enrichment
- `GET/POST /api/v1/entities` - Legal entity operations  
- `GET /api/v1/transparency` - MiFID II transparency calculations
- `GET /api/v1/cfi/{cfi_code}` - CFI code decoding

#### File Management
- `POST /api/v1/files/download-by-criteria` - **Main endpoint** for downloading by date/type/dataset
- `GET /api/v1/files` - List files with advanced filtering
- `GET /api/v1/esma-files` - Browse ESMA registry
- `GET /api/v1/files/stats` - Storage statistics and monitoring
- `POST /api/v1/files/cleanup` - Automated file cleanup

#### Batch Operations
- `POST /api/v1/batch/instruments` - Bulk instrument processing
- `POST /api/v1/batch/entities` - Bulk entity processing

**📖 Complete API Documentation**: Available at `/api/v1/swagger` (interactive) and `docs/api/`

## Project Structure

```
MarketDataAPI/
├── marketdata_api/
│   ├── models/           # SQLAlchemy models
│   │   ├── instrument.py # Instrument models with polymorphic inheritance
│   │   ├── legal_entity.py # Legal Entity models
│   │   ├── figi.py       # FIGI mapping models
│   │   └── utils/        # Utilities for models
│   ├── services/         # Business logic & external APIs
│   │   ├── file_management_service.py # Advanced file management
│   │   ├── esma_data_loader.py # ESMA data loading and processing
│   │   ├── esma_utils.py # ESMA utility functions
│   │   ├── instrument_service.py # Instrument operations
│   │   └── transparency_service.py # Transparency calculations
│   ├── routes/          # API endpoints
│   │   ├── file_management.py # File management endpoints
│   │   ├── instrument_routes.py # Instrument endpoints
│   │   ├── entity_routes.py # Legal entity endpoints
│   │   └── transparency_routes.py # Transparency endpoints
│   ├── database/        # Database configuration
│   ├── config/          # Configuration management
│   └── tests/           # Test suite
├── downloads/           # Downloaded ESMA files
│   ├── firds/          # FIRDS files (organized by type)
│   └── fitrs/          # FITRS files (organized by type)
├── frontend/
│   ├── static/          # JavaScript & CSS
│   │   ├── admin_files.js # File management interface
│   │   └── config.js    # Frontend configuration
│   └── templates/       # HTML templates
├── scripts/             # CLI tools and example scripts
│   ├── cli.py          # Command line interface
│   ├── esma_example.py # FIRDS data usage example
│   └── esma_fitrs_example.py # FITRS data usage example
├── docs/               # Documentation
│   ├── api/            # API documentation
│   │   ├── file_management_endpoints.md # File management API docs
│   │   ├── instruments.md # Instrument API docs
│   │   └── transparency.md # Transparency API docs
│   └── development/    # Development documentation
└── alembic/            # Database migrations
```

## Technologies

- Python 3.8+
- Flask
- SQLAlchemy 2.0+
- OpenFIGI API
- GLEIF API
- SQLite (with PostgreSQL support planned)
- JavaScript/HTML/CSS
- Alembic for migrations
- Pytest for testing

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
