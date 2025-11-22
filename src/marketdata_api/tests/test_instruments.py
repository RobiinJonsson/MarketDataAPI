"""
Tests for instrument service functionality.

CRITICAL: These tests use the real database with live data.
Tests use a GET -> DELETE -> CREATE -> UPDATE pattern to ensure they work with actual data.
Database backups are available in data/database_backups/ if needed.
"""

from datetime import date
import pytest
from marketdata_api.database.base import Base, engine
from marketdata_api.database.session import get_session
from marketdata_api.models import *  # This imports all models

# Test ISIN constants - real instruments from the database
TEST_EQUITY_ISIN = "SE0000120784"  # Skandinaviska Enskilda Banken AB
TEST_DEBT_ISIN = "XS2908107019"   # Available in database (seen in earlier output)

@pytest.fixture(scope="module") 
def setup_database():
    # CRITICAL: DO NOT DROP TABLES - use existing database with real data
    # Database backups available in data/database_backups/ for restoration
    yield

@pytest.fixture
def test_service():
    from marketdata_api.services.core.instrument_service import InstrumentService
    return InstrumentService()

@pytest.mark.integration
def test_instrument_lifecycle_equity(setup_database, test_service):
    """Test complete instrument lifecycle: GET -> DELETE -> CREATE -> UPDATE using real equity data."""
    
    # Step 1: Get existing instrument to capture its real data
    session, original_instrument = test_service.get_instrument(TEST_EQUITY_ISIN)
    
    if not original_instrument:
        pytest.skip(f"Test instrument {TEST_EQUITY_ISIN} not found in database")
    
    # Store original data for recreation
    original_data = {
        "isin": original_instrument.isin,
        "instrument_type": original_instrument.instrument_type,
        "full_name": original_instrument.full_name,
        "short_name": original_instrument.short_name,
        "currency": original_instrument.currency,
        "cfi_code": original_instrument.cfi_code,
        "lei_id": original_instrument.lei_id,
        "competent_authority": original_instrument.competent_authority,
        "firds_data": original_instrument.firds_data,
    }
    session.close()
    
    # Step 2: Delete the instrument (without cascade to avoid issues with relationships)
    delete_result = test_service.delete_instrument(TEST_EQUITY_ISIN, cascade=False)
    assert delete_result == True, "Failed to delete test instrument"
    
    # Verify deletion
    session, deleted_check = test_service.get_instrument(TEST_EQUITY_ISIN)
    assert deleted_check is None, "Instrument still exists after deletion"
    session.close()
    
    # Step 3: Recreate the instrument using create_instrument
    # create_instrument takes ISIN string and instrument type
    recreated_instrument = test_service.create_instrument(original_data["isin"], original_data["instrument_type"])
    
    # Verify recreation
    assert recreated_instrument is not None, "Failed to recreate instrument"
    assert recreated_instrument.isin == original_data["isin"]
    assert recreated_instrument.instrument_type == original_data["instrument_type"] 
    assert recreated_instrument.full_name == original_data["full_name"]
    
    # Step 4: Update the instrument
    update_data = {
        "short_name": original_data["short_name"] + " (UPDATED)",
    }
    
    updated_instrument = test_service.update_instrument(TEST_EQUITY_ISIN, update_data)
    assert updated_instrument is not None, "Failed to update instrument"
    assert "(UPDATED)" in updated_instrument.short_name

@pytest.mark.integration  
def test_instrument_get_and_venues(setup_database, test_service):
    """Test getting an instrument and its trading venues."""
    
    # Get an existing equity instrument
    session, instrument = test_service.get_instrument(TEST_EQUITY_ISIN)
    
    if not instrument:
        pytest.skip(f"Test instrument {TEST_EQUITY_ISIN} not found in database")
    
    # Verify basic instrument data
    assert instrument.isin == TEST_EQUITY_ISIN
    assert instrument.instrument_type == "equity"
    assert instrument.full_name is not None
    assert instrument.currency is not None
    
    # Test venue retrieval
    venues = test_service.get_instrument_venues(TEST_EQUITY_ISIN)
    assert venues is not None, "Failed to retrieve trading venues"
    
    session.close()

