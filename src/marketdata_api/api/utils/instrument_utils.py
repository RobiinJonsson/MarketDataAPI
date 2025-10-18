"""
Instrument Utilities

Pure utility functions for instrument data processing and response building.
Extracted from routes/instrument_routes.py for reusability across the application.
"""

from ...models.utils.cfi import CFI


def build_instrument_response(instrument, include_rich_details=True):
    """
    Build comprehensive response with CLI-style rich data extraction using unified architecture.
    
    Args:
        instrument: SQLAlchemy Instrument model instance
        include_rich_details: Whether to include rich FIRDS data extraction and analysis
        
    Returns:
        dict: Comprehensive instrument response with CFI decoding, FIGI mappings, rich FIRDS data, etc.
    """
    # Start with the model's built-in serialization method
    response = instrument.to_api_response()

    if include_rich_details:
        # Add CLI-style rich data extraction
        response.update(_extract_rich_financial_details(instrument))
        response.update(_extract_rich_status_indicators(instrument))
        response.update(_extract_rich_type_specific_data(instrument))

    # Add trading venues count and details
    response["trading_venues_count"] = (
        len(instrument.trading_venues) if instrument.trading_venues else 0
    )
    
    if instrument.trading_venues:
        response["trading_venues"] = _format_trading_venues_data(instrument.trading_venues)

    # Add enhanced CFI decoding with business context
    if instrument.cfi_code and len(instrument.cfi_code) == 6:
        try:
            cfi = CFI(instrument.cfi_code)
            cfi_description = cfi.describe()
            response["cfi_decoded"] = cfi_description
            response["cfi_display"] = f"{instrument.cfi_code} ({cfi_description.get('description', 'N/A')})"
        except Exception as e:
            response["cfi_decoded"] = {"error": str(e)}
            response["cfi_display"] = f"{instrument.cfi_code} (decoding error)"

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

    # Normalize response structure for consistent frontend interface
    return _normalize_instrument_response(response)


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


def _extract_rich_financial_details(instrument):
    """Extract rich financial details like CLI formatting"""
    details = {}
    
    # Enhanced primary venue display with MIC lookup
    if instrument.relevant_trading_venue:
        details["primary_venue_display"] = _format_primary_venue_with_mic(instrument.relevant_trading_venue)
    
    # Extract financial data from FIRDS fields
    if instrument.firds_data and isinstance(instrument.firds_data, dict):
        firds = instrument.firds_data
        financial_data = {}
        
        # Price multiplier (common across derivatives)
        if firds.get('DerivInstrmAttrbts_PricMltplr'):
            financial_data['price_multiplier'] = firds['DerivInstrmAttrbts_PricMltplr']
            
        # Debt-specific financial fields
        if firds.get('DebtInstrmAttrbts_TtlIssdNmnlAmt'):
            amount = firds['DebtInstrmAttrbts_TtlIssdNmnlAmt']
            financial_data['total_issued_nominal'] = {
                'amount': float(amount),
                'formatted': f"{int(amount):,} {instrument.currency or ''}",
                'currency': instrument.currency
            }
            
        if firds.get('DebtInstrmAttrbts_NmnlValPerUnit'):
            financial_data['nominal_per_unit'] = firds['DebtInstrmAttrbts_NmnlValPerUnit']
            
        if firds.get('DebtInstrmAttrbts_IntrstRate_Fxd'):
            financial_data['fixed_interest_rate'] = {
                'rate': float(firds['DebtInstrmAttrbts_IntrstRate_Fxd']),
                'formatted': f"{firds['DebtInstrmAttrbts_IntrstRate_Fxd']}%"
            }
        
        if financial_data:
            details["financial_data"] = financial_data
    
    return details


def _extract_rich_status_indicators(instrument):
    """Extract status indicators like CLI formatting"""
    status_info = {
        "status_indicators": [],
        "display_status": ""
    }
    
    # Status indicators
    status_icons = []
    if instrument.commodity_derivative_indicator:
        status_icons.append("🌾 Commodity Derivative")
    if instrument.legal_entity:
        status_icons.append("✅ Issuer Verified")
    if instrument.figi_mappings:
        status_icons.append("🏷️ FIGI Mapped")
    
    status_info["status_indicators"] = status_icons
    status_info["display_status"] = " • ".join(status_icons) if status_icons else "ℹ️ Basic Information"
    
    return status_info


