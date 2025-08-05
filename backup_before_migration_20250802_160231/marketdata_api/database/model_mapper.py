import logging
from typing import Dict, Any, Type, Optional
from datetime import datetime, timezone
from ..models.instrument import Instrument, Equity, Debt
from ..models.figi import FigiMapping
from ..schema.schema_mapper import SchemaMapper

# Setup logging
logger = logging.getLogger(__name__)

def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string to timezone-naive datetime object (SQL Server compatibility)"""
    if not date_str:
        return None
    try:
        # First try ISO format with timezone
        if 'T' in date_str:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            # Convert to timezone-naive for SQL Server compatibility (store as UTC)
            if dt.tzinfo is not None:
                dt = dt.utctimetuple()
                dt = datetime(*dt[:6])
            return dt
        # Fallback to simple YYYY-MM-DD format - return as timezone-naive datetime
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt  # Already timezone-naive
    except (ValueError, TypeError) as e:
        logger.debug(f"Date parsing failed for {date_str}: {str(e)}")
        return None

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
        'issuer_req': data.get('TradgVnRltdAttrbts_IssrReq'),  # Keep as string, not boolean
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

def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string to timezone-naive datetime object (SQL Server compatibility)"""
    if not date_str:
        return None
    try:
        # First try ISO format with timezone
        if 'T' in date_str:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            # Convert to timezone-naive for SQL Server compatibility (store as UTC)
            if dt.tzinfo is not None:
                dt = dt.utctimetuple()
                dt = datetime(*dt[:6])
            return dt
        # Fallback to simple YYYY-MM-DD format - return as timezone-naive datetime
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt  # Already timezone-naive
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
    
    def safe_bic_value(value):
        """Extract first BIC code to fit in 11-character limit"""
        if isinstance(value, list) and value:
            return str(value[0])[:11]  # Take first BIC and truncate to 11 chars
        elif isinstance(value, str):
            return value.split(',')[0].strip()[:11]  # Take first if comma-separated
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
            "bic": safe_bic_value(attributes.get("bic")),
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

def map_transparency_data(data: Dict[str, Any], calculation_type: str, instrument_type: str) -> Dict[str, Dict[str, Any]]:
    """
    Maps FITRS transparency data to transparency model fields.
    
    Args:
        data: Dictionary containing FITRS transparency data
        calculation_type: 'EQUITY' or 'NON_EQUITY'
        instrument_type: 'equity', 'debt', 'futures', or 'non_equity'
        
    Returns:
        Dictionary with 'base' and 'specific' mappings
    """
    
    # Base transparency calculation fields
    base_mapping = {
        'tech_record_id': data.get('TechRcrdId'),
        'isin': data.get('ISIN'),
        'calculation_type': calculation_type,
        'from_date': parse_date(data.get('FrDt')),
        'to_date': parse_date(data.get('ToDt')),
        'liquidity': parse_boolean(data.get('Lqdty')),
        'total_transactions_executed': parse_int(data.get('TtlNbOfTxsExctd')),
        'total_volume_executed': parse_float(data.get('TtlVolOfTxsExctd')),
        'statistics': data.get('Sttstcs') if calculation_type == "EQUITY" else None
    }
    
    # Specific mapping based on calculation and instrument type
    if calculation_type == "EQUITY":
        specific_mapping = _map_equity_transparency(data)
    else:
        if instrument_type == "debt":
            specific_mapping = _map_debt_transparency(data)
        elif instrument_type == "futures":
            specific_mapping = _map_futures_transparency(data)
        else:
            specific_mapping = _map_non_equity_transparency(data)
    
    return {
        'base': {k: v for k, v in base_mapping.items() if v is not None},
        'specific': {k: v for k, v in specific_mapping.items() if v is not None}
    }

def _map_equity_transparency(data: Dict[str, Any]) -> Dict[str, Any]:
    """Map equity-specific transparency fields from FULECR data"""
    return {
        'financial_instrument_classification': data.get('FinInstrmClssfctn'),
        'methodology': data.get('Mthdlgy'),
        'average_daily_turnover': parse_float(data.get('AvrgDalyTrnvr')),
        'large_in_scale': parse_float(data.get('LrgInScale')),
        'average_daily_number_of_transactions': parse_float(data.get('AvrgDalyNbOfTxs')),
        'secondary_id': data.get('Id_2'),
        'average_daily_transactions_secondary': parse_float(data.get('AvrgDalyNbOfTxs_2')),
        'average_transaction_value': parse_float(data.get('AvrgTxVal')),
        'standard_market_size': parse_float(data.get('StdMktSz'))
    }

def _map_non_equity_transparency(data: Dict[str, Any]) -> Dict[str, Any]:
    """Map non-equity transparency fields from FULNCR data"""
    return {
        'description': data.get('Desc'),
        'criterion_name': data.get('CritNm'),
        'criterion_value': data.get('CritVal'),
        'financial_instrument_classification': data.get('FinInstrmClssfctn'),
        'pre_trade_large_in_scale_threshold': parse_float(data.get('PreTradLrgInScaleThrshld_Amt')),
        'post_trade_large_in_scale_threshold': parse_float(data.get('PstTradLrgInScaleThrshld_Amt')),
        'pre_trade_instrument_size_specific_threshold': parse_float(data.get('PreTradInstrmSzSpcfcThrshld_Amt')),
        'post_trade_instrument_size_specific_threshold': parse_float(data.get('PstTradInstrmSzSpcfcThrshld_Amt')),
        'criterion_name_secondary': data.get('CritNm_2'),
        'criterion_value_secondary': data.get('CritVal_2')
    }

