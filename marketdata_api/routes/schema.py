import yaml
from flask import Blueprint, jsonify, request, Response
from typing import Dict, Any
from ..schema.schema_mapper import SchemaMapper
from ..database.session import get_session
from ..models.instrument import Instrument
import os

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