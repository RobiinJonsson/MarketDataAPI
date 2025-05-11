import yaml
import logging
from flask import Blueprint, jsonify, request, Response
from typing import Dict, Any
from ..schema.schema_mapper import SchemaMapper
from ..database.session import get_session
from ..models.instrument import Instrument
import os

logger = logging.getLogger(__name__)
schema_bp = Blueprint("schema", __name__)

@schema_bp.route('/api/schema/search', methods=['POST'])
def schema_search():
    """Endpoint to search using a schema-based query."""
    try:
        data = request.get_json()
        if not data or 'filters' not in data:
            return jsonify({"error": "No filters provided"}), 400

        schema_name = data.get('schema_type', 'base')
        output_format = data.get('format', 'json').lower()
        mapper = SchemaMapper()

        with get_session() as session:
            # Get instrument
            instrument = session.query(Instrument).filter(
                Instrument.isin == data['filters']['identifier']
            ).first()

            if not instrument:
                return jsonify({"error": "Instrument not found"}), 404

            try:
                version, _ = mapper.get_schema_version(schema_name)
                result = mapper.map_to_schema(instrument, schema_name)
                
                response = {
                    "results": [result],
                    "count": 1,
                    "schema": schema_name,
                    "version": version,
                    "unmapped_fields": []  # Add empty list for frontend compatibility
                }

                if output_format == 'xml':
                    xml_data = mapper.output_as_xml(response)
                    return Response(xml_data, mimetype='application/xml')
                    
                return jsonify(response)

            except ValueError as e:
                return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@schema_bp.route('/api/schema/validate', methods=['POST'])
def validate_schema():
    """Validate a schema definition"""
    try:
        schema_data = request.get_json()
        if not schema_data:
            return jsonify({"error": "No schema provided"}), 400

        mapper = SchemaMapper()
        is_valid = mapper.validate_value(schema_data, None)  # None as field for basic validation
        
        return jsonify({
            "valid": is_valid,
            "schema": schema_data.get('name', 'unknown')
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@schema_bp.route('/api/schema/examples/<path:filename>', methods=['GET'])
def get_example_schema(filename):
    """Serve example schema files"""
    examples_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'examples', 'schemas')
    try:
        with open(os.path.join(examples_dir, filename)) as f:
            content = f.read()
            return Response(content, mimetype='application/x-yaml')
    except FileNotFoundError:
        return jsonify({"error": "Schema example not found"}), 404

@schema_bp.route('/api/schema', methods=['POST'])
def create_schema():
    """Create a new schema"""
    try:
        content_type = request.headers.get('Content-Type', '')
        
        if 'yaml' in content_type.lower():
            # Handle YAML input
            schema_data = yaml.safe_load(request.data)
        else:
            # Handle JSON input
            schema_data = request.get_json()
            
        if not schema_data:
            return jsonify({"error": "No schema data provided"}), 400

        mapper = SchemaMapper()
        name = schema_data.get('name')
        
        # Check for existing schema
        if name in mapper.mappings:
            return jsonify({"error": f"Schema {name} already exists"}), 409
            
        # Add schema to registry
        mapper.add_schema(schema_data)
        version, schema = mapper.get_schema_version(name)
        
        return jsonify({
            "message": "Schema created successfully",
            "schema": name,
            "version": version
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@schema_bp.route('/api/schema/<name>', methods=['GET'])
def get_schema(name):
    """Get schema by name"""
    try:
        mapper = SchemaMapper()
        version = request.args.get('version')
        
        if version:
            schema = mapper.get_schema_by_version(name, version)
        else:
            _, schema = mapper.get_schema_version(name)
            
        if not schema:
            return jsonify({"error": "Schema not found"}), 404
            
        return jsonify(schema)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@schema_bp.route('/api/schema/<name>', methods=['PUT'])
def update_schema(name):
    """Update existing schema"""
    try:
        schema_data = request.get_json()
        if not schema_data:
            return jsonify({"error": "No schema data provided"}), 400

        # Validate schema name matches URL
        if schema_data.get('name') != name:
            return jsonify({"error": f"Schema name in data ({schema_data.get('name')}) does not match URL param ({name})"}), 400

        mapper = SchemaMapper()
        if name not in mapper.mappings:
            return jsonify({"error": f"Schema '{name}' not found"}), 404
            
        try:
            # Update schema with version increment
            mapper.update_schema(name, schema_data)
            version, schema = mapper.get_schema_version(name)
            
            return jsonify({
                "message": "Schema updated successfully",
                "schema": name,
                "version": version,
                "fields": len(schema.fields)
            })

        except ValueError as ve:
            return jsonify({"error": f"Schema update failed: {str(ve)}"}), 400
        except Exception as e:
            logger.error(f"Error updating schema: {str(e)}")
            return jsonify({"error": f"Internal error updating schema: {str(e)}"}), 500

    except Exception as e:
        logger.error(f"Schema update route error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@schema_bp.route('/api/schema/<name>', methods=['DELETE'])
def delete_schema(name):
    """Delete schema"""
    try:
        mapper = SchemaMapper()
        force = request.args.get('force', '').lower() == 'true'
        
        if name not in mapper.mappings:
            return jsonify({"error": "Schema not found"}), 404
            
        # Check for dependencies unless force=true
        if not force and mapper.has_dependents(name):
            return jsonify({"error": "Schema has dependent schemas"}), 409
            
        mapper.delete_schema(name)
        return jsonify({"message": "Schema deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@schema_bp.route('/api/schema/<name>/versions', methods=['GET'])
def get_schema_versions(name):
    """Get schema version history"""
    try:
        mapper = SchemaMapper()
        if name not in mapper.mappings:
            return jsonify({"error": "Schema not found"}), 404
            
        versions = mapper.get_schema_versions(name)
        return jsonify({
            "schema": name,
            "versions": versions
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500