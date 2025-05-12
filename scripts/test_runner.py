"""Test runner script to avoid import issues"""
import os
import sys

# Get the absolute path to the project root
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.insert(0, project_root)

from marketdata_api.services.instrument_service import InstrumentService
from marketdata_api.services.legal_entity_service import LegalEntityService
from marketdata_api.database.initialize_db import init_database

def run_tests():
    # Initialize database with force recreate to apply schema changes
    init_database(force_recreate=False)  # Changed to False to prevent data loss
    
    print("\nTesting Legal Entity Service...")
    test_legal_entities()
    
    service = InstrumentService()
    
    print("\nTesting Equity Instrument...")
    test_equity(service)
    
    print("\nTesting Debt Instrument...")
    test_debt(service)

def test_legal_entities():
    service = LegalEntityService()
    session = None
    
    try:
        # Test create/update
        print("\nTesting create/update legal entity...")
        lei = "R0MUWSFPU8MPRO8K5P83"  # BNP Paribas LEI
        session, entity = service.create_or_update_entity(lei)
        
        if entity:
            print(f"Created/Updated entity: {entity.lei}")
            print(f"Name: {entity.name}")
            print(f"Jurisdiction: {entity.jurisdiction}")
            print(f"Status: {entity.status}")
            print(f"BIC: {entity.bic}")
            if entity.addresses:
                print("\nAddresses:")
                for addr in entity.addresses:
                    print(f"- {addr.type}: {addr.city}, {addr.country}")
                    if addr.address_lines:
                        print(f"  Address: {addr.address_lines}")

        # Test get
        print("\nTesting get entity...")
        get_session, retrieved = service.get_entity(lei)
        if retrieved:
            print(f"Retrieved entity: {retrieved.lei}")
            get_session.close()
        
        # Test get all
        print("\nTesting get all entities...")
        all_session, all_entities = service.get_all_entities()
        print(f"Total entities: {len(all_entities)}")
        all_session.close()
        
    except Exception as e:
        print(f"Error creating/updating entity: {str(e)}")
        raise
    finally:
        if session:
            session.close()

def test_equity(service):
    isin = "FR0000131104"  # BNP Paribas
    session = None
    try:
        # First get/create the basic instrument
        instrument = service.get_or_create_instrument(isin, "equity")
        if instrument:
            # Then enrich it with additional data
            session, instrument = service.enrich_instrument(instrument)
            print_instrument_details(session, instrument, "Equity")
    except Exception as e:
        print(f"Error testing equity: {str(e)}")
        raise
    finally:
        if session:
            session.close()

def test_debt(service):
    isin = "XS2332219612"  # Example bond
    session = None
    try:
        # First get/create the basic instrument
        instrument = service.get_or_create_instrument(isin, "debt")
        if instrument:
            # Then enrich it with additional data
            session, instrument = service.enrich_instrument(instrument)
            print_instrument_details(session, instrument, "Debt")
    except Exception as e:
        print(f"Error testing debt: {str(e)}")
        raise
    finally:
        if session:
            session.close()

def print_instrument_details(session, instrument, type_name):
    """Print instrument details using active session"""
    print(f"\n{type_name} Instrument Details:")
    print("-" * 25)
    if not instrument:
        print("No instrument found or created")
        return

    # Use the active session to refresh and access relationships
    session.refresh(instrument)
        
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
