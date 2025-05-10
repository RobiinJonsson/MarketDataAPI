import os
import yaml
import logging
from typing import Dict, Any, List, Optional, Type, Union, Tuple
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, date
from functools import lru_cache
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
        self._schema_cache = {}
        self.load_mappings()
    
    @lru_cache(maxsize=32)
    def get_schema_version(self, schema_name: str) -> Tuple[str, SchemaMapping]:
        """Get latest version of a schema"""
        if schema_name not in self.mappings:
            raise ValueError(f"Unknown schema: {schema_name}")
        return self.mappings[schema_name].version, self.mappings[schema_name]

    def get_schema_fields(self, schema_name: str) -> List[SchemaField]:
        """Get fields for a schema including inherited fields"""
        if schema_name not in self.mappings:
            raise ValueError(f"Unknown schema: {schema_name}")
            
        return self._get_all_fields(schema_name)
    
    def load_mappings(self) -> None:
        """Load all schema mappings from YAML files"""
        mapping_dir = Path(__file__).parent / "mappings"
        if not mapping_dir.exists():
            raise ValueError(f"Schema mapping directory not found: {mapping_dir}")
            
        loaded = {}
        # Load base schema first
        base_path = mapping_dir / "base.yaml"
        if base_path.exists():
            loaded["base"] = self._load_schema_file(base_path)
            
        # Load other schemas
        for file in mapping_dir.glob("*.yaml"):
            if file.stem != "base":
                loaded[file.stem] = self._load_schema_file(file)
                
        self.mappings = loaded
    
    def _load_schema_file(self, path: Path) -> SchemaMapping:
        """Load and validate a single schema file"""
        with open(path) as f:
            data = yaml.safe_load(f)
            try:
                fields = [SchemaField(**field) for field in data["fields"]]
                return SchemaMapping(
                    version=data["version"],
                    name=data["name"],
                    description=data["description"],
                    fields=fields,
                    extends=data.get("extends")
                )
            except (KeyError, TypeError) as e:
                logger.error(f"Error loading schema from {path}: {e}")
                raise ValueError(f"Invalid schema file: {path}")

    def map_to_schema(self, instrument: Union[Instrument, Dict[str, Any]], schema_name: str) -> Dict[str, Any]:
        """Map instrument data to requested schema format"""
        if schema_name not in self.mappings:
            raise ValueError(f"Unknown schema: {schema_name}")

        # Handle both dict and model instances
        if isinstance(instrument, dict):
            return self._map_dict_to_schema(instrument, schema_name)
        else:
            return self._map_model_to_schema(instrument, schema_name)

    def _map_dict_to_schema(self, data: Dict[str, Any], schema_name: str) -> Dict[str, Any]:
        """Map dictionary data to schema format"""
        mapping = self.mappings[schema_name]
        result = {}
        fields = self._get_all_fields(schema_name)
        
        for field in fields:
            try:
                value = data.get(field.source)
                if value is not None and field.transformation:
                    value = self._apply_transformation(value, field.transformation)
                if value is not None or field.required:
                    result[field.name] = value
            except Exception as e:
                logger.error(f"Error processing field {field.name}: {str(e)}")
                if field.required:
                    raise
                result[field.name] = None

        return result

    def _map_model_to_schema(self, instrument: Instrument, schema_name: str) -> Dict[str, Any]:
        """Map model instance to schema format"""
        expected_type = self.type_mapping.get(schema_name)
        if expected_type and not isinstance(instrument, expected_type):
            raise ValueError(f"Invalid instrument type for schema {schema_name}")

        return self._map_dict_to_schema(instrument.__dict__, schema_name)

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

    def output_as_xml(self, data: Dict[str, Any]) -> str:
        """Convert mapped data to XML format"""
        from dicttoxml import dicttoxml
        xml_bytes = dicttoxml(data, custom_root='instrument', attr_type=False)
        return xml_bytes.decode('utf-8')  # Convert bytes to string
