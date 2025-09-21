"""
Model Registration Module

This module handles the registration of all Swagger models with the API instance.
"""

from .common import create_common_models
from .mic import create_mic_models
from .instruments import create_instrument_models
from .legal_entities import create_legal_entity_models
from .relationships import create_relationship_models
from .transparency import create_transparency_models

def register_all_models(api):
    """
    Register all Swagger models with the API instance.
    
    Args:
        api: Flask-RESTx API instance
        
    Returns:
        dict: Dictionary containing all registered models organized by category
    """
    
    # Register common models first
    common_models = create_common_models(api)
    
    # Register domain-specific models
    mic_models = create_mic_models(api, common_models)
    instrument_models = create_instrument_models(api, common_models)
    legal_entity_models = create_legal_entity_models(api, common_models)
    relationship_models = create_relationship_models(api, common_models)
    transparency_models = create_transparency_models(api, common_models)
    
    return {
        'common': common_models,
        'mic': mic_models,
        'instruments': instrument_models,
        'legal_entities': legal_entity_models,
        'relationships': relationship_models,
        'transparency': transparency_models,
    }
