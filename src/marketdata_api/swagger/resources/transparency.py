"""
Transparency API Resources - Working Implementation

This module contains the actual working transparency endpoints with business logic,
migrated from the old swagger.py but organized in the new modular structure.
"""

import logging

from flask import current_app, request
from flask_restx import Namespace, Resource

from ...constants import ErrorMessages, HTTPStatus, Pagination, ResponseFields

logger = logging.getLogger(__name__)


def create_transparency_resources(api, models):
    """
    Create and register transparency-related API resources with actual working endpoints.

    Args:
        api: Flask-RESTx API instance
        models: Dictionary of registered models

    Returns:
        Namespace: Transparency namespace with registered resources
    """

    # Create namespace
    transparency_ns = api.namespace(
        "transparency", description="Transparency calculation operations"
    )

    # Get model references
    transparency_models = models["transparency"]
    common_models = models["common"]

    @transparency_ns.route("")
    class TransparencyList(Resource):
        @transparency_ns.doc(
            description="Get all transparency calculations with optional filtering",
            params={
                "file_type": "Filter by FITRS file type",
                "calculation_type": "Legacy filter - maps to file_type patterns (EQUITY/NON_EQUITY)",
                "isin": "Filter by ISIN",
                "page": "Page number (default: 1)",
                "per_page": "Items per page (default: 20, max: 100)",
            },
            responses={
                HTTPStatus.OK: ("Success", transparency_models["transparency_list_response"]),
                HTTPStatus.BAD_REQUEST: ("Invalid request", common_models["error_model"]),
                HTTPStatus.UNAUTHORIZED: ("Unauthorized", common_models["error_model"]),
            },
        )
        @transparency_ns.marshal_with(transparency_models["transparency_list_response"])
        def get(self):
            """Get all transparency calculations with optional filtering"""
            from sqlalchemy.orm import joinedload

            try:
                # Get query parameters
                calculation_type = request.args.get("calculation_type")
                file_type = request.args.get("file_type")
                isin = request.args.get("isin")
                page = request.args.get("page", 1, type=int)
                per_page = min(request.args.get("per_page", 20, type=int), 100)

                # Get models directly
                # Create a new session
                from ...database.session import SessionLocal
                from ...models.sqlite.transparency import TransparencyCalculation

                session = SessionLocal()
                try:
                    # Build query - unified model no longer needs joinedload for polymorphic relationships
                    query = session.query(TransparencyCalculation)

                    # Apply filters - updated for unified transparency model
                    if file_type:
                        # Direct file_type filtering
                        query = query.filter(TransparencyCalculation.file_type == file_type)
                    elif calculation_type:
                        # Map old calculation_type to new file_type patterns (fallback)
                        if calculation_type.upper() == "EQUITY":
                            query = query.filter(TransparencyCalculation.file_type.like("FULECR_%"))
                        elif calculation_type.upper() == "NON_EQUITY":
                            query = query.filter(TransparencyCalculation.file_type.like("FULNCR_%"))

                    if isin:
                        query = query.filter(TransparencyCalculation.isin == isin)

                    # Get total count
                    total = query.count()

                    # Apply pagination
                    offset = (page - 1) * per_page
                    calculations = query.offset(offset).limit(per_page).all()

                    # Format results
                    result = []
                    for calc in calculations:
                        result.append(
                            {
                                "id": calc.id,
                                "isin": calc.isin,
                                "instrument_name": calc.description or "N/A",  # Use description or default
                                "file_type": calc.file_type,
                                "calculation_date": (
                                    calc.from_date.isoformat()
                                    if calc.from_date
                                    else None
                                ),
                                "instrument_type": calc.instrument_category,
                                "currency": "N/A",  # Not available in current model
                                "trading_venue": "N/A",  # Not available in current model
                                "has_transaction_data": (calc.total_transactions_executed or 0) > 0,
                                "has_threshold_data": len(calc.thresholds or []) > 0,
                            }
                        )

                    return {
                        ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                        ResponseFields.DATA: result,
                        ResponseFields.META: {
                            ResponseFields.PAGE: page,
                            ResponseFields.PER_PAGE: per_page,
                            ResponseFields.TOTAL: total,
                        },
                    }

                finally:
                    session.close()

            except Exception as e:
                logger.error(f"Error in swagger list_transparency: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @transparency_ns.route("/<string:transparency_id>")
    @transparency_ns.param("transparency_id", "Transparency calculation ID")
    class TransparencyDetail(Resource):
        @transparency_ns.doc(
            description="Get detailed information about a specific transparency calculation",
            responses={
                HTTPStatus.OK: ("Success", transparency_models["transparency_detail_response"]),
                HTTPStatus.NOT_FOUND: (
                    "Transparency calculation not found",
                    common_models["error_model"],
                ),
                HTTPStatus.UNAUTHORIZED: ("Unauthorized", common_models["error_model"]),
            },
        )
        def get(self, transparency_id):
            """Get detailed information about a specific transparency calculation"""
            from ...database.session import SessionLocal
            from ...models.sqlite.transparency import TransparencyCalculation

            try:
                session = SessionLocal()
                try:
                    # Get the transparency calculation
                    calculation = (
                        session.query(TransparencyCalculation)
                        .filter(TransparencyCalculation.id == transparency_id)
                        .first()
                    )

                    if not calculation:
                        return {
                            ResponseFields.STATUS: "error",
                            ResponseFields.ERROR: {
                                "code": str(HTTPStatus.NOT_FOUND),
                                ResponseFields.MESSAGE: "Transparency calculation not found",
                            },
                        }, HTTPStatus.NOT_FOUND

                    # Build detailed response
                    result = {
                        "id": calculation.id,
                        "isin": calculation.isin,
                        "instrument_name": calculation.description or "N/A",
                        "file_type": calculation.file_type,
                        "calculation_date": (
                            calculation.from_date.isoformat()
                            if calculation.from_date
                            else None
                        ),
                        "instrument_type": calculation.instrument_category,
                        "currency": "N/A",  # Not available in current model
                        "trading_venue": "N/A",  # Not available in current model
                        "has_transaction_data": (calculation.total_transactions_executed or 0) > 0,
                        "has_threshold_data": len(calculation.thresholds or []) > 0,
                        "created_at": (
                            calculation.created_at.isoformat() if calculation.created_at else None
                        ),
                        "updated_at": (
                            calculation.updated_at.isoformat() if calculation.updated_at else None
                        ),
                    }

                    return {
                        ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                        ResponseFields.DATA: result,
                    }

                finally:
                    session.close()

            except Exception as e:
                logger.error(f"Error in swagger get_transparency: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @transparency_ns.route("/isin/<string:isin>")
    @transparency_ns.param("isin", "International Securities Identification Number")
    class TransparencyByISIN(Resource):
        @transparency_ns.doc(
            description="Get transparency calculations for a specific ISIN",
            responses={
                HTTPStatus.OK: ("Success", transparency_models["transparency_list_response"]),
                HTTPStatus.NOT_FOUND: (
                    "No transparency data found for ISIN",
                    common_models["error_model"],
                ),
                HTTPStatus.UNAUTHORIZED: ("Unauthorized", common_models["error_model"]),
            },
        )
        def get(self, isin):
            """Get transparency calculations for a specific ISIN"""
            from ...database.session import SessionLocal
            from ...models.sqlite.transparency import TransparencyCalculation

            try:
                session = SessionLocal()
                try:
                    # Get all calculations for this ISIN
                    calculations = (
                        session.query(TransparencyCalculation)
                        .filter(TransparencyCalculation.isin == isin)
                        .all()
                    )

                    if not calculations:
                        return {
                            ResponseFields.STATUS: "error",
                            ResponseFields.ERROR: {
                                "code": str(HTTPStatus.NOT_FOUND),
                                ResponseFields.MESSAGE: f"No transparency data found for ISIN: {isin}",
                            },
                        }, HTTPStatus.NOT_FOUND

                    # Format results
                    result = []
                    for calc in calculations:
                        result.append(
                            {
                                "id": calc.id,
                                "isin": calc.isin,
                                "tech_record_id": calc.tech_record_id,
                                "file_type": calc.file_type,
                                "from_date": calc.from_date.isoformat() if calc.from_date else None,
                                "to_date": calc.to_date.isoformat() if calc.to_date else None,
                                "liquidity": calc.liquidity,
                                "total_transactions_executed": calc.total_transactions_executed,
                                "total_volume_executed": calc.total_volume_executed,
                                "source_file": calc.source_file,
                            }
                        )

                    return {
                        ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                        ResponseFields.DATA: result,
                        ResponseFields.META: {ResponseFields.TOTAL: len(result)},
                    }

                finally:
                    session.close()

            except Exception as e:
                logger.error(f"Error in swagger get_transparency_by_isin: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    return transparency_ns
