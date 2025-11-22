"""
System API Resources - Health checks and API information

This module contains system-level endpoints migrated from routes/common_routes.py
"""

import logging
from datetime import UTC, datetime

from flask import current_app, request
from flask_restx import Namespace, Resource
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ...constants import API, Endpoints, ErrorMessages, HTTPStatus, ResponseFields

# Optional psutil import for system monitoring
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

logger = logging.getLogger(__name__)


def create_system_resources(api, models):
    """
    Create and register system-related API resources.

    Args:
        api: Flask-RESTx API instance
        models: Dictionary of registered models

    Returns:
        Namespace: System namespace with registered resources
    """

    # Create namespace
    system_ns = api.namespace(
        "system", description="System information and health monitoring"
    )

    # Get model references
    common_models = models["common"]

    @system_ns.route("/info")
    class APIInfo(Resource):
        @system_ns.doc(
            description="Get API information and available endpoints",
            responses={
                HTTPStatus.OK: ("Success", common_models["success_model"]),
            },
        )
        def get(self):
            """API information endpoint"""
            return {
                "api": API.NAME,
                "version": API.VERSION,
                "endpoints": {
                    "instruments": f"{API.PREFIX}{Endpoints.INSTRUMENTS}",
                    "entities": f"{API.PREFIX}{Endpoints.ENTITIES}",
                    "transparency": f"{API.PREFIX}/transparency",
                    "mic": f"{API.PREFIX}/mic",
                    "files": f"{API.PREFIX}/files",
                    "swagger": f"{API.PREFIX}/swagger",
                },
            }

    @system_ns.route("/health")
    class HealthCheck(Resource):
        @system_ns.doc(
            description="Basic health check endpoint",
            responses={
                HTTPStatus.OK: ("Success", common_models["success_model"]),
            },
        )
        def get(self):
            """Basic health check endpoint"""
            return {
                ResponseFields.STATUS: "healthy",
                "message": "API is running"
            }

    @system_ns.route("/health/detailed")
    class DetailedHealthCheck(Resource):
        @system_ns.doc(
            description="Detailed health check with system and service information",
            responses={
                HTTPStatus.OK: ("Success", common_models["success_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Service degraded", common_models["error_model"]),
            },
        )
        def get(self):
            """Detailed health check with system information"""
            from ...database.session import get_session

            health_data = {
                ResponseFields.STATUS: "healthy",
                "timestamp": datetime.now(UTC).isoformat(),
                "services": {},
                "system": {},
            }

            # Database health
            try:
                with get_session() as session:
                    session.execute(text("SELECT 1")).fetchone()
                health_data["services"]["database"] = {"status": "healthy", "type": "sqlite"}
            except Exception as e:
                health_data["services"]["database"] = {"status": "unhealthy", "error": str(e)}
                health_data[ResponseFields.STATUS] = "degraded"

            # API endpoints health
            try:
                from ...interfaces.factory.services_factory import ServicesFactory

                instrument_service = ServicesFactory.get_instrument_service()
                health_data["services"]["instrument_service"] = {
                    "status": "healthy",
                    "type": type(instrument_service).__name__,
                }
            except Exception as e:
                health_data["services"]["instrument_service"] = {"status": "unhealthy", "error": str(e)}
                health_data[ResponseFields.STATUS] = "degraded"

            # System information (optional, only if psutil is available)
            if HAS_PSUTIL:
                try:
                    health_data["system"] = {
                        "cpu_percent": psutil.cpu_percent(interval=1),
                        "memory_percent": psutil.virtual_memory().percent,
                        "disk_usage_percent": psutil.disk_usage("/").percent,
                    }
                except Exception as e:
                    health_data["system"] = {"error": f"System monitoring error: {str(e)}"}
            else:
                health_data["system"] = {"info": "System monitoring unavailable (psutil not installed)"}

            return health_data

    @system_ns.route("/status")
    class SystemStatus(Resource):
        @system_ns.doc(
            description="System status with database statistics",
            responses={
                HTTPStatus.OK: ("Success", common_models["success_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Database error", common_models["error_model"]),
            },
        )
        def get(self):
            """System status endpoint with API statistics"""
            from ...database.session import get_session

            status_data = {
                "timestamp": datetime.now(UTC).isoformat(),
                "api_info": {"name": API.NAME, "version": API.VERSION, "status": "operational"},
                "database": {},
                "statistics": {},
            }

            try:
                with get_session() as session:
                    # Get basic database statistics
                    instruments_count = session.execute(text("SELECT COUNT(*) FROM instruments")).scalar()
                    entities_count = session.execute(text("SELECT COUNT(*) FROM legal_entities")).scalar()
                    mic_codes_count = session.execute(
                        text("SELECT COUNT(*) FROM market_identification_codes")
                    ).scalar()

                    status_data["database"] = {"status": "connected", "type": "sqlite"}

                    status_data["statistics"] = {
                        "instruments": instruments_count,
                        "legal_entities": entities_count,
                        "mic_codes": mic_codes_count,
                        "total_records": instruments_count + entities_count + mic_codes_count,
                    }

            except Exception as e:
                status_data["database"] = {"status": "error", "error": str(e)}
                status_data["api_info"]["status"] = "degraded"

            return status_data

    return system_ns
