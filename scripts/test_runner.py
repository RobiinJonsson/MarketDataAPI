"""Test runner script to avoid import issues"""
import os
import sys

# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from marketdata_api.services.instrument_service import InstrumentService
from marketdata_api.database.db import Base, engine
from marketdata_api.database.initialize_db import init_database

def run_tests():
    # Initialize database only if it doesn't exist
    init_database(force_recreate=False)
    
    service = InstrumentService()
    
    print("\nTesting Equity Instrument...")
    test_equity(service)
    
    print("\nTesting Debt Instrument...")
    test_debt(service)

def test_equity(service):
    isin = "FR0000131104"  # BNP Paribas
    session = None
    try:
        instrument = service.get_or_create_instrument(isin, "equity")
        # Ensure we have all relationships loaded before closing session
        if instrument and instrument.figi_mapping:
            _ = instrument.figi_mapping.security_type  # Force load
        print_instrument_details(instrument, "Equity")
    except Exception as e:
        print(f"Error testing equity: {str(e)}")
        raise
    finally:
        if session:
            session.close()

def test_debt(service):
    isin = "XS2332219612"  # Example bond
    try:
        instrument = service.get_or_create_instrument(isin, "debt")
        print_instrument_details(instrument, "Debt")
    except Exception as e:
        print(f"Error testing debt: {str(e)}")
        raise

def print_instrument_details(instrument, type_name):
    print(f"\n{type_name} Instrument Details:")
    print("-" * 25)
    if not instrument:
        print("No instrument found or created")
        return
        
    print(f"ID: {instrument.id}")
    print(f"ISIN: {instrument.isin}")
    print(f"Type: {instrument.type}")
    print(f"Name: {instrument.full_name}")
    print(f"Short Name: {instrument.short_name}")
    print(f"Currency: {instrument.currency}")
    print(f"Trading Venue: {instrument.trading_venue}")
    print(f"LEI: {instrument.lei_id}")
    print(f"FIGI: {instrument.figi}")
    
    # Add FIGI mapping details
    if hasattr(instrument, 'figi_mapping') and instrument.figi_mapping:
        print("\nFIGI Mapping Details:")
        print("-" * 25)
        fm = instrument.figi_mapping
        print(f"FIGI: {fm.figi}")
        print(f"Composite FIGI: {fm.composite_figi}")
        print(f"Share Class FIGI: {fm.share_class_figi}")
        print(f"Ticker: {fm.ticker}")
        print(f"Security Type: {fm.security_type}")
        print(f"Market Sector: {fm.market_sector}")
        print(f"Security Description: {fm.security_description}")
        print(f"Last Updated: {fm.last_updated}")
    
    if hasattr(instrument, 'price_multiplier'):
        print(f"\nPrice Multiplier: {instrument.price_multiplier}")
    if hasattr(instrument, 'maturity_date'):
        print(f"Maturity Date: {instrument.maturity_date}")
        print(f"Fixed Interest Rate: {instrument.fixed_interest_rate}")
    
    print(f"\nAdditional Data: {instrument.additional_data}")

if __name__ == "__main__":
    run_tests()
