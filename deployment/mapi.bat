@echo off
REM MarketData API CLI Wrapper
REM This script provides a convenient way to run the MarketData API CLI
REM Uses the installed package's console script entry point

REM Set PYTHONPATH to include src directory for development
set "PYTHONPATH=src;%PYTHONPATH%"

REM Run the CLI using the module entry point
python -m marketdata_api.cli %*
