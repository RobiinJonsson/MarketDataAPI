"""
Resource Registration Module

This module handles the registration of all Swagger API resources.
"""

# from .mic import create_mic_resources  # Skip MIC - it has separate working routes
from .mic import create_mic_resources  # Add MIC to Swagger documentation
from .instruments import create_instrument_resources  # Use the working version
from .legal_entities import create_legal_entity_resources  # Use the working version
from .relationships import create_relationship_resources
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
    
    return {
        # 'mic': mic_ns,  # Skip MIC - handled by separate blueprint
        'instruments': instruments_ns,
        'legal_entities': legal_entities_ns,
        'relationships': relationships_ns,
        'transparency': transparency_ns,
    }
