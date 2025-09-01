#!/usr/bin/env python3
"""
Test script to verify the updated FIRDS service layer supports all 10 instrument types.

This script will:
1. Test the FIRDS type auto-detection
2. Test the instrument creation process
3. Verify the new model structure works
4. Show the venue records creation
"""

import logging
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from marketdata_api.services.sqlite.instrument_service import SqliteInstrumentService
from marketdata_api.constants import FirdsTypes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_firds_type_mappings():
    """Test that all FIRDS type mappings are correctly defined."""
    print("=== Testing FIRDS Type Mappings ===")
    
    # Test that all 10 FIRDS types are mapped
    expected_types = ['C', 'D', 'E', 'F', 'H', 'I', 'J', 'S', 'R', 'O']
    
    for firds_type in expected_types:
        if firds_type in FirdsTypes.MAPPING:
            business_type = FirdsTypes.MAPPING[firds_type]
            print(f"✓ FIRDS Type {firds_type} -> {business_type}")
        else:
            print(f"✗ Missing FIRDS Type {firds_type}")
    
    print(f"\nTotal FIRDS types mapped: {len(FirdsTypes.MAPPING)}")
    print(f"Column mappings defined: {len(FirdsTypes.COLUMN_MAPPING)}")

def test_service_initialization():
    """Test that the service initializes correctly."""
    print("\n=== Testing Service Initialization ===")
    
    try:
        service = SqliteInstrumentService()
        print(f"✓ Service initialized successfully")
        print(f"✓ Database type: {service.database_type}")
        print(f"✓ Logger configured: {service.logger.name}")
        return service
    except Exception as e:
        print(f"✗ Service initialization failed: {e}")
        return None

def test_firds_file_search():
    """Test the FIRDS file search functionality."""
    print("\n=== Testing FIRDS File Search ===")
    
    service = SqliteInstrumentService()
    
    # Test with a known ISIN (you can replace with any ISIN from your files)
    test_isin = "NL0011821202"  # Example ISIN
    
    try:
        records, detected_type = service._get_firds_data_from_storage_all_types(test_isin)
        
        if records and detected_type:
            print(f"✓ Found {len(records)} records for {test_isin}")
            print(f"✓ Detected FIRDS type: {detected_type}")
            
            # Show the business instrument type mapping
            if detected_type in FirdsTypes.MAPPING:
                business_type = FirdsTypes.MAPPING[detected_type]
                print(f"✓ Maps to business type: {business_type}")
            
            # Show some sample fields from first record
            first_record = records[0]
            sample_fields = ['FinInstrmGnlAttrbts_FullNm', 'FinInstrmGnlAttrbts_ClssfctnTp', 
                           'FinInstrmGnlAttrbts_NtnlCcy', 'Issr']
            
            print(f"✓ Sample fields from first record:")
            for field in sample_fields:
                if field in first_record:
                    print(f"    {field}: {first_record[field]}")
                    
        else:
            print(f"✗ No records found for {test_isin}")
            print("  This might be expected if the ISIN is not in your FIRDS files")
            
    except Exception as e:
        print(f"✗ File search failed: {e}")

def test_attribute_processors():
    """Test the attribute processing methods."""
    print("\n=== Testing Attribute Processors ===")
    
    service = SqliteInstrumentService()
    
    # Create sample FIRDS record
    sample_record = {
        'FinInstrmGnlAttrbts_FullNm': 'Test Instrument',
        'FinInstrmGnlAttrbts_ClssfctnTp': 'ESXXXX',
        'FinInstrmGnlAttrbts_NtnlCcy': 'EUR',
        'DerivInstrmAttrbts_PricMltplr': '100.0',
        'DebtInstrmAttrbts_MtrtyDt': '2025-12-31'
    }
    
    # Test different business types
    business_types = ['equity', 'debt', 'future', 'collective_investment', 'hybrid']
    
    for business_type in business_types:
        try:
            attributes = service._process_instrument_attributes(sample_record, business_type, 'E')
            print(f"✓ Processed attributes for {business_type}: {len(attributes)} attributes")
            
            # Show some key attributes
            if 'business_type' in attributes:
                print(f"    Business type: {attributes['business_type']}")
            if 'firds_type' in attributes:
                print(f"    FIRDS type: {attributes['firds_type']}")
                
        except Exception as e:
            print(f"✗ Failed to process {business_type}: {e}")

def main():
    """Run all tests."""
    print("🧪 Testing Updated FIRDS Service Layer")
    print("=" * 50)
    
    # Run all tests
    test_firds_type_mappings()
    
    service = test_service_initialization()
    if not service:
        print("❌ Cannot proceed with tests - service initialization failed")
        return
    
    test_firds_file_search()
    test_attribute_processors()
    
    print("\n" + "=" * 50)
    print("🎉 Service layer testing complete!")
    print("\nNext steps:")
    print("1. Test with real ISIN data")
    print("2. Update API routes")
    print("3. Run integration tests")

if __name__ == "__main__":
    main()
