# Enrichment Optimization Strategy

## Current Analysis

### LEI Enrichment - ✅ Already Optimal
- **Relationship**: 1:1 (ISIN → LEI)
- **Current Implementation**: ✅ Perfect
- **API Efficiency**: Only 1 GLEIF API call per unique LEI
- **Multi-venue Impact**: None (LEI is consistent across all venues for same ISIN)

### OpenFIGI Enrichment - ⚠️ Needs Optimization

#### Current Issues
1. **Venue Selection**: Using first venue record arbitrarily
2. **Exchange Code Dependency**: OpenFIGI requires specific exchange codes for best results
3. **Response Reliability**: Some MIC codes don't return successful responses
4. **Multi-venue Data**: Not leveraging all available venue information

## Recommended OpenFIGI Optimization Strategies

### Strategy 1: Intelligent Venue Prioritization
```python
def get_optimal_venue_for_figi(venue_records: List[Dict]) -> Dict:
    """
    Select the best venue record for OpenFIGI API calls based on:
    1. Primary trading venue (largest volume/most liquid)
    2. Exchange code reliability in OpenFIGI
    3. Venue status and dates
    """
    
    # Priority order for venue selection
    venue_priorities = {
        'XSTO': 1,  # Stockholm Stock Exchange (primary for SE ISINs)
        'XHEL': 2,  # Helsinki
        'XCSE': 3,  # Copenhagen
        'XOSL': 4,  # Oslo
        'MTAA': 5,  # Multilateral trading facilities
        # Add more based on experience
    }
    
    # Filter active venues
    active_venues = [
        record for record in venue_records 
        if not record.get('TradgVnRltdAttrbts_TermntnDt')  # No termination date
    ]
    
    # Sort by priority and return best match
    return min(active_venues, 
              key=lambda x: venue_priorities.get(
                  x.get('TradgVnRltdAttrbts_Id'), 999
              ))
```

### Strategy 2: Fallback Chain Approach
```python
def enrich_figi_with_fallback(isin: str, venue_records: List[Dict]) -> FigiMapping:
    """
    Try multiple venues in order of priority until successful
    """
    
    # Order venues by reliability/priority
    ordered_venues = prioritize_venues(venue_records)
    
    for venue_record in ordered_venues:
        venue_id = venue_record.get('TradgVnRltdAttrbts_Id')
        exchange_code = map_venue_to_exchange_code(venue_id)
        
        # Try OpenFIGI with specific venue
        figi_data = search_openfigi_with_venue(isin, exchange_code)
        if figi_data and not is_error_response(figi_data):
            return map_figi_data(figi_data, isin)
    
    # Final fallback: try without venue specification
    return search_openfigi(isin, instrument_type)
```

### Strategy 3: Multi-venue FIGI Collection
```python
def collect_all_venue_figis(isin: str, venue_records: List[Dict]) -> List[FigiMapping]:
    """
    Collect FIGI data for all available venues (for instruments with multiple listings)
    """
    
    figi_mappings = []
    for venue_record in venue_records:
        venue_id = venue_record.get('TradgVnRltdAttrbts_Id')
        exchange_code = map_venue_to_exchange_code(venue_id)
        
        figi_data = search_openfigi_with_venue(isin, exchange_code)
        if figi_data:
            mapping = map_figi_data(figi_data, isin)
            if mapping:
                mapping.venue_id = venue_id  # Track which venue this FIGI relates to
                figi_mappings.append(mapping)
    
    return figi_mappings
```

## Exchange Code Mapping Enhancement

### Current Implementation Analysis
Your current `EXCHANGE_CODES` mapping in config.py:
```python
EXCHANGE_CODES = {
    'SE': 'SS',  # Sweden (Stockholm)
    'DE': 'GR',  # Germany (Xetra)  
    'US': 'US',  # United States
    # etc...
}
```

### Enhanced Venue-to-Exchange Mapping
```python
VENUE_TO_EXCHANGE_MAP = {
    # Stockholm Stock Exchange
    'XSTO': 'SS',    # Primary Stockholm
    'MSTX': 'SS',    # Stockholm variants
    
    # Other Nordic
    'XHEL': 'HE',    # Helsinki
    'XCSE': 'DC',    # Copenhagen  
    'XOSL': 'OL',    # Oslo
    
    # German venues
    'XETR': 'GR',    # Xetra (most liquid)
    'XFRA': 'GR',    # Frankfurt
    'MTAA': 'GR',    # MTF venues
    
    # Add venue-specific mappings based on MIC codes
}

def get_exchange_code_for_venue(venue_id: str, isin: str) -> str:
    """
    Get exchange code prioritizing venue-specific mapping,
    falling back to country-code mapping
    """
    # Try venue-specific mapping first
    if venue_id in VENUE_TO_EXCHANGE_MAP:
        return VENUE_TO_EXCHANGE_MAP[venue_id]
    
    # Fallback to country code
    country_code = isin[:2]
    return EXCHANGE_CODES.get(country_code, DEFAULT_EXCHANGE_CODE)
```

## Recommended Implementation Plan

### Phase 1: Immediate Improvements
1. **Implement Strategy 1** (Intelligent Venue Prioritization)
2. **Add venue-to-exchange mapping** for known reliable venues
3. **Add logging** to track OpenFIGI success rates per venue

### Phase 2: Advanced Optimization  
1. **Implement Strategy 2** (Fallback Chain)
2. **Add venue success rate tracking** to improve prioritization
3. **Consider caching** successful venue-exchange combinations

### Phase 3: Multi-venue Support (Optional)
1. **Implement Strategy 3** if you need multiple FIGIs per instrument
2. **Extend FIGI model** to support venue-specific FIGIs
3. **API endpoints** to access venue-specific FIGI data

## Key Benefits

1. **Higher Success Rates**: More reliable OpenFIGI responses
2. **Venue Awareness**: Leverage your multi-venue FIRDS data
3. **Fallback Reliability**: Multiple attempts increase success probability
4. **Future-proof**: Ready for transparency data integration
5. **Optimal API Usage**: Minimal unnecessary API calls

## Risk Mitigation

- **LEI Unchanged**: No impact on LEI enrichment (already optimal)
- **Backward Compatibility**: Existing FIGI enrichment still works
- **Gradual Implementation**: Can be deployed incrementally
- **Monitoring**: Enhanced logging for performance tracking
