#!/usr/bin/env python3
"""
Test script for the updated CFI decoder
Tests various CFI codes to ensure comprehensive coverage
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from marketdata_api.models.utils.cfi import CFI, decode_cfi
import json

def test_cfi_codes():
    """Test various CFI codes from different categories"""
    
    # Test cases covering all major categories
    test_codes = [
        # Equities (E)
        "ESVUFR",  # Common shares - Voting, Free, Fully paid, Registered
        "EPVNFB",  # Preferred shares - Voting, Perpetual, Fixed income, Bearer
        "EDSPFR",  # Depository receipts - Common shares, Perpetual, Fixed income, Registered
        "EYAMFB",  # Structured participation - Tracker, Others, Cash, Baskets
        
        # Debt instruments (D)
        "DBFUFB",  # Bonds - Fixed rate, Unsecured, Fixed maturity, Bearer
        "DCVSGR",  # Convertible bonds - Variable rate, Secured, Call feature, Registered
        
        # Collective Investment Vehicles (C) 
        "CIOGEU",  # Standard funds - Open-end, Accumulation, Equities, Units
        "CHDXXX",  # Hedge funds - Directional strategy
        "CBIGES",  # REIT - Income, Accumulation, Real estate, Shares
        "CEIGEU",  # ETF - Open-end, Accumulation, Equities, Units
        
        # Invalid codes
        "INVALID",  # Too short
        "TOOLONG", # Too long
        "ZZZZZZ",  # Unknown category
    ]
    
    print("🧪 CFI Decoder Test Results")
    print("=" * 60)
    
    for code in test_codes:
        print(f"\n📋 Testing CFI Code: {code}")
        print("-" * 30)
        
        try:
            result = decode_cfi(code)
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Category: {result['category']} - {result['category_description']}")
                print(f"✅ Group: {result['group']} - {result['group_description']}")
                print(f"✅ Attributes: {result['attributes']}")
                
                # Print decoded attributes
                if result['decoded_attributes']:
                    print("📊 Decoded Attributes:")
                    for key, value in result['decoded_attributes'].items():
                        print(f"   • {key.replace('_', ' ').title()}: {value}")
                        
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🏁 CFI Decoder Test Complete")

def test_firds_common_cfis():
    """Test CFI codes commonly found in FIRDS data"""
    
    print("\n🗂️  FIRDS Common CFI Codes")
    print("=" * 60)
    
    # Common FIRDS CFI patterns
    firds_codes = [
        "ESVUFR",  # Typical equity
        "DBFNFR",  # Typical bond
        "CEIGEU",  # ETF
        "CIOGEU",  # Investment fund
        "FFXXXX",  # Future (placeholder attributes)
        "OCXXXX",  # Call option
        "OPXXXX",  # Put option
    ]
    
    for code in firds_codes:
        try:
            cfi = CFI(code)
            desc = cfi.describe()
            print(f"\n{code}: {desc['category_description']} - {desc['group_description']}")
            
            # Show business type mapping like in our FIRDS service
            if cfi.is_equity():
                business_type = "equity"
            elif cfi.is_debt():
                business_type = "debt" 
            elif cfi.is_collective_investment():
                business_type = "collective_investment"
            elif code.startswith('F'):
                business_type = "future"
            elif code.startswith('O'):
                business_type = "option"
            else:
                business_type = "other"
            
            print(f"   → Maps to business type: {business_type}")
            
        except Exception as e:
            print(f"{code}: ❌ {str(e)}")

if __name__ == "__main__":
    test_cfi_codes()
    test_firds_common_cfis()
