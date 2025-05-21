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
    """Maps ESMA/FIRDS data to instrument model fields"""
    # Base instrument fields
    mapped = {
        'isin': data.get('Id'),
        'full_name': data.get('FinInstrmGnlAttrbts_FullNm'),
        'short_name': data.get('FinInstrmGnlAttrbts_ShrtNm'),
        'symbol': data.get('FinInstrmGnlAttrbts_ShrtNm'),  # Using short name as symbol if no specific symbol
        'currency': data.get('FinInstrmGnlAttrbts_NtnlCcy'),
        'cfi_code': data.get('FinInstrmGnlAttrbts_ClssfctnTp'),
        'commodity_derivative': str(data.get('FinInstrmGnlAttrbts_CmmdtyDerivInd', 'false')).lower() == 'true',  # Proper boolean conversion
        'lei_id': data.get('Issr'),
        'trading_venue': data.get('TradgVnRltdAttrbts_Id_'),
        'issuer_req': data.get('TradgVnRltdAttrbts_IssrReq', False),
        'first_trade_date': parse_date(data.get('TradgVnRltdAttrbts_FrstTradDt')),
        'termination_date': parse_date(data.get('TradgVnRltdAttrbts_TermntnDt')),
        'relevant_authority': data.get('TechAttrbts_RlvntCmptntAuthrty'),
        'relevant_venue': data.get('TechAttrbts_RlvntTradgVn'),
        'from_date': parse_date(data.get('TechAttrbts_PblctnPrd_FrDt'))
    }

    # Update type-specific fields
    if instrument_type == "equity":
        mapped.update({
            'admission_approval_date': parse_date(data.get('TradgVnRltdAttrbts_AdmssnApprvlDtByIssr')),
            'admission_request_date': parse_date(data.get('TradgVnRltdAttrbts_ReqForAdmssnDt')),
            'price_multiplier': parse_float(data.get('DerivInstrmAttrbts_PricMltplr')),
            'basket_isin': data.get('DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN'),
            'underlying_index_isin': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN'),
            'underlying_single_index_name': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm'),
            'basket_lei': data.get('DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI'),
            # Keep existing asset class specific fields
            'oil_type': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct'),
            'sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct'),
            'additional_sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct'),
            'metal_type': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct'),
            'precious_metal': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct'),
            'underlying_single_isin': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'),
            'additional_metal_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct'),
        })
    elif instrument_type == "debt": # Debt instrument specific fields "DebtInstrmAttrbts"
        mapped.update({
            'total_issued_nominal': parse_float(data.get('DebtInstrmAttrbts_TtlIssdNmnlAmt')),
            'maturity_date': parse_date(data.get('DebtInstrmAttrbts_MtrtyDt')),
            'nominal_value_per_unit': parse_float(data.get('DebtInstrmAttrbts_NmnlValPerUnit')),
            'fixed_interest_rate': parse_float(data.get('DebtInstrmAttrbts_IntrstRate_Fxd')),
            'debt_seniority': data.get('DebtInstrmAttrbts_DebtSnrty'),
            'floating_rate_reference': data.get('DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm'),
            'floating_rate_term_unit': data.get('DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit'),
            'floating_rate_term_value': parse_float(data.get('DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val')),
            'floating_rate_basis_points_spread': parse_float(data.get('DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd')),
            'interest_rate_floating_reference_index': data.get('DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx'),
            'interest_rate_floating_reference_isin': data.get('DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN'),
            'underlying_single_isin': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'),
            'basket_isin': data.get('DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN'),
            'underlying_index_isin': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN'),
            'underlying_single_index_name': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm'),
            'underlying_single_lei': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI'),
            'additional_metal_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct'),
            'oil_type': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct'),
            'sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct'),
            'additional_sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct'),
            'metal_type': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct'),
            'precious_metal': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct'),
            'other_commodity_base_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct'),
            'underlying_index_name_term_unit': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit'),
            'underlying_index_name_term_value': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val'),
        })
    elif instrument_type == "future":
        mapped.update({
            'admission_approval_date': parse_date(data.get('TradgVnRltdAttrbts_AdmssnApprvlDtByIssr')),
            'admission_request_date': parse_date(data.get('TradgVnRltdAttrbts_ReqForAdmssnDt')),
            'expiration_date': parse_date(data.get('DerivInstrmAttrbts_XpryDt')),
            'delivery_type': data.get('DerivInstrmAttrbts_DlvryTp'),
            'price_multiplier': parse_float(data.get('DerivInstrmAttrbts_PricMltplr')),
            'final_price_type': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp'),
            'transaction_type': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp'),
            'underlying_index_name': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm'),
            'fx_type': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp'),
            'other_notional_currency': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy'),
            'interest_rate_reference': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm'),
            'interest_rate_term_unit': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit'),
            'interest_rate_term_value': parse_float(data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val')),
            'index_reference_rate': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx'),
            
            # JSON fields for complex attributes
            'agricultural_attributes': {
                'dairy': {
                    'base_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_BasePdct'),
                    'sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_SubPdct')
                },
                'grain': {
                    'base_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_BasePdct'),
                    'sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_SubPdct'),
                    'additional_sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_AddtlSubPdct')
                }
            },
            'natural_gas_attributes': {
                'base_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct'),
                'sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct'),
                'additional_sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct')
            },
            'electricity_attributes': {
                'base_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct'),
                'sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct'),
                'additional_sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_AddtlSubPdct')
            },
            'environmental_attributes': {
                'base_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct'),
                'sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct'),
                'additional_sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_AddtlSubPdct')
            },
            'freight_attributes': {
                'dry': {
                    'base_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_BasePdct'),
                    'sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_SubPdct'),
                    'additional_sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Dry_AddtlSubPdct')
                },
                'wet': {
                    'base_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_BasePdct'),
                    'sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_SubPdct'),
                    'additional_sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Frght_Wet_AddtlSubPdct')
                }
            },
            'underlying_single_isin': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'),
            'basket_isin': data.get('DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN'),
            'underlying_index_isin': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN'),
            'underlying_single_index_name': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm'),
            'underlying_single_lei': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI'),
            'additional_metal_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct'),
            'oil_type': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct'),
            'sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct'),
            'additional_sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct'),
            'metal_type': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct'),
            'precious_metal': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct'),
            'multi_commodity_base_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct'),
            'other_c10_nondeliverable_base_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct'),
            'other_c10_nondeliverable_sub_product': data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct'),
            'underlying_index_name_term_unit': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit'),
            'underlying_index_name_term_value': data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val'),
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
