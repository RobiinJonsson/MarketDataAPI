#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from marketdata_api.database.session import SessionLocal
from marketdata_api.models.instrument import Instrument, Equity

def check_database_directly():
    """Check the database directly for the instrument"""
    session = SessionLocal()
    try:
        print("Checking instruments table...")
        
        # Check instruments table
        instruments = session.query(Instrument).filter(Instrument.isin == 'NL00150001S5').all()
        print(f"Found {len(instruments)} instruments with ISIN NL00150001S5")
        
        for instrument in instruments:
            print(f"  ID: {instrument.id}")
            print(f"  ISIN: {instrument.isin}")
            print(f"  Type: {instrument.type}")
            print(f"  Full Name: {instrument.full_name}")
            print(f"  Symbol: {instrument.symbol}")
            print()
        
        # Check equities table specifically
        print("Checking equities table...")
        equities = session.query(Equity).join(Instrument).filter(Instrument.isin == 'NL00150001S5').all()
        print(f"Found {len(equities)} equities with ISIN NL00150001S5")
        
        for equity in equities:
            print(f"  Equity ID: {equity.id}")
            print(f"  Parent Instrument ISIN: {equity.isin}")
            print(f"  Type: {equity.type}")
            print()
        
        # Check if there are any instruments at all
        total_instruments = session.query(Instrument).count()
        print(f"Total instruments in database: {total_instruments}")
        
        total_equities = session.query(Equity).count()
        print(f"Total equities in database: {total_equities}")
        
    except Exception as e:
        print(f"Error checking database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    check_database_directly()
