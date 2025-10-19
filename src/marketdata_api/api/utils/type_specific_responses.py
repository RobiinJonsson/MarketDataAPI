"""
Type-specific API response builders following CLI pattern.

This module handles all presentation logic for instrument API responses,
including normalization and type-specific formatting.
"""

from typing import Any, Dict, Optional
from datetime import datetime


def build_raw_instrument_response(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build basic normalized response from raw model data.
    Used as fallback for legacy to_api_response calls.
    """
    return normalize_base_fields(raw_data)


def build_instrument_response(instrument, include_rich_details: bool = True) -> Dict[str, Any]:
    """
    Build complete instrument response with type-specific formatting.
    
    Args:
        instrument: SQLAlchemy Instrument model instance
        include_rich_details: Whether to include enriched data
        
    Returns:
        dict: Complete normalized response with type-specific attributes
    """
    # Get raw data from model
    raw_data = instrument.to_raw_data()
    
    # Normalize base fields
    response = normalize_base_fields(raw_data)
    
    if include_rich_details:
        # Add enriched data
        response.update(_extract_rich_data(instrument, raw_data))
        
        # Add type-specific attributes based on instrument type
        response.update(_build_type_specific_attributes(instrument, raw_data))
    
    return response


def build_detailed_instrument_response(instrument) -> Dict[str, Any]:
    """
    Build detailed response for single instrument endpoint (/api/v1/instruments/{isin}).
    Includes all available data formatted for the specific instrument type.
    """
    # Get base response with rich details
    response = build_instrument_response(instrument, include_rich_details=True)
    
    # Add type-specific detailed sections
    instrument_type = instrument.instrument_type
    
    if instrument_type == "swap":
        response.update(_build_swap_detailed_response(instrument, response))
    elif instrument_type == "equity":
        response.update(_build_equity_detailed_response(instrument, response))
    elif instrument_type == "debt":
        response.update(_build_debt_detailed_response(instrument, response))
    elif instrument_type == "option":
        response.update(_build_option_detailed_response(instrument, response))
    # Add more type-specific detailed builders as needed
    
    return response


def normalize_base_fields(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize base fields to ensure consistent types across all instrument types.
    """
    # Handle datetime fields
    created_at = raw_data.get('created_at')
    updated_at = raw_data.get('updated_at') 
    publication_date = raw_data.get('publication_from_date')
    
    return {
        # Core identification - always strings or None
        "id": str(raw_data.get('id')) if raw_data.get('id') else None,
        "isin": str(raw_data.get('isin')) if raw_data.get('isin') else None,
        "instrument_type": str(raw_data.get('instrument_type')) if raw_data.get('instrument_type') else None,
        "full_name": str(raw_data.get('full_name')) if raw_data.get('full_name') else None,
        "short_name": str(raw_data.get('short_name')) if raw_data.get('short_name') else None,
        "currency": str(raw_data.get('currency')) if raw_data.get('currency') else None,
        "cfi_code": str(raw_data.get('cfi_code')) if raw_data.get('cfi_code') else None,
        
        # Boolean fields - consistent type
        "commodity_derivative_indicator": bool(raw_data.get('commodity_derivative_indicator', False)),
        
        # Optional string fields
        "lei_id": str(raw_data.get('lei_id')) if raw_data.get('lei_id') else None,
        "competent_authority": str(raw_data.get('competent_authority')) if raw_data.get('competent_authority') else None,
        "relevant_trading_venue": str(raw_data.get('relevant_trading_venue')) if raw_data.get('relevant_trading_venue') else None,
        
        # Datetime fields - ISO format or None
        "publication_from_date": publication_date.isoformat() if publication_date else None,
        "created_at": created_at.isoformat() if created_at else None,
        "updated_at": updated_at.isoformat() if updated_at else None,
        
        # Arrays - always present as empty arrays if no data
        "status_indicators": [],
        "trading_venues": [],
        "figi_mappings": [],
        
        # Counts - always integers
        "trading_venues_count": 0,
        
        # Objects - can be None or populated
        "legal_entity": None,
        "cfi_decoded": None,
        "primary_venue_display": None,
        
        # Type-specific attributes placeholder - will be populated by type builders
        # Pattern: {instrument_type}_attributes
    }


def _extract_rich_data(instrument, raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract rich data like status indicators, FIGI mappings, legal entity info."""
    rich_data = {}
    
    # Status indicators
    status_indicators = []
    if instrument.legal_entity:
        status_indicators.append("[OK] Issuer Verified")
    if instrument.figi_mappings:
        status_indicators.append("[FIGI] FIGI Mapped")
    
    rich_data["status_indicators"] = status_indicators
    rich_data["display_status"] = " • ".join(status_indicators) if status_indicators else "[WARN] Not Enriched"
    
    # Trading venues
    if instrument.trading_venues:
        rich_data["trading_venues"] = [
            {
                "venue_id": venue.venue_id,
                "mic_code": venue.mic_code,
                "first_trade_date": venue.first_trade_date.isoformat() if venue.first_trade_date else None,
                "termination_date": venue.termination_date.isoformat() if venue.termination_date else None,
                "venue_full_name": venue.venue_full_name,
                "venue_short_name": venue.venue_short_name,
            }
            for venue in instrument.trading_venues
        ]
        rich_data["trading_venues_count"] = len(instrument.trading_venues)
    
    # Legal entity info
    if instrument.legal_entity:
        rich_data["legal_entity"] = {
            "lei": instrument.legal_entity.lei,
            "name": instrument.legal_entity.name,
            "jurisdiction": instrument.legal_entity.jurisdiction,
            "legal_form": instrument.legal_entity.legal_form,
            "status": instrument.legal_entity.status,
            "creation_date": (
                instrument.legal_entity.creation_date.isoformat()
                if instrument.legal_entity.creation_date else None
            ),
        }
    
    # FIGI mappings - handle multiple FIGIs
    if instrument.figi_mappings:
        # All FIGI mappings
        rich_data["figi_mappings"] = [
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
        
        # Primary FIGI (first one) for backward compatibility
        primary_figi = instrument.figi_mappings[0]
        rich_data.update({
            "figi": primary_figi.figi,
            "composite_figi": primary_figi.composite_figi,
            "share_class_figi": primary_figi.share_class_figi,
            "security_type": primary_figi.security_type,
            "market_sector": primary_figi.market_sector,
            "ticker": primary_figi.ticker,
        })
    
    # CFI decoding
    cfi_code = raw_data.get('cfi_code')
    if cfi_code and len(cfi_code) == 6:
        try:
            from ...models.utils.cfi import CFI
            cfi = CFI(cfi_code)
            cfi_description = cfi.describe()
            rich_data["cfi_decoded"] = cfi_description
            rich_data["cfi_display"] = f"{cfi_code} ({cfi_description.get('description', 'N/A')})"
        except Exception as e:
            rich_data["cfi_decoded"] = {"error": str(e)}
            rich_data["cfi_display"] = f"{cfi_code} (decoding error)"
    
    # Primary venue display with MIC lookup
    relevant_venue = raw_data.get('relevant_trading_venue')
    if relevant_venue:
        rich_data["primary_venue_display"] = _format_primary_venue_display(relevant_venue)
    
    return rich_data


def _build_type_specific_attributes(instrument, raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Build type-specific attributes based on instrument type."""
    instrument_type = raw_data.get('instrument_type')
    if not instrument_type:
        return {}
    
    # Get cleaned processed attributes
    processed_attrs = raw_data.get('processed_attributes', {}) or {}
    firds_data = raw_data.get('firds_data', {}) or {}
    
    type_attrs = None
    
    if instrument_type == "collective_investment":
        type_attrs = _build_collective_investment_attributes(processed_attrs, firds_data)
    elif instrument_type == "debt":
        type_attrs = _build_debt_attributes(processed_attrs, firds_data)
    elif instrument_type == "equity":
        type_attrs = _build_equity_attributes(processed_attrs, firds_data)
    elif instrument_type == "future":
        type_attrs = _build_future_attributes(processed_attrs, firds_data)
    elif instrument_type == "structured":
        type_attrs = _build_structured_attributes(processed_attrs, firds_data)
    elif instrument_type == "spot":
        type_attrs = _build_spot_attributes(processed_attrs, firds_data)
    elif instrument_type == "forward":
        type_attrs = _build_forward_attributes(processed_attrs, firds_data)
    elif instrument_type == "option":
        type_attrs = _build_option_attributes(processed_attrs, firds_data)
    elif instrument_type == "rights":
        type_attrs = _build_rights_attributes(processed_attrs, firds_data)
    elif instrument_type == "swap":
        type_attrs = _build_swap_attributes(processed_attrs, firds_data)
    
    # Add type-specific attributes with standard naming
    result = {}
    if type_attrs:
        result[f"{instrument_type}_attributes"] = type_attrs
    
    return result


# Type-specific attribute builders (moved from model layer)

def _build_swap_attributes(processed_attrs: Dict, firds_data: Dict) -> Optional[Dict[str, Any]]:
    """Build swap attributes from FIRDS data."""
    if not firds_data:
        return None
    
    swap_attrs = {}
    
    # Expiration and termination dates
    if firds_data.get('DerivInstrmAttrbts_XpryDt'):
        swap_attrs["expiration_date"] = firds_data['DerivInstrmAttrbts_XpryDt']
    
    if firds_data.get('TradgVnRltdAttrbts_TermntnDt'):
        swap_attrs["termination_date"] = firds_data['TradgVnRltdAttrbts_TermntnDt']

    # Settlement/Delivery type
    if firds_data.get('DerivInstrmAttrbts_DlvryTp'):
        delivery_type = firds_data['DerivInstrmAttrbts_DlvryTp']
        swap_attrs["settlement_type"] = delivery_type
        
        # Map settlement type codes
        settlement_mapping = {
            'PHYS': 'Physical',
            'CASH': 'Cash',
            'OPTL': 'Optional'
        }
        swap_attrs["settlement_description"] = settlement_mapping.get(delivery_type, delivery_type)

    # Price multiplier
    if firds_data.get('DerivInstrmAttrbts_PricMltplr'):
        swap_attrs["price_multiplier"] = firds_data['DerivInstrmAttrbts_PricMltplr']

    # Underlying basket ISIN for credit swaps
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN'):
        swap_attrs["underlying_basket_isin"] = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN']

    # Reference rate information for interest rate swaps
    if firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx'):
        swap_attrs["reference_index"] = firds_data['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx']
    elif firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx'):
        swap_attrs["reference_index"] = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx']

    # Floating term for interest rate swaps
    term_val = firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val')
    term_unit = firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit')
    if term_val and term_unit:
        swap_attrs["floating_term"] = f"{term_val} {term_unit}"

    # Reference rate frequency for interest rate swaps
    underlying_val = firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val')
    underlying_unit = firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit')
    if underlying_val and underlying_unit:
        swap_attrs["reference_rate_frequency"] = f"{underlying_val} {underlying_unit}"

    # Fixed rate leg information
    if firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd'):
        swap_attrs["fixed_rate"] = firds_data['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd']

    # Determine swap type based on CFI code and data structure
    cfi_code = firds_data.get('FinInstrmGnlAttrbts_ClssfctnTp', '')
    if cfi_code.startswith('SC'):
        swap_attrs["swap_type"] = "Credit Default Swap"
        swap_attrs["swap_category"] = "Credit"
    elif cfi_code.startswith('SR'):
        # Interest Rate Swaps - check 3rd character for specific type
        if len(cfi_code) >= 3 and cfi_code[2] == 'H':
            swap_attrs["swap_type"] = "OIS Interest Rate Swap"
            swap_attrs["swap_category"] = "Interest Rate"
        else:
            swap_attrs["swap_type"] = "Interest Rate Swap"
            swap_attrs["swap_category"] = "Interest Rate"
    elif cfi_code.startswith('SF'):
        swap_attrs["swap_type"] = "FX Swap"
        swap_attrs["swap_category"] = "Foreign Exchange"
    elif cfi_code.startswith('SE'):
        swap_attrs["swap_type"] = "Equity Total Return Swap"
        swap_attrs["swap_category"] = "Equity"
    elif firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp'):
        swap_attrs["swap_type"] = "FX Swap"
        swap_attrs["swap_category"] = "Foreign Exchange"
    else:
        swap_attrs["swap_type"] = "Interest Rate Swap"  # Default fallback
        swap_attrs["swap_category"] = "Interest Rate"

    # Enhanced classification based on swap type
    if swap_attrs.get("swap_category") == "Interest Rate":
        # Special handling for OIS swaps
        if swap_attrs.get("swap_type") == "OIS Interest Rate Swap":
            if swap_attrs.get("reference_index") and swap_attrs.get("floating_term"):
                swap_attrs["classification"] = f"OIS {swap_attrs['floating_term']} {swap_attrs['reference_index']}"
            else:
                swap_attrs["classification"] = "Overnight Index Swap (OIS)"
        # Regular Interest Rate Swaps
        elif swap_attrs.get("reference_index") and swap_attrs.get("floating_term"):
            swap_attrs["classification"] = f"Fixed-Float {swap_attrs['floating_term']} {swap_attrs['reference_index']}"
        else:
            swap_attrs["classification"] = "Interest Rate Swap"
    elif swap_attrs.get("swap_category") == "Credit":
        if swap_attrs.get("underlying_basket_isin"):
            swap_attrs["classification"] = "Credit Default Swap - Basket"
        else:
            swap_attrs["classification"] = "Credit Default Swap - Single Name"
    elif swap_attrs.get("swap_category") == "Equity":
        if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
            swap_attrs["classification"] = "Equity Total Return Swap - Single Name"
            swap_attrs["underlying_equity_isin"] = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']
        else:
            swap_attrs["classification"] = "Equity Total Return Swap"
    elif swap_attrs.get("swap_category") == "Foreign Exchange":
        if firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp'):
            fx_type = firds_data['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp']
            if fx_type == 'FXMJ':
                swap_attrs["classification"] = "FX Major Currency Swap"
            elif fx_type == 'FXEM':
                swap_attrs["classification"] = "FX Emerging Market Swap"
            else:
                swap_attrs["classification"] = f"FX Swap ({fx_type})"
        
        # Add currency pair information
        base_currency = firds_data.get('FinInstrmGnlAttrbts_NtnlCcy')
        other_currency = firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy')
        if base_currency and other_currency:
            swap_attrs["currency_pair"] = f"{base_currency}/{other_currency}"
            if not swap_attrs.get("classification"):
                swap_attrs["classification"] = f"FX Swap {base_currency}/{other_currency}"
    else:
        swap_attrs["classification"] = swap_attrs.get("swap_type", "Swap")

    # Calculate time to maturity if available
    if swap_attrs.get("expiration_date"):
        from datetime import datetime, date
        try:
            if isinstance(swap_attrs["expiration_date"], str):
                expiry = datetime.strptime(swap_attrs["expiration_date"][:10], '%Y-%m-%d').date()
            else:
                expiry = swap_attrs["expiration_date"]
            
            today = date.today()
            if expiry > today:
                days_to_expiry = (expiry - today).days
                years_to_expiry = round(days_to_expiry / 365.25, 2)
                swap_attrs["years_to_expiry"] = years_to_expiry
                swap_attrs["days_to_expiry"] = days_to_expiry
        except (ValueError, TypeError):
            pass

    return swap_attrs if swap_attrs else None


def _build_collective_investment_attributes(processed_attrs: Dict, firds_data: Dict) -> Optional[Dict]:
    """Build collective investment attributes from FIRDS data."""
    if not firds_data:
        return None
    
    collective_attrs = {}
    
    # Fund identification and basic info
    if firds_data.get('FinInstrmGnlAttrbts_ShrtNm'):
        collective_attrs["short_name"] = firds_data['FinInstrmGnlAttrbts_ShrtNm']
        
    if firds_data.get('FinInstrmGnlAttrbts_FullNm'):
        collective_attrs["full_name"] = firds_data['FinInstrmGnlAttrbts_FullNm']
    
    # Collective investment specific attributes
    if firds_data.get('CollctdInvstmtVhclAttrbts_FndTp'):
        fund_type = firds_data['CollctdInvstmtVhclAttrbts_FndTp']
        collective_attrs["fund_type_code"] = fund_type
        
        # Map fund type codes to descriptions
        fund_type_mapping = {
            'ETFS': 'Exchange Traded Fund',
            'REIT': 'Real Estate Investment Trust',
            'MMFR': 'Money Market Fund',
            'UCIT': 'UCITS Fund',
            'HEDG': 'Hedge Fund',
            'PENS': 'Pension Fund',
            'SOVW': 'Sovereign Wealth Fund',
            'INVT': 'Investment Trust',
            'MUTU': 'Mutual Fund',
            'VARI': 'Variable Fund'
        }
        collective_attrs["fund_type"] = fund_type_mapping.get(fund_type, fund_type)
    
    # Investment strategy and focus
    if firds_data.get('CollctdInvstmtVhclAttrbts_StrgyTp'):
        strategy_type = firds_data['CollctdInvstmtVhclAttrbts_StrgyTp']
        collective_attrs["strategy_type"] = strategy_type
        
        # Map strategy codes
        strategy_mapping = {
            'BLND': 'Balanced/Mixed',
            'EQUI': 'Equity Focused',
            'BOND': 'Bond/Fixed Income',
            'MMON': 'Money Market',
            'REAL': 'Real Estate',
            'COMM': 'Commodities',
            'ABSO': 'Absolute Return',
            'EMER': 'Emerging Markets',
            'GLOB': 'Global',
            'REGI': 'Regional'
        }
        collective_attrs["strategy_description"] = strategy_mapping.get(strategy_type, strategy_type)
    
    # Distribution information
    if firds_data.get('CollctdInvstmtVhclAttrbts_DstrbnPlcy'):
        distribution_policy = firds_data['CollctdInvstmtVhclAttrbts_DstrbnPlcy']
        collective_attrs["distribution_policy"] = distribution_policy
        
        policy_mapping = {
            'DIST': 'Distributing',
            'ACCU': 'Accumulating',
            'BOTH': 'Mixed'
        }
        collective_attrs["distribution_type"] = policy_mapping.get(distribution_policy, distribution_policy)
    
    # Currency hedge information
    if firds_data.get('CollctdInvstmtVhclAttrbts_BaseCcyHdgd'):
        collective_attrs["base_currency_hedged"] = firds_data['CollctdInvstmtVhclAttrbts_BaseCcyHdgd'] == "true"
    
    # Investment focus region/market
    if firds_data.get('CollctdInvstmtVhclAttrbts_GeoFcs'):
        collective_attrs["geographic_focus"] = firds_data['CollctdInvstmtVhclAttrbts_GeoFcs']
    
    # Determine fund category based on attributes
    fund_category = "Investment Fund"  # Default
    
    if collective_attrs.get("fund_type_code") == "ETFS":
        fund_category = "Exchange Traded Fund"
        
        # Further categorize ETFs by strategy
        if collective_attrs.get("strategy_type") == "EQUI":
            fund_category = "Equity ETF"
        elif collective_attrs.get("strategy_type") == "BOND":
            fund_category = "Bond ETF"
        elif collective_attrs.get("strategy_type") == "COMM":
            fund_category = "Commodity ETF"
        elif collective_attrs.get("strategy_type") == "REAL":
            fund_category = "Real Estate ETF"
    
    elif collective_attrs.get("fund_type_code") == "REIT":
        fund_category = "Real Estate Investment Trust"
        
    elif collective_attrs.get("fund_type_code") == "MMFR":
        fund_category = "Money Market Fund"
        
    elif collective_attrs.get("strategy_type") == "HEDG":
        fund_category = "Hedge Fund"
    
    collective_attrs["fund_category"] = fund_category
    
    # Build descriptive summary
    description_parts = [collective_attrs.get("fund_category", "Fund")]
    
    if collective_attrs.get("strategy_description"):
        description_parts.append(collective_attrs["strategy_description"])
        
    if collective_attrs.get("distribution_type"):
        description_parts.append(collective_attrs["distribution_type"])
        
    if collective_attrs.get("base_currency_hedged"):
        description_parts.append("Currency Hedged")
        
    if collective_attrs.get("geographic_focus"):
        description_parts.append(f"Focus: {collective_attrs['geographic_focus']}")
    
    collective_attrs["fund_description"] = " | ".join(description_parts)
    
    return collective_attrs if collective_attrs else None


def _build_debt_attributes(processed_attrs: Dict, firds_data: Dict) -> Optional[Dict]:
    """Build debt instrument attributes from FIRDS data."""
    if not firds_data:
        return None
    
    debt_attrs = {}
    
    # Maturity information
    if firds_data.get('DebtInstrmAttrbts_MtrtyDt'):
        debt_attrs["maturity_date"] = firds_data['DebtInstrmAttrbts_MtrtyDt']
        
    if firds_data.get('DebtInstrmAttrbts_PrncplAmnt'):
        debt_attrs["principal_amount"] = firds_data['DebtInstrmAttrbts_PrncplAmnt']
        
    if firds_data.get('DebtInstrmAttrbts_PrncplAmntCcy'):
        debt_attrs["principal_currency"] = firds_data['DebtInstrmAttrbts_PrncplAmntCcy']
    
    # Interest rate and coupon information - CRITICAL debt fields
    if firds_data.get('DebtInstrmAttrbts_IntrstRate_Fxd'):
        debt_attrs["fixed_interest_rate"] = float(firds_data['DebtInstrmAttrbts_IntrstRate_Fxd'])
        debt_attrs["interest_rate"] = float(firds_data['DebtInstrmAttrbts_IntrstRate_Fxd'])  # For backward compatibility
        debt_attrs["interest_rate_type"] = "Fixed"
        
    # Floating rate information
    if firds_data.get('DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx'):
        debt_attrs["floating_rate_index"] = firds_data['DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx']
        debt_attrs["interest_rate_type"] = "Floating"
        
    if firds_data.get('DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd'):
        debt_attrs["floating_rate_spread"] = firds_data['DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd']
        
    # Nominal amount and issuance information
    if firds_data.get('DebtInstrmAttrbts_NmnlValPerUnit'):
        debt_attrs["nominal_value_per_unit"] = int(firds_data['DebtInstrmAttrbts_NmnlValPerUnit'])
        
    if firds_data.get('DebtInstrmAttrbts_TtlIssdNmnlAmt'):
        debt_attrs["total_issued_nominal_amount"] = int(firds_data['DebtInstrmAttrbts_TtlIssdNmnlAmt'])
        
    # Debt seniority - CRITICAL for credit analysis  
    if firds_data.get('DebtInstrmAttrbts_DebtSnrty'):
        seniority_code = firds_data['DebtInstrmAttrbts_DebtSnrty']
        debt_attrs["seniority_code"] = seniority_code
        
        # Map seniority codes to descriptions
        seniority_mapping = {
            'SNDB': 'Senior',
            'SBOD': 'Senior Subordinated', 
            'JUND': 'Junior',
            'OTHR': 'Other'
        }
        debt_attrs["seniority"] = seniority_mapping.get(seniority_code, seniority_code)
        
    # Legacy field handling for backward compatibility
    if firds_data.get('DebtInstrmAttrbts_IntrstRate'):
        debt_attrs["legacy_interest_rate"] = firds_data['DebtInstrmAttrbts_IntrstRate']
        
    if firds_data.get('DebtInstrmAttrbts_IntrstRateInd'):
        debt_attrs["interest_rate_indicator"] = firds_data['DebtInstrmAttrbts_IntrstRateInd']
    
    # Bond specific attributes
    if firds_data.get('DebtInstrmAttrbts_AssetClssSpcfcAttrbts_Bond_IntrstAccrlDt'):
        debt_attrs["interest_accrual_date"] = firds_data['DebtInstrmAttrbts_AssetClssSpcfcAttrbts_Bond_IntrstAccrlDt']
        
    if firds_data.get('DebtInstrmAttrbts_AssetClssSpcfcAttrbts_Bond_TotalIssdNmnlAmnt'):
        debt_attrs["total_issued_amount"] = firds_data['DebtInstrmAttrbts_AssetClssSpcfcAttrbts_Bond_TotalIssdNmnlAmnt']
        
    if firds_data.get('DebtInstrmAttrbts_AssetClssSpcfcAttrbts_Bond_MtrtyDt'):
        debt_attrs["bond_maturity_date"] = firds_data['DebtInstrmAttrbts_AssetClssSpcfcAttrbts_Bond_MtrtyDt']
    
    # Convertible bond attributes
    if firds_data.get('DebtInstrmAttrbts_CnvrtblInd'):
        debt_attrs["convertible_indicator"] = firds_data['DebtInstrmAttrbts_CnvrtblInd']
        
        if debt_attrs["convertible_indicator"] == "true":
            debt_attrs["is_convertible"] = True
            if firds_data.get('DebtInstrmAttrbts_CnvrsRatio'):
                debt_attrs["conversion_ratio"] = firds_data['DebtInstrmAttrbts_CnvrsRatio']
        else:
            debt_attrs["is_convertible"] = False
    
    # Security type and classification
    if firds_data.get('FinInstrmGnlAttrbts_ShrtNm'):
        debt_attrs["short_name"] = firds_data['FinInstrmGnlAttrbts_ShrtNm']
        
    # Determine debt instrument type based on available data
    debt_type = "Corporate Bond"  # Default
    
    if debt_attrs.get("is_convertible"):
        debt_type = "Convertible Bond"
    elif debt_attrs.get("interest_rate_type") == "Floating":
        debt_type = "Floating Rate Note"
    elif not debt_attrs.get("fixed_interest_rate") and not debt_attrs.get("floating_rate_index"):
        debt_type = "Zero Coupon Bond"
    elif firds_data.get('FinInstrmGnlAttrbts_ShrtNm'):
        short_name = firds_data['FinInstrmGnlAttrbts_ShrtNm'].upper()
        if any(term in short_name for term in ['GOVERNMENT', 'TREASURY', 'SOVEREIGN']):
            debt_type = "Government Bond"
        elif any(term in short_name for term in ['MUNICIPAL', 'MUNI']):
            debt_type = "Municipal Bond"
        elif any(term in short_name for term in ['COVERED', 'PFANDBRIEF', 'MORTG']):
            debt_type = "Covered Bond"
        elif any(term in short_name for term in ['MTN', 'EMTN', 'NOTE', 'FRN']):
            debt_type = "Medium Term Note"
    
    debt_attrs["debt_type"] = debt_type
    
    # Calculate time to maturity if maturity date available
    if debt_attrs.get("maturity_date"):
        from datetime import datetime, date
        try:
            if isinstance(debt_attrs["maturity_date"], str):
                maturity = datetime.strptime(debt_attrs["maturity_date"][:10], '%Y-%m-%d').date()
            else:
                maturity = debt_attrs["maturity_date"]
            
            today = date.today()
            if maturity > today:
                days_to_maturity = (maturity - today).days
                years_to_maturity = round(days_to_maturity / 365.25, 2)
                debt_attrs["years_to_maturity"] = years_to_maturity
                debt_attrs["days_to_maturity"] = days_to_maturity
        except (ValueError, TypeError):
            pass
    
    # Build debt description
    if debt_attrs.get("debt_type") and debt_attrs.get("interest_rate"):
        rate_str = f"{debt_attrs['interest_rate']}%"
        maturity_str = ""
        if debt_attrs.get("maturity_date"):
            maturity_str = f" due {debt_attrs['maturity_date'][:10]}"
        currency_str = ""
        if debt_attrs.get("principal_currency"):
            currency_str = f" ({debt_attrs['principal_currency']})"
        
        debt_attrs["instrument_description"] = f"{debt_attrs['debt_type']} {rate_str}{maturity_str}{currency_str}"
    
    return debt_attrs if debt_attrs else None


def _build_equity_attributes(processed_attrs: Dict, firds_data: Dict) -> Optional[Dict]:
    """Build equity instrument attributes from FIRDS data."""
    if not firds_data:
        return None
    
    equity_attrs = {}
    
    # Equity specific attributes
    if firds_data.get('EqtyInstrmAttrbts_DvddRate'):
        equity_attrs["dividend_rate"] = firds_data['EqtyInstrmAttrbts_DvddRate']
        
    if firds_data.get('EqtyInstrmAttrbts_DvddRateCcy'):
        equity_attrs["dividend_currency"] = firds_data['EqtyInstrmAttrbts_DvddRateCcy']
        
    if firds_data.get('EqtyInstrmAttrbts_DvddTp'):
        dividend_type = firds_data['EqtyInstrmAttrbts_DvddTp']
        equity_attrs["dividend_type"] = dividend_type
        
        # Map dividend type codes
        dividend_type_mapping = {
            'FIXD': 'Fixed Dividend',
            'VARI': 'Variable Dividend',
            'NONE': 'No Dividend',
            'PREF': 'Preferred Dividend'
        }
        equity_attrs["dividend_type_description"] = dividend_type_mapping.get(dividend_type, dividend_type)
    
    # Voting rights
    if firds_data.get('EqtyInstrmAttrbts_VtngRghtsPerShr'):
        equity_attrs["voting_rights_per_share"] = firds_data['EqtyInstrmAttrbts_VtngRghtsPerShr']
        
    # Rights and entitlements
    if firds_data.get('EqtyInstrmAttrbts_RghtsAttchd'):
        equity_attrs["rights_attached"] = firds_data['EqtyInstrmAttrbts_RghtsAttchd']
    
    # Share class information
    if firds_data.get('FinInstrmGnlAttrbts_ShrtNm'):
        equity_attrs["short_name"] = firds_data['FinInstrmGnlAttrbts_ShrtNm']
        
    if firds_data.get('FinInstrmGnlAttrbts_ClssfctnTp'):
        equity_attrs["classification_type"] = firds_data['FinInstrmGnlAttrbts_ClssfctnTp']
    
    # Additional equity identifiers
    if firds_data.get('FinInstrmGnlAttrbts_Id'):
        equity_attrs["instrument_id"] = firds_data['FinInstrmGnlAttrbts_Id']
    
    # Determine equity type based on available attributes
    equity_type = "Common Share"  # Default
    
    if equity_attrs.get("dividend_type") == "PREF":
        equity_type = "Preferred Share"
    elif equity_attrs.get("voting_rights_per_share") == "0":
        equity_type = "Non-Voting Share"
    elif equity_attrs.get("rights_attached"):
        if "WARRANT" in equity_attrs["rights_attached"].upper():
            equity_type = "Share with Warrants"
        elif "RIGHT" in equity_attrs["rights_attached"].upper():
            equity_type = "Share with Rights"
    elif firds_data.get('FinInstrmGnlAttrbts_ShrtNm'):
        short_name = firds_data['FinInstrmGnlAttrbts_ShrtNm'].upper()
        if any(term in short_name for term in ['ETF', 'FUND', 'INDEX']):
            equity_type = "Exchange Traded Fund"
        elif "REIT" in short_name:
            equity_type = "Real Estate Investment Trust"
        elif "PREF" in short_name or "PREFERRED" in short_name:
            equity_type = "Preferred Share"
        elif any(term in short_name for term in ['A', 'B', 'C']) and "CLASS" in short_name:
            equity_type = f"Class {short_name.split('CLASS')[1].strip()[:1]} Share"
    
    equity_attrs["equity_type"] = equity_type
    
    # Determine if share has enhanced rights
    has_enhanced_rights = False
    enhanced_rights_details = []
    
    if equity_attrs.get("voting_rights_per_share") and float(equity_attrs["voting_rights_per_share"]) > 1:
        has_enhanced_rights = True
        enhanced_rights_details.append("Multiple voting rights")
        
    if equity_attrs.get("dividend_type") == "PREF":
        has_enhanced_rights = True
        enhanced_rights_details.append("Preferred dividend rights")
        
    if equity_attrs.get("rights_attached"):
        has_enhanced_rights = True
        enhanced_rights_details.append("Additional rights attached")
    
    equity_attrs["has_enhanced_rights"] = has_enhanced_rights
    if enhanced_rights_details:
        equity_attrs["enhanced_rights_details"] = enhanced_rights_details
    
    # Calculate dividend yield if both rate and currency are available
    if equity_attrs.get("dividend_rate") and equity_attrs.get("dividend_currency"):
        try:
            dividend_rate = float(equity_attrs["dividend_rate"])
            if dividend_rate > 0:
                equity_attrs["annual_dividend_rate"] = dividend_rate
        except (ValueError, TypeError):
            pass
    
    # Build equity description
    description_parts = [equity_attrs.get("equity_type", "Equity")]
    
    if equity_attrs.get("dividend_rate") and float(equity_attrs["dividend_rate"]) > 0:
        div_str = f"{equity_attrs['dividend_rate']}"
        if equity_attrs.get("dividend_currency"):
            div_str = f"{equity_attrs['dividend_currency']} {div_str}"
        description_parts.append(f"Dividend: {div_str}")
    
    if equity_attrs.get("voting_rights_per_share"):
        voting_str = f"{equity_attrs['voting_rights_per_share']} vote(s) per share"
        description_parts.append(voting_str)
    
    equity_attrs["instrument_description"] = " | ".join(description_parts)
    
    return equity_attrs if equity_attrs else None


def _build_future_attributes(processed_attrs: Dict, firds_data: Dict) -> Optional[Dict]:
    """Build future contract attributes from FIRDS data."""
    if not firds_data:
        return None
    
    future_attrs = {}
    
    # Contract expiration and dates
    if firds_data.get('DerivInstrmAttrbts_XpryDt'):
        future_attrs["expiration_date"] = firds_data['DerivInstrmAttrbts_XpryDt']
    
    if firds_data.get('TradgVnRltdAttrbts_TermntnDt'):
        future_attrs["termination_date"] = firds_data['TradgVnRltdAttrbts_TermntnDt']
        
    if firds_data.get('TradgVnRltdAttrbts_FrstTradDt'):
        future_attrs["first_trade_date"] = firds_data['TradgVnRltdAttrbts_FrstTradDt']
    
    # Contract specifications
    if firds_data.get('DerivInstrmAttrbts_PricMltplr'):
        future_attrs["price_multiplier"] = firds_data['DerivInstrmAttrbts_PricMltplr']
        
    if firds_data.get('DerivInstrmAttrbts_DlvryTp'):
        future_attrs["delivery_type"] = firds_data['DerivInstrmAttrbts_DlvryTp']
    
    # Underlying asset information - CRITICAL for derivatives
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
        future_attrs["underlying_isin"] = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']
        
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm'):
        future_attrs["underlying_name"] = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm']
        
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Id'):
        future_attrs["underlying_id"] = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Id']
        
    # Also check processed attributes as backup source for underlying ISIN
    if not future_attrs.get("underlying_isin") and processed_attrs.get('underlying_isin'):
        future_attrs["underlying_isin"] = processed_attrs['underlying_isin']
    
    # Contract size and units
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit'):
        future_attrs["contract_unit"] = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit']
        
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val'):
        future_attrs["contract_value"] = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val']
    
    # Commodity derivative indicator
    if firds_data.get('FinInstrmGnlAttrbts_CmmdtyDerivInd'):
        future_attrs["commodity_derivative"] = firds_data['FinInstrmGnlAttrbts_CmmdtyDerivInd']
    
    # Determine contract type based on available data
    contract_type = "Future"
    if future_attrs.get("commodity_derivative"):
        contract_type = "Commodity Future"
    elif firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm'):
        underlying = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm']
        if any(term in underlying.upper() for term in ['EQUITY', 'STOCK', 'INDEX']):
            contract_type = "Equity Future"
        elif any(term in underlying.upper() for term in ['BOND', 'RATE', 'INTEREST']):
            contract_type = "Financial Future"
    
    future_attrs["contract_type"] = contract_type
    
    # Build contract description
    if future_attrs.get("underlying_name") and future_attrs.get("expiration_date"):
        expiry_str = future_attrs["expiration_date"][:10] if future_attrs["expiration_date"] else "TBD"
        future_attrs["contract_description"] = f"{contract_type} on {future_attrs['underlying_name']} expiring {expiry_str}"
    
    return future_attrs if future_attrs else None


def _build_structured_attributes(processed_attrs: Dict, firds_data: Dict) -> Optional[Dict]:
    """Build structured product attributes from FIRDS data."""
    if not firds_data:
        return None
    
    structured_attrs = {}
    
    # Basic product information
    if firds_data.get('FinInstrmGnlAttrbts_ShrtNm'):
        structured_attrs["short_name"] = firds_data['FinInstrmGnlAttrbts_ShrtNm']
        
    if firds_data.get('FinInstrmGnlAttrbts_FullNm'):
        structured_attrs["full_name"] = firds_data['FinInstrmGnlAttrbts_FullNm']
    
    # Maturity and term information
    if firds_data.get('StrctrdPdctAttrbts_MtrtyDt'):
        structured_attrs["maturity_date"] = firds_data['StrctrdPdctAttrbts_MtrtyDt']
        
    if firds_data.get('TradgVnRltdAttrbts_TermntnDt'):
        structured_attrs["termination_date"] = firds_data['TradgVnRltdAttrbts_TermntnDt']
        
    if firds_data.get('TradgVnRltdAttrbts_FrstTradDt'):
        structured_attrs["first_trade_date"] = firds_data['TradgVnRltdAttrbts_FrstTradDt']
    
    # Capital protection features
    if firds_data.get('StrctrdPdctAttrbts_CptlPrtctn'):
        protection_level = firds_data['StrctrdPdctAttrbts_CptlPrtctn']
        structured_attrs["capital_protection_level"] = protection_level
        
        # Determine protection type
        try:
            protection_pct = float(protection_level)
            if protection_pct >= 100:
                structured_attrs["protection_type"] = "Full Capital Protection"
            elif protection_pct >= 90:
                structured_attrs["protection_type"] = "High Capital Protection"
            elif protection_pct >= 50:
                structured_attrs["protection_type"] = "Partial Capital Protection"
            elif protection_pct > 0:
                structured_attrs["protection_type"] = "Limited Capital Protection"
            else:
                structured_attrs["protection_type"] = "No Capital Protection"
        except (ValueError, TypeError):
            structured_attrs["protection_type"] = "Capital Protection Level Unknown"
    
    # Participation features
    if firds_data.get('StrctrdPdctAttrbts_PrtcptnRate'):
        structured_attrs["participation_rate"] = firds_data['StrctrdPdctAttrbts_PrtcptnRate']
        
    if firds_data.get('StrctrdPdctAttrbts_RtrrnPymnt'):
        structured_attrs["return_payment"] = firds_data['StrctrdPdctAttrbts_RtrrnPymnt']
    
    # Barrier features
    if firds_data.get('StrctrdPdctAttrbts_BrrierLvl'):
        structured_attrs["barrier_level"] = firds_data['StrctrdPdctAttrbts_BrrierLvl']
        
    if firds_data.get('StrctrdPdctAttrbts_BrrierTp'):
        barrier_type = firds_data['StrctrdPdctAttrbts_BrrierTp']
        structured_attrs["barrier_type"] = barrier_type
        
        # Map barrier types
        barrier_mapping = {
            'KNIN': 'Knock-In Barrier',
            'KNOU': 'Knock-Out Barrier',
            'UPAN': 'Up-and-In Barrier',
            'UPAO': 'Up-and-Out Barrier',
            'DWAI': 'Down-and-In Barrier',
            'DWAO': 'Down-and-Out Barrier'
        }
        structured_attrs["barrier_description"] = barrier_mapping.get(barrier_type, barrier_type)
    
    # Underlying asset information
    if firds_data.get('StrctrdPdctAttrbts_UndrlygAsstTp'):
        underlying_type = firds_data['StrctrdPdctAttrbts_UndrlygAsstTp']
        structured_attrs["underlying_asset_type"] = underlying_type
        
        # Map underlying asset types
        underlying_mapping = {
            'EQUI': 'Equity',
            'BOND': 'Bond',
            'CURR': 'Currency',
            'COMM': 'Commodity',
            'INDX': 'Index',
            'BASP': 'Basket',
            'INTR': 'Interest Rate'
        }
        structured_attrs["underlying_description"] = underlying_mapping.get(underlying_type, underlying_type)
    
    # Determine structured product type
    product_type = "Structured Product"  # Default
    
    # Classify based on protection and participation features
    has_protection = structured_attrs.get("capital_protection_level") and float(structured_attrs.get("capital_protection_level", 0)) > 0
    has_participation = structured_attrs.get("participation_rate")
    has_barriers = structured_attrs.get("barrier_level")
    
    if has_protection and has_participation:
        if has_barriers:
            product_type = "Barrier Reverse Convertible"
        else:
            product_type = "Capital Protected Note"
    elif has_barriers:
        product_type = "Barrier Certificate"
    elif has_participation:
        product_type = "Participation Certificate"
    elif structured_attrs.get("underlying_description") == "Index":
        product_type = "Index Certificate"
    elif structured_attrs.get("underlying_description") == "Basket":
        product_type = "Basket Certificate"
    
    # Further classification based on short name patterns
    if structured_attrs.get("short_name"):
        short_name = structured_attrs["short_name"].upper()
        if "AUTOCALL" in short_name:
            product_type = "Autocallable Note"
        elif "REVERSE" in short_name and "CONVERTIBLE" in short_name:
            product_type = "Reverse Convertible Note"
        elif "TRACKER" in short_name:
            product_type = "Tracker Certificate"
        elif "BONUS" in short_name:
            product_type = "Bonus Certificate"
    
    structured_attrs["product_type"] = product_type
    
    # Calculate time to maturity
    if structured_attrs.get("maturity_date"):
        from datetime import datetime, date
        try:
            if isinstance(structured_attrs["maturity_date"], str):
                maturity = datetime.strptime(structured_attrs["maturity_date"][:10], '%Y-%m-%d').date()
            else:
                maturity = structured_attrs["maturity_date"]
            
            today = date.today()
            if maturity > today:
                days_to_maturity = (maturity - today).days
                years_to_maturity = round(days_to_maturity / 365.25, 2)
                structured_attrs["years_to_maturity"] = years_to_maturity
                structured_attrs["days_to_maturity"] = days_to_maturity
        except (ValueError, TypeError):
            pass
    
    # Build product description
    description_parts = [structured_attrs.get("product_type", "Structured Product")]
    
    if structured_attrs.get("protection_type") and "No Capital Protection" not in structured_attrs["protection_type"]:
        description_parts.append(structured_attrs["protection_type"])
        
    if structured_attrs.get("underlying_description"):
        description_parts.append(f"on {structured_attrs['underlying_description']}")
        
    if structured_attrs.get("maturity_date"):
        maturity_str = structured_attrs["maturity_date"][:10] if structured_attrs["maturity_date"] else "TBD"
        description_parts.append(f"due {maturity_str}")
    
    structured_attrs["product_description"] = " | ".join(description_parts)
    
    return structured_attrs if structured_attrs else None


def _build_spot_attributes(processed_attrs: Dict, firds_data: Dict) -> Optional[Dict]:
    """Build spot instrument attributes from FIRDS data."""
    if not firds_data:
        return None
    
    spot_attrs = {}
    
    # Basic spot information
    if firds_data.get('FinInstrmGnlAttrbts_ShrtNm'):
        spot_attrs["short_name"] = firds_data['FinInstrmGnlAttrbts_ShrtNm']
        
    if firds_data.get('FinInstrmGnlAttrbts_NtnlCcy'):
        spot_attrs["base_currency"] = firds_data['FinInstrmGnlAttrbts_NtnlCcy']
    
    # Spot-specific attributes (currency pairs, commodities, etc.)
    if firds_data.get('SpotInstrmAttrbts_CurrPair'):
        currency_pair = firds_data['SpotInstrmAttrbts_CurrPair']
        spot_attrs["currency_pair"] = currency_pair
        
        # Extract base and quote currencies
        if len(currency_pair) == 6:  # Standard format like EURUSD
            spot_attrs["base_currency"] = currency_pair[:3]
            spot_attrs["quote_currency"] = currency_pair[3:]
        elif '/' in currency_pair:  # Format like EUR/USD
            parts = currency_pair.split('/')
            if len(parts) == 2:
                spot_attrs["base_currency"] = parts[0].strip()
                spot_attrs["quote_currency"] = parts[1].strip()
    
    # Commodity information
    if firds_data.get('SpotInstrmAttrbts_CmmdtyTp'):
        commodity_type = firds_data['SpotInstrmAttrbts_CmmdtyTp']
        spot_attrs["commodity_type"] = commodity_type
        
        # Map commodity types
        commodity_mapping = {
            'AGRI': 'Agricultural',
            'NRGY': 'Energy', 
            'METL': 'Metals',
            'PREC': 'Precious Metals',
            'BASE': 'Base Metals',
            'SOFT': 'Soft Commodities'
        }
        spot_attrs["commodity_category"] = commodity_mapping.get(commodity_type, commodity_type)
    
    # Trading venue and settlement info
    if firds_data.get('TradgVnRltdAttrbts_Id'):
        spot_attrs["trading_venue"] = firds_data['TradgVnRltdAttrbts_Id']
        
    if firds_data.get('SpotInstrmAttrbts_SttlmDt'):
        spot_attrs["settlement_date"] = firds_data['SpotInstrmAttrbts_SttlmDt']
        
    if firds_data.get('SpotInstrmAttrbts_SttlmTp'):
        settlement_type = firds_data['SpotInstrmAttrbts_SttlmTp']
        spot_attrs["settlement_type"] = settlement_type
        
        # Map settlement types
        settlement_mapping = {
            'T0': 'Same Day Settlement',
            'T1': 'Next Day Settlement', 
            'T2': 'T+2 Settlement',
            'T3': 'T+3 Settlement',
            'CASH': 'Cash Settlement',
            'PHYS': 'Physical Delivery'
        }
        spot_attrs["settlement_description"] = settlement_mapping.get(settlement_type, settlement_type)
    
    # Determine spot instrument type
    spot_type = "Spot"  # Default
    
    if spot_attrs.get("currency_pair"):
        spot_type = "FX Spot"
    elif spot_attrs.get("commodity_type"):
        commodity_cat = spot_attrs.get("commodity_category", "")
        if "Energy" in commodity_cat:
            spot_type = "Energy Spot"
        elif "Metal" in commodity_cat:
            spot_type = "Metals Spot" 
        elif "Agricultural" in commodity_cat:
            spot_type = "Agricultural Spot"
        else:
            spot_type = "Commodity Spot"
    elif firds_data.get('FinInstrmGnlAttrbts_ShrtNm'):
        short_name = firds_data['FinInstrmGnlAttrbts_ShrtNm'].upper()
        if any(term in short_name for term in ['GOLD', 'SILVER', 'PLATINUM']):
            spot_type = "Precious Metals Spot"
        elif any(term in short_name for term in ['OIL', 'GAS', 'BRENT']):
            spot_type = "Energy Spot"
    
    spot_attrs["spot_type"] = spot_type
    
    # Build description
    description_parts = [spot_attrs.get("spot_type", "Spot")]
    
    if spot_attrs.get("currency_pair"):
        description_parts.append(f"({spot_attrs['currency_pair']})")
    elif spot_attrs.get("commodity_category"):
        description_parts.append(f"- {spot_attrs['commodity_category']}")
        
    if spot_attrs.get("settlement_description"):
        description_parts.append(spot_attrs["settlement_description"])
    
    spot_attrs["instrument_description"] = " ".join(description_parts)
    
    return spot_attrs if spot_attrs else None


def _build_forward_attributes(processed_attrs: Dict, firds_data: Dict) -> Optional[Dict]:
    """Build forward contract attributes from FIRDS data."""
    if not firds_data:
        return None
    
    forward_attrs = {}
    
    # Expiration/Maturity date (using derivative structure)
    if firds_data.get('DerivInstrmAttrbts_XpryDt'):
        forward_attrs["expiration_date"] = firds_data['DerivInstrmAttrbts_XpryDt']
        
    # Settlement/termination date 
    if firds_data.get('TradgVnRltdAttrbts_TermntnDt'):
        forward_attrs["termination_date"] = firds_data['TradgVnRltdAttrbts_TermntnDt']
        
    if firds_data.get('TradgVnRltdAttrbts_FrstTradDt'):
        forward_attrs["first_trade_date"] = firds_data['TradgVnRltdAttrbts_FrstTradDt']
    
    # Settlement type and description
    if firds_data.get('DerivInstrmAttrbts_DlvryTp'):
        settlement_type = firds_data['DerivInstrmAttrbts_DlvryTp']
        forward_attrs["settlement_type"] = settlement_type
        
        # Map settlement types
        settlement_mapping = {
            'CASH': 'Cash Settlement',
            'PHYS': 'Physical Delivery',
            'NETC': 'Net Cash Settlement',
            'NETS': 'Net Share Settlement',
            'OPTL': 'Optional Settlement'
        }
        forward_attrs["settlement_description"] = settlement_mapping.get(settlement_type, settlement_type)

    # Price multiplier
    if firds_data.get('DerivInstrmAttrbts_PricMltplr'):
        forward_attrs["price_multiplier"] = firds_data['DerivInstrmAttrbts_PricMltplr']

    # Underlying asset information
    underlying_details = []
    
    # Single underlying ISIN
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
        underlying_isin = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']
        forward_attrs["underlying_isin"] = underlying_isin
        underlying_details.append(f"Single: {underlying_isin}")
    
    # Basket underlying ISIN(s)
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN'):
        basket_isins = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN']
        if isinstance(basket_isins, list) and len(basket_isins) > 0:
            forward_attrs["basket_isins"] = basket_isins
            forward_attrs["basket_size"] = len(basket_isins)
            underlying_details.append(f"Basket ({len(basket_isins)} assets)")
        elif isinstance(basket_isins, str):
            forward_attrs["basket_isin"] = basket_isins
            underlying_details.append(f"Basket: {basket_isins}")
    
    # Index information
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN'):
        index_isin = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN']
        forward_attrs["index_isin"] = index_isin
        underlying_details.append(f"Index: {index_isin}")
    
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm'):
        index_name = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm']
        forward_attrs["index_name"] = index_name
        underlying_details.append(f"Index: {index_name}")
    
    if underlying_details:
        forward_attrs["underlying_summary"] = " | ".join(underlying_details)

    # FX-specific information
    if firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp'):
        forward_attrs["fx_type"] = firds_data['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp']
    
    if firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy'):
        other_currency = firds_data['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy']
        base_currency = firds_data.get('FinInstrmGnlAttrbts_NtnlCcy')
        forward_attrs["other_currency"] = other_currency
        if base_currency:
            forward_attrs["currency_pair"] = f"{base_currency}/{other_currency}"

    # Interest rate information
    if firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm'):
        forward_attrs["reference_rate"] = firds_data['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm']
    
    if firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val') and firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit'):
        term_val = firds_data['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val']
        term_unit = firds_data['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit']
        forward_attrs["interest_term"] = f"{term_val} {term_unit}"

    # Determine forward contract type based on CFI code and data
    cfi_code = firds_data.get('FinInstrmGnlAttrbts_ClssfctnTp', '')
    forward_type = "Forward Contract"  # Default
    classification = "Forward Contract"
    
    if len(cfi_code) >= 2:
        second_char = cfi_code[1]  # Group character
        
        # Equity Forwards (JE****)
        if second_char == 'E':
            forward_type = "Equity Forward"
            if forward_attrs.get("basket_size"):
                classification = f"Equity Basket Forward ({forward_attrs['basket_size']} assets)"
            elif forward_attrs.get("underlying_isin"):
                classification = "Equity Forward - Single Name"
            else:
                classification = "Equity Forward"
        
        # Foreign Exchange Forwards (JF****)
        elif second_char == 'F':
            forward_type = "FX Forward"
            if forward_attrs.get("currency_pair"):
                classification = f"FX Forward {forward_attrs['currency_pair']}"
            elif forward_attrs.get("fx_type"):
                fx_type = forward_attrs["fx_type"]
                if fx_type == 'FXCR':
                    classification = "Non-Deliverable Forward (NDF)"
                elif fx_type == 'FXMJ':
                    classification = "FX Major Currency Forward"
                else:
                    classification = f"FX Forward ({fx_type})"
            else:
                classification = "FX Forward"
        
        # Rate Forwards (JR****)
        elif second_char == 'R':
            forward_type = "Interest Rate Forward"
            if forward_attrs.get("reference_rate"):
                classification = f"Forward Rate Agreement ({forward_attrs['reference_rate']})"
            else:
                classification = "Interest Rate Forward"
        
        # Commodity Forwards (JC****)
        elif second_char == 'C':
            forward_type = "Commodity Forward"
            classification = "Commodity Forward"
    
    forward_attrs["forward_type"] = forward_type
    forward_attrs["classification"] = classification
    forward_attrs["contract_description"] = classification
    
    # Calculate time to maturity if available
    if forward_attrs.get("expiration_date"):
        from datetime import datetime, date
        try:
            if isinstance(forward_attrs["expiration_date"], str):
                expiry = datetime.strptime(forward_attrs["expiration_date"][:10], '%Y-%m-%d').date()
            else:
                expiry = forward_attrs["expiration_date"]
            
            today = date.today()
            if expiry > today:
                days_to_expiry = (expiry - today).days
                years_to_expiry = round(days_to_expiry / 365.25, 2)
                forward_attrs["days_to_expiry"] = days_to_expiry
                forward_attrs["years_to_expiry"] = years_to_expiry
                
                # Term classification
                if days_to_expiry <= 90:
                    forward_attrs["term_classification"] = "Short Term"
                elif days_to_expiry <= 365:
                    forward_attrs["term_classification"] = "Medium Term"
                else:
                    forward_attrs["term_classification"] = "Long Term"
        except (ValueError, TypeError):
            pass

    return forward_attrs if forward_attrs else None
    
    return forward_attrs if forward_attrs else None
    return None  # Placeholder


def _build_option_attributes(processed_attrs: Dict, firds_data: Dict) -> Optional[Dict]:
    """Build option contract attributes from FIRDS data."""
    if not firds_data:
        return None
    
    option_attrs = {}
    
    # Option expiration and dates
    if firds_data.get('DerivInstrmAttrbts_XpryDt'):
        option_attrs["expiration_date"] = firds_data['DerivInstrmAttrbts_XpryDt']
    
    if firds_data.get('TradgVnRltdAttrbts_FrstTradDt'):
        option_attrs["first_trade_date"] = firds_data['TradgVnRltdAttrbts_FrstTradDt']
        
    if firds_data.get('TradgVnRltdAttrbts_TermntnDt'):
        option_attrs["termination_date"] = firds_data['TradgVnRltdAttrbts_TermntnDt']
    
    # Strike price and option type
    if firds_data.get('DerivInstrmAttrbts_StrkPric'):
        option_attrs["strike_price"] = firds_data['DerivInstrmAttrbts_StrkPric']
        
    if firds_data.get('DerivInstrmAttrbts_StrkPricCcy'):
        option_attrs["strike_currency"] = firds_data['DerivInstrmAttrbts_StrkPricCcy']
        
    if firds_data.get('DerivInstrmAttrbts_OptnTp'):
        option_type = firds_data['DerivInstrmAttrbts_OptnTp']
        option_attrs["option_type"] = option_type
        
        # Map option type codes to descriptive names
        type_mapping = {
            'CALL': 'Call Option',
            'PUT': 'Put Option',
            'CPUT': 'Call/Put Option'
        }
        option_attrs["option_type_description"] = type_mapping.get(option_type, option_type)
    
    # Exercise style and settlement
    if firds_data.get('DerivInstrmAttrbts_OptnExrcStyle'):
        exercise_style = firds_data['DerivInstrmAttrbts_OptnExrcStyle']
        option_attrs["exercise_style"] = exercise_style
        
        # Map exercise style codes
        style_mapping = {
            'EURO': 'European',
            'AMER': 'American',
            'BERM': 'Bermudan',
            'ASIA': 'Asian'
        }
        option_attrs["exercise_style_description"] = style_mapping.get(exercise_style, exercise_style)
    
    if firds_data.get('DerivInstrmAttrbts_SttlmTp'):
        option_attrs["settlement_type"] = firds_data['DerivInstrmAttrbts_SttlmTp']
    
    # Underlying asset information - CRITICAL for derivatives
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
        option_attrs["underlying_isin"] = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']
        
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Eq_Id'):
        option_attrs["underlying_equity_id"] = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Eq_Id']
        
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm'):
        option_attrs["underlying_name"] = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm']
        
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Id'):
        option_attrs["underlying_id"] = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Id']
        
    # Also check processed attributes as backup source for underlying ISIN
    if not option_attrs.get("underlying_isin") and processed_attrs.get('underlying_isin'):
        option_attrs["underlying_isin"] = processed_attrs['underlying_isin']
    
    # Contract multiplier and size
    if firds_data.get('DerivInstrmAttrbts_PricMltplr'):
        option_attrs["price_multiplier"] = firds_data['DerivInstrmAttrbts_PricMltplr']
        
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit'):
        option_attrs["contract_unit"] = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit']
        
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val'):
        option_attrs["contract_size"] = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val']
    
    # Barrier and exotic option features
    if firds_data.get('DerivInstrmAttrbts_BrrierTouchd'):
        option_attrs["barrier_touched"] = firds_data['DerivInstrmAttrbts_BrrierTouchd']
        
    # Determine option category
    option_category = "Standard Option"
    if option_attrs.get("barrier_touched"):
        option_category = "Barrier Option"
    elif option_attrs.get("exercise_style") in ['ASIA', 'BERM']:
        option_category = "Exotic Option"
    elif option_attrs.get("underlying_equity_id"):
        option_category = "Equity Option"
    elif option_attrs.get("underlying_name") and "INDEX" in option_attrs["underlying_name"].upper():
        option_category = "Index Option"
    
    option_attrs["option_category"] = option_category
    
    # Build option description
    if option_attrs.get("option_type_description") and option_attrs.get("strike_price") and option_attrs.get("expiration_date"):
        strike_str = f"{option_attrs['strike_price']}"
        if option_attrs.get("strike_currency"):
            strike_str = f"{option_attrs['strike_currency']} {strike_str}"
        expiry_str = option_attrs["expiration_date"][:10] if option_attrs["expiration_date"] else "TBD"
        underlying_str = option_attrs.get("underlying_name", "Underlying Asset")
        
        option_attrs["contract_description"] = f"{option_attrs['option_type_description']} on {underlying_str} @ {strike_str} exp {expiry_str}"
    
    return option_attrs if option_attrs else None


def _build_rights_attributes(processed_attrs: Dict, firds_data: Dict) -> Optional[Dict]:
    """Build rights and warrants attributes from FIRDS data."""
    if not firds_data:
        return None
    
    rights_attrs = {}
    
    # Rights/Warrants expiration
    if firds_data.get('RghtsInstrmAttrbts_XpryDt'):
        rights_attrs["expiration_date"] = firds_data['RghtsInstrmAttrbts_XpryDt']
        
    if firds_data.get('TradgVnRltdAttrbts_TermntnDt'):
        rights_attrs["termination_date"] = firds_data['TradgVnRltdAttrbts_TermntnDt']
        
    if firds_data.get('TradgVnRltdAttrbts_FrstTradDt'):
        rights_attrs["first_trade_date"] = firds_data['TradgVnRltdAttrbts_FrstTradDt']
    
    # Exercise and conversion information
    if firds_data.get('RghtsInstrmAttrbts_ExrcPric'):
        rights_attrs["exercise_price"] = firds_data['RghtsInstrmAttrbts_ExrcPric']
        
    if firds_data.get('RghtsInstrmAttrbts_ExrcPricCcy'):
        rights_attrs["exercise_currency"] = firds_data['RghtsInstrmAttrbts_ExrcPricCcy']
        
    if firds_data.get('RghtsInstrmAttrbts_ExrcRatio'):
        rights_attrs["exercise_ratio"] = firds_data['RghtsInstrmAttrbts_ExrcRatio']
    
    # Underlying instrument information
    if firds_data.get('RghtsInstrmAttrbts_UndrlygInstrm_Eq_Id'):
        rights_attrs["underlying_equity_id"] = firds_data['RghtsInstrmAttrbts_UndrlygInstrm_Eq_Id']
        
    if firds_data.get('RghtsInstrmAttrbts_UndrlygInstrm_Eq_Nm'):
        rights_attrs["underlying_equity_name"] = firds_data['RghtsInstrmAttrbts_UndrlygInstrm_Eq_Nm']
    
    # Rights type determination based on CFI code and data
    rights_type = "Rights"  # Default
    
    # Check CFI code for more specific classification
    cfi_code = firds_data.get('FinInstrmGnlAttrbts_CFI') or processed_attrs.get('cfi_code', '')
    if cfi_code and len(cfi_code) >= 2:
        # R = Rights, second character gives more detail
        if cfi_code[1] == 'W':
            rights_type = "Warrant"
        elif cfi_code[1] == 'A':
            rights_type = "Allotment Rights"
        elif cfi_code[1] == 'S':
            rights_type = "Subscription Rights"
        elif cfi_code[1] == 'P':
            rights_type = "Purchase Rights"
    
    # Further refinement based on data characteristics
    if rights_attrs.get("exercise_price") and rights_attrs.get("underlying_equity_id"):
        if rights_type == "Rights":
            rights_type = "Stock Purchase Rights"
    
    rights_attrs["rights_type"] = rights_type
    
    # Calculate intrinsic value information if possible
    if rights_attrs.get("exercise_price") and rights_attrs.get("exercise_ratio"):
        try:
            exercise_price = float(rights_attrs["exercise_price"])
            exercise_ratio = float(rights_attrs["exercise_ratio"])
            rights_attrs["exercise_multiple"] = exercise_ratio
            rights_attrs["cost_per_share"] = exercise_price / exercise_ratio if exercise_ratio != 0 else exercise_price
        except (ValueError, TypeError, ZeroDivisionError):
            pass
    
    # Time to expiry calculation
    if rights_attrs.get("expiration_date"):
        from datetime import datetime, date
        try:
            if isinstance(rights_attrs["expiration_date"], str):
                expiry = datetime.strptime(rights_attrs["expiration_date"][:10], '%Y-%m-%d').date()
            else:
                expiry = rights_attrs["expiration_date"]
            
            today = date.today()
            if expiry > today:
                days_to_expiry = (expiry - today).days
                rights_attrs["days_to_expiry"] = days_to_expiry
                
                # Determine if rights are near expiry
                if days_to_expiry <= 30:
                    rights_attrs["near_expiry"] = True
                    rights_attrs["expiry_status"] = "Expiring Soon"
                elif days_to_expiry <= 90:
                    rights_attrs["expiry_status"] = "Short Term"
                else:
                    rights_attrs["expiry_status"] = "Long Term"
            else:
                rights_attrs["expiry_status"] = "Expired"
        except (ValueError, TypeError):
            pass
    
    # Exercise method determination
    exercise_method = "Physical Exercise"  # Default assumption
    if firds_data.get('RghtsInstrmAttrbts_SttlmTp'):
        settlement_type = firds_data['RghtsInstrmAttrbts_SttlmTp']
        if settlement_type in ['CASH', 'C']:
            exercise_method = "Cash Settlement"
        elif settlement_type in ['PHYS', 'P']:
            exercise_method = "Physical Delivery"
        rights_attrs["settlement_type"] = settlement_type
    
    rights_attrs["exercise_method"] = exercise_method
    
    # Build rights description
    description_parts = [rights_attrs.get("rights_type", "Rights")]
    
    if rights_attrs.get("underlying_equity_name"):
        description_parts.append(f"on {rights_attrs['underlying_equity_name']}")
    
    if rights_attrs.get("exercise_price") and rights_attrs.get("exercise_currency"):
        price_str = f"{rights_attrs['exercise_currency']} {rights_attrs['exercise_price']}"
        description_parts.append(f"@ {price_str}")
    
    if rights_attrs.get("expiration_date"):
        expiry_str = rights_attrs["expiration_date"][:10] if rights_attrs["expiration_date"] else "TBD"
        description_parts.append(f"exp {expiry_str}")
    
    rights_attrs["instrument_description"] = " ".join(description_parts)
    
    return rights_attrs if rights_attrs else None


# Type-specific detailed response builders for single instrument endpoint

def _build_swap_detailed_response(instrument, base_response: Dict) -> Dict:
    """Build detailed swap response with additional swap-specific sections."""
    return {
        "swap_details": {
            "risk_metrics": "placeholder",  # Add swap-specific risk data
            "curve_data": "placeholder",    # Add yield curve data
        }
    }


def _build_equity_detailed_response(instrument, base_response: Dict) -> Dict:
    """Build detailed equity response."""
    return {
        "equity_details": {
            "market_data": "placeholder",   # Add market data
            "corporate_actions": "placeholder",  # Add corporate actions
        }
    }


def _build_debt_detailed_response(instrument, base_response: Dict) -> Dict:
    """Build detailed debt response.""" 
    return {
        "debt_details": {
            "yield_analysis": "placeholder",  # Add yield analysis
            "credit_ratings": "placeholder",  # Add ratings data
        }
    }


def _build_option_detailed_response(instrument, base_response: Dict) -> Dict:
    """Build detailed option response."""
    return {
        "option_details": {
            "greeks": "placeholder",        # Add Greeks calculations
            "payoff_diagram": "placeholder", # Add payoff data
        }
    }


def _format_primary_venue_display(mic_code: str) -> Dict[str, Any]:
    """Format primary venue with MIC lookup."""
    try:
        from ...database.session import get_session
        from ...models.sqlite.market_identification_code import MarketIdentificationCode
        
        with get_session() as session:
            mic_data = session.query(MarketIdentificationCode).filter(
                MarketIdentificationCode.mic == mic_code
            ).first()
            
            if mic_data:
                return {
                    "mic_code": mic_code,
                    "market_name": mic_data.market_name,
                    "country_code": mic_data.iso_country_code,
                    "status": mic_data.status.value if mic_data.status else None,
                    "formatted": f"{mic_code} ({mic_data.market_name})"
                }
    except Exception:
        pass
    
    return {
        "mic_code": mic_code,
        "market_name": "Unknown",
        "country_code": None,
        "status": None,
        "formatted": mic_code
    }