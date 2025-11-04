"""
Documentation API Resources - Documentation serving endpoints

This module contains documentation-related endpoints migrated from routes/docs.py
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

from flask import current_app, jsonify, send_from_directory
from flask_restx import Namespace, Resource

from ...constants import HTTPStatus

logger = logging.getLogger(__name__)


def create_docs_resources(api, models):
    """
    Create and register documentation-related API resources.

    Args:
        api: Flask-RESTx API instance
        models: Dictionary of registered models

    Returns:
        Namespace: Documentation namespace with registered resources
    """

    # Create namespace
    docs_ns = api.namespace(
        "docs", description="Documentation and specification endpoints"
    )

    # Get model references
    common_models = models["common"]

    @docs_ns.route("/")
    class DocsIndex(Resource):
        @docs_ns.doc(
            description="Serve the main documentation index",
            responses={
                HTTPStatus.OK: ("Documentation served successfully", None),
                HTTPStatus.NOT_FOUND: ("Documentation not found", common_models["error_model"]),
            },
        )
        def get(self):
            """Serve the main documentation index"""
            try:
                return send_from_directory(
                    os.path.join(current_app.root_path, "..", "..", "docs"), 
                    "README.md"
                )
            except Exception as e:
                logger.error(f"Error serving documentation: {str(e)}")
                return {"error": f"Documentation not found: {str(e)}"}, HTTPStatus.NOT_FOUND

    @docs_ns.route("/api")
    class APIDocsIndex(Resource):
        @docs_ns.doc(
            description="Serve API documentation index",
            responses={
                HTTPStatus.OK: ("API documentation served successfully", None),
                HTTPStatus.NOT_FOUND: ("API documentation not found", common_models["error_model"]),
            },
        )
        def get(self):
            """Serve API documentation index"""
            try:
                return send_from_directory(
                    os.path.join(current_app.root_path, "..", "..", "docs", "api"), 
                    "README.md"
                )
            except Exception as e:
                logger.error(f"Error serving API documentation: {str(e)}")
                return {"error": f"API documentation not found: {str(e)}"}, HTTPStatus.NOT_FOUND

    @docs_ns.route("/openapi")
    class OpenAPISpec(Resource):
        @docs_ns.doc(
            description="Serve the OpenAPI specification",
            responses={
                HTTPStatus.OK: ("OpenAPI specification served successfully", None),
                HTTPStatus.NOT_FOUND: ("OpenAPI specification not found", common_models["error_model"]),
            },
        )
        def get(self):
            """Serve the OpenAPI specification"""
            try:
                return send_from_directory(
                    os.path.join(current_app.root_path, "..", "..", "docs", "openapi"),
                    "openapi.yaml",
                    mimetype="text/yaml",
                )
            except Exception as e:
                logger.error(f"Error serving OpenAPI specification: {str(e)}")
                return {"error": f"OpenAPI specification not found: {str(e)}"}, HTTPStatus.NOT_FOUND

    @docs_ns.route("/status")
    class DocsStatus(Resource):
        @docs_ns.doc(
            description="Check status of documentation files",
            responses={
                HTTPStatus.OK: ("Status checked successfully", common_models["success_model"]),
            },
        )
        def get(self):
            """Check status of documentation files"""
            docs_root = os.path.join(current_app.root_path, "..", "docs")
            files_status = {}

            # Check for key documentation files
            check_files = ["README.md", "openapi/openapi.yaml", "openapi.yaml.backup", "api/README.md"]

            for file_path in check_files:
                full_path = os.path.join(docs_root, file_path)
                files_status[file_path] = {
                    "exists": os.path.exists(full_path), 
                    "path": full_path
                }

            return {
                "status": "success", 
                "docs_root": docs_root, 
                "files": files_status
            }

    @docs_ns.route("/regenerate")
    class RegenerateDocs(Resource):
        @docs_ns.doc(
            description="Regenerate documentation from swagger definitions (development only)",
            responses={
                HTTPStatus.OK: ("Documentation regenerated successfully", common_models["success_model"]),
                HTTPStatus.FORBIDDEN: ("Not available in production", common_models["error_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Regeneration failed", common_models["error_model"]),
            },
        )
        def post(self):
            """Regenerate documentation from swagger definitions"""
            try:
                # Only allow in development/testing mode
                if not current_app.config.get("TESTING") and not current_app.config.get("DEBUG"):
                    return {
                        "error": "Documentation regeneration only available in development mode"
                    }, HTTPStatus.FORBIDDEN

                # Run the generation script
                script_path = Path(current_app.root_path).parent / "scripts" / "generate_docs.py"
                result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)

                return {
                    "status": "success" if result.returncode == 0 else "error",
                    "message": (
                        "Documentation regeneration completed"
                        if result.returncode == 0
                        else "Documentation regeneration failed"
                    ),
                    "output": result.stdout,
                    "errors": result.stderr if result.stderr else None,
                    "return_code": result.returncode,
                }

            except Exception as e:
                logger.error(f"Error regenerating documentation: {str(e)}")
                return {"error": f"Failed to regenerate documentation: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR

    return docs_ns