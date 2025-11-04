"""
Frontend API Resources - Template serving and API root

This module contains frontend-related endpoints that serve the modern TypeScript
frontend templates and provide API root information.
"""

import logging

from flask import render_template
from flask_restx import Namespace, Resource

from ...constants import HTTPStatus

logger = logging.getLogger(__name__)


def create_frontend_resources(api, models):
    """
    Create and register frontend-related API resources.

    Args:
        api: Flask-RESTx API instance
        models: Dictionary of registered models

    Returns:
        Namespace: Frontend namespace with registered resources
    """

    # Create namespace
    frontend_ns = api.namespace(
        "frontend", description="Frontend template serving and API root"
    )

    # Get model references
    frontend_models = models["frontend"]
    common_models = models["common"]

    @frontend_ns.route("/")
    class APIRoot(Resource):
        @frontend_ns.doc(
            description="API root endpoint with basic information and navigation links",
            responses={
                HTTPStatus.OK: ("Success", frontend_models["api_root"]),
            },
        )
        @frontend_ns.marshal_with(frontend_models["api_root"])
        def get(self):
            """API root endpoint - simple response to avoid conflicts"""
            return {
                "message": "MarketData API",
                "version": "1.0",
                "info": "/api/v1/system/info",
                "swagger": "/api/v1/swagger",
                "health": "/api/v1/system/health"
            }

    @frontend_ns.route("/admin")
    class AdminPage(Resource):
        @frontend_ns.doc(
            description="Serve the modern frontend admin interface",
            responses={
                HTTPStatus.OK: ("Admin page served", frontend_models["frontend_page"]),
                HTTPStatus.NOT_FOUND: ("Template not found", common_models["error_model"]),
            },
        )
        def get(self):
            """Serve the modern frontend admin interface"""
            try:
                return render_template("admin.html")
            except Exception as e:
                logger.error(f"Error serving admin page: {str(e)}")
                return {
                    "error": f"Admin template not found: {str(e)}"
                }, HTTPStatus.NOT_FOUND

    return frontend_ns


def create_frontend_blueprint():
    """
    Create the frontend blueprint for non-API routes (without prefix).
    
    Returns:
        Blueprint: Frontend blueprint for serving the main web interface
    """
    from flask import Blueprint
    
    # Blueprint for non-API routes (without API prefix)
    frontend_bp = Blueprint("frontend_routes", __name__)

    @frontend_bp.route("/", methods=["GET"])
    def home():
        """Serve the modern frontend index page"""
        try:
            return render_template("index.html")
        except Exception as e:
            logger.error(f"Error serving home page: {str(e)}")
            return f"Frontend template not found: {str(e)}", HTTPStatus.NOT_FOUND

    return frontend_bp