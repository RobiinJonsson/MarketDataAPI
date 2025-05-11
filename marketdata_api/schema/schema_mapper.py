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
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class SchemaMapper:
    def __init__(self):
        self.mappings: Dict[str, SchemaMapping] = {}
        self.type_mapping = {
            "equity": Equity,
            "debt": Debt,
            "base": Instrument
        }
        self._schema_cache = {}
        self._version_history = {}  # Store version history
        self._dependents = {}  # Track schema dependencies
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
            # Initialize version history for base schema
            self._version_history["base"] = {
                loaded["base"].version: self._schema_to_dict(loaded["base"])
            }
            
        # Load other schemas
        for file in mapping_dir.glob("*.yaml"):
            if file.stem != "base":
                schema = self._load_schema_file(file)
                loaded[file.stem] = schema
                # Initialize version history for each schema
                self._version_history[file.stem] = {
                    schema.version: self._schema_to_dict(schema)
                }
                
        self.mappings = loaded

    def _schema_to_dict(self, schema: SchemaMapping) -> Dict[str, Any]:
        """Convert SchemaMapping to dictionary for version history"""
        return {
            "version": schema.version,
            "name": schema.name,
            "description": schema.description,
            "fields": [vars(f) for f in schema.fields],
            "extends": schema.extends,
            "created_at": schema.created_at,
            "updated_at": schema.updated_at
        }

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
                    extends=data.get("extends"),
                    created_at=data.get("created_at"),
                    updated_at=data.get("updated_at")
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

    def _save_schema_to_file(self, schema_data: Dict[str, Any], version: str) -> None:
        """Save schema to filesystem with version"""
        name = schema_data['name']
        mapping_dir = Path(__file__).parent / "mappings"
        mapping_dir.mkdir(exist_ok=True)  # Ensure directory exists
        
        # Save current version
        schema_path = mapping_dir / f"{name}.yaml"
        with open(schema_path, 'w') as f:
            yaml.dump(schema_data, f, sort_keys=False, default_flow_style=False)
            
        # Save versioned copy
        versions_dir = mapping_dir / "versions" / name
        versions_dir.mkdir(parents=True, exist_ok=True)
        version_path = versions_dir / f"{name}_v{version}.yaml"
        with open(version_path, 'w') as f:
            yaml.dump(schema_data, f, sort_keys=False, default_flow_style=False)

    def add_schema(self, schema_data: Dict[str, Any]) -> None:
        """Add new schema to registry"""
        name = schema_data.get('name')
        if not name:
            raise ValueError("Schema must have a name")
            
        # Store initial version
        schema_data['version'] = '1.0'
        schema_data['created_at'] = datetime.now().isoformat()
        
        # Save to filesystem with versioning
        self._save_schema_to_file(schema_data, '1.0')
            
        # Add to memory
        self.mappings[name] = SchemaMapping(**schema_data)
        self._version_history[name] = {
            '1.0': schema_data.copy()
        }
        
        # Track dependencies
        if schema_data.get('extends'):
            parent = schema_data['extends']
            if parent not in self._dependents:
                self._dependents[parent] = set()
            self._dependents[parent].add(name)

    def update_schema(self, name: str, schema_data: Dict[str, Any]) -> None:
        """Update existing schema with version increment"""
        if name not in self.mappings:
            raise ValueError(f"Schema '{name}' not found")
            
        try:
            logger.info(f"Updating schema {name}")
            
            # Initialize version history if it doesn't exist
            if name not in self._version_history:
                self._version_history[name] = {
                    self.mappings[name].version: self.mappings[name].__dict__
                }
            
            # Get current version and increment
            current = self.mappings[name].version
            major, minor = current.split('.')
            new_version = f"{major}.{int(minor) + 1}"
            logger.info(f"Incrementing version from {current} to {new_version}")
            
            # Update metadata but preserve created_at if it exists
            schema_data['version'] = new_version
            schema_data['updated_at'] = datetime.now().isoformat()
            if hasattr(self.mappings[name], 'created_at'):
                schema_data['created_at'] = self.mappings[name].created_at
            
            try:
                # Convert raw field dicts to SchemaField objects
                fields = []
                for field_data in schema_data.get('fields', []):
                    logger.debug(f"Processing field: {field_data}")
                    field = SchemaField(
                        name=field_data['name'],
                        source=field_data['source'],
                        type=field_data['type'],
                        required=field_data['required'],
                        description=field_data['description'],
                        transformation=field_data.get('transformation')
                    )
                    fields.append(field)
            except Exception as field_error:
                logger.error(f"Field processing error: {field_error}")
                raise ValueError(f"Invalid field data: {field_error}")

            try:
                # Create new schema mapping
                new_mapping = SchemaMapping(
                    version=new_version,
                    name=schema_data['name'],
                    description=schema_data['description'],
                    fields=fields,
                    extends=schema_data.get('extends'),
                    created_at=schema_data.get('created_at'),
                    updated_at=schema_data['updated_at']
                )
                logger.info(f"Created new mapping object: {new_mapping}")
            except Exception as mapping_error:
                logger.error(f"Schema mapping creation error: {mapping_error}")
                raise ValueError(f"Invalid schema mapping: {mapping_error}")

            # Save to filesystem
            self._save_schema_to_file(schema_data, new_version)
            
            # Update memory storage
            self.mappings[name] = new_mapping
            self._version_history[name][new_version] = schema_data

        except Exception as e:
            logger.error(f"Schema update error for {name}: {str(e)}", exc_info=True)
            raise ValueError(f"Failed to update schema: {str(e)}")

    def get_schema_by_version(self, name: str, version: str) -> Optional[SchemaMapping]:
        """Get specific version of a schema"""
        if name not in self._version_history:
            return None
        schema_data = self._version_history[name].get(version)
        return SchemaMapping(**schema_data) if schema_data else None

    def get_schema_versions(self, name: str) -> List[Dict[str, Any]]:
        """Get version history for a schema"""
        if name not in self._version_history:
            return []
        
        versions = []
        for version, schema in self._version_history[name].items():
            versions.append({
                'version': version,
                'timestamp': schema.get('updated_at', schema.get('created_at', '')),
                'description': schema.get('description', ''),
                'extends': schema.get('extends'),
                'fields_count': len(schema.get('fields', [])),
                'created_at': schema.get('created_at', ''),
                'updated_at': schema.get('updated_at', '')
            })
        return sorted(versions, key=lambda x: x['version'])

    def has_dependents(self, name: str) -> bool:
        """Check if schema has dependent schemas"""
        return name in self._dependents and bool(self._dependents[name])

    def delete_schema(self, name: str) -> None:
        """Delete schema from registry"""
        if name not in self.mappings:
            raise ValueError(f"Schema {name} not found")
            
        # Check dependencies first
        if self.has_dependents(name):
            raise ValueError(f"Cannot delete schema {name}: has dependent schemas")
            
        # Get parent info before deletion
        schema = self.mappings[name]
        parent = schema.extends
            
        # Remove from main registry
        del self.mappings[name]
        
        # Update dependencies
        if parent and parent in self._dependents:
            self._dependents[parent].remove(name)
        if name in self._dependents:
            del self._dependents[name]
