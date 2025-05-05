from typing import Dict, Any
from datetime import datetime
from ..models.instrument import Instrument, Equity, Debt

# Add model mapping to complement existing field mappings
MODEL_FIELD_MAPPING = {
    'instruments': {
        'FinInstrmGnlAttrbts_Id': 'isin',  # Make sure ISIN is properly mapped
        'FinInstrmGnlAttrbts_FullNm': 'full_name',
        'FinInstrmGnlAttrbts_ShrtNm': 'short_name',
        'Issr': 'lei_id'
    },
    'debts': {
        'DebtInstrmAttrbts_TtlIssdNmnlAmt': ('total_issued_nominal', float),
        'DebtInstrmAttrbts_MtrtyDt': ('maturity_date', lambda x: datetime.strptime(x, '%Y-%m-%d').date()),
        'DebtInstrmAttrbts_IntrstRate_Fxd': ('fixed_interest_rate', float)
    }
}

def map_to_model(data: Dict[str, Any], instrument_type: str = "equity") -> Dict[str, Any]:
    """Maps ESMA/FIRDS data to instrument model fields"""
    # Base instrument fields
    mapped = {
        'isin': data.get('Id'),
        'full_name': data.get('FullNm'),
        'short_name': data.get('ShrtNm'),
        'symbol': data.get('ShrtNm'),  # Using short name as symbol if no specific symbol
        'currency': data.get('NtnlCcy'),
        'cfi_code': data.get('ClssfctnTp'),
        'commodity_derivative': data.get('CmmdtyDerivInd', False),
        'lei_id': data.get('Issr'),
        'trading_venue': data.get('Id_2'),
        'issuer_req': data.get('IssrReq', False),
        'first_trade_date': parse_date(data.get('FrstTradDt')),
        'termination_date': parse_date(data.get('TermntnDt')),
        'relevant_authority': data.get('RlvntCmptntAuthrty'),
        'relevant_venue': data.get('RlvntTradgVn'),
        'from_date': parse_date(data.get('FrDt'))
    }

    # Add type-specific fields
    if instrument_type == "equity":
        mapped.update({
            'admission_approval_date': parse_date(data.get('AdmssnApprvlDtByIssr')),
            'admission_request_date': parse_date(data.get('ReqForAdmssnDt')),
            'price_multiplier': parse_float(data.get('PricMltplr')),
            'asset_class': data.get('AsstClssSpcfcAttrbts'),
            'commodity_product': data.get('Cmmdty_Pdct'),
            'energy_type': data.get('Nrgy'),
            'oil_type': data.get('Oil'),
            'base_product': data.get('BasePdct'),
            'sub_product': data.get('SubPdct'),
            'additional_sub_product': data.get('AddtlSubPdct'),
            'metal_type': data.get('Metl'),
            'precious_metal': data.get('Prcs'),
            'underlying_isins': extract_underlying_isins(data)
        })
    elif instrument_type == "debt":
        mapped.update({
            'total_issued_nominal': parse_float(data.get('TtlIssdNmnlAmt')),
            'maturity_date': parse_date(data.get('MtrtyDt')),
            'nominal_value_per_unit': parse_float(data.get('NmnlValPerUnit')),
            'fixed_interest_rate': parse_float(data.get('IntrstRate_Fxd')),
            'debt_seniority': data.get('DebtSnrty'),
            'coupon_frequency': data.get('CpnFreq'),  # If available in FIRDS data
            'credit_rating': data.get('CrdtRtg')  # If available in FIRDS data
        })

    return {k: v for k, v in mapped.items() if v is not None}

def parse_date(date_str: str) -> datetime.date:
    """Parse date string to datetime.date object"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None

def parse_float(value: Any) -> float:
    """Parse string or other value to float"""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def extract_underlying_isins(data: Dict[str, Any]) -> list:
    """Extract all underlying ISINs from the data"""
    isins = []
    i = 2
    while True:
        isin = data.get(f'ISIN_{i}')
        if not isin:
            break
        isins.append(isin)
        i += 1
    return isins if isins else None
