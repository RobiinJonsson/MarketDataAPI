@echo off
REM MarketDataAPI Installation Script for Windows

echo 🚀 MarketDataAPI Installation Script
echo ====================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Show Python version
echo 📋 Python version:
python --version

REM Create virtual environment
echo 🔧 Creating virtual environment...
python -m venv .venv

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM Install package
echo 🔨 Installing MarketDataAPI...
pip install -e .

REM Create directories
echo 📁 Creating data directories...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "downloads" mkdir downloads

REM Run alembic migrations if needed
if exist "alembic.ini" (
    echo 🗃️  Running database migrations...
    alembic upgrade head
)

echo ✅ Installation complete!
echo.
echo 🎯 Usage:
echo   Activate environment: .venv\Scripts\activate.bat
echo   CLI usage: marketdata --help
echo   Short alias: mapi --help
echo   Batch file: mapi.bat --help
echo.
echo 🌐 To start the web API:
echo   flask run --host=0.0.0.0 --port=5000
echo.
echo 📚 Check README.md for detailed usage instructions.
pause
