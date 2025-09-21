"""
Swagger API Configuration

This module contains the core Flask-RESTx API configuration and setup.
"""

from flask_restx import Api
from ..constants import HTTPStatus, API as APIConstants

def create_swagger_api(blueprint):
    """
    Create and configure the Flask-RESTx API instance.
    
    Args:
        blueprint: Flask blueprint to attach the API to
        
    Returns:
        Api: Configured Flask-RESTx API instance
    """
    api = Api(
        blueprint,
        version=APIConstants.VERSION,
        title='MarketDataAPI',
        description='API for financial market data, instrument details, legal entity information, and MIC codes',
        doc='/swagger/',
        authorizations={
            'apikey': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            }
        },
        security='apikey'
    )
    
    return api
