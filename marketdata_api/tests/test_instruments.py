import pytest
from datetime import date
from marketdata_api.services.instrument_service import InstrumentService
from marketdata_api.database.session import get_session
from marketdata_api.database.base import Base, engine
from marketdata_api.models import *  # This imports all models

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def test_service():
    return InstrumentService()

def test_create_equity(setup_database, test_service):
    data = {
        'FinInstrmGnlAttrbts_Id': 'SE0000108656',
        'FinInstrmGnlAttrbts_FullNm': 'Ericsson B',
        'FinInstrmGnlAttrbts_ShrtNm': 'ERIC B',
        'Issr': 'M312WZV08Y7LYUC71685'
    }
    
    instrument = test_service.create_instrument(data, 'equity')
    
    assert instrument.isin == 'SE0000108656'
    assert instrument.type == 'equity'

def test_create_debt(setup_database, test_service):
    data = {
        'FinInstrmGnlAttrbts_Id': 'XS2332219612',
        'FinInstrmGnlAttrbts_FullNm': 'Swedish Gov Bond 2026',
        'DebtInstrmAttrbts_MtrtyDt': '2026-06-01',
        'DebtInstrmAttrbts_IntrstRate_Fxd': '0.375'
    }
    
    instrument = test_service.create_instrument(data, 'debt')
    assert instrument.isin == 'XS2332219612'
    assert instrument.type == 'debt'
    assert instrument.fixed_interest_rate == 0.375

def test_create_debt_invalid_date(setup_database, test_service):
    """Test handling of invalid date format"""
    data = {
        'FinInstrmGnlAttrbts_Id': 'XS2332219612',
        'DebtInstrmAttrbts_MtrtyDt': 'invalid-date',
        'DebtInstrmAttrbts_IntrstRate_Fxd': '0.375'
    }
    
    instrument = test_service.create_instrument(data, 'debt')
    assert instrument.maturity_date is None  # Should skip invalid date conversion

def test_create_instrument_with_relationships(setup_database, test_service):
    """Test creation of instrument with FIGI and Legal Entity relationships"""
    # Add relationship testing

def test_get_instrument(test_service):
    service = test_service
    instrument = service.get_instrument('SE0000108656')
    assert instrument is not None
    assert instrument.isin == 'SE0000108656'

def test_update_instrument(setup_database, test_service):
    # Create initial instrument
    data = {
        'FinInstrmGnlAttrbts_Id': 'SE0000108656',
        'FinInstrmGnlAttrbts_ShrtNm': 'ERIC B'
    }
    instrument = test_service.create_instrument(data, 'equity')
    
    # Update the instrument
    updated_data = {
        'FinInstrmGnlAttrbts_ShrtNm': 'ERIC B NEW'
    }
    updated = test_service.update_instrument('SE0000108656', updated_data)
    assert updated.short_name == 'ERIC B NEW'
