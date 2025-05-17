import logging
from typing import Dict, Any, Type, Optional
from datetime import datetime
from ..models.instrument import Instrument, Equity, Debt
from ..models.figi import FigiMapping
from ..schema.schema_mapper import SchemaMapper

# Setup logging
logger = logging.getLogger(__name__)

def map_to_schema(data: Dict[str, Any], instrument_type: str = "equity") -> Dict[str, Any]:
    """Maps ESMA/FIRDS data to instrument model fields"""
    # First convert FIRDS field names to our schema fields
    firds_mapping = {
        'Id': 'isin',
        'FullNm': 'full_name',
        'ShrtNm': 'short_name',
        'NtnlCcy': 'currency',
        'ClssfctnTp': 'cfi_code',
        'CmmdtyDerivInd': 'commodity_derivative',
        'PricMltplr': 'price_multiplier'
    }
    
    # Map FIRDS fields to our field names
    mapped_data = {}
    for firds_key, model_key in firds_mapping.items():
        if firds_key in data:
            mapped_data[model_key] = data[firds_key]
    
    try:
        # Get schema mapper instance
        schema_mapper = SchemaMapper()
        schema_type = instrument_type if instrument_type in schema_mapper.type_mapping else "base"
        
        # Add schema-based mapping
        schema_fields = schema_mapper.get_schema_fields(schema_type)
        for field in schema_fields:
            if field.source in mapped_data:
                value = mapped_data[field.source]
                if value is not None:
                    if field.type == "date":
                        value = parse_date(value)
                    elif field.type == "number":
                        value = parse_float(value)
                    elif field.type == "boolean":
                        value = str(value).lower() == "true"
                    mapped_data[field.source] = value
        
        return {k: v for k, v in mapped_data.items() if v is not None}
        
    except Exception as e:
        logger.error(f"Schema mapping failed: {str(e)}, falling back to legacy mapping")
        return map_to_model(data, instrument_type)

def map_to_model(data: Dict[str, Any], instrument_type: str = "equity") -> Dict[str, Any]:
    """Legacy mapping function as fallback"""
    # Base instrument fields
    mapped = {
        'isin': data.get('Id'),
        'full_name': data.get('FullNm'),
        'short_name': data.get('ShrtNm'),
        'symbol': data.get('ShrtNm'),  # Using short name as symbol if no specific symbol
        'currency': data.get('NtnlCcy'),
        'cfi_code': data.get('ClssfctnTp'),
        'commodity_derivative': str(data.get('CmmdtyDerivInd', 'false')).lower() == 'true',  # Proper boolean conversion
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
    elif instrument_type == "future":
        mapped.update({
            'admission_approval_date': parse_date(data.get('AdmssnApprvlDtByIssr')),
            'admission_request_date': parse_date(data.get('ReqForAdmssnDt')),
            'expiration_date': parse_date(data.get('ExprtnDt')),
            'final_settlement_date': parse_date(data.get('FnlSttlmDt')),
            'delivery_type': data.get('DlvryTp'),
            'settlement_method': data.get('SttlmtMtd'),
            'contract_size': parse_float(data.get('CtrctSz')),
            'contract_unit': data.get('CtrctUnit'),
            'price_multiplier': parse_float(data.get('PricMltplr')),
            'settlement_currency': data.get('SttlmtCcy'),
            'contract_details': {
                'trading_hours': data.get('TrdngHrs'),
                'tick_size': parse_float(data.get('TckSz')),
                'market_segment': data.get('MktSgmt'),
                'underlying_type': data.get('UndrlygTp'),
                'trading_cycle': data.get('TrdngCycl')
            }
        })

    return {k: v for k, v in mapped.items() if v is not None}

def parse_date(date_str: str) -> datetime.date:
    """Parse date string to datetime.date object"""
    if not date_str:
        return None
    try:
        # First try ISO format with timezone
        if 'T' in date_str:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
        # Fallback to simple YYYY-MM-DD format
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError) as e:
        logger.debug(f"Date parsing failed for {date_str}: {str(e)}")
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

