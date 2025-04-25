import yaml
from flask import Blueprint, jsonify, request
from marketdata_api.database.db import DB_PATH
import sqlite3
from typing import Dict, Any, Tuple, List, Set, Union
from marketdata_api.config import SCHEMA_REGISTRY, SCHEMA_TO_DB_MAPPING, SchemaField, SchemaDefinition
import os

schema_bp = Blueprint("schema", __name__)

def load_schema(schema_source: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Load a schema from either a file path, a YAML string, or a dictionary.
    If loading from a file, the schema must include a 'type' field that matches a schema in the registry.
    
    Args:
        schema_source: Either a file path to a YAML schema, a YAML string, or a dictionary containing the schema
        
    Returns:
        Dict containing the loaded and validated schema
        
    Raises:
        ValueError: If the schema is invalid or the type is not found in the registry
    """
    # If schema_source is already a dictionary, use it directly
    if isinstance(schema_source, dict):
        schema = schema_source
    else:
        try:
            # First try to parse as YAML string
            schema = yaml.safe_load(schema_source)
        except yaml.YAMLError:
            # If that fails, try to load as a file
            if not os.path.exists(schema_source):
                raise ValueError(f"Schema file not found: {schema_source}")
            
            with open(schema_source, 'r') as file:
                schema = yaml.safe_load(file)
    
    # Validate that the schema has a type that exists in the registry
    if 'type' not in schema:
        raise ValueError("Schema must specify a type")
    
    schema_type = schema['type']
    if schema_type not in SCHEMA_REGISTRY:
        raise ValueError(f"Unknown schema type: {schema_type}")
    
    return schema

def get_schema_fields(schema_name: str, visited: Set[str] = None) -> List[SchemaField]:
    """Get all fields for a schema, including inherited fields."""
    if visited is None:
        visited = set()
    
    if schema_name in visited:
        return []
    
    visited.add(schema_name)
    schema = SCHEMA_REGISTRY[schema_name]
    fields = schema.fields.copy()
    
    # Add fields from extended schema
    if schema.extends:
        fields.extend(get_schema_fields(schema.extends, visited))
    
    return fields

def validate_schema(schema: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate the schema structure against the registry.
    Returns (is_valid, error_message)
    """
    try:
        # Check if schema type is specified
        if 'type' not in schema:
            return False, "Schema must specify a type"
        
        schema_type = schema['type']
        if schema_type not in SCHEMA_REGISTRY:
            return False, f"Unknown schema type: {schema_type}"
        
        # Get all fields including inherited ones
        all_fields = get_schema_fields(schema_type)
        required_fields = {f.name for f in all_fields if f.required}
        
        # Check for required fields
        missing_fields = []
        for field in required_fields:
            if field not in schema.get('properties', {}):
                missing_fields.append(field)
        
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        return True, "Schema is valid"
    
    except Exception as e:
        return False, f"Error validating schema: {str(e)}"

def search_by_schema(schema: Dict[str, Any], filters: Dict[str, Any]) -> Tuple[list, list]:
    """
    Search the database using the provided schema and filters.
    Returns a tuple of (results, unmapped_fields)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get all available columns from the database
        cursor.execute("PRAGMA table_info(firds_e)")
        available_columns = [col[1] for col in cursor.fetchall()]

        # Build the SQL query based on the schema and filters
        query = "SELECT * FROM firds_e WHERE 1=1"
        params = []

        print(f"Received filters: {filters}")  # Debug print

        # Only use the identifier field for searching
        if 'identifier' in filters:
            query += f" AND {SCHEMA_TO_DB_MAPPING['identifier']} = ?"
            params.append(filters['identifier'])

        print(f"Generated SQL query: {query}")  # Debug print
        print(f"Query parameters: {params}")    # Debug print

        cursor.execute(query, params)
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Track unmapped fields
        unmapped_fields = []

        # Process the results to match the requested schema
        processed_results = []
        for result in results:
            processed_result = {}
            # Map database columns to schema fields
            for schema_field, include in schema.get('properties', {}).items():
                if include:  # Only include fields that are requested
                    # Try to find the corresponding database column
                    db_column = SCHEMA_TO_DB_MAPPING.get(schema_field)
                    if db_column and db_column in result:
                        processed_result[schema_field] = result[db_column]
                    else:
                        # Field is not mapped or not in database, set to None
                        processed_result[schema_field] = None
                        if schema_field not in unmapped_fields:
                            unmapped_fields.append(schema_field)
            
            processed_results.append(processed_result)

        print(f"Found {len(processed_results)} results")  # Debug print
        return processed_results, unmapped_fields

    finally:
        conn.close()

@schema_bp.route('/api/schema/search', methods=['POST'])
def schema_search():
    """Endpoint to search using a schema-based query."""
    try:
        data = request.get_json()
        if not data or 'filters' not in data:
            return jsonify({"error": "No filters provided"}), 400

        print(f"Received request data: {data}")  # Debug print

        # Get the schema from the request
        if 'schema' not in data:
            return jsonify({"error": "No schema provided"}), 400

        # Parse the schema from the request
        try:
            schema = load_schema(data['schema'])
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        # Validate the schema
        is_valid, error_message = validate_schema(schema)
        if not is_valid:
            return jsonify({"error": f"Invalid schema: {error_message}"}), 400
        
        # Perform the search
        results, unmapped_fields = search_by_schema(schema, data['filters'])
        
        return jsonify({
            "count": len(results),
            "results": results,
            "unmapped_fields": unmapped_fields
        })

    except Exception as e:
        print(f"Error in schema_search: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 500 