@echo off
REM MarketDataAPI Professional CLI - Windows Batch Script  
REM Usage: mapi instruments list

cd /d "%~dp0"
C:/Users/robin/Projects/MarketDataAPI/.venv/Scripts/python.exe marketdata_cli.py %*
