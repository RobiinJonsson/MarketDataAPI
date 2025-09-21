@echo off
REM Development task runner for MarketDataAPI
REM Usage: dev.bat [task] [options]

setlocal enabledelayedexpansion

set "PROJECT_ROOT=%~dp0.."
cd /d "%PROJECT_ROOT%"

set "TASK=%1"
if "%TASK%"=="" goto HELP

if "%TASK%"=="install" goto INSTALL
if "%TASK%"=="test" goto TEST
if "%TASK%"=="test-quick" goto TEST_QUICK
if "%TASK%"=="test-unit" goto TEST_UNIT
if "%TASK%"=="test-integration" goto TEST_INTEGRATION
if "%TASK%"=="test-cli" goto TEST_CLI
if "%TASK%"=="test-upgrade" goto TEST_UPGRADE
if "%TASK%"=="coverage" goto COVERAGE
if "%TASK%"=="lint" goto LINT
if "%TASK%"=="format" goto FORMAT
if "%TASK%"=="build" goto BUILD
if "%TASK%"=="clean" goto CLEAN
if "%TASK%"=="docs" goto DOCS
goto HELP

:HELP
echo MarketDataAPI Development Task Runner
echo.
echo Available tasks:
echo   install      - Install development dependencies
echo   test         - Run full test suite
echo   test-quick   - Run quick tests (unit + CLI)
echo   test-unit    - Run unit tests only
echo   test-integration - Run integration tests
echo   test-cli     - Run CLI tests
echo   test-upgrade - Run upgrade compatibility tests
echo   coverage     - Run tests with coverage report
echo   lint         - Run code quality checks
echo   format       - Format code with black and isort
echo   build        - Build distribution packages
echo   clean        - Clean build artifacts
echo   docs         - Generate documentation
echo.
echo Examples:
echo   dev.bat install
echo   dev.bat test
echo   dev.bat coverage
echo   dev.bat build
goto END

:INSTALL
echo Installing development dependencies...
pip install -e ".[dev,test,docs]"
echo.
echo Development environment ready!
goto END

:TEST
echo Running full test suite...
python -m pytest -v --tb=short
goto END

:TEST_QUICK
echo Running quick tests...
python -m pytest -m "unit or cli" -v --tb=line -x
goto END

:TEST_UPGRADE
echo Running upgrade compatibility tests...
python -m pytest -m upgrade -v --tb=short
goto END

:TEST_UNIT
echo Running unit tests only...
python -m pytest -m unit -v --tb=short
goto END

:TEST_INTEGRATION
echo Running integration tests...
python -m pytest -m integration -v --tb=short
goto END

:TEST_CLI
echo Running CLI tests...
python -m pytest -m cli -v --tb=short
goto END

:COVERAGE
echo Running tests with coverage...
python -m pytest --cov=marketdata_api --cov-report=html --cov-report=term
echo.
echo Coverage report generated in htmlcov/index.html
goto END

:LINT
echo Running code quality checks...
echo [1/3] Checking with flake8...
python -m flake8 src/marketdata_api --count --select=E9,F63,F7,F82 --show-source --statistics 2>nul
if !errorlevel! neq 0 (
    echo Warning: flake8 not installed. Run 'deployment\dev.bat install' first.
)
echo [2/3] Checking with mypy...
python -m mypy src/marketdata_api --ignore-missing-imports 2>nul
if !errorlevel! neq 0 (
    echo Warning: mypy not installed. Run 'deployment\dev.bat install' first.
)
echo [3/3] Checking imports with isort...
python -m isort --check-only --diff src/marketdata_api 2>nul
if !errorlevel! neq 0 (
    echo Warning: isort not installed. Run 'deployment\dev.bat install' first.
)
echo.
echo Code quality checks complete!
goto END

:FORMAT
echo Formatting code...
echo [1/2] Formatting with black...
python -m black src/marketdata_api 2>nul
if !errorlevel! neq 0 (
    echo Warning: black not installed. Run 'deployment\dev.bat install' first.
    goto END
)
echo [2/2] Sorting imports with isort...
python -m isort src/marketdata_api 2>nul
if !errorlevel! neq 0 (
    echo Warning: isort not installed. Run 'deployment\dev.bat install' first.
    goto END
)
echo.
echo Code formatting complete!
goto END

:BUILD
echo Building distribution packages...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
python -m build
echo.
echo Packages built in dist/ folder:
dir /b dist\
goto END

:CLEAN
echo Cleaning build artifacts...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "src\marketdata_api.egg-info" rmdir /s /q "src\marketdata_api.egg-info"
if exist ".coverage" del ".coverage"
if exist "htmlcov" rmdir /s /q "htmlcov"
if exist ".pytest_cache" rmdir /s /q ".pytest_cache"
if exist "test-results" rmdir /s /q "test-results"

REM Clean __pycache__ directories
for /r . %%i in (__pycache__) do (
    if exist "%%i" rmdir /s /q "%%i"
)

REM Clean .pyc files
for /r . %%i in (*.pyc) do (
    if exist "%%i" del "%%i"
)

echo Build artifacts cleaned!
goto END

:DOCS
echo Generating documentation...
python -c "import sphinx" 2>nul
if !errorlevel! neq 0 (
    echo Error: Sphinx not installed. Run 'deployment\dev.bat install' first.
    goto END
)
if not exist "docs\_build" mkdir "docs\_build"
python -m sphinx.cmd.build docs docs\_build\html
echo.
echo Documentation generated in docs\_build\html\index.html
goto END

:END
endlocal
