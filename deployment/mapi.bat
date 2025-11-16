@echo off
REM MarketData API CLI Wrapper
REM This script provides a convenient way to run the MarketData API CLI
REM Uses the installed package's console script entry point

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
REM Go up one level to project root (deployment -> project root)
set "PROJECT_ROOT=%SCRIPT_DIR%.."

REM Change to project directory
pushd "%PROJECT_ROOT%"

REM Set PYTHONPATH to include src directory for development
set "PYTHONPATH=%PROJECT_ROOT%\src;%PYTHONPATH%"

REM Set database path to ensure CLI works from any directory
set "SQLITE_DB_PATH=%PROJECT_ROOT%\src\marketdata_api\database\marketdata-sqlite-dev.db"

REM Run the CLI using the module entry point
python -m marketdata_api.cli %*

REM Restore original directory
popd
