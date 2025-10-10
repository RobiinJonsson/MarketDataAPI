"""
Schema Swagger Models

This module contains Swagger model definitions for schema-related endpoints.
"""

from flask_restx import fields


def create_schema_models(api, common_models):
    """
    Create and register schema-related Swagger models.

    Args:
        api: Flask-RESTx API instance
        common_models: Dictionary of common models

    Returns:
        dict: Dictionary of schema models
    """

    # Schema definition model
    schema_definition_model = api.model("SchemaDefinition", {
        "name": fields.String(required=True, description="Schema name"),
        "version": fields.String(required=False, description="Schema version"),
        "description": fields.String(required=False, description="Schema description"),
        "schema": fields.Raw(required=True, description="JSON schema definition"),
        "created_at": fields.DateTime(description="Creation timestamp"),
        "updated_at": fields.DateTime(description="Last update timestamp"),
    })

    # Schema search request model
    schema_search_request_model = api.model("SchemaSearchRequest", {
        "query": fields.Raw(required=True, description="Search query using schema format"),
        "schema_name": fields.String(required=False, description="Schema to use for search"),
        "limit": fields.Integer(required=False, description="Maximum results to return", default=100),
    })

    # Schema validation request model
    schema_validation_request_model = api.model("SchemaValidationRequest", {
        "schema": fields.Raw(required=True, description="Schema definition to validate"),
        "data": fields.Raw(required=False, description="Optional data to validate against schema"),
    })

    # Schema validation response model
    schema_validation_response_model = api.model("SchemaValidationResponse", {
        "valid": fields.Boolean(required=True, description="Whether the schema/data is valid"),
        "errors": fields.List(fields.String, description="Validation errors if any"),
        "message": fields.String(description="Validation message"),
    })

    # Schema list response model
    schema_list_response_model = api.model("SchemaListResponse", {
        "schemas": fields.List(fields.Nested(schema_definition_model), description="List of schemas"),
        "total": fields.Integer(description="Total number of schemas"),
        "page": fields.Integer(description="Current page number"),
        "per_page": fields.Integer(description="Results per page"),
    })

    # Schema version model
    schema_version_model = api.model("SchemaVersion", {
        "version": fields.String(required=True, description="Version identifier"),
        "created_at": fields.DateTime(description="Version creation timestamp"),
        "description": fields.String(description="Version description"),
        "schema": fields.Raw(description="Schema definition for this version"),
    })

    # Schema versions response model
    schema_versions_response_model = api.model("SchemaVersionsResponse", {
        "versions": fields.List(fields.Nested(schema_version_model), description="List of schema versions"),
        "total": fields.Integer(description="Total number of versions"),
    })

    return {
        "schema_definition": schema_definition_model,
        "schema_search_request": schema_search_request_model,
        "schema_validation_request": schema_validation_request_model,
        "schema_validation_response": schema_validation_response_model,
        "schema_list_response": schema_list_response_model,
        "schema_version": schema_version_model,
        "schema_versions_response": schema_versions_response_model,
    }