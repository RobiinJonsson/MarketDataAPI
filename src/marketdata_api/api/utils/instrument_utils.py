"""
Instrument Utilities

Pure utility functions for instrument data processing and response building.
Extracted from routes/instrument_routes.py for reusability across the application.
"""

from ...models.utils.cfi import CFI


def build_instrument_response(instrument):
    """
    Build comprehensive response with all instrument details using unified architecture.
    
    Args:
        instrument: SQLAlchemy Instrument model instance
        
    Returns:
        dict: Comprehensive instrument response with CFI decoding, FIGI mappings, etc.
    """
    # Start with the model's built-in serialization method
    response = instrument.to_api_response()

    # Add trading venues count
    response["trading_venues_count"] = (
        len(instrument.trading_venues) if instrument.trading_venues else 0
    )

    # Add CFI decoding if available
    if instrument.cfi_code and len(instrument.cfi_code) == 6:
        try:
            cfi = CFI(instrument.cfi_code)
            response["cfi_decoded"] = cfi.describe()
        except Exception as e:
            response["cfi_decoded"] = {"error": str(e)}

    # Add related entity info if available
    if instrument.legal_entity:
        response["legal_entity"] = {
            "lei": instrument.legal_entity.lei,
            "name": instrument.legal_entity.name,
            "jurisdiction": instrument.legal_entity.jurisdiction,
            "legal_form": instrument.legal_entity.legal_form,
            "status": instrument.legal_entity.status,
            "creation_date": (
                instrument.legal_entity.creation_date.isoformat()
                if instrument.legal_entity.creation_date
                else None
            ),
        }

    # Add FIGI mappings if available (now supporting multiple FIGIs)
    if instrument.figi_mappings:
        # For backward compatibility, use first FIGI for top-level fields
        primary_figi = instrument.figi_mappings[0]
        response["figi"] = primary_figi.figi
        response["composite_figi"] = primary_figi.composite_figi
        response["share_class_figi"] = primary_figi.share_class_figi
        response["security_type"] = primary_figi.security_type
        response["market_sector"] = primary_figi.market_sector
        response["ticker"] = primary_figi.ticker

        # Backward compatibility: single figi_mapping object with primary FIGI
        response["figi_mapping"] = {
            "figi": primary_figi.figi,
            "composite_figi": primary_figi.composite_figi,
            "share_class_figi": primary_figi.share_class_figi,
            "security_type": primary_figi.security_type,
            "market_sector": primary_figi.market_sector,
            "ticker": primary_figi.ticker,
        }

        # New field: all FIGI mappings as array
        response["figi_mappings"] = [
            {
                "figi": figi.figi,
                "composite_figi": figi.composite_figi,
                "share_class_figi": figi.share_class_figi,
                "security_type": figi.security_type,
                "market_sector": figi.market_sector,
                "ticker": figi.ticker,
            }
            for figi in instrument.figi_mappings
        ]

    return response


def validate_instrument_data(data):
    """
    Validate instrument data for creation/update operations.
    
    Args:
        data: Dictionary of instrument data
        
    Returns:
        tuple: (is_valid, errors_list)
    """
    errors = []
    
    # Required fields validation
    required_fields = ['isin', 'type']
    for field in required_fields:
        if not data.get(field):
            errors.append(f"Missing required field: {field}")
    
    # ISIN format validation
    isin = data.get('isin', '').strip().upper()
    if isin and len(isin) != 12:
        errors.append("ISIN must be exactly 12 characters")
    
    # CFI code validation
    cfi_code = data.get('cfi_code')
    if cfi_code and len(cfi_code) != 6:
        errors.append("CFI code must be exactly 6 characters")
    
    return len(errors) == 0, errors


def format_instrument_list_response(instruments, total_count, page=1, per_page=20):
    """
    Format a standardized instrument list response.
    
    Args:
        instruments: List of instrument model instances
        total_count: Total number of matching instruments
        page: Current page number
        per_page: Items per page
        
    Returns:
        dict: Formatted response with data and metadata
    """
    return {
        "status": "success",
        "data": [build_instrument_response(inst) for inst in instruments],
        "meta": {
            "page": page,
            "per_page": per_page,
            "total": total_count,
            "has_next": (page * per_page) < total_count,
            "has_prev": page > 1,
        },
    }