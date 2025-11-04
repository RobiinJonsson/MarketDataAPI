"""
System Swagger Models

This module contains Swagger model definitions for system endpoints.
"""

from flask_restx import fields


def create_system_models(api, common_models):
    """
    Create and register system-related Swagger models.

    Args:
        api: Flask-RESTx API instance
        common_models: Dictionary of common models

    Returns:
        dict: Dictionary of system models
    """

    # Service status model
    service_status_model = api.model("ServiceStatus", {
        "status": fields.String(required=True, description="Service status", enum=["healthy", "unhealthy", "degraded"]),
        "type": fields.String(description="Service type or class name"),
        "error": fields.String(description="Error message if service is unhealthy"),
    })

    # System metrics model
    system_metrics_model = api.model("SystemMetrics", {
        "cpu_percent": fields.Float(description="CPU usage percentage"),
        "memory_percent": fields.Float(description="Memory usage percentage"),
        "disk_usage_percent": fields.Float(description="Disk usage percentage"),
        "error": fields.String(description="Error message if system monitoring failed"),
        "info": fields.String(description="Information about system monitoring availability"),
    })

    # API info model
    api_info_model = api.model("APIInfo", {
        "api": fields.String(required=True, description="API name"),
        "version": fields.String(required=True, description="API version"),
        "endpoints": fields.Raw(description="Available API endpoints"),
    })

    # Health check response model
    health_response_model = api.model("HealthResponse", {
        "status": fields.String(required=True, description="Overall health status", enum=["healthy", "degraded", "unhealthy"]),
        "message": fields.String(description="Health status message"),
        "timestamp": fields.String(description="Health check timestamp"),
        "services": fields.Raw(description="Individual service health statuses"),
        "system": fields.Nested(system_metrics_model, description="System metrics"),
    })

    # Database statistics model
    database_stats_model = api.model("DatabaseStatistics", {
        "instruments": fields.Integer(description="Number of instruments"),
        "legal_entities": fields.Integer(description="Number of legal entities"),
        "mic_codes": fields.Integer(description="Number of MIC codes"),
        "total_records": fields.Integer(description="Total number of records"),
    })

    # Database status model
    database_status_model = api.model("DatabaseStatus", {
        "status": fields.String(required=True, description="Database status", enum=["connected", "error"]),
        "type": fields.String(description="Database type"),
        "error": fields.String(description="Error message if database has issues"),
    })

    # System status response model
    status_response_model = api.model("SystemStatusResponse", {
        "timestamp": fields.String(required=True, description="Status check timestamp"),
        "api_info": fields.Raw(description="API information"),
        "database": fields.Nested(database_status_model, description="Database status"),
        "statistics": fields.Nested(database_stats_model, description="Database statistics"),
    })

    # Documentation file status model
    doc_file_status_model = api.model("DocumentationFileStatus", {
        "exists": fields.Boolean(required=True, description="Whether the file exists"),
        "path": fields.String(description="Full file path"),
    })

    # Documentation status response model
    docs_status_response_model = api.model("DocumentationStatusResponse", {
        "status": fields.String(required=True, description="Status check result"),
        "docs_root": fields.String(description="Documentation root directory"),
        "files": fields.Raw(description="Status of individual documentation files"),
    })

    # Documentation regeneration response model
    docs_regen_response_model = api.model("DocumentationRegenerationResponse", {
        "status": fields.String(required=True, description="Regeneration status", enum=["success", "error"]),
        "message": fields.String(description="Status message"),
        "output": fields.String(description="Script output"),
        "errors": fields.String(description="Error output if any"),
        "return_code": fields.Integer(description="Script return code"),
    })

    return {
        "service_status": service_status_model,
        "system_metrics": system_metrics_model,
        "api_info": api_info_model,
        "health_response": health_response_model,
        "database_stats": database_stats_model,
        "database_status": database_status_model,
        "status_response": status_response_model,
        "doc_file_status": doc_file_status_model,
        "docs_status_response": docs_status_response_model,
        "docs_regen_response": docs_regen_response_model,
    }