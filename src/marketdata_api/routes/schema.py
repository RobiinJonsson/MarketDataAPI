import logging
import os
from typing import Any, Dict

import yaml
from flask import Blueprint, Response, jsonify, request

from ..constants import (
    ErrorMessages,
    FormFields,
    HTTPStatus,
    QueryParams,
    ResponseFields,
    SuccessMessages,
)
from ..database.session import get_session
from ..schema.schema_mapper import SchemaMapper

logger = logging.getLogger(__name__)
schema_bp = Blueprint("schema", __name__)


@schema_bp.route("/api/schema/search", methods=["POST"])
def schema_search():
    """Endpoint to search using a schema-based query."""
    try:
        data = request.get_json()
        if not data or "filters" not in data:
            return (
                jsonify({ResponseFields.ERROR: ErrorMessages.NO_FILTERS_PROVIDED}),
                HTTPStatus.BAD_REQUEST,
            )

        schema_name = data.get("schema_type", "base")
        output_format = data.get("format", "json").lower()
        mapper = SchemaMapper()

        # Get the correct Instrument model with direct import
        from ..models.sqlite.instrument import Instrument

        with get_session() as session:
            # Get instrument
            instrument = (
                session.query(Instrument)
                .filter(Instrument.isin == data["filters"]["identifier"])
                .first()
            )

            if not instrument:
                return (
                    jsonify({ResponseFields.ERROR: ErrorMessages.INSTRUMENT_NOT_FOUND}),
                    HTTPStatus.NOT_FOUND,
                )

            # Check if we need to load a specific subtype
            instrument_type = instrument.type.lower()
            logger.debug(f"Found instrument of type: {instrument_type}")
            # If schema_name is 'base', use the instrument's actual type if it matches a schema
            if schema_name == "base" and instrument_type in mapper.type_mapping:
                schema_name = instrument_type
                logger.debug(f"Using instrument type schema: {schema_name}")

            try:
                version, _ = mapper.get_schema_version(schema_name)
                result = mapper.map_to_schema(instrument, schema_name)

                response = {
                    "results": [result],
                    "count": 1,
                    "schema": schema_name,
                    "version": version,
                    "unmapped_fields": [],  # Add empty list for frontend compatibility
                }

                if output_format == "xml":
                    xml_data = mapper.output_as_xml(response)
                    return Response(xml_data, mimetype="application/xml")

                return jsonify(response)

            except ValueError as e:
                return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.BAD_REQUEST

    except Exception as e:
        logger.error(f"Schema search error: {str(e)}", exc_info=True)
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@schema_bp.route("/api/schema/validate", methods=["POST"])
def validate_schema():
    """Validate a schema definition"""
    try:
        schema_data = request.get_json()
        if not schema_data:
            return (
                jsonify({ResponseFields.ERROR: ErrorMessages.NO_SCHEMA_DATA}),
                HTTPStatus.BAD_REQUEST,
            )

        mapper = SchemaMapper()
        is_valid = mapper.validate_value(schema_data, None)  # None as field for basic validation

        return jsonify({"valid": is_valid, "schema": schema_data.get("name", "unknown")})

    except Exception as e:
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.BAD_REQUEST


@schema_bp.route("/api/schema/examples/<path:filename>", methods=["GET"])
def get_example_schema(filename):
    """Serve example schema files"""
    examples_dir = os.path.join(os.path.dirname(__file__), "..", "..", "examples", "schemas")
    try:
        with open(os.path.join(examples_dir, filename)) as f:
            content = f.read()
            return Response(content, mimetype="application/x-yaml")
    except FileNotFoundError:
        return (
            jsonify({ResponseFields.ERROR: ErrorMessages.SCHEMA_EXAMPLE_NOT_FOUND}),
            HTTPStatus.NOT_FOUND,
        )