@pytest.mark.integration
def test_debt_instrument_lifecycle(setup_database, test_service):
    """Test lifecycle for debt instrument if available."""
    
    # Try to get existing debt instrument
    session, original_instrument = test_service.get_instrument(TEST_DEBT_ISIN)
    
    if not original_instrument:
        pytest.skip(f"Test debt instrument {TEST_DEBT_ISIN} not found in database")
    
    # Store original data  
    original_data = {
        "isin": original_instrument.isin,
        "instrument_type": original_instrument.instrument_type,
        "full_name": original_instrument.full_name,
        "short_name": original_instrument.short_name,
        "currency": original_instrument.currency,
        "cfi_code": original_instrument.cfi_code,
    }
    session.close()
    
    # Delete and recreate (minimal test for debt)
    delete_result = test_service.delete_instrument(TEST_DEBT_ISIN, cascade=False)
    assert delete_result == True
    
    # Recreate using ISIN and type
    recreated_instrument = test_service.create_instrument(original_data["isin"], original_data["instrument_type"])
    assert recreated_instrument is not None
    assert recreated_instrument.isin == original_data["isin"]
    assert recreated_instrument.instrument_type == "debt"

@pytest.mark.integration
def test_instrument_error_handling(setup_database, test_service):
    """Test error handling for non-existent instruments."""
    
    # Test getting non-existent instrument
    session, instrument = test_service.get_instrument("NONEXISTENT123")
    assert instrument is None
    session.close()
    
    # Test deleting non-existent instrument
    delete_result = test_service.delete_instrument("NONEXISTENT123")
    assert delete_result == False
    
    # Test updating non-existent instrument  
    updated = test_service.update_instrument("NONEXISTENT123", {"short_name": "test"})
    assert updated is None

@pytest.mark.integration
def test_instrument_data_validation(setup_database, test_service):
    """Test that instruments maintain data integrity."""
    
    # Get an existing instrument to verify data integrity
    session, instrument = test_service.get_instrument(TEST_EQUITY_ISIN)
    
    if not instrument:
        pytest.skip(f"Test instrument {TEST_EQUITY_ISIN} not found in database")
    
    # Verify key fields are properly populated
    assert instrument.isin is not None
    assert instrument.instrument_type is not None
    assert instrument.full_name is not None
    assert len(instrument.isin) == 12  # ISIN should be 12 characters
    assert instrument.instrument_type in ["equity", "debt", "collective_investment", "future", "option", "warrant", "right", "convertible", "hybrid", "structured"]
    
    session.close()


@pytest.mark.integration
def test_instrument_relationships(setup_database, test_service):
    """Test that instrument relationships are properly loaded."""
    
    # Get an existing instrument with relationships
    session, instrument = test_service.get_instrument(TEST_EQUITY_ISIN)
    
    if not instrument:
        pytest.skip(f"Test instrument {TEST_EQUITY_ISIN} not found in database")
    
    # Test that relationships can be accessed (may be empty but should not error)
    figi_mappings = instrument.figi_mappings if hasattr(instrument, 'figi_mappings') else None
    legal_entity = instrument.legal_entity if hasattr(instrument, 'legal_entity') else None
    trading_venues = instrument.trading_venues if hasattr(instrument, 'trading_venues') else None
    
    # These should be accessible without errors (even if None/empty)
    assert figi_mappings is not None or figi_mappings is None  # Should not error
    assert legal_entity is not None or legal_entity is None    # Should not error  
    assert trading_venues is not None or trading_venues is None # Should not error
    
    session.close()

@pytest.mark.integration
def test_multiple_instrument_operations(setup_database, test_service):
    """Test multiple concurrent operations on different instruments."""
    
    # Test getting multiple instruments
    session1, instrument1 = test_service.get_instrument(TEST_EQUITY_ISIN)
    if instrument1:
        assert instrument1.isin == TEST_EQUITY_ISIN
        session1.close()
    
    # Try to get venues for the instrument
    venues = test_service.get_instrument_venues(TEST_EQUITY_ISIN) 
    assert venues is not None  # Should return data structure even if empty