def _extract_rich_type_specific_data(instrument):
    """Extract type-specific rich data based on instrument classification"""
    type_data = {}
    
    # Extract commodity classification if applicable
    if instrument.firds_data and instrument.commodity_derivative_indicator:
        commodity_info = _get_commodity_classification(instrument.firds_data)
        if commodity_info:
            type_data["commodity_classification"] = commodity_info
    
    # Extract swap classification if CFI indicates swap
    if instrument.cfi_code and len(instrument.cfi_code) >= 2 and instrument.cfi_code[0] == 'S':
        swap_info = _get_swap_classification(instrument, instrument.firds_data or {})
        if swap_info:
            type_data["swap_classification"] = swap_info
    
    # Extract forward classification if CFI indicates forward
    if instrument.cfi_code and len(instrument.cfi_code) >= 2 and instrument.cfi_code[0] == 'J':
        forward_info = _get_forward_classification(instrument, instrument.firds_data or {})
        if forward_info:
            type_data["forward_classification"] = forward_info
    
    return type_data


def _format_trading_venues_data(trading_venues):
    """Format trading venues data like CLI tables"""
    return [
        {
            "venue_id": venue.venue_id if hasattr(venue, 'venue_id') else None,
            "mic_code": venue.mic_code if hasattr(venue, 'mic_code') else None,
            "first_trade_date": venue.first_trade_date.isoformat() if hasattr(venue, 'first_trade_date') and venue.first_trade_date else None,
            "venue_status": venue.venue_status if hasattr(venue, 'venue_status') else None,
        }
        for venue in trading_venues
    ]


def _format_primary_venue_with_mic(mic_code):
    """Format primary venue with rich MIC data lookup like CLI"""
    try:
        from ...database.session import get_session
        from ...models.sqlite.market_identification_code import MarketIdentificationCode
        
        with get_session() as session:
            mic_data = session.query(MarketIdentificationCode).filter(
                MarketIdentificationCode.mic == mic_code
            ).first()
            
            if mic_data:
                # Build rich display with MIC information
                venue_display = {
                    "mic_code": mic_code,
                    "market_name": mic_data.market_name,
                    "country_code": mic_data.iso_country_code,
                    "status": mic_data.status.value if mic_data.status else None,
                    "formatted": f"{mic_code}"
                }
                
                if mic_data.market_name:
                    # Truncate long market names for display
                    market_name = mic_data.market_name
                    if len(market_name) > 40:
                        market_name = market_name[:40] + "..."
                    venue_display["formatted"] += f" ({market_name})"
                
                return venue_display
            else:
                return {
                    "mic_code": mic_code,
                    "market_name": None,
                    "country_code": None,
                    "status": None,
                    "formatted": f"{mic_code} (MIC not found in registry)"
                }
                
    except Exception:
        # Fallback to basic display if lookup fails
        return {
            "mic_code": mic_code,
            "formatted": mic_code
        }


