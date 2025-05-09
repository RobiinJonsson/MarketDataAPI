import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from marketdata_api.services.openfigi import search_openfigi

def test_openfigi_search():
    # Test ISIN - HUFVUDSTADEN AB
    isin = "XS2332219612"
    instrument_type = "debt"
    mic_code = "DSTO"  # Xetra
    exch_code = "SS"  # Xetra
    
    print(f"Testing OpenFIGI search for:")
    print(f"ISIN: {isin}")
    print(f"Type: {instrument_type}")
    print(f"MIC: {mic_code}")
    print(f"Exchange: {exch_code}")
    print("\nSearching...")
    
    result = search_openfigi(isin, instrument_type)
    
    print("\nResponse:")
    if result:
        for item in result:
            print("\nFIGI Data:")
            for key, value in item.items():
                print(f"{key}: {value}")
    else:
        print("No data found or error occurred")

if __name__ == "__main__":
    test_openfigi_search()
