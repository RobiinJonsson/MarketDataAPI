@echo off
echo.
echo ===============================================
echo MarketDataAPI Package Upgrade Script
echo ===============================================
echo.

REM Check if version parameter is provided
if "%1"=="" (
    echo ERROR: Please provide version number
    echo Usage: upgrade.bat 1.0.1
    exit /b 1
)

set VERSION=%1
echo Upgrading to version %VERSION%...
echo.

REM Update version in setup.py (you'll need to do this manually for now)
echo 1. Please update version in setup.py to "%VERSION%"
echo 2. Please update version in pyproject.toml to "%VERSION%"
pause

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist src\*.egg-info rmdir /s /q src\*.egg-info

REM Build new package
echo Building package...
python -m build

REM Check if build was successful
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Build failed!
    exit /b 1
)

echo.
echo ===============================================
echo Package built successfully!
echo ===============================================
echo.
echo Latest package files:
dir dist\*%VERSION%* /B
echo.
echo To install/upgrade:
echo   pip install --force-reinstall dist\marketdata_api-%VERSION%-py3-none-any.whl
echo.
echo To test in clean environment:
echo   python -m venv test_env_v%VERSION%
echo   test_env_v%VERSION%\Scripts\activate
echo   pip install dist\marketdata_api-%VERSION%-py3-none-any.whl
echo   marketdata --help
echo.
