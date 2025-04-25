import requests
import os
from marketdata_api.config import OPENFIGI_API_KEY, EXCHANGE_CODES, DEFAULT_EXCHANGE_CODE
from flask import jsonify
from marketdata_api.services.firds import process_all_xml_files_cli, downloads_dir
from marketdata_api.database.db import map_fields, FIELD_MAPPING


OPENFIGI_API_URL = "https://api.openfigi.com/v3/mapping"
OPENFIGI_KEY = os.getenv("OPENFIGI_API_KEY")  # Store API key in .env

#Unused function
def fetch_fi_data(identifier: str, identifier_type: str) -> dict:
    """
    Fetch data from FI based on the identifier and type.
    
    Args:
        identifier (str): The identifier (ISIN, ticker, etc.)
        identifier_type (str): The type of identifier ('ISIN', 'TICKER', etc.)
        
    Returns:
        dict: The raw FI data
    """
    if identifier_type.upper() != 'ISIN':
        return None
        
    # Process the XML files to get FI data
    result = process_all_xml_files_cli(downloads_dir, identifier)
    if not result:
        print(f"No data found for ISIN: {identifier}")
        return None
        
    # Debug output
    print(f"Raw XML data: {result}")
    
    # Ensure we have the required fields
    required_fields = [
        "FinInstrmGnlAttrbts_Id",
        "FinInstrmGnlAttrbts_FullNm",
        "FinInstrmGnlAttrbts_ShrtNm",
        "FinInstrmGnlAttrbts_ClssfctnTp",
        "FinInstrmGnlAttrbts_NtnlCcy"
    ]
    
    # Check if all required fields are present
    missing_fields = [field for field in required_fields if field not in result]
    if missing_fields:
        print(f"Missing required fields: {missing_fields}")
        return None
    
    # Return the raw data - mapping will be done in the route handler
    return result

    
def get_exchange_code(isin):
    """
    Get the appropriate exchange code based on ISIN country code.
    Returns DEFAULT_EXCHANGE_CODE if no mapping exists.
    """
    # Extract country code from ISIN (first 2 characters)
    country_code = isin[:2].upper()
    
    # Get exchange code from config
    return EXCHANGE_CODES.get(country_code, DEFAULT_EXCHANGE_CODE)

def search_openfigi(isin: str, mic_code: str = None) -> list:
    """Search OpenFIGI for an ISIN and return the results."""
    url = "https://api.openfigi.com/v3/mapping"
    headers = {
        "Content-Type": "application/json",
        "X-OPENFIGI-APIKEY": OPENFIGI_API_KEY
    }
    
    # Use MIC code if provided for equity
    if mic_code:
        payload = [
            {
                "idType": "ID_ISIN",
                "idValue": isin,
                "micCode": mic_code
            }
        ]
        print(f"Searching OpenFIGI for ISIN: {isin} with MIC code: {mic_code}")  # Debug
    # Else exclude MIC code in payload for debt
    else:
        exch_code = get_exchange_code(isin)
        payload = [
            {
                "idType": "ID_ISIN",
                "idValue": isin
            }
        ]
        print(f"Searching OpenFIGI for ISIN: {isin} with exchange code: {exch_code}")  # Debug  
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"OpenFIGI response status: {response.status_code}")  # Debug
        print(f"OpenFIGI response data: {response.json()}")  # Debug
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0 and 'data' in data[0]:
                return data[0]['data']
        return []
        
    except Exception as e:
        print(f"Error in OpenFIGI search: {str(e)}")
        return []
    
def batch_search_openfigi(isin_list, max_results=10):
    """Fetch instrument details for a batch of ISINs from OpenFIGI."""
    isin_list = isin_list[:max_results]  # Limit to max_results (default: 10)
    
    headers = {"Content-Type": "application/json"}
    if OPENFIGI_API_KEY:
        headers["X-OPENFIGI-APIKEY"] = OPENFIGI_API_KEY

    payload = [{"idType": "ID_ISIN", "idValue": isin} for isin in isin_list]
    
    print(f"Sending batch request to OpenFIGI: {payload}")  # Debugging

    response = requests.post(OPENFIGI_API_URL, json=payload, headers=headers)
    print(f"OpenFIGI response: {response.status_code}, {response.json()}")  # Debugging

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data", "status_code": response.status_code}