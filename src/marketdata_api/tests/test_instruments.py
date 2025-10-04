"""
Tests for instrument service functionality.

CRITICAL: These tests use the real database with live data.
NEVER use drop_all() or any destructive database operations.
Database backups are available in data/database_backups/ if needed.
"""

from datetime import date

import pytest

from marketdata_api.database.base import Base, engine
from marketdata_api.database.session import get_session
from marketdata_api.models import *  # This imports all models
from marketdata_api.services.sqlite.instrument_service import SqliteInstrumentService


@pytest.fixture(scope="module") 
def setup_database():
    # CRITICAL: DO NOT DROP TABLES - use existing database with real data
    # Database backups available in data/database_backups/ for restoration
    yield


@pytest.fixture
def test_service():
    return SqliteInstrumentService()


@pytest.mark.skip(reason="Test requires FIRDS data not available in test environment")
@pytest.mark.integration
def test_create_equity(setup_database, test_service):
    # Use a real ISIN that exists in the database
    data = {
        "FinInstrmGnlAttrbts_Id": "SE0000120784",  # SEB - exists in database
        "FinInstrmGnlAttrbts_FullNm": "Skandinaviska Enskilda Banken AB",
        "FinInstrmGnlAttrbts_ShrtNm": "SEB/SH C",
        "Issr": "213800WAVVOPS85N2205",
    }

    instrument = test_service.create_instrument(data, "equity")

    assert instrument.isin == "SE0000120784"
    assert instrument.type == "equity"


@pytest.mark.skip(reason="Test requires FIRDS data not available in test environment")
@pytest.mark.integration
def test_create_debt(setup_database, test_service):
    # Use a real debt ISIN that exists in the database
    data = {
        "FinInstrmGnlAttrbts_Id": "XS2908107019",  # ING Bank bond - exists in database
        "FinInstrmGnlAttrbts_FullNm": "ING Bank N.V. EO-M.-T. Mortg.Cov.Bds 24(29)",
        "DebtInstrmAttrbts_MtrtyDt": "2029-06-01",
        "DebtInstrmAttrbts_IntrstRate_Fxd": "3.75",
    }

    instrument = test_service.create_instrument(data, "debt")
    assert instrument.isin == "XS2908107019"
    assert instrument.type == "debt"
    assert instrument.fixed_interest_rate == 3.75


@pytest.mark.skip(reason="Test requires FIRDS data not available in test environment")
@pytest.mark.integration
def test_create_debt_invalid_date(setup_database, test_service):
    """Test handling of invalid date format"""
    # Use real ISIN but with invalid date to test error handling
    data = {
        "FinInstrmGnlAttrbts_Id": "XS2908107019",  # Real ISIN
        "DebtInstrmAttrbts_MtrtyDt": "invalid-date",
        "DebtInstrmAttrbts_IntrstRate_Fxd": "3.75",
    }

    instrument = test_service.create_instrument(data, "debt")
    assert instrument.maturity_date is None  # Should skip invalid date conversion


@pytest.mark.integration
def test_create_instrument_with_relationships(setup_database, test_service):
    """Test creation of instrument with FIGI and Legal Entity relationships"""
    # Add relationship testing


@pytest.mark.integration
def test_get_instrument(setup_database, test_service):
    service = test_service
    # Use real ISIN from database
    result = service.get_instrument("SE0000120784")  # SEB
    if isinstance(result, tuple):
        session, instrument = result
        assert instrument is not None
        assert instrument.isin == "SE0000120784"
    else:
        assert result is not None
        assert result.isin == "SE0000120784"


@pytest.mark.skip(reason="Test requires FIRDS data not available in test environment")
@pytest.mark.integration
def test_update_instrument(setup_database, test_service):
    # Create initial instrument using real ISIN
    data = {
        "FinInstrmGnlAttrbts_Id": "SE0000120784",  # Real SEB ISIN
        "FinInstrmGnlAttrbts_ShrtNm": "SEB/SH C",
    }
    instrument = test_service.create_instrument(data, "equity")

    # Update the instrument
    updated_data = {"FinInstrmGnlAttrbts_ShrtNm": "ERIC B NEW"}
    updated = test_service.update_instrument("SE0000108656", updated_data)
    assert updated.short_name == "ERIC B NEW"
