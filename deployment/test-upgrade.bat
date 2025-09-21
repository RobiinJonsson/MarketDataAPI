@echo off
REM Version Upgrade Test Runner for MarketDataAPI
REM This script runs comprehensive tests before and after version upgrades

set "PROJECT_ROOT=%~dp0.."
cd /d "%PROJECT_ROOT%"

echo.
echo ========================================================================
echo MarketDataAPI Version Upgrade Test Runner
echo ========================================================================
echo.

REM Check if we're in the right directory
if not exist "src\marketdata_api\cli.py" (
    echo ERROR: Not in MarketDataAPI project directory
    echo Please run this script from the deployment folder
    exit /b 1
)

REM Set argument if provided
set "TEST_PHASE=%1"
if "%TEST_PHASE%"=="" set "TEST_PHASE=pre-upgrade"

echo Test Phase: %TEST_PHASE%
echo Current Directory: %cd%
echo Timestamp: %date% %time%
echo.

REM Create test results directory if it doesn't exist
if not exist "test-results" mkdir "test-results"

if "%TEST_PHASE%"=="pre-upgrade" goto PRE_UPGRADE
if "%TEST_PHASE%"=="post-upgrade" goto POST_UPGRADE
if "%TEST_PHASE%"=="full" goto FULL_TEST
if "%TEST_PHASE%"=="quick" goto QUICK_TEST

:USAGE
echo Usage: test-upgrade.bat [pre-upgrade^|post-upgrade^|full^|quick]
echo.
echo   pre-upgrade  - Run tests before version upgrade (default)
echo   post-upgrade - Run tests after version upgrade  
echo   full         - Run complete test suite
echo   quick        - Run quick tests only
echo.
goto END

:PRE_UPGRADE
echo Running PRE-UPGRADE tests...
echo ----------------------------------------

echo [1/4] Checking test collection...
python -m pytest --collect-only -q > test-results\collection-check.log 2>&1
if errorlevel 1 (
    echo ERROR: Test collection failed
    type test-results\collection-check.log
    goto END
)
echo     ✓ Test collection OK

echo [2/4] Running unit tests...
python -m pytest -m unit -v --tb=short > test-results\unit-tests.log 2>&1
if errorlevel 1 (
    echo WARNING: Some unit tests failed - check test-results\unit-tests.log
) else (
    echo     ✓ Unit tests passed
)

echo [3/4] Running CLI tests...
python -m pytest -m cli -v --tb=short > test-results\cli-tests.log 2>&1
if errorlevel 1 (
    echo WARNING: Some CLI tests failed - check test-results\cli-tests.log
) else (
    echo     ✓ CLI tests passed
)

echo [4/4] Testing current CLI functionality...
deployment\mapi.bat stats > test-results\cli-functionality.log 2>&1
if errorlevel 1 (
    echo ERROR: CLI not working - check test-results\cli-functionality.log
    goto END
) else (
    echo     ✓ CLI functionality verified
)

echo.
echo PRE-UPGRADE TESTS COMPLETE
echo Results saved in test-results\ folder
echo.
echo Ready for version upgrade!
goto END

:POST_UPGRADE  
echo Running POST-UPGRADE tests...
echo ----------------------------------------

echo [1/5] Verifying CLI works from different directories...
cd C:\
C:\Users\robin\Projects\MarketDataAPI\deployment\mapi.bat stats > C:\Users\robin\Projects\MarketDataAPI\test-results\cli-portability.log 2>&1
cd /d "%PROJECT_ROOT%"
if errorlevel 1 (
    echo ERROR: CLI doesn't work from different directory
    type test-results\cli-portability.log
    goto END
) else (
    echo     ✓ CLI portable across directories
)

echo [2/5] Running upgrade-specific tests...
python -m pytest -m upgrade -v --tb=short > test-results\upgrade-tests.log 2>&1  
if errorlevel 1 (
    echo WARNING: Some upgrade tests failed - check test-results\upgrade-tests.log
) else (
    echo     ✓ Upgrade tests passed
)

echo [3/5] Verifying data integrity...
deployment\mapi.bat instruments list --limit 3 > test-results\data-integrity.log 2>&1
deployment\mapi.bat mic list --limit 3 >> test-results\data-integrity.log 2>&1
if errorlevel 1 (
    echo ERROR: Data access problems - check test-results\data-integrity.log
    goto END
) else (
    echo     ✓ Data integrity verified
)

echo [4/5] Running integration tests...
python -m pytest -m integration -v --tb=short > test-results\integration-tests.log 2>&1
if errorlevel 1 (
    echo WARNING: Some integration tests failed - check test-results\integration-tests.log  
) else (
    echo     ✓ Integration tests passed
)

echo [5/5] Testing configuration compatibility...
python -m pytest src\marketdata_api\tests\test_version_upgrade.py::TestConfigurationCompatibility -v > test-results\config-compatibility.log 2>&1
if errorlevel 1 (
    echo WARNING: Config compatibility issues - check test-results\config-compatibility.log
) else (
    echo     ✓ Configuration compatibility verified
)

echo.
echo POST-UPGRADE TESTS COMPLETE
echo Results saved in test-results\ folder
echo.
echo Version upgrade verification complete!
goto END

:FULL_TEST
echo Running FULL test suite...
echo ----------------------------------------
python src\marketdata_api\tests\run_tests.py --upgrade-report
goto END

:QUICK_TEST
echo Running QUICK tests...
echo ----------------------------------------
python src\marketdata_api\tests\run_tests.py --quick
goto END

:END
echo.
echo Test runner finished at %date% %time%
echo ========================================================================
