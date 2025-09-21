# MarketDataAPI - Deployment Guide

This guide covers how to deploy MarketDataAPI on another PC or server.

## 🚀 Quick Start Installation

### Option 1: Local Installation (Recommended for Development)

#### Windows
1. **Download/Clone** the project to your target PC
2. **Run the installer**:
   ```cmd
   install.bat
   ```
3. **Activate environment and test**:
   ```cmd
   .venv\Scripts\activate.bat
   mapi --help
   ```

#### Linux/macOS
1. **Download/Clone** the project to your target system
2. **Make installer executable and run**:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
3. **Activate environment and test**:
   ```bash
   source venv/bin/activate
   mapi --help
   ```

### Option 2: Docker Installation (Recommended for Production)

#### Prerequisites
- Docker and Docker Compose installed on target system

#### Quick Deploy
```bash
# Clone/download project
git clone <repository-url>
cd MarketDataAPI

# Start with Docker Compose
docker-compose up -d

# The API will be available at http://localhost:5000
```

#### Custom Configuration
```bash
# Build custom image
docker build -t marketdata-api .

# Run with custom settings
docker run -d \
  -p 5000:5000 \
  -v ./data:/app/data \
  -v ./downloads:/app/downloads \
  -e DATABASE_URL=sqlite:///data/marketdata.db \
  marketdata-api
```

### Option 3: Package Installation (PyPI - Future)

*Coming soon: PyPI package distribution*

```bash
pip install marketdata-api
marketdata --help
```

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space (for data files)
- **OS**: Windows 10+, Linux (Ubuntu 18.04+), macOS 10.15+

### Optional Requirements
- **SQL Server**: For production database (Azure SQL supported)
- **Docker**: For containerized deployment
- **Git**: For source code management

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=sqlite:///data/marketdata.db
# DATABASE_URL=mssql+pyodbc://user:pass@server/database?driver=ODBC+Driver+17+for+SQL+Server

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=false
SECRET_KEY=your-secret-key-here

# File Management
FIRDS_PATH=./downloads/firds
FITRS_PATH=./downloads/fitrs
RETENTION_DAYS=30

# API Keys (if needed)
# BLOOMBERG_API_KEY=your-key-here
```

### Database Setup

#### SQLite (Default)
No additional setup required. Database will be created automatically.

#### SQL Server / Azure SQL
1. Update `DATABASE_URL` in `.env`
2. Install SQL Server dependencies:
   ```bash
   pip install pyodbc
   ```
3. Run migrations:
   ```bash
   alembic upgrade head
   ```

## 🗃️ Data Migration

### From Existing Installation
1. **Backup current data**:
   ```bash
   mapi files stats  # Check current data
   cp data/marketdata.db data/marketdata_backup.db
   ```

2. **Export/Import** (if needed):
   ```bash
   # Export instruments
   mapi instruments list --format json > instruments_export.json
   
   # Import on new system
   # (Custom import functionality can be added)
   ```

### Fresh Installation
1. **Download ESMA files**:
   ```bash
   mapi files download firds --dataset FULINS_E
   mapi files download fitrs
   ```

2. **Load MIC codes**:
   ```bash
   mapi mic load  # Downloads latest ISO 10383 MIC data
   ```

## 🌐 Web API Deployment

### Development Server
```bash
# Start Flask development server
flask run --host=0.0.0.0 --port=5000

# Or using the CLI
mapi api start --port 5000
```

### Production Deployment

#### Using Gunicorn (Linux/macOS)
```bash
# Install Gunicorn
pip install gunicorn

# Start production server
gunicorn -w 4 -b 0.0.0.0:5000 "marketdata_api:create_app()"
```

#### Using Waitress (Windows)
```bash
# Install Waitress
pip install waitress

# Start production server
waitress-serve --host=0.0.0.0 --port=5000 marketdata_api:create_app
```

#### Using Docker (Recommended)
```bash
# Production ready with health checks
docker-compose -f docker-compose.yml up -d
```

## 🔍 Verification & Testing

### CLI Verification
```bash
# Check installation
mapi --help
mapi stats

# Test file operations
mapi files list
mapi files available firds --days 5

# Test data operations
mapi instruments list --limit 5
mapi transparency list --limit 5
```

### API Verification
```bash
# Check API health
curl http://localhost:5000/health

# Test API endpoints
curl http://localhost:5000/api/instruments?limit=5
curl http://localhost:5000/api/mic/codes?limit=5
```

### Web Interface
Open browser and navigate to:
- **API Documentation**: http://localhost:5000/
- **Health Check**: http://localhost:5000/health

## 📊 Monitoring & Logs

### Log Files
- **Application logs**: `logs/debug.log`
- **Error logs**: `logs/error.log`
- **Access logs**: `logs/access.log`

### Health Monitoring
```bash
# Check system status
mapi stats

# Check file storage
mapi files stats

# Monitor API health
curl http://localhost:5000/health
```

## 🛠️ Troubleshooting

### Common Issues

#### Import Errors
```bash
# Reinstall package
pip install -e . --force-reinstall
```

#### Database Issues
```bash
# Reset database
rm data/marketdata.db
alembic upgrade head
```

#### Permission Issues (Linux/macOS)
```bash
# Fix permissions
chmod +x install.sh
chmod +x mapi.bat
sudo chown -R $USER:$USER ./data ./logs ./downloads
```

#### Windows PATH Issues
```cmd
# Add Python to PATH
set PATH=%PATH%;C:\Python3X\Scripts
```

### Getting Help

1. **Check logs**: `logs/debug.log`
2. **Verify installation**: `mapi stats`
3. **Check configuration**: Review `.env` file
4. **Database status**: `mapi files stats`

## 🔄 Updates & Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Reinstall package
pip install -e . --force-reinstall

# Run migrations
alembic upgrade head
```

### Regular Maintenance
```bash
# Clean old files
mapi files cleanup --older-than 30

# Update MIC codes
mapi mic update

# Backup database
cp data/marketdata.db data/backup_$(date +%Y%m%d).db
```

---

## 📞 Support

For deployment issues:
1. Check this guide first
2. Review logs in `logs/` directory  
3. Verify system requirements
4. Check GitHub issues for known problems

**Ready to deploy!** 🚀
