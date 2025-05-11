import pytest
import logging
from ..services.instrument_service import InstrumentService
from ..models.instrument import Instrument, Equity, Debt
from ..database.base import engine
from ..models.base_model import Base

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def test_service():
    return InstrumentService()

def test_get_or_create_equity(setup_database, test_service):
    """Test getting or creating an equity instrument"""
    isin = "SE0000113250"  # Use a known ISIN (e.g., BNP Paribas)
    
    try:
        instrument = test_service.get_or_create_instrument(isin, "equity")
        
        print("\nEquity Instrument Details:")
        print("-------------------------")
        if instrument:
            print(f"ID: {instrument.id}")
            print(f"ISIN: {instrument.isin}")
            print(f"Type: {instrument.type}")
            print(f"Name: {instrument.full_name}")
            print(f"Short Name: {instrument.short_name}")
            print(f"Currency: {instrument.currency}")
            print(f"Trading Venue: {instrument.trading_venue}")
            print(f"LEI: {instrument.lei_id}")
            print(f"FIGI: {instrument.figi}")
            if isinstance(instrument, Equity):
                print(f"Price Multiplier: {instrument.price_multiplier}")
                print(f"Asset Class: {instrument.asset_class}")
            print(f"Additional Data: {instrument.additional_data}")
        else:
            print("No instrument found or created")
            
        assert instrument is not None
        assert instrument.isin == isin
        assert instrument.type == "equity"
        
    except Exception as e:
        print(f"Error in test: {str(e)}")
        raise

def test_get_or_create_debt(setup_database, test_service):
    """Test getting or creating a debt instrument"""
    isin = "XS2332219612"  # Use a known ISIN (e.g., a government bond)
    
    try:
        instrument = test_service.get_or_create_instrument(isin, "debt")
        
        print("\nDebt Instrument Details:")
        print("-------------------------")
        if instrument:
            print(f"ID: {instrument.id}")
            print(f"ISIN: {instrument.isin}")
            print(f"Type: {instrument.type}")
            print(f"Name: {instrument.full_name}")
            print(f"Currency: {instrument.currency}")
            print(f"LEI: {instrument.lei_id}")
            if isinstance(instrument, Debt):
                print(f"Maturity Date: {instrument.maturity_date}")
                print(f"Fixed Interest Rate: {instrument.fixed_interest_rate}")
                print(f"Total Issued Nominal: {instrument.total_issued_nominal}")
            print(f"Additional Data: {instrument.additional_data}")
        else:
            print("No instrument found or created")
            
        assert instrument is not None
        assert instrument.isin == isin
        assert instrument.type == "debt"
        
    except Exception as e:
        print(f"Error in test: {str(e)}")
        raise

if __name__ == "__main__":
    # Manual test execution
    service = InstrumentService()
    
    print("\nTesting Equity Instrument...")
    test_get_or_create_equity(None, service)
    
    print("\nTesting Debt Instrument...")
    test_get_or_create_debt(None, service)
