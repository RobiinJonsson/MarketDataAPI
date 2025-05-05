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
    # Initialize database properly with force recreation
    init_database(force_recreate=True)
    
    service = InstrumentService()
    
    print("\nTesting Equity Instrument...")
    test_equity(service)
    
    print("\nTesting Debt Instrument...")
    test_debt(service)

def test_equity(service):
    isin = "FR0000131104"  # BNP Paribas
    try:
        instrument = service.get_or_create_instrument(isin, "equity")
        print_instrument_details(instrument, "Equity")
    except Exception as e:
        print(f"Error testing equity: {str(e)}")
        raise

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
    
    if hasattr(instrument, 'price_multiplier'):
        print(f"Price Multiplier: {instrument.price_multiplier}")
    if hasattr(instrument, 'maturity_date'):
        print(f"Maturity Date: {instrument.maturity_date}")
        print(f"Fixed Interest Rate: {instrument.fixed_interest_rate}")
    
    print(f"Additional Data: {instrument.additional_data}")

if __name__ == "__main__":
    run_tests()
