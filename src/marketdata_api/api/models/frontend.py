"""
Frontend Swagger Models

This module contains Swagger model definitions for frontend-related endpoints.
"""

from flask_restx import fields


def create_frontend_models(api, common_models):
    """
    Create and register frontend-related Swagger models.

    Args:
        api: Flask-RESTx API instance
        common_models: Dictionary of common models

    Returns:
        dict: Dictionary of frontend models
    """

    # API root response model
    api_root_model = api.model("APIRootResponse", {
        "message": fields.String(required=True, description="API welcome message"),
        "version": fields.String(required=True, description="API version"),
        "info": fields.String(description="Link to detailed API information"),
        "swagger": fields.String(description="Link to Swagger documentation"),
        "health": fields.String(description="Link to health check endpoint"),
    })

    # Frontend page response (for documentation purposes)
    frontend_page_model = api.model("FrontendPageResponse", {
        "content_type": fields.String(description="Content type (text/html)"),
        "description": fields.String(description="Page description"),
    })

    return {
        "api_root": api_root_model,
        "frontend_page": frontend_page_model,
    }