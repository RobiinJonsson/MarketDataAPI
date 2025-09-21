# MarketDataAPI Project Structure 📁

This project follows modern Python packaging best practices with a clean, organized directory structure.

## Directory Overview

```
MarketDataAPI/
├── 📁 src/                          # Source code
│   └── marketdata_api/              # Main package
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

### Running from Source (Development)
```bash
# Install in development mode
pip install -e .

# Or run CLI directly
python src/marketdata_api/cli.py --help
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
