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

def map_to_model(data: Dict[str, Any], instrument_type: str = 'equity') -> Dict[str, Any]:
    """Maps XML/API data to SQLAlchemy model fields"""
    mapped_data = {}
    
    # Map base instrument fields
    for xml_field, model_field in MODEL_FIELD_MAPPING['instruments'].items():
        if xml_field in data:
            mapped_data[model_field] = data[xml_field]
    
    # Map type-specific fields with type conversion
    if instrument_type == 'debt' and 'debts' in MODEL_FIELD_MAPPING:
        for xml_field, (model_field, converter) in MODEL_FIELD_MAPPING['debts'].items():
            if xml_field in data:
                try:
                    mapped_data[model_field] = converter(data[xml_field])
                except (ValueError, TypeError):
                    continue  # Skip conversion if it fails
    
    return mapped_data
