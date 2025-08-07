"""
API Response Examples: Current vs Proposed Unified Approach

This shows the dramatic improvement in API responses with the new design.
"""

# CURRENT API RESPONSE (what you're getting now)
current_venues_response = {
    "venues": [
        {
            "isin": "SE0000195646",
            "venue_id": "XSTO",
            "issuer_requested": "true",
            "first_trade_date": "2015-04-01T00:00:00Z",
            "admission_approval_date": "2015-03-31T00:00:00Z",
            "termination_date": None,
            "request_for_admission_date": "2015-03-01T00:00:00Z",
            "competent_authority": "SE",
            "publication_from_date": "2025-07-12T00:00:00Z",
            "relevant_trading_venue": "XSTO",
            "full_name": "Swedbank AB (publ) Class A",
            "short_name": "SEB A",
            "classification_type": "ESTTMM",
            "currency": "SEK",
            "lei": "M312WZV08Y7LYUC71685",
            # RAW FIRDS DATA INCLUDED (UNWANTED)
            "raw_record": {
                "Id": "SE0000195646",
                "FinInstrmGnlAttrbts_FullNm": "Swedbank AB (publ) Class A",
                "FinInstrmGnlAttrbts_ShrtNm": "SEB A",
                "FinInstrmGnlAttrbts_ClssfctnTp": "ESTTMM",
                "FinInstrmGnlAttrbts_NtnlCcy": "SEK",
                "FinInstrmGnlAttrbts_CmmdtyDerivInd": "false",
                "Issr": "M312WZV08Y7LYUC71685",
                "TradgVnRltdAttrbts_Id": "XSTO",
                "TradgVnRltdAttrbts_IssrReq": "true",
                "TradgVnRltdAttrbts_FrstTradDt": "2015-04-01T00:00:00Z",
                "TradgVnRltdAttrbts_AdmssnApprvlDtByIssr": "2015-03-31T00:00:00Z",
                "TradgVnRltdAttrbts_ReqForAdmssnDt": "2015-03-01T00:00:00Z",
                "TechAttrbts_RlvntCmptntAuthrty": "SE",
                "TechAttrbts_PblctnPrd_FrDt": "2025-07-12T00:00:00Z",
                "TechAttrbts_RlvntTradgVn": "XSTO",
                # ... 20+ more raw FIRDS fields
            }
        },
        # More venues with same raw data structure...
    ]
}

# PROPOSED API RESPONSE (clean, structured, no raw data)
proposed_venues_response = {
    "venues": [
        {
            "id": "venue-uuid-1",
            "venue_id": "XSTO",
            "isin": "SE0000195646",
            "first_trade_date": "2015-04-01T00:00:00Z",
            "termination_date": None,
            "admission_approval_date": "2015-03-31T00:00:00Z",
            "request_for_admission_date": "2015-03-01T00:00:00Z",
            "venue_full_name": "Swedbank AB (publ) Class A",
            "venue_short_name": "SEB A",
            "classification_type": "ESTTMM",
            "venue_currency": "SEK",
            "issuer_requested": "true",
            "competent_authority": "SE",
            "relevant_trading_venue": "XSTO",
            "publication_from_date": "2025-07-12T00:00:00Z",
            "created_at": "2025-08-07T15:30:00Z",
            "updated_at": "2025-08-07T15:30:00Z"
        },
        {
            "id": "venue-uuid-2", 
            "venue_id": "XHEL",
            "isin": "SE0000195646",
            "first_trade_date": "2015-04-01T00:00:00Z",
            "termination_date": None,
            "admission_approval_date": "2015-03-31T00:00:00Z",
            "request_for_admission_date": "2015-03-01T00:00:00Z",
            "venue_full_name": "Swedbank AB (publ) Class A",
            "venue_short_name": "SEB A",
            "classification_type": "ESTTMM", 
            "venue_currency": "SEK",
            "issuer_requested": "true",
            "competent_authority": "SE",
            "relevant_trading_venue": "XHEL",
            "publication_from_date": "2025-07-12T00:00:00Z",
            "created_at": "2025-08-07T15:30:00Z",
            "updated_at": "2025-08-07T15:30:00Z"
        }
        # ... more venues, all clean structured data
    ]
}

# INSTRUMENT RESPONSE WITH NEW APPROACH
proposed_instrument_response = {
    "id": "instrument-uuid",
    "isin": "SE0000195646",
    "instrument_type": "equity",
    "full_name": "Swedbank AB (publ) Class A",
    "short_name": "SEB A", 
    "currency": "SEK",
    "cfi_code": "ESTTMM",
    "lei_id": "M312WZV08Y7LYUC71685",
    "created_at": "2025-08-07T15:30:00Z",
    "updated_at": "2025-08-07T15:30:00Z",
    
    # Type-specific attributes (clean structure)
    "price_multiplier": 1.0,
    "underlying_isin": "US1234567890",
    "asset_class": {
        "oil_type": "crude",
        "sub_product": "WTI"
    },
    
    # Relationships (eagerly loaded)
    "figi_mapping": {
        "figi": "BBG000BQXJJ1",
        "market_sector": "Equity",
        "security_type": "Common Stock"
    },
    "legal_entity": {
        "lei": "M312WZV08Y7LYUC71685",
        "legal_name": "Swedbank AB",
        "jurisdiction": "SE"
    },
    "trading_venues_count": 39,  # Quick count without loading all venues
}

"""
KEY IMPROVEMENTS:

1. NO RAW FIRDS DATA in API responses
2. Clean, consistent field names
3. Proper data types (dates as ISO strings, numbers as numbers)
4. Structured JSON for complex attributes
5. All venue records stored in database (not read from files)
6. Much faster venue queries
7. Consistent response format across all instrument types

PERFORMANCE BENEFITS:

Current approach:
- get_instrument_venues(): Read CSV files, parse, format = ~100-500ms
- Complex polymorphic queries with many NULL columns
- Large response payloads with raw data

Proposed approach:  
- get_instrument_venues(): Simple database query = ~5-10ms
- Clean table structure with indexes
- Compact response payloads

MAINTAINABILITY BENEFITS:

Current: 5 model classes, 120+ columns, complex inheritance, file I/O
Proposed: 2 main classes, ~20 columns, JSON flexibility, database-only

The "controversial" JSON approach actually makes the code much cleaner
and handles the varying FIRDS column structures naturally.
"""