def _map_debt_transparency(data: Dict[str, Any]) -> Dict[str, Any]:
    """Map debt-specific transparency fields"""
    base_mapping = _map_non_equity_transparency(data)
    
    # Add debt-specific fields
    base_mapping.update({
        'bond_type': _determine_bond_type(data.get('CritVal'), data.get('Desc')),
        'security_type': data.get('Desc'),
        'is_securitised_derivative': data.get('CritVal') == 'SDRV',
        'is_corporate_bond': data.get('Desc') == 'Corporate bond',
        'is_liquid': parse_boolean(data.get('Lqdty'))
    })
    
    return base_mapping

def _map_futures_transparency(data: Dict[str, Any]) -> Dict[str, Any]:
    """Map futures-specific transparency fields"""
    base_mapping = _map_non_equity_transparency(data)
    
    # Add futures-specific fields
    base_mapping.update({
        'criterion_name_3': data.get('CritNm_3'),
        'criterion_value_3': data.get('CritVal_3'),
        'criterion_name_4': data.get('CritNm_4'),
        'criterion_value_4': data.get('CritVal_4'),
        'criterion_name_5': data.get('CritNm_5'),
        'criterion_value_5': data.get('CritVal_5'),
        'criterion_name_6': data.get('CritNm_6'),
        'criterion_value_6': data.get('CritVal_6'),
        'criterion_name_7': data.get('CritNm_7'),
        'criterion_value_7': data.get('CritVal_7'),
        'pre_trade_large_in_scale_threshold_nb': parse_float(data.get('PreTradLrgInScaleThrshld_Nb')),
        'post_trade_large_in_scale_threshold_nb': parse_float(data.get('PstTradLrgInScaleThrshld_Nb')),
        'pre_trade_instrument_size_specific_threshold_nb': parse_float(data.get('PreTradInstrmSzSpcfcThrshld_Nb')),
        'post_trade_instrument_size_specific_threshold_nb': parse_float(data.get('PstTradInstrmSzSpcfcThrshld_Nb')),
        'is_stock_dividend_future': 'Stock dividend' in data.get('Desc', ''),
        'underlying_isin': data.get('CritVal_2') if data.get('CritNm_2') == 'UINS' else None
    })
    
    return base_mapping

def _determine_bond_type(crit_val: str, description: str) -> str:
    """Determine bond type from criterion value and description"""
    if not crit_val:
        return None
    
    if crit_val == 'SDRV':
        return 'Securitised Derivative'
    elif 'BOND' in crit_val:
        return 'Corporate Bond'
    elif description and 'bond' in description.lower():
        return 'Bond'
    
    return None

def parse_boolean(value: Any) -> bool:
    """Parse boolean values from FITRS data"""
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'y')
    return bool(value)

def parse_int(value: Any) -> int:
    """Parse integer values"""
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

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
        'issuer_req': data.get('TradgVnRltdAttrbts_IssrReq'),  # Keep as string, not boolean
        'first_trade_date': parse_date(data.get('TradgVnRltdAttrbts_FrstTradDt')),
        'termination_date': parse_date(data.get('TradgVnRltdAttrbts_TermntnDt')),
        'relevant_authority': data.get('TechAttrbts_RlvntCmptntAuthrty'),
        'relevant_venue': data.get('TechAttrbts_RlvntTradgVn'),
        'from_date': parse_date(data.get('TechAttrbts_PblctnPrd_FrDt'))
    }

    # Log the issuer_req field specifically to debug the issue
    issuer_req_raw = data.get('TradgVnRltdAttrbts_IssrReq')
    logger.info(f"DEBUG: issuer_req raw value: {issuer_req_raw} (type: {type(issuer_req_raw)})")
    
    # Basic mapping for Instrument fields
    model_data = {
        'isin': data.get('Id'),
        'full_name': data.get('FinInstrmGnlAttrbts_FullNm'),
        'short_name': data.get('FinInstrmGnlAttrbts_ShrtNm'),
        'symbol': data.get('FinInstrmGnlAttrbts_ShrtNm'),  # Using short name as symbol if no specific symbol
        'currency': data.get('FinInstrmGnlAttrbts_NtnlCcy'),
        'cfi_code': data.get('FinInstrmGnlAttrbts_ClssfctnTp'),
        'commodity_derivative': str(data.get('FinInstrmGnlAttrbts_CmmdtyDerivInd', 'false')).lower() == 'true',  # Proper boolean conversion
        'lei_id': data.get('Issr'),
        'trading_venue': data.get('TradgVnRltdAttrbts_Id_'),
        'issuer_req': data.get('TradgVnRltdAttrbts_IssrReq'),  # Keep as string, not boolean
        'first_trade_date': parse_date(data.get('TradgVnRltdAttrbts_FrstTradDt')),
        'termination_date': parse_date(data.get('TradgVnRltdAttrbts_TermntnDt')),
        'relevant_authority': data.get('TechAttrbts_RlvntCmptntAuthrty'),
        'relevant_venue': data.get('TechAttrbts_RlvntTradgVn'),
        'from_date': parse_date(data.get('TechAttrbts_PblctnPrd_FrDt'))
    }
    
    logger.info(f"DEBUG: mapped issuer_req value: {model_data.get('issuer_req')} (type: {type(model_data.get('issuer_req'))})")
    
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
