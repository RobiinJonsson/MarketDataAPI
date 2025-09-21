import logging

from flask import Blueprint, jsonify, render_template
from sqlalchemy.exc import SQLAlchemyError

from ..constants import API, Endpoints, ErrorMessages, HTTPStatus, Pagination, ResponseFields

# Optional psutil import for system monitoring
try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# Setup logging
logger = logging.getLogger(__name__)

# Create blueprint for common routes
common_bp = Blueprint("common", __name__, url_prefix=API.PREFIX)

# Create a separate blueprint for non-API routes (without prefix)
frontend_bp = Blueprint("frontend_routes", __name__)  # Changed name to avoid conflict


# Error handler for database errors
@common_bp.errorhandler(SQLAlchemyError)
def handle_db_error(error):
    logger.error(f"Database error: {str(error)}")
    return (
        jsonify({ResponseFields.ERROR: ErrorMessages.DATABASE_ERROR, "details": str(error)}),
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )


# Root endpoint to provide API information
@common_bp.route("/info", methods=["GET"])
def api_info():
    """API information endpoint"""
    return jsonify(
        {
            "api": API.NAME,
            "version": API.VERSION,
            "endpoints": {
                "instruments": f"{API.PREFIX}{Endpoints.INSTRUMENTS}",
                "entities": f"{API.PREFIX}{Endpoints.ENTITIES}",
            },
        }
    )


@common_bp.route("/", methods=["GET"])
def api_root():
    """Root endpoint - simple response to avoid conflicts"""
    return jsonify(
        {"message": "MarketData API", "version": API.VERSION, "info": f"{API.PREFIX}/info"}
    )


@common_bp.route("/health", methods=["GET"])
def health_check():
    """Basic health check endpoint"""
    return jsonify({ResponseFields.STATUS: "healthy", "message": "API is running"})


@common_bp.route("/health/detailed", methods=["GET"])
def detailed_health_check():
    """Detailed health check with system information"""
    from datetime import UTC, datetime

    from ..database.session import get_session

    health_data = {
        ResponseFields.STATUS: "healthy",
        "timestamp": datetime.now(UTC).isoformat(),
        "services": {},
        "system": {},
    }

    # Database health
    try:
        from sqlalchemy import text

        with get_session() as session:
            session.execute(text("SELECT 1")).fetchone()
        health_data["services"]["database"] = {"status": "healthy", "type": "sqlite"}
    except Exception as e:
        health_data["services"]["database"] = {"status": "unhealthy", "error": str(e)}
        health_data[ResponseFields.STATUS] = "degraded"

    # API endpoints health
    try:
        from ..interfaces.factory.services_factory import ServicesFactory

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

    return jsonify(health_data)


@common_bp.route("/status", methods=["GET"])
def system_status():
    """System status endpoint with API statistics"""
    from datetime import UTC, datetime

    from sqlalchemy import text

    from ..database.session import get_session

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

    return jsonify(status_data)


# Route for the admin page
@common_bp.route("/admin", methods=["GET"])
def admin():
    return render_template("admin.html")


# Route for the home page (no API prefix)
@frontend_bp.route("/", methods=["GET"])
def home():
    return render_template("index.html")
