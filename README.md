# Market Data API

A comprehensive market data management system that integrates FIRDS, OpenFIGI, and GLEIF data sources.

## Features

- **Instrument Management**
  - ISIN-based instrument lookup and creation
  - Support for equity and debt instruments
  - Automatic data enrichment from multiple sources
  - Relationship handling between instruments and legal entities

- **Data Integration**
  - FIRDS (Financial Instruments Reference Data System) integration
  - OpenFIGI mapping for global instrument identification
  - GLEIF (Global Legal Entity Identifier) data integration
  - Automatic data enrichment pipeline

- **API Features**
  - RESTful API endpoints
  - Batch processing support
  - Search and filtering capabilities
  - Schema-based data mapping

- **User Interface**
  - Web-based interface for data operations
  - Real-time data display
  - Interactive data exploration
  - Toast notifications for operation feedback

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
```

### API Endpoints

- `GET /api/search/<isin>` - Search for instrument by ISIN
- `POST /api/fetch` - Fetch and create new instrument
- `GET /api/instruments` - List all instruments
- `POST /api/batch_search` - Batch search instruments

## Project Structure

```
MarketDataAPI/
├── marketdata_api/
│   ├── models/           # SQLAlchemy models
│   ├── services/         # Business logic & external APIs
│   ├── routes/          # API endpoints
│   ├── database/        # Database configuration
│   └── config/          # Configuration management
├── frontend/
│   ├── static/          # JavaScript & CSS
│   └── templates/       # HTML templates
├── scripts/             # CLI tools
├── tests/              # Test suite
└── docs/               # Documentation
```

## Technologies

- Python 3.8+
- Flask
- SQLAlchemy
- OpenFIGI API
- GLEIF API
- SQLite
- JavaScript/HTML/CSS

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
