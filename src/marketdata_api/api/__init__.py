"""
Swagger API Documentation Module

This module provides a refactored, modular approach to API documentation
using Flask-RESTx, maintaining the same URL structure as the original swagger.py.

Structure:
- config.py: API configuration and setup
- models/: Swagger model definitions
- resources/: API endpoint resources

URL Structure (same as original):
- API Endpoints: /api/v1/instruments/, /api/v1/legal-entities/, etc.
- SwaggerUI: /api/v1/swagger/
"""

from flask import Blueprint
from flask_restx import Api

from ..constants import API as APIConstants
from .config import create_swagger_api
from .resources import register_all_resources


def create_swagger_blueprint():
    """
    Create and configure the Swagger blueprint with the same URL structure as the old swagger.py.

    Returns:
        Blueprint: Configured Swagger blueprint
    """
    # Create the blueprint with the SAME prefix as the old swagger.py
    swagger_bp = Blueprint("swagger", __name__, url_prefix=APIConstants.PREFIX)

    # Create the API instance
    api = create_swagger_api(swagger_bp)

    # Register all resources
    register_all_resources(api)

    return swagger_bp
