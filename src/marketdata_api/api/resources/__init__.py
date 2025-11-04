"""
Resource Registration Module

This module handles the registration of all Swagger API resources.
"""

from .docs import create_docs_resources
from .files import create_file_resources
from .frontend import create_frontend_resources
from .instruments import create_instrument_resources  # Use the working version
from .legal_entities import create_legal_entity_resources  # Use the working version
from .mic import create_mic_resources  # Add MIC to Swagger documentation
from .relationships import create_relationship_resources
from .schema import create_schema_resources
from .system import create_system_resources
from .transparency import create_transparency_resources  # Use the working version


def register_all_resources(api):
    """
    Register all API resources with the Flask-RESTx API instance.

    Args:
        api: Flask-RESTx API instance
    """

    # Import and register models first
    from ..models import register_all_models

    models = register_all_models(api)

    # Register domain-specific resources with complete working endpoints
    instruments_ns = create_instrument_resources(api, models)  # Working endpoints
    legal_entities_ns = create_legal_entity_resources(api, models)  # Working endpoints
    relationships_ns = create_relationship_resources(api, models)
    transparency_ns = create_transparency_resources(api, models)  # Working endpoints
    mic_ns = create_mic_resources(api, models)  # MIC endpoints in Swagger
    schema_ns = create_schema_resources(api, models)  # Schema endpoints migrated to Swagger
    system_ns = create_system_resources(api, models)  # System endpoints migrated from routes
    docs_ns = create_docs_resources(api, models)  # Documentation endpoints migrated from routes
    frontend_ns = create_frontend_resources(api, models)  # Frontend endpoints migrated from routes
    files_ns = create_file_resources(api, models)  # File management endpoints migrated to Swagger

    return {
        "mic": mic_ns,  # MIC endpoints now in Swagger
        "instruments": instruments_ns,
        "legal_entities": legal_entities_ns,
        "relationships": relationships_ns,
        "transparency": transparency_ns,
        "schema": schema_ns,
        "system": system_ns,
        "docs": docs_ns,
        "frontend": frontend_ns,
        "files": files_ns,
    }
