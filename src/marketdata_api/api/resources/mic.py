"""
MIC API Resources

This module contains Flask-RESTx resource definitions for all MIC-related endpoints.
Includes both local database operations and remote real-time operations.
"""

import logging

from flask import current_app, request
from flask_restx import Namespace, Resource

from ...constants import ErrorMessages, HTTPStatus, Pagination, ResponseFields

logger = logging.getLogger(__name__)


def create_mic_resources(api, models):
    """
    Create and register MIC-related API resources.

    Args:
        api: Flask-RESTx API instance
        models: Dictionary of registered models

    Returns:
        Namespace: MIC namespace with registered resources
    """

    # Create namespace
    mic_ns = api.namespace("mic", description="Market Identification Code operations")

    # Get model references
    mic_models = models["mic"]
    common_models = models["common"]

    @mic_ns.route("/")
    class MICList(Resource):
        @mic_ns.doc(
            description="List MICs with advanced filtering (country, status, type, category)",
            params={
                "country": 'Filter by ISO country code (e.g., "US", "GB")',
                "status": "Filter by MIC status (ACTIVE, EXPIRED, DELETED, MODIFIED)",
                "category": "Filter by market category (APPA, REGULATED, MULTMK, etc.)",
                "mic_type": "Filter by MIC type (OPRT for operating, SGMT for segment)",
                "operating_mic": "Filter segment MICs by their operating MIC",
                "page": f"Page number for paginated results (default: {Pagination.DEFAULT_PAGE})",
                "per_page": f"Number of records per page (default: {Pagination.DEFAULT_PER_PAGE}, max: {Pagination.MAX_PER_PAGE})",
                "limit": "Maximum number of records to return",
            },
            responses={
                HTTPStatus.OK: ("Success", mic_models["mic_list_response"]),
                HTTPStatus.BAD_REQUEST: ("Invalid request", common_models["error_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @mic_ns.marshal_with(mic_models["mic_list_response"])
        def get(self):
            """List MICs with advanced filtering"""
            try:
                # Call business logic directly instead of route function
                from ...database.session import get_session
                from ...models.sqlite.market_identification_code import MarketIdentificationCode

                with get_session() as session:
                    query = session.query(MarketIdentificationCode)

                    # Apply filters
                    country = request.args.get("country")
                    if country:
                        query = query.filter(
                            MarketIdentificationCode.iso_country_code == country.upper()
                        )

                    status = request.args.get("status")
                    if status:
                        query = query.filter(MarketIdentificationCode.status == status.upper())

                    mic_type = request.args.get("type")
                    if mic_type:
                        query = query.filter(
                            MarketIdentificationCode.operation_type == mic_type.upper()
                        )

                    category = request.args.get("category")
                    if category:
                        query = query.filter(
                            MarketIdentificationCode.market_category_code == category.upper()
                        )

                    search = request.args.get("search")
                    if search:
                        search_term = f"%{search}%"
                        query = query.filter(
                            MarketIdentificationCode.market_name.ilike(search_term)
                            | MarketIdentificationCode.legal_entity_name.ilike(search_term)
                        )

                    # Pagination
                    limit = min(int(request.args.get("limit", 100)), 1000)
                    offset = int(request.args.get("offset", 0))

                    total = query.count()
                    mics = query.offset(offset).limit(limit).all()

                    return {
                        ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                        ResponseFields.DATA: [mic.to_dict() for mic in mics],
                        ResponseFields.META: {
                            "total": total,
                            "limit": limit,
                            "offset": offset,
                            "count": len(mics),
                        },
                    }

            except Exception as e:
                logger.error(f"Error in MIC list endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @mic_ns.route("/<string:mic_code>")
    @mic_ns.param("mic_code", "The 4-character MIC code (e.g., XNYS)")
    class MICDetail(Resource):
        @mic_ns.doc(
            description="Get detailed MIC information with optional trading venues",
            params={
                "include_venues": "Include related trading venues (true/false, default: false)",
                "include_segments": "Include segment MICs for operating MICs (true/false, default: true)",
            },
            responses={
                HTTPStatus.OK: ("Success", mic_models["mic_detail_response"]),
                HTTPStatus.NOT_FOUND: ("MIC not found", common_models["error_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @mic_ns.marshal_with(mic_models["mic_detail_response"])
        def get(self, mic_code):
            """Get detailed MIC information"""
            try:
                # Call business logic directly instead of route function
                from ...database.session import get_session
                from ...models.sqlite.market_identification_code import MarketIdentificationCode

                with get_session() as session:
                    mic = (
                        session.query(MarketIdentificationCode)
                        .filter_by(mic=mic_code.upper())
                        .first()
                    )

                    if not mic:
                        return {
                            ResponseFields.STATUS: "error",
                            ResponseFields.ERROR: {
                                "code": str(HTTPStatus.NOT_FOUND),
                                ResponseFields.MESSAGE: f"MIC not found: {mic_code}",
                            },
                        }, HTTPStatus.NOT_FOUND

                    # Optionally include related trading venues
                    include_venues = request.args.get("include_venues", "false").lower() == "true"

                    result = mic.to_dict()

                    if include_venues:
                        # Get trading venues that use this MIC
                        from ...models.sqlite.instrument import TradingVenue

                        venues = (
                            session.query(TradingVenue).filter_by(mic_code=mic_code.upper()).all()
                        )
                        result["trading_venues"] = [
                            {
                                "id": venue.id,
                                "venue_id": venue.venue_id,
                                "isin": venue.isin,
                                "first_trade_date": (
                                    venue.first_trade_date.isoformat()
                                    if venue.first_trade_date
                                    else None
                                ),
                            }
                            for venue in venues
                        ]

                    return {
                        ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                        ResponseFields.DATA: result,
                    }

            except Exception as e:
                logger.error(f"Error in MIC detail endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @mic_ns.route("/<string:mic_code>/segments")
    @mic_ns.param("mic_code", "The operating MIC code")
    class MICSegments(Resource):
        @mic_ns.doc(
            description="Get segment MICs for an operating MIC",
            responses={
                HTTPStatus.OK: ("Success", mic_models["mic_list_response"]),
                HTTPStatus.NOT_FOUND: ("Operating MIC not found", common_models["error_model"]),
                HTTPStatus.BAD_REQUEST: (
                    "MIC is not an operating MIC",
                    common_models["error_model"],
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @mic_ns.marshal_with(mic_models["mic_list_response"])
        def get(self, mic_code):
            """Get segment MICs for operating MIC"""
            try:
                from ...database.session import get_session
                from ..utils.mic_utils import get_mic_segments_data

                with get_session() as session:
                    return get_mic_segments_data(session, mic_code)
            except Exception as e:
                logger.error(f"Error in MIC segments endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @mic_ns.route("/countries")
    class MICCountries(Resource):
        @mic_ns.doc(
            description="Get countries with MIC counts and statistics",
            params={
                "include_markets": "Include sample markets for each country (true/false, default: false)",
                "min_mics": "Minimum number of MICs required for a country to be included",
                "status": "Filter by MIC status (ACTIVE, EXPIRED, etc.)",
            },
            responses={
                HTTPStatus.OK: ("Success", mic_models["mic_list_response"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        def get(self):
            """Get countries with MIC statistics"""
            try:
                from ...database.session import get_session
                from ..utils.mic_utils import get_countries_data

                with get_session() as session:
                    return get_countries_data(session)
            except Exception as e:
                logger.error(f"Error in MIC countries endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @mic_ns.route("/search")
    class MICSearch(Resource):
        @mic_ns.doc(
            description="Advanced MIC search by name, entity, or code",
            params={
                "name": "Search in market name (case-insensitive)",
                "entity": "Search in legal entity name (case-insensitive)",
                "mic": "Search for specific MIC code",
                "country": "Filter by ISO country code",
                "status": "Filter by MIC status",
                "category": "Filter by market category",
                "limit": "Maximum number of results (default: 100)",
            },
            responses={
                HTTPStatus.OK: ("Success", mic_models["mic_list_response"]),
                HTTPStatus.BAD_REQUEST: (
                    "No search criteria provided",
                    common_models["error_model"],
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @mic_ns.marshal_with(mic_models["mic_list_response"])
        def get(self):
            """Advanced MIC search"""
            try:
                from flask import request
                from ...database.session import get_session
                from ..utils.mic_utils import search_mics_data

                # Extract filters from request arguments
                filters = {}
                if request.args.get('name'):
                    filters['market_name'] = request.args.get('name')
                if request.args.get('entity'):
                    filters['legal_entity_name'] = request.args.get('entity')
                if request.args.get('mic'):
                    filters['mic_code'] = request.args.get('mic')
                if request.args.get('country'):
                    filters['country'] = request.args.get('country')
                if request.args.get('status'):
                    filters['status'] = request.args.get('status')
                if request.args.get('type'):
                    filters['mic_type'] = request.args.get('type')
                
                # Pagination
                try:
                    filters['page'] = int(request.args.get('page', 1))
                    filters['per_page'] = min(int(request.args.get('per_page', 50)), 1000)
                except (ValueError, TypeError):
                    filters['page'] = 1
                    filters['per_page'] = 50

                with get_session() as session:
                    return search_mics_data(session, **filters)
            except Exception as e:
                logger.error(f"Error in MIC search endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @mic_ns.route("/statistics")
    class MICStatistics(Resource):
        @mic_ns.doc(
            description="Get MIC registry statistics and data quality metrics",
            responses={
                HTTPStatus.OK: ("Success", mic_models["mic_statistics_response"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @mic_ns.marshal_with(mic_models["mic_statistics_response"])
        def get(self):
            """Get MIC registry statistics"""
            try:
                from ...database.session import get_session
                from ..utils.mic_utils import get_mic_statistics_data

                with get_session() as session:
                    return get_mic_statistics_data(session)
            except Exception as e:
                logger.error(f"Error in MIC statistics endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @mic_ns.route("/load-data")
    class MICLoadData(Resource):
        @mic_ns.doc(
            description="Load MIC data from local file or remote source",
            responses={
                HTTPStatus.OK: ("Success", mic_models["mic_load_response"]),
                HTTPStatus.BAD_REQUEST: (
                    "Invalid request parameters",
                    common_models["error_model"],
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @mic_ns.expect(mic_models["mic_load_request"])
        @mic_ns.marshal_with(mic_models["mic_load_response"])
        def post(self):
            """Load MIC data from local file or remote source"""
            try:
                from ...database.session import get_session
                from ..utils.mic_utils import load_mic_data_logic

                with get_session() as session:
                    return load_mic_data_logic(session)
            except Exception as e:
                logger.error(f"Error in MIC load data endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @mic_ns.route("/enums")
    class MICEnums(Resource):
        @mic_ns.doc(
            description="Get available enum values for MIC fields",
            responses={
                HTTPStatus.OK: ("Success", mic_models["mic_enums_response"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @mic_ns.marshal_with(mic_models["mic_enums_response"])
        def get(self):
            """Get available enum values for MIC fields"""
            try:
                from ...database.session import get_session
                from ..utils.mic_utils import get_mic_enums

                with get_session() as session:
                    return get_mic_enums(session)
            except Exception as e:
                logger.error(f"Error in MIC enums endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    # Remote MIC operations namespace
    remote_ns = api.namespace("mic/remote", description="Remote real-time MIC operations")

    @remote_ns.route("/lookup/<string:mic_code>")
    @remote_ns.param("mic_code", "The 4-character MIC code to lookup")
    class RemoteMICLookup(Resource):
        @remote_ns.doc(
            description="Direct lookup from ISO registry (real-time)",
            responses={
                HTTPStatus.OK: ("Success", mic_models["remote_mic_response"]),
                HTTPStatus.NOT_FOUND: (
                    "MIC not found in remote registry",
                    common_models["error_model"],
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Remote service unavailable",
                    common_models["error_model"],
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @remote_ns.marshal_with(mic_models["remote_mic_response"])
        def get(self, mic_code):
            """Direct lookup from ISO registry"""
            try:
                # Call business logic directly instead of route function
                from ...services.mic_data_loader import OFFICIAL_MIC_CSV_URL, remote_mic_service

                mic_info = remote_mic_service.lookup_mic(mic_code.upper())

                if mic_info is None:
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.NOT_FOUND),
                            ResponseFields.MESSAGE: f"MIC code {mic_code.upper()} not found in ISO registry",
                        },
                    }, HTTPStatus.NOT_FOUND

                # Map field names to match Swagger model expectations
                mapped_data = {
                    "mic": mic_info.get("mic"),
                    "operating_mic": mic_info.get("operating_mic"),
                    "oprt_sgmt": mic_info.get("operation_type"),  # Map operation_type to oprt_sgmt
                    "market_name": mic_info.get("market_name"),
                    "legal_entity_name": mic_info.get("legal_entity_name"),
                    "lei": mic_info.get("lei"),
                    "market_category_code": mic_info.get("market_category_code"),
                    "acronym": mic_info.get("acronym"),
                    "iso_country_code": mic_info.get("iso_country_code"),
                    "city": mic_info.get("city"),
                    "website": mic_info.get("website"),
                    "status": mic_info.get("status"),
                    "creation_date": mic_info.get("creation_date"),
                    "last_update_date": mic_info.get("last_update_date"),
                    "last_validation_date": mic_info.get("last_validation_date"),
                    "expiry_date": mic_info.get("expiry_date"),
                    "comments": mic_info.get("comments"),
                }

                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: mapped_data,
                    ResponseFields.META: {
                        "source": "iso_registry_remote",
                        "cached": True,  # Remote service uses caching
                        "cache_expires": None,  # Could add cache expiry info from service
                        "last_updated": None,  # Could add last update timestamp
                    },
                }

            except ValueError as e:
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.BAD_REQUEST),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.BAD_REQUEST
            except Exception as e:
                logger.error(f"Error in remote MIC lookup endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @remote_ns.route("/search")
    class RemoteMICSearch(Resource):
        @remote_ns.doc(
            description="Real-time search in official ISO data",
            params={
                "name": "Search in market name",
                "country": "Filter by ISO country code",
                "status": "Filter by MIC status",
                "limit": "Maximum number of results (default: 100)",
            },
            responses={
                HTTPStatus.OK: ("Success", mic_models["mic_list_response"]),
                HTTPStatus.BAD_REQUEST: (
                    "No search criteria provided",
                    common_models["error_model"],
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Remote service unavailable",
                    common_models["error_model"],
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @remote_ns.marshal_with(mic_models["mic_list_response"])
        def get(self):
            """Real-time search in official data"""
            try:
                # Call business logic directly instead of route function
                from ...services.mic_data_loader import remote_mic_service

                # Get query parameters
                name = request.args.get("name", "").strip()
                country = request.args.get("country", "").strip()
                status = request.args.get("status", "").strip()
                limit = min(int(request.args.get("limit", 100)), 1000)

                if not name and not country and not status:
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.BAD_REQUEST),
                            ResponseFields.MESSAGE: "At least one search parameter (name, country, status) is required",
                        },
                    }, HTTPStatus.BAD_REQUEST

                # Get search results from remote service
                if name:
                    # If name is provided, use search functionality
                    results = remote_mic_service.search_mics(name, limit=limit)
                else:
                    # If only country/status filters, get all data and filter manually
                    # Use a common term to get broader results, then filter
                    cached_data = remote_mic_service._get_cached_data()
                    results = list(cached_data.values())[:limit]  # Limit initial results

                # Apply additional filters and map field names
                filtered_results = []
                for mic in results:
                    if country and mic.get("iso_country_code", "").upper() != country.upper():
                        continue
                    if status and mic.get("status", "").upper() != status.upper():
                        continue

                    # Map field names to match Swagger model expectations
                    mapped_mic = {
                        "mic": mic.get("mic"),
                        "operating_mic": mic.get("operating_mic"),
                        "oprt_sgmt": mic.get("operation_type"),  # Map operation_type to oprt_sgmt
                        "market_name": mic.get("market_name"),
                        "legal_entity_name": mic.get("legal_entity_name"),
                        "lei": mic.get("lei"),
                        "market_category_code": mic.get("market_category_code"),
                        "acronym": mic.get("acronym"),
                        "iso_country_code": mic.get("iso_country_code"),
                        "city": mic.get("city"),
                        "website": mic.get("website"),
                        "status": mic.get("status"),
                        "creation_date": mic.get("creation_date"),
                        "last_update_date": mic.get("last_update_date"),
                        "last_validation_date": mic.get("last_validation_date"),
                        "expiry_date": mic.get("expiry_date"),
                        "comments": mic.get("comments"),
                    }
                    filtered_results.append(mapped_mic)

                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: filtered_results,
                    ResponseFields.META: {
                        "total": len(filtered_results),
                        "limit": limit,
                        "source": "iso_registry_remote",
                    },
                }

            except Exception as e:
                logger.error(f"Error in remote MIC search endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @remote_ns.route("/country/<string:country_code>")
    @remote_ns.param("country_code", "ISO 3166-1 alpha-2 country code")
    class RemoteMICByCountry(Resource):
        @remote_ns.doc(
            description="Get country MICs from official source",
            responses={
                HTTPStatus.OK: ("Success", mic_models["mic_list_response"]),
                HTTPStatus.NOT_FOUND: ("Country not found", common_models["error_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Remote service unavailable",
                    common_models["error_model"],
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @remote_ns.marshal_with(mic_models["mic_list_response"])
        def get(self, country_code):
            """Get country MICs from official source"""
            try:
                # Call business logic directly instead of route function
                from ...services.mic_data_loader import OFFICIAL_MIC_CSV_URL, remote_mic_service

                results = remote_mic_service.get_country_mics(country_code.upper())

                # Map field names to match Swagger model expectations
                mapped_results = []
                for mic in results:
                    mapped_mic = {
                        "mic": mic.get("mic"),
                        "operating_mic": mic.get("operating_mic"),
                        "oprt_sgmt": mic.get("operation_type"),  # Map operation_type to oprt_sgmt
                        "market_name": mic.get("market_name"),
                        "legal_entity_name": mic.get("legal_entity_name"),
                        "lei": mic.get("lei"),
                        "market_category_code": mic.get("market_category_code"),
                        "acronym": mic.get("acronym"),
                        "iso_country_code": mic.get("iso_country_code"),
                        "city": mic.get("city"),
                        "website": mic.get("website"),
                        "status": mic.get("status"),
                        "creation_date": mic.get("creation_date"),
                        "last_update_date": mic.get("last_update_date"),
                        "last_validation_date": mic.get("last_validation_date"),
                        "expiry_date": mic.get("expiry_date"),
                        "comments": mic.get("comments"),
                    }
                    mapped_results.append(mapped_mic)

                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: {
                        "country_code": country_code.upper(),
                        "source": "iso_registry_remote",
                        "url": OFFICIAL_MIC_CSV_URL,
                        "count": len(mapped_results),
                        "mics": mapped_results,
                    },
                }

            except Exception as e:
                logger.error(f"Error in remote country MICs endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @remote_ns.route("/validate/<string:mic_code>")
    @remote_ns.param("mic_code", "The 4-character MIC code to validate")
    class RemoteMICValidation(Resource):
        @remote_ns.doc(
            description="Official MIC validation from ISO registry",
            responses={
                HTTPStatus.OK: ("Success", mic_models["remote_validation_response"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Remote service unavailable",
                    common_models["error_model"],
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @remote_ns.marshal_with(mic_models["remote_validation_response"])
        def get(self, mic_code):
            """Official MIC validation"""
            try:
                # Call business logic directly instead of route function
                from ...services.mic_data_loader import OFFICIAL_MIC_CSV_URL, remote_mic_service

                validation_result = remote_mic_service.validate_mic(mic_code.upper())

                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: {
                        "mic_code": mic_code.upper(),
                        "source": "iso_registry_remote",
                        "url": OFFICIAL_MIC_CSV_URL,
                        **validation_result,
                    },
                }

            except Exception as e:
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.DATA: {
                        "mic_code": mic_code.upper(),
                        "valid": False,
                        "error": f"Failed to validate MIC: {str(e)}",
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR
            except Exception as e:
                logger.error(f"Error in remote MIC validation endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @remote_ns.route("/cache/clear")
    class RemoteCacheClear(Resource):
        @remote_ns.doc(
            description="Clear remote data cache",
            responses={
                HTTPStatus.OK: ("Cache cleared successfully"),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        def post(self):
            """Clear remote data cache"""
            try:
                # Call business logic directly instead of route function
                from ...services.mic_data_loader import remote_mic_service

                remote_mic_service.clear_cache()

                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.MESSAGE: "Cache cleared successfully",
                }

            except Exception as e:
                logger.error(f"Error in clear cache endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    return mic_ns