def map_figi_data(data: list, isin: str) -> FigiMapping:
    """Maps OpenFIGI API response to FigiMapping model"""
    if not data or len(data) == 0:
        return None
        
    # Handle nested data structure from OpenFIGI
    try:
        if 'data' in data[0]:
            figi_data = data[0]['data'][0]  # Get first result from nested data array
        else:
            figi_data = data[0]  # Fallback to old structure

        if 'warning' in figi_data:  # Handle case where no data found
            return None

        return FigiMapping(
            isin=isin,
            figi=figi_data.get('figi'),
            composite_figi=figi_data.get('compositeFIGI'),
            share_class_figi=figi_data.get('shareClassFIGI'),
            ticker=figi_data.get('ticker'),
            security_type=figi_data.get('securityType'),
            market_sector=figi_data.get('marketSector'),
            security_description=figi_data.get('securityDescription')
        )
    except (KeyError, IndexError):
        return None

def flatten_address(address: Dict[str, Any], address_type: str, lei: str) -> Dict[str, Any]:
    return {
        "lei": lei,
        "type": address_type,
        "language": address.get("language"),
        "addressLines": ", ".join(address.get("addressLines", [])),
        "city": address.get("city"),
        "region": address.get("region"),
        "country": address.get("country"),
        "postalCode": address.get("postalCode")
    }

def parse_iso_date(date_str: str) -> datetime:
    """Parse ISO format datetime string"""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except (ValueError, TypeError):
        return None

def map_lei_record(response: Dict[str, Any]) -> Dict[str, Any]:
    data = response.get("data", {})
    attributes = data.get("attributes", {})
    entity = attributes.get("entity", {})
    registration = attributes.get("registration", {})

    def safe_list_to_str(value):
        if isinstance(value, list):
            return ", ".join(str(item) for item in value)
        return value

    return {
        "lei_record": {
            "lei": data.get("id"),  # Using id from data as LEI
            "name": entity.get("legalName", {}).get("name"),
            "jurisdiction": entity.get("jurisdiction"),
            "legal_form": entity.get("legalForm", {}).get("id"),
            "registered_as": entity.get("registeredAs"),
            "status": entity.get("status"),
            "creation_date": parse_iso_date(registration.get("initialRegistrationDate")),
            "bic": safe_list_to_str(attributes.get("bic")),
            "next_renewal_date": parse_iso_date(registration.get("nextRenewalDate")),
            "registration_status": registration.get("status"),
            "managing_lou": registration.get("managingLou")
        },
        "addresses": [
            {
                "lei": data.get("id"),
                "type": "legal",
                "address_lines": ", ".join(entity.get("legalAddress", {}).get("addressLines", [])),
                "city": entity.get("legalAddress", {}).get("city"),
                "region": entity.get("legalAddress", {}).get("region"),
                "country": entity.get("legalAddress", {}).get("country"),
                "postal_code": entity.get("legalAddress", {}).get("postalCode")
            },
            {
                "lei": data.get("id"),
                "type": "headquarters",
                "address_lines": ", ".join(entity.get("headquartersAddress", {}).get("addressLines", [])),
                "city": entity.get("headquartersAddress", {}).get("city"),
                "region": entity.get("headquartersAddress", {}).get("region"),
                "country": entity.get("headquartersAddress", {}).get("country"),
                "postal_code": entity.get("headquartersAddress", {}).get("postalCode")
            }
        ],
        "registration": {
            "lei": data.get("id"),
            "last_update": parse_iso_date(registration.get("lastUpdateDate")),
            "status": registration.get("status"),
            "next_renewal": parse_iso_date(registration.get("nextRenewalDate")),
            "managing_lou": registration.get("managingLou"),
            "validation_sources": registration.get("validatedAt", {}).get("id")
        }
    }
