import logging
from flask import Blueprint, jsonify
from sqlalchemy.exc import SQLAlchemyError
from ..constants import (
    API, Endpoints, ResponseFields, ErrorMessages, HTTPStatus,
    Pagination, CFI as CFIConstants
)

# Setup logging
logger = logging.getLogger(__name__)

# Create blueprint for common routes
common_bp = Blueprint("common", __name__, url_prefix=API.PREFIX)

# Error handler for database errors
@common_bp.errorhandler(SQLAlchemyError)
def handle_db_error(error):
    logger.error(f"Database error: {str(error)}")
    return jsonify({ResponseFields.ERROR: ErrorMessages.DATABASE_ERROR, "details": str(error)}), HTTPStatus.INTERNAL_SERVER_ERROR

# Root endpoint to provide API information
@common_bp.route("/info", methods=["GET"])
def api_info():
    """API information endpoint"""
    return jsonify({
        "api": API.NAME,
        "version": API.VERSION,
        "endpoints": {
            "instruments": f"{API.PREFIX}{Endpoints.INSTRUMENTS}",
            "entities": f"{API.PREFIX}{Endpoints.ENTITIES}",
            "cfi": f"{API.PREFIX}{Endpoints.CFI}/{{cfi_code}}"
        }
    })

@common_bp.route("/", methods=["GET"])
def api_root():
    """Root endpoint - simple response to avoid conflicts"""
    return jsonify({
        "message": "MarketData API",
        "version": API.VERSION,
        "info": f"{API.PREFIX}/info"
    })

@common_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        ResponseFields.STATUS: "healthy",
        "message": "API is running"
    })

