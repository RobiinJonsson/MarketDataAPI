"""
Venues API Resources

This module contains Flask-RESTx resource definitions for trading venue endpoints.
Provides comprehensive venue management and MIC-integrated operations.
"""

import logging

from flask import current_app, request
from flask_restx import Namespace, Resource

from ...constants import ErrorMessages, HTTPStatus, Pagination, ResponseFields

logger = logging.getLogger(__name__)


def create_venue_resources(api, models):
    """
    Create and register venue-related API resources.

    Args:
        api: Flask-RESTx API instance
        models: Dictionary of registered models

    Returns:
        Namespace: Venues namespace with registered resources
    """

    # Create namespace
    venues_ns = api.namespace("venues", description="Trading venue operations")

    # Get model references
    venue_models = models["venues"]
    common_models = models["common"]

    @venues_ns.route("/")
    @venues_ns.route("")
    class VenueList(Resource):
        @venues_ns.doc(
            description="List trading venues with advanced filtering and MIC integration",
            params={
                "country": 'Filter by ISO country code (e.g., "US", "GB")',
                "status": "Filter by MIC status (ACTIVE, EXPIRED, SUSPENDED, UPDATED)",
                "mic_type": "Filter by MIC type (OPRT for operating, SGMT for segment)",
                "operating_mic": "Filter segment MICs by their operating MIC",
                "search": "Search venue names and legal entities",
                "has_instruments": "Filter venues with/without instruments (true/false)",
                "page": f"Page number for paginated results (default: {Pagination.DEFAULT_PAGE})",
                "per_page": f"Number of records per page (default: {Pagination.DEFAULT_PER_PAGE}, max: {Pagination.MAX_PER_PAGE})",
                "limit": "Maximum number of records to return",
            },
            responses={
                HTTPStatus.OK: ("Success", venue_models["venue_list_response"]),
                HTTPStatus.BAD_REQUEST: ("Invalid request", common_models["error_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @venues_ns.marshal_with(venue_models["venue_list_response"])
        def get(self):
            """List trading venues with comprehensive filtering"""
            try:
                from ...services.sqlite.venue_service import SqliteVenueService
                
                service = SqliteVenueService()
                
                # Extract filters from request
                filters = {
                    "country": request.args.get("country"),
                    "status": request.args.get("status"),
                    "mic_type": request.args.get("mic_type"),
                    "operating_mic": request.args.get("operating_mic"),
                    "search": request.args.get("search"),
                    "has_instruments": request.args.get("has_instruments"),
                }
                
                # Pagination
                page = int(request.args.get("page", Pagination.DEFAULT_PAGE))
                per_page = min(
                    int(request.args.get("per_page", Pagination.DEFAULT_PER_PAGE)),
                    Pagination.MAX_PER_PAGE
                )
                limit = request.args.get("limit")
                if limit:
                    per_page = min(int(limit), Pagination.MAX_PER_PAGE)
                    page = 1
                
                result = service.get_venues_list(filters, page, per_page)
                
                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: result["venues"],
                    "pagination": {
                        "page": page,
                        "per_page": per_page,
                        "total": result["total"],
                        "pages": (result["total"] + per_page - 1) // per_page,
                    },
                }

            except Exception as e:
                logger.error(f"Error in venues list endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: ErrorMessages.DATABASE_ERROR,
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @venues_ns.route("/<string:mic_code>")
    @venues_ns.param("mic_code", "The 4-character MIC code (e.g., XNYS)")
    class VenueDetail(Resource):
        @venues_ns.doc(
            description="Get detailed venue information with MIC data and optional instruments",
            params={
                "include_instruments": "Include instruments traded on this venue (true/false, default: false)",
                "instrument_limit": "Maximum number of instruments to include (default: 50, max: 200)",
            },
            responses={
                HTTPStatus.OK: ("Success", venue_models["venue_detail_response"]),
                HTTPStatus.NOT_FOUND: ("Venue not found", common_models["error_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @venues_ns.marshal_with(venue_models["venue_detail_response"])
        def get(self, mic_code):
            """Get detailed venue information"""
            try:
                from ...services.sqlite.venue_service import SqliteVenueService
                
                service = SqliteVenueService()
                
                include_instruments = request.args.get("include_instruments", "false").lower() == "true"
                instrument_limit = min(int(request.args.get("instrument_limit", 50)), 200)
                
                result = service.get_venue_detail(mic_code, include_instruments, instrument_limit)
                
                if not result:
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.NOT_FOUND),
                            ResponseFields.MESSAGE: f"Venue not found: {mic_code}",
                        },
                    }, HTTPStatus.NOT_FOUND

                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: result,
                }

            except Exception as e:
                logger.error(f"Error in venue detail endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: ErrorMessages.DATABASE_ERROR,
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @venues_ns.route("/<string:mic_code>/instruments")
    @venues_ns.param("mic_code", "The 4-character MIC code")
    class VenueInstruments(Resource):
        @venues_ns.doc(
            description="Get paginated list of instruments traded on a venue",
            params={
                "instrument_type": "Filter by instrument type (equity, bond, etc.)",
                "page": f"Page number for paginated results (default: {Pagination.DEFAULT_PAGE})",
                "per_page": f"Number of records per page (default: {Pagination.DEFAULT_PER_PAGE}, max: {Pagination.MAX_PER_PAGE})",
            },
            responses={
                HTTPStatus.OK: ("Success", venue_models["venue_instruments_response"]),
                HTTPStatus.NOT_FOUND: ("Venue not found", common_models["error_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @venues_ns.marshal_with(venue_models["venue_instruments_response"])
        def get(self, mic_code):
            """Get instruments traded on a venue"""
            try:
                from ...services.sqlite.venue_service import SqliteVenueService
                
                service = SqliteVenueService()
                
                # Extract filters
                instrument_type = request.args.get("instrument_type")
                
                # Pagination
                page = int(request.args.get("page", Pagination.DEFAULT_PAGE))
                per_page = min(
                    int(request.args.get("per_page", Pagination.DEFAULT_PER_PAGE)),
                    Pagination.MAX_PER_PAGE
                )
                
                result = service.get_venue_instruments(mic_code, instrument_type, page, per_page)
                
                if result is None:
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.NOT_FOUND),
                            ResponseFields.MESSAGE: f"Venue not found: {mic_code}",
                        },
                    }, HTTPStatus.NOT_FOUND

                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: result["instruments"],
                    ResponseFields.PAGINATION: {
                        "page": page,
                        "per_page": per_page,
                        "total": result["total"],
                        "pages": (result["total"] + per_page - 1) // per_page,
                    },
                }

            except Exception as e:
                logger.error(f"Error in venue instruments endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: ErrorMessages.DATABASE_ERROR,
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @venues_ns.route("/search")
    class VenueSearch(Resource):
        @venues_ns.doc(
            description="Advanced venue search with fuzzy matching",
            params={
                "query": "Search term for venue names, MIC codes, legal entities",
                "country": "Filter by country code",
                "status": "Filter by venue status",
                "limit": "Maximum results to return (default: 20, max: 100)",
            },
            responses={
                HTTPStatus.OK: ("Success", venue_models["venue_search_response"]),
                HTTPStatus.BAD_REQUEST: ("Missing query parameter", common_models["error_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @venues_ns.marshal_with(venue_models["venue_search_response"])
        def get(self):
            """Search venues with fuzzy matching"""
            try:
                query = request.args.get("query")
                if not query:
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.BAD_REQUEST),
                            ResponseFields.MESSAGE: "Query parameter is required",
                        },
                    }, HTTPStatus.BAD_REQUEST

                from ...services.sqlite.venue_service import SqliteVenueService
                
                service = SqliteVenueService()
                
                filters = {
                    "country": request.args.get("country"),
                    "status": request.args.get("status"),
                }
                
                limit = min(int(request.args.get("limit", 20)), 100)
                
                results = service.search_venues(query, filters, limit)
                
                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: results,
                }

            except Exception as e:
                logger.error(f"Error in venue search endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: ErrorMessages.DATABASE_ERROR,
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @venues_ns.route("/statistics")
    class VenueStatistics(Resource):
        @venues_ns.doc(
            description="Get venue and trading statistics",
            responses={
                HTTPStatus.OK: ("Success", venue_models["venue_statistics_response"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @venues_ns.marshal_with(venue_models["venue_statistics_response"])
        def get(self):
            """Get venue and trading statistics"""
            try:
                from ...services.sqlite.venue_service import SqliteVenueService
                
                service = SqliteVenueService()
                
                stats = service.get_venue_statistics()
                
                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: stats,
                }

            except Exception as e:
                logger.error(f"Error in venue statistics endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: ErrorMessages.DATABASE_ERROR,
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @venues_ns.route("/countries")
    class VenueCountries(Resource):
        @venues_ns.doc(
            description="Get list of countries with venue counts",
            responses={
                HTTPStatus.OK: ("Success", venue_models["venue_countries_response"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @venues_ns.marshal_with(venue_models["venue_countries_response"])
        def get(self):
            """Get countries with venue counts"""
            try:
                from ...services.sqlite.venue_service import SqliteVenueService
                
                service = SqliteVenueService()
                
                countries = service.get_venue_countries()
                
                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: countries,
                }

            except Exception as e:
                logger.error(f"Error in venue countries endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: ErrorMessages.DATABASE_ERROR,
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    return venues_ns