import requests
import os
from marketdata_api.config import OPENFIGI_API_KEY, EXCHANGE_CODES, DEFAULT_EXCHANGE_CODE
from flask import jsonify


OPENFIGI_API_URL = "https://api.openfigi.com/v3/mapping"
OPENFIGI_KEY = os.getenv("OPENFIGI_API_KEY")  # Store API key in .env

    
def get_exchange_code(isin):
    """
    Get the appropriate exchange code based on ISIN country code.
    Returns DEFAULT_EXCHANGE_CODE if no mapping exists.
    """
    # Extract country code from ISIN (first 2 characters)
    country_code = isin[:2].upper()
    
    # Get exchange code from config
    return EXCHANGE_CODES.get(country_code, DEFAULT_EXCHANGE_CODE)

def get_exchange_code_for_venue(venue_id: str, isin: str) -> str:
    """
    Get exchange code prioritizing venue-specific mapping for better OpenFIGI results.
    
    Args:
        venue_id: MIC code from FIRDS venue data (e.g., 'XSTO', 'XHEL')
        isin: ISIN for fallback country-based mapping
        
    Returns:
        Exchange code optimized for OpenFIGI API
    """
    # Venue-specific mappings for known reliable combinations
    VENUE_TO_EXCHANGE_MAP = {
        # Nordic venues - high reliability
        'XSTO': 'SS',    # Stockholm Stock Exchange (primary for Swedish equities)
        'XHEL': 'HE',    # Nasdaq Helsinki
        'XCSE': 'DC',    # Nasdaq Copenhagen  
        'XOSL': 'OL',    # Oslo Børs
        
        # German venues
        'XETR': 'GR',    # Xetra (most liquid German venue)
        'XFRA': 'GR',    # Frankfurt Stock Exchange
        
        # Other major European venues
        'XLON': 'LN',    # London Stock Exchange
        'XPAR': 'FP',    # Euronext Paris
        'XAMS': 'NA',    # Euronext Amsterdam
        'XBRU': 'BR',    # Euronext Brussels
        'XMIL': 'IM',    # Borsa Italiana
        'XMAD': 'MC',    # Bolsas y Mercados Españoles
        
        # US venues
        'XNYS': 'US',    # New York Stock Exchange
        'XNAS': 'US',    # NASDAQ
        
        # Swiss
        'XSWX': 'SW',    # SIX Swiss Exchange
    }
    
    # Try venue-specific mapping first (most reliable)
    if venue_id and venue_id in VENUE_TO_EXCHANGE_MAP:
        return VENUE_TO_EXCHANGE_MAP[venue_id]
    
    # Fallback to country-based mapping
    return get_exchange_code(isin)

def search_openfigi(isin: str, instrument_type, venue_id: str = None) -> list:
    """
    Search OpenFIGI for an ISIN and return the results.
    
    Args:
        isin: ISIN to search for
        instrument_type: Type of instrument ('equity', 'debt', 'future')  
        venue_id: Optional MIC code for venue-specific search
        
    Returns:
        List of FIGI data results
    """
    url = "https://api.openfigi.com/v3/mapping"
    headers = {
        "Content-Type": "application/json",
        "X-OPENFIGI-APIKEY": OPENFIGI_API_KEY
    }
    
    # Get exchange code (venue-aware if venue_id provided)
    if venue_id:
        exch_code = get_exchange_code_for_venue(venue_id, isin)
        search_context = f"venue {venue_id} -> exchange {exch_code}"
    else:
        exch_code = get_exchange_code(isin)
        search_context = f"country-based exchange {exch_code}"
    
    # Use exchange code for equity instruments (better specificity)
    if instrument_type == "equity":
        payload = [
            {
                "idType": "ID_ISIN",
                "idValue": isin,
                "exchCode": exch_code
            }
        ]
        print(f"Searching OpenFIGI for ISIN: {isin} with {search_context}")
    else:
        # For debt/other instruments, exclude exchange code (broader search)
        payload = [
            {
                "idType": "ID_ISIN",
                "idValue": isin
            }
        ]
        print(f"Searching OpenFIGI for ISIN: {isin} (broad search, no exchange filter)")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"OpenFIGI response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"OpenFIGI response data: {data}")
            
            if data and len(data) > 0 and 'data' in data[0]:
                # Return only the first item from data array
                return [data[0]['data'][0]] if data[0]['data'] else []
        return []
        
    except Exception as e:
        print(f"Error in OpenFIGI search: {str(e)}")
        return []

def search_openfigi_with_fallback(isin: str, instrument_type: str, venue_records: list = None) -> list:
    """
    Search OpenFIGI with intelligent venue selection and fallback strategy.
    
    Args:
        isin: ISIN to search for
        instrument_type: Type of instrument
        venue_records: List of venue records from FIRDS (optional)
        
    Returns:
        List of FIGI data results, or empty list if no results found
    """
    
    def prioritize_venues(records):
        """Prioritize venues based on reliability and liquidity"""
        if not records:
            return []
            
        # Venue priority scores (lower = higher priority)
        venue_priorities = {
            'XSTO': 1,   # Stockholm - primary for Swedish equities
            'XHEL': 2,   # Helsinki - good Nordic coverage
            'XCSE': 3,   # Copenhagen - reliable
            'XOSL': 4,   # Oslo - decent coverage
            'XETR': 1,   # Xetra - primary for German instruments
            'XLON': 2,   # London - good international coverage
            'XNYS': 1,   # NYSE - primary US venue
            'XNAS': 2,   # NASDAQ - secondary US venue
        }
        
        # Filter to active venues (no termination date)
        active_venues = [
            record for record in records 
            if not record.get('TradgVnRltdAttrbts_TermntnDt')
        ]
        
        # Sort by priority score
        return sorted(active_venues, 
                     key=lambda x: venue_priorities.get(
                         x.get('TradgVnRltdAttrbts_Id'), 999
                     ))
    
    # Strategy 1: Try with prioritized venues if available
    if venue_records:
        prioritized_venues = prioritize_venues(venue_records)
        
        for venue_record in prioritized_venues[:3]:  # Try top 3 venues max
            venue_id = venue_record.get('TradgVnRltdAttrbts_Id')
            if venue_id:
                result = search_openfigi(isin, instrument_type, venue_id)
                if result:  # Found data
                    print(f"✅ OpenFIGI success with venue {venue_id}")
                    return result
                else:
                    print(f"❌ OpenFIGI failed with venue {venue_id}, trying next...")
    
    # Strategy 2: Fallback to country-based search  
    print(f"🔄 Falling back to country-based OpenFIGI search for {isin}")
    result = search_openfigi(isin, instrument_type)
    
    if result:
        print(f"✅ OpenFIGI success with country-based search")
    else:
        print(f"❌ OpenFIGI failed completely for {isin}")
    
    return result
    
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