def _get_commodity_classification(firds_data):
    """Extract and format commodity classification information from FIRDS data like CLI"""
    classification_info = {
        'icon': '🌾',
        'display_name': 'Commodity',
        'additional_info': ''
    }
    
    # Natural Gas futures
    if (firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct') or
        firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct')):
        classification_info.update({
            'icon': '⛽',
            'display_name': 'Natural Gas',
            'additional_info': firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct', '')
        })
    
    # Agricultural - Seafood
    elif (firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_BasePdct') or
          firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_SubPdct')):
        classification_info.update({
            'icon': '🐟',
            'display_name': 'Seafood',
            'additional_info': 'Agricultural derivative'
        })
    
    # Only return if we found actual commodity classification
    base_product_found = any([
        firds_data.get(key) for key in firds_data.keys() 
        if '_BasePdct' in key and firds_data.get(key)
    ])
    
    return classification_info if base_product_found else None


def _get_swap_classification(instrument, firds_data):
    """Extract and format swap classification information from CFI code and FIRDS data like CLI"""
    try:
        cfi_code = instrument.cfi_code
        
        if not cfi_code or len(cfi_code) < 6:
            return None
        
        classification_info = {
            'icon': '🔄',
            'display_name': 'Swap',
            'additional_info': '',
            'swap_details': {}
        }
        
        # Credit Default Swaps (SCBCCA)
        if cfi_code == 'SCBCCA':
            classification_info.update({
                'icon': '💳',
                'display_name': 'Credit Default Swap',
                'additional_info': 'Credit protection derivative'
            })
        
        # Interest Rate Swaps - Standard (SRCCSP)
        elif cfi_code == 'SRCCSP':
            classification_info.update({
                'icon': '📊',
                'display_name': 'Interest Rate Swap',
                'additional_info': 'Fixed-float interest rate derivative'
            })
        
        return classification_info
    except Exception as e:
        return {
            'icon': '🔄',
            'display_name': 'Swap',
            'additional_info': f'Error in classification: {str(e)}',
            'swap_details': {}
        }


def _get_forward_classification(instrument, firds_data):
    """Extract and format forward classification information from CFI code and FIRDS data like CLI"""
    try:
        cfi_code = instrument.cfi_code
        
        if not cfi_code or len(cfi_code) < 2:
            return None
        
        classification_info = {
            'icon': '📈',
            'display_name': 'Forward',
            'additional_info': '',
            'forward_details': {}
        }
        
        # Basic forward classification based on CFI pattern
        if cfi_code.startswith('JE'):
            classification_info.update({
                'display_name': 'Equity Forward',
                'additional_info': 'Equity-based forward contract'
            })
        elif cfi_code.startswith('JF'):
            classification_info.update({
                'display_name': 'Foreign Exchange Forward',
                'additional_info': 'Currency forward contract'
            })
        
        return classification_info
    except Exception as e:
        return {
            'icon': '📈',
            'display_name': 'Forward',
            'additional_info': f'Error in classification: {str(e)}',
            'forward_details': {}
        }


def _safe_str(value):
    """Convert value to string or return None for null values."""
    return str(value) if value is not None else None


def _normalize_instrument_response(response):
    """
    Comprehensive API normalization ensuring ALL instruments have identical structure.
    
    Key principles:
    1. Every instrument gets the same exact field set
    2. FIGI fields always present (null if not enriched)  
    3. Type-specific attributes preserved without modification
    4. Consistent types for shared fields
    5. Frontend gets predictable, type-safe interface
    """
    
    # STANDARD FIELD SET - Every instrument response will have these exact fields
    # This ensures frontend TypeScript interfaces work consistently
    standard_structure = {
        # === CORE IDENTIFICATION ===
        'id': _safe_str(response.get('id')),
        'isin': _safe_str(response.get('isin')),
        'instrument_type': _safe_str(response.get('instrument_type')),
        'full_name': _safe_str(response.get('full_name')),
        'short_name': _safe_str(response.get('short_name')),
        'currency': _safe_str(response.get('currency')),
        'cfi_code': _safe_str(response.get('cfi_code')),
        
        # === BOOLEAN FIELDS (never null) ===
        'commodity_derivative_indicator': bool(response.get('commodity_derivative_indicator', False)),
        
        # === REGULATORY FIELDS (nullable) ===
        'lei_id': _safe_str(response.get('lei_id')),
        'publication_from_date': _safe_str(response.get('publication_from_date')),
        'competent_authority': _safe_str(response.get('competent_authority')),
        'relevant_trading_venue': _safe_str(response.get('relevant_trading_venue')),
        
        # === TIMESTAMPS ===
        'created_at': _safe_str(response.get('created_at')),
        'updated_at': _safe_str(response.get('updated_at')),
        
        # === BUSINESS CLASSIFICATION ===
        'firds_type': _safe_str(response.get('firds_type')),
        'business_type': _safe_str(response.get('business_type')),
        
        # === RICH RESPONSE ELEMENTS (never null) ===
        'status_indicators': response.get('status_indicators', []),
        'display_status': str(response.get('display_status', '')),
        'trading_venues_count': int(response.get('trading_venues_count', 0)),
        'trading_venues': response.get('trading_venues', []),
        
        # === PRIMARY VENUE ===
        'primary_venue_display': response.get('primary_venue_display'),
        
        # === FINANCIAL DATA ===
        'financial_data': response.get('financial_data'),
        
        # === CFI DECODING ===
        'cfi_decoded': response.get('cfi_decoded'),
        'cfi_display': _safe_str(response.get('cfi_display')),
        
        # === LEGAL ENTITY ===
        'legal_entity': response.get('legal_entity'),
        
        # === FIGI FIELDS - ALWAYS PRESENT (enrichment dependent) ===
        'figi': _safe_str(response.get('figi')),
        'composite_figi': _safe_str(response.get('composite_figi')), 
        'share_class_figi': _safe_str(response.get('share_class_figi')),
        'security_type': _safe_str(response.get('security_type')),
        'market_sector': _safe_str(response.get('market_sector')),
        'ticker': _safe_str(response.get('ticker')),
        'figi_mapping': response.get('figi_mapping'),
        'figi_mappings': response.get('figi_mappings', []),
        
        # === RICH CLASSIFICATIONS ===
        'swap_classification': response.get('swap_classification'),
        'commodity_classification': response.get('commodity_classification'),
        'forward_classification': response.get('forward_classification'),
    }
    
    
    # === TYPE-SPECIFIC ATTRIBUTES ===
    # Add all possible type-specific attribute fields (null if not applicable)
    type_specific_attributes = {
        'collective_investment_attributes': response.get('collective_investment_attributes'),
        'debt_attributes': response.get('debt_attributes'),
        'equity_attributes': response.get('equity_attributes'),
        'future_attributes': response.get('future_attributes'),
        'structured_attributes': response.get('structured_attributes'),
        'spot_attributes': response.get('spot_attributes'),
        'forward_attributes': response.get('forward_attributes'),
        'option_attributes': response.get('option_attributes'),
        'rights_attributes': response.get('rights_attributes'),
        'swap_attributes': response.get('swap_attributes'),
    }
    
    # Combine standard structure with type-specific attributes
    standard_structure.update(type_specific_attributes)
    
    return standard_structure