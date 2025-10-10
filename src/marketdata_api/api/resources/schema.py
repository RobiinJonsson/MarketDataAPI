"""
Schema API Resources

This module contains Flask-RESTx resource definitions for schema-related endpoints.
Migrated from routes/schema.py to provide proper Swagger documentation.
"""

import logging
import os
from typing import Any, Dict

import yaml
from flask import current_app, request
from flask_restx import Namespace, Resource

from ...constants import ErrorMessages, HTTPStatus, ResponseFields

logger = logging.getLogger(__name__)


def create_schema_resources(api, models):
    """
    Create and register schema-related API resources.

    Args:
        api: Flask-RESTx API instance
        models: Dictionary of registered models

    Returns:
        Namespace: Schema namespace with registered resources
    """

    # Create namespace
    schema_ns = api.namespace("schema", description="Schema management operations")

    # Get model references
    schema_models = models["schema"]
    common_models = models["common"]

    @schema_ns.route("/search")
    class SchemaSearch(Resource):
        @schema_ns.doc(
            description="Search using a schema-based query",
            responses={
                HTTPStatus.OK: ("Search results", common_models["success_model"]),
                HTTPStatus.BAD_REQUEST: ("Invalid request", common_models["error_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Server error", common_models["error_model"]),
            },
        )
        @schema_ns.expect(schema_models["schema_search_request"])
        def post(self):
            """Search using a schema-based query"""
            try:
                from ...database.session import get_session
                from ...schema.schema_mapper import SchemaMapper

                data = request.get_json()
                if not data:
                    return {
                        ResponseFields.ERROR: ErrorMessages.INVALID_REQUEST_BODY
                    }, HTTPStatus.BAD_REQUEST

                query = data.get("query")
                schema_name = data.get("schema_name")
                limit = data.get("limit", 100)

                if not query:
                    return {
                        ResponseFields.ERROR: "Query is required"
                    }, HTTPStatus.BAD_REQUEST

                with get_session() as session:
                    mapper = SchemaMapper(session)
                    results = mapper.search_by_schema(query, schema_name, limit)

                    return {
                        ResponseFields.MESSAGE: "Search completed successfully",
                        "results": results,
                        "total": len(results),
                    }, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error in schema search: {str(e)}")
                return {
                    ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                    "details": str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @schema_ns.route("/validate")
    class SchemaValidate(Resource):
        @schema_ns.doc(
            description="Validate a schema definition",
            responses={
                HTTPStatus.OK: ("Validation result", schema_models["schema_validation_response"]),
                HTTPStatus.BAD_REQUEST: ("Invalid request", common_models["error_model"]),
            },
        )
        @schema_ns.expect(schema_models["schema_validation_request"])
        @schema_ns.marshal_with(schema_models["schema_validation_response"])
        def post(self):
            """Validate a schema definition"""
            try:
                data = request.get_json()
                if not data:
                    return {
                        "valid": False,
                        "errors": ["Request body is required"],
                        "message": "Invalid request",
                    }, HTTPStatus.BAD_REQUEST

                schema_def = data.get("schema")
                test_data = data.get("data")

                if not schema_def:
                    return {
                        "valid": False,
                        "errors": ["Schema definition is required"],
                        "message": "Schema is required",
                    }, HTTPStatus.BAD_REQUEST

                # Basic validation (you can expand this with jsonschema)
                if not isinstance(schema_def, dict):
                    return {
                        "valid": False,
                        "errors": ["Schema must be a valid JSON object"],
                        "message": "Invalid schema format",
                    }, HTTPStatus.OK

                # If test data is provided, validate it against the schema
                errors = []
                if test_data is not None:
                    # Add your schema validation logic here
                    pass

                return {
                    "valid": len(errors) == 0,
                    "errors": errors,
                    "message": "Schema validation completed",
                }, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error in schema validation: {str(e)}")
                return {
                    "valid": False,
                    "errors": [str(e)],
                    "message": "Validation error",
                }, HTTPStatus.OK

    @schema_ns.route("/examples/<path:filename>")
    @schema_ns.param("filename", "Example schema filename")
    class SchemaExample(Resource):
        @schema_ns.doc(
            description="Get an example schema file",
            responses={
                HTTPStatus.OK: ("Schema example", common_models["success_model"]),
                HTTPStatus.NOT_FOUND: ("Schema not found", common_models["error_model"]),
            },
        )
        def get(self, filename):
            """Serve example schema files"""
            try:
                examples_dir = os.path.join(current_app.root_path, "..", "..", "examples", "schemas")
                file_path = os.path.join(examples_dir, filename)

                if not os.path.exists(file_path) or not os.path.isfile(file_path):
                    return {
                        ResponseFields.ERROR: f"Schema example '{filename}' not found"
                    }, HTTPStatus.NOT_FOUND

                with open(file_path, "r", encoding="utf-8") as f:
                    if filename.endswith((".yml", ".yaml")):
                        schema_content = yaml.safe_load(f)
                    else:
                        schema_content = f.read()

                return {
                    ResponseFields.MESSAGE: "Schema example retrieved successfully",
                    "filename": filename,
                    "content": schema_content,
                }, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error retrieving schema example: {str(e)}")
                return {
                    ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                    "details": str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @schema_ns.route("/")
    class SchemaList(Resource):
        @schema_ns.doc(
            description="List all schemas or create a new schema",
            responses={
                HTTPStatus.OK: ("Schema list", schema_models["schema_list_response"]),
                HTTPStatus.CREATED: ("Schema created", schema_models["schema_definition"]),
                HTTPStatus.BAD_REQUEST: ("Invalid request", common_models["error_model"]),
            },
        )
        @schema_ns.marshal_with(schema_models["schema_list_response"])
        def get(self):
            """List all schemas"""
            try:
                # Add your schema listing logic here
                # This is a placeholder implementation
                schemas = []
                return {
                    "schemas": schemas,
                    "total": len(schemas),
                    "page": 1,
                    "per_page": 100,
                }, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error listing schemas: {str(e)}")
                return {
                    ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                    "details": str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

        @schema_ns.expect(schema_models["schema_definition"])
        @schema_ns.marshal_with(schema_models["schema_definition"])
        def post(self):
            """Create a new schema"""
            try:
                data = request.get_json()
                if not data:
                    return {
                        ResponseFields.ERROR: ErrorMessages.INVALID_REQUEST_BODY
                    }, HTTPStatus.BAD_REQUEST

                name = data.get("name")
                schema_def = data.get("schema")

                if not name or not schema_def:
                    return {
                        ResponseFields.ERROR: "Name and schema definition are required"
                    }, HTTPStatus.BAD_REQUEST

                # Add your schema creation logic here
                # This is a placeholder implementation
                created_schema = {
                    "name": name,
                    "schema": schema_def,
                    "description": data.get("description", ""),
                    "version": data.get("version", "1.0.0"),
                }

                return created_schema, HTTPStatus.CREATED

            except Exception as e:
                logger.error(f"Error creating schema: {str(e)}")
                return {
                    ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                    "details": str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @schema_ns.route("/<string:name>")
    @schema_ns.param("name", "Schema name")
    class SchemaDetail(Resource):
        @schema_ns.doc(
            description="Get, update, or delete a specific schema",
            responses={
                HTTPStatus.OK: ("Schema details", schema_models["schema_definition"]),
                HTTPStatus.NOT_FOUND: ("Schema not found", common_models["error_model"]),
                204: ("Schema deleted", None),
            },
        )
        @schema_ns.marshal_with(schema_models["schema_definition"])
        def get(self, name):
            """Get a schema by name"""
            try:
                # Add your schema retrieval logic here
                # This is a placeholder implementation
                return {
                    ResponseFields.ERROR: f"Schema '{name}' not found"
                }, HTTPStatus.NOT_FOUND

            except Exception as e:
                logger.error(f"Error retrieving schema: {str(e)}")
                return {
                    ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                    "details": str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

        @schema_ns.expect(schema_models["schema_definition"])
        @schema_ns.marshal_with(schema_models["schema_definition"])
        def put(self, name):
            """Update a schema"""
            try:
                data = request.get_json()
                if not data:
                    return {
                        ResponseFields.ERROR: ErrorMessages.INVALID_REQUEST_BODY
                    }, HTTPStatus.BAD_REQUEST

                # Add your schema update logic here
                # This is a placeholder implementation
                updated_schema = {
                    "name": name,
                    "schema": data.get("schema"),
                    "description": data.get("description", ""),
                    "version": data.get("version", "1.0.0"),
                }

                return updated_schema, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error updating schema: {str(e)}")
                return {
                    ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                    "details": str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

        def delete(self, name):
            """Delete a schema"""
            try:
                # Add your schema deletion logic here
                # This is a placeholder implementation
                return "", 204

            except Exception as e:
                logger.error(f"Error deleting schema: {str(e)}")
                return {
                    ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                    "details": str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @schema_ns.route("/<string:name>/versions")
    @schema_ns.param("name", "Schema name")
    class SchemaVersions(Resource):
        @schema_ns.doc(
            description="Get all versions of a schema",
            responses={
                HTTPStatus.OK: ("Schema versions", schema_models["schema_versions_response"]),
                HTTPStatus.NOT_FOUND: ("Schema not found", common_models["error_model"]),
            },
        )
        @schema_ns.marshal_with(schema_models["schema_versions_response"])
        def get(self, name):
            """Get all versions of a schema"""
            try:
                # Add your schema versions logic here
                # This is a placeholder implementation
                versions = []
                return {
                    "versions": versions,
                    "total": len(versions),
                }, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error retrieving schema versions: {str(e)}")
                return {
                    ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                    "details": str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    return schema_ns