@schema_bp.route("/api/schema", methods=["POST"])
def create_schema():
    """Create a new schema"""
    try:
        content_type = request.headers.get("Content-Type", "")

        if "yaml" in content_type.lower():
            # Handle YAML input
            schema_data = yaml.safe_load(request.data)
        else:
            # Handle JSON input
            schema_data = request.get_json()

        if not schema_data:
            return (
                jsonify({ResponseFields.ERROR: ErrorMessages.NO_SCHEMA_DATA}),
                HTTPStatus.BAD_REQUEST,
            )

        mapper = SchemaMapper()
        name = schema_data.get("name")

        # Check for existing schema
        if name in mapper.mappings:
            return jsonify({ResponseFields.ERROR: ErrorMessages.SCHEMA_EXISTS}), HTTPStatus.CONFLICT

        # Add schema to registry
        mapper.add_schema(schema_data)
        version, schema = mapper.get_schema_version(name)

        return (
            jsonify(
                {
                    ResponseFields.MESSAGE: SuccessMessages.SCHEMA_CREATED,
                    "schema": name,
                    "version": version,
                }
            ),
            HTTPStatus.CREATED,
        )

    except Exception as e:
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@schema_bp.route("/api/schema/<name>", methods=["GET"])
def get_schema(name):
    """Get schema by name"""
    try:
        mapper = SchemaMapper()
        version = request.args.get("version")

        if version:
            schema = mapper.get_schema_by_version(name, version)
        else:
            _, schema = mapper.get_schema_version(name)

        if not schema:
            return (
                jsonify({ResponseFields.ERROR: ErrorMessages.SCHEMA_NOT_FOUND}),
                HTTPStatus.NOT_FOUND,
            )

        return jsonify(schema)

    except Exception as e:
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@schema_bp.route("/api/schema/<name>", methods=["PUT"])
def update_schema(name):
    """Update existing schema"""
    try:
        schema_data = request.get_json()
        if not schema_data:
            return (
                jsonify({ResponseFields.ERROR: ErrorMessages.NO_SCHEMA_DATA}),
                HTTPStatus.BAD_REQUEST,
            )

        # Validate schema name matches URL
        if schema_data.get("name") != name:
            return (
                jsonify({ResponseFields.ERROR: ErrorMessages.SCHEMA_NAME_MISMATCH}),
                HTTPStatus.BAD_REQUEST,
            )

        mapper = SchemaMapper()
        if name not in mapper.mappings:
            return (
                jsonify({ResponseFields.ERROR: ErrorMessages.SCHEMA_NOT_FOUND}),
                HTTPStatus.NOT_FOUND,
            )

        try:
            # Update schema with version increment
            mapper.update_schema(name, schema_data)
            version, schema = mapper.get_schema_version(name)

            return jsonify(
                {
                    ResponseFields.MESSAGE: SuccessMessages.SCHEMA_UPDATED,
                    "schema": name,
                    "version": version,
                    "fields": len(schema.fields),
                }
            )

        except ValueError as ve:
            return (
                jsonify({ResponseFields.ERROR: f"Schema update failed: {str(ve)}"}),
                HTTPStatus.BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Error updating schema: {str(e)}")
            return (
                jsonify({ResponseFields.ERROR: f"Internal error updating schema: {str(e)}"}),
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    except Exception as e:
        logger.error(f"Schema update route error: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@schema_bp.route("/api/schema/<name>", methods=["DELETE"])
def delete_schema(name):
    """Delete schema"""
    try:
        mapper = SchemaMapper()
        force = request.args.get("force", "").lower() == "true"

        if name not in mapper.mappings:
            return (
                jsonify({ResponseFields.ERROR: ErrorMessages.SCHEMA_NOT_FOUND}),
                HTTPStatus.NOT_FOUND,
            )

        # Check for dependencies unless force=true
        if not force and mapper.has_dependents(name):
            return (
                jsonify({ResponseFields.ERROR: ErrorMessages.SCHEMA_HAS_DEPENDENTS}),
                HTTPStatus.CONFLICT,
            )

        mapper.delete_schema(name)
        return jsonify({ResponseFields.MESSAGE: SuccessMessages.SCHEMA_DELETED})

    except Exception as e:
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@schema_bp.route("/api/schema/<name>/versions", methods=["GET"])
def get_schema_versions(name):
    """Get schema version history"""
    try:
        mapper = SchemaMapper()
        if name not in mapper.mappings:
            return (
                jsonify({ResponseFields.ERROR: ErrorMessages.SCHEMA_NOT_FOUND}),
                HTTPStatus.NOT_FOUND,
            )

        versions = mapper.get_schema_versions(name)
        return jsonify({"schema": name, "versions": versions})

    except Exception as e:
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
