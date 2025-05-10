import os
import yaml
import logging
from typing import Dict, Any, List, Optional, Type, Union
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, date
from ..models.instrument import Instrument, Equity, Debt

logger = logging.getLogger(__name__)

@dataclass
class SchemaField:
    name: str
    source: str
    type: str
    required: bool
    description: str
    transformation: Optional[str] = None

@dataclass
class SchemaMapping:
    version: str
    name: str
    description: str
    fields: List[SchemaField]
    extends: Optional[str] = None

class SchemaMapper:
    def __init__(self):
        self.mappings: Dict[str, SchemaMapping] = {}
        self.type_mapping = {
            "equity": Equity,
            "debt": Debt,
            "base": Instrument
        }
        self.load_mappings()
    
    def load_mappings(self) -> None:
        """Load all schema mappings from YAML files"""
        mapping_dir = Path(__file__).parent / "mappings"
        for file in mapping_dir.glob("*.yaml"):
            with open(file) as f:
                data = yaml.safe_load(f)
                fields = [SchemaField(**field) for field in data["fields"]]
                self.mappings[data["name"]] = SchemaMapping(
                    version=data["version"],
                    name=data["name"],
                    description=data["description"],
                    fields=fields,
                    extends=data.get("extends")
                )

    def map_to_schema(self, instrument: Instrument, schema_name: str) -> Dict[str, Any]:
        """Map instrument data to requested schema format"""
        if schema_name not in self.mappings:
            raise ValueError(f"Unknown schema: {schema_name}")

        # Validate instrument type matches schema
        expected_type = self.type_mapping.get(schema_name)
        if expected_type and not isinstance(instrument, expected_type):
            raise ValueError(f"Invalid instrument type for schema {schema_name}")

        try:
            mapping = self.mappings[schema_name]
            result = {}
            fields = self._get_all_fields(schema_name)
            
            for field in fields:
                try:
                    value = self._get_field_value(instrument, field)
                    if not self.validate_value(value, field):
                        logger.warning(f"Invalid value for field {field.name}: {value}")
                        value = None
                    if value is not None or field.required:
                        result[field.name] = value
                except Exception as e:
                    logger.error(f"Error processing field {field.name}: {str(e)}")
                    if field.required:
                        raise
                    result[field.name] = None

            return result
        except Exception as e:
            logger.error(f"Error mapping schema {schema_name}: {str(e)}")
            raise

    def _get_all_fields(self, schema_name: str, visited=None) -> List[SchemaField]:
        """Get all fields including from extended schemas"""
        if visited is None:
            visited = set()
        
        if schema_name in visited:
            return []
            
        visited.add(schema_name)
        mapping = self.mappings[schema_name]
        fields = mapping.fields.copy()
        
        if mapping.extends:
            fields.extend(self._get_all_fields(mapping.extends, visited))
            
        return fields

    def _get_field_value(self, instrument: Instrument, field: SchemaField) -> Any:
        """Get field value using source mapping"""
        try:
            value = getattr(instrument, field.source, None)
            if value is not None and field.transformation:
                value = self._apply_transformation(value, field.transformation)
            return value
        except AttributeError:
            return None

    def _apply_transformation(self, value: Any, transformation: str) -> Any:
        """Apply transformation rule to value"""
        try:
            if not transformation:
                return value
                
            if transformation.startswith("round"):
                decimals = int(transformation.split("(")[1].split(")")[0])
                return round(float(value), decimals)
                
            if transformation.startswith("format"):
                format_str = transformation.split("(")[1].split(")")[0]
                if isinstance(value, (datetime, date)):
                    return value.strftime(format_str)
                return value
                
            if transformation == "upper":
                return str(value).upper()
                
            if transformation == "lower":
                return str(value).lower()
                
            logger.warning(f"Unknown transformation: {transformation}")
            return value
        except Exception as e:
            logger.error(f"Transformation error: {str(e)}")
            return value

    def validate_value(self, value: Any, field: SchemaField) -> bool:
        """Validate a value against field requirements"""
        try:
            if field.required and value is None:
                return False
                
            if value is None:
                return True
                
            if field.type == "number":
                return isinstance(value, (int, float))
            elif field.type == "date":
                return isinstance(value, (datetime, date))
            elif field.type == "string":
                return isinstance(value, str)
            elif field.type == "boolean":
                return isinstance(value, bool)
                
            return True
        except Exception as e:
            logger.error(f"Validation error for field {field.name}: {str(e)}")
            return False
