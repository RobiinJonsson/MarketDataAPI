from typing import Dict, Any
from ..models.instrument import Instrument, Equity, Debt

# Add model mapping to complement existing field mappings
MODEL_FIELD_MAPPING = {
    'instruments': {
        'FinInstrmGnlAttrbts_Id': 'isin',
        'FinInstrmGnlAttrbts_FullNm': 'full_name',
        # ...existing field mappings...
    },
    'debts': {
        'DebtInstrmAttrbts_TtlIssdNmnlAmt': 'total_issued_nominal',
        # ...existing debt mappings...
    }
}

def map_to_model(data: Dict[str, Any], instrument_type: str = 'equity') -> Dict[str, Any]:
    """Maps XML/API data to SQLAlchemy model fields"""
    mapped_data = {}
    
    # Map base instrument fields
    for xml_field, model_field in MODEL_FIELD_MAPPING['instruments'].items():
        if xml_field in data:
            mapped_data[model_field] = data[xml_field]
    
    # Map type-specific fields
    if instrument_type == 'debt' and 'debts' in MODEL_FIELD_MAPPING:
        for xml_field, model_field in MODEL_FIELD_MAPPING['debts'].items():
            if xml_field in data:
                mapped_data[model_field] = data[xml_field]
    
    return mapped_data
