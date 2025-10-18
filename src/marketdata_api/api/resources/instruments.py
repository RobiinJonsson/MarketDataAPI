"""
Instrument API Resources

This module contains the actual working instrument endpoints with business logic,
migrated from the old swagger.py but organized in the new modular structure.
"""

import logging

from flask import current_app, request
from flask_restx import Namespace, Resource

from ...constants import ErrorMessages, HTTPStatus, Pagination, ResponseFields

logger = logging.getLogger(__name__)


def create_instrument_resources(api, models):
    """
    Create and register instrument-related API resources with actual working endpoints.

    Args:
        api: Flask-RESTx API instance
        models: Dictionary of registered models

    Returns:
        Namespace: Instruments namespace with registered resources
    """

    # Create namespace
    instruments_ns = api.namespace("instruments", description="Instrument operations")

    # Get model references
    instrument_models = models["instruments"]
    common_models = models["common"]

    @instruments_ns.route("/")
    class InstrumentList(Resource):
        @instruments_ns.doc(
            description="Retrieves a paginated list of instruments",
            params={
                "type": 'Filter by instrument type (e.g., "equity", "debt", "future")',
                "cfi_type": 'Filter by CFI instrument type (C=Collective, D=Debt, E=Equity, F=Future, H=Structured, I=Interest Rate, J=Commodity, O=Option, R=Rights, S=Swap)',
                "currency": "Filter by currency code",
                "mic_code": "Filter by Market Identification Code",
                "cfi_code": "Filter by CFI code",
                "page": f"Page number for paginated results (default: {Pagination.DEFAULT_PAGE})",
                "per_page": f"Number of records per page (default: {Pagination.DEFAULT_PER_PAGE}, max: {Pagination.MAX_PER_PAGE})",
                "limit": "Maximum number of records to return",
                "offset": "Number of records to skip",
            },
            responses={
                HTTPStatus.OK: ("Success", instrument_models["instrument_list_response"]),
                HTTPStatus.BAD_REQUEST: ("Invalid request", common_models["error_model"]),
                HTTPStatus.UNAUTHORIZED: ("Unauthorized", common_models["error_model"]),
            },
        )
        # @instruments_ns.marshal_with(instrument_models["instrument_list_response"])  # Removed to allow rich response
        def get(self):
            """Retrieves a paginated list of instruments"""
            from ...database.session import get_session
            from ..utils.api_utils import (
                handle_api_errors,
                validate_pagination_params,
                validate_filter_params,
                validate_currency_code,
                validate_mic_code,
                validate_cfi_code,
            )

            try:
                # Validate pagination parameters
                pagination = validate_pagination_params()
                
                # Validate filter parameters
                allowed_filters = {
                    'type': str,  # No specific validation for instrument type
                    'cfi_type': lambda x: x.upper() if x.upper() in 'CDEFHIJORS' else None,  # CFI first letter
                    'currency': validate_currency_code,
                    'mic_code': validate_mic_code,
                    'cfi_code': validate_cfi_code,
                }
                filters = validate_filter_params(allowed_filters)

                # Get models directly
                from ...models.sqlite import Instrument

                with get_session() as session:
                    query = session.query(Instrument)

                    # Apply filters
                    logger.debug(f"Swagger: Filtering instruments with filters={filters}")
                    
                    if 'type' in filters:
                        query = query.filter(Instrument.instrument_type == filters['type'])
                        count = query.count()
                        logger.debug(f"Swagger: Found {count} instruments with type={filters['type']}")
                    
                    if 'cfi_type' in filters:
                        # Filter by CFI first letter (instrument classification)
                        cfi_prefix = filters['cfi_type'] + '%'
                        query = query.filter(Instrument.cfi_code.like(cfi_prefix))
                        count = query.count()
                        logger.debug(f"Swagger: Found {count} instruments with CFI type={filters['cfi_type']}")
                    
                    if 'currency' in filters:
                        query = query.filter(Instrument.currency == filters['currency'])
                    
                    if 'mic_code' in filters:
                        # Filter by MIC code through trading venues
                        from ...models.sqlite.instrument import TradingVenue
                        query = query.join(TradingVenue).filter(TradingVenue.mic_code == filters['mic_code'])
                    
                    if 'cfi_code' in filters:
                        query = query.filter(Instrument.cfi_code == filters['cfi_code'])

                    # Get total count for pagination
                    total_count = query.count()

                    # Apply pagination
                    limit = pagination['limit'] or pagination['per_page']
                    offset = pagination['offset'] or (pagination['page'] - 1) * pagination['per_page']
                    instruments = query.limit(limit).offset(offset).all()

                    # Use rich instrument response builder following CLI pattern
                    from ..utils.type_specific_responses import build_instrument_response, build_raw_instrument_response
                    
                    logger.info(f"Building rich responses for {len(instruments)} instruments")
                    result = []
                    for instrument in instruments:
                        try:
                            rich_response = build_instrument_response(instrument, include_rich_details=True)
                            logger.info(f"Rich response for {instrument.isin} has keys: {list(rich_response.keys())}")
                            result.append(rich_response)
                        except Exception as e:
                            logger.error(f"Error building rich response for {instrument.isin}: {e}")
                            # Fallback to basic response
                            result.append(build_raw_instrument_response(instrument.to_raw_data()))

                    return {
                        ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                        ResponseFields.DATA: result,
                        ResponseFields.META: {
                            ResponseFields.PAGE: pagination['page'],
                            ResponseFields.PER_PAGE: pagination['per_page'],
                            ResponseFields.TOTAL: total_count,
                        },
                    }

            except Exception as e:
                logger.error(f"Error in swagger list_instruments: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

        @instruments_ns.doc(
            description="Create a new instrument from FIRDS data",
            responses={
                HTTPStatus.CREATED: (
                    "Instrument created successfully",
                    instrument_models["instrument_detail_response"],
                ),
                HTTPStatus.BAD_REQUEST: ("Invalid request data", common_models["error_model"]),
                HTTPStatus.NOT_FOUND: (
                    "Instrument not found in FIRDS data",
                    common_models["error_model"],
                ),
                HTTPStatus.UNAUTHORIZED: ("Unauthorized", common_models["error_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: (
                    "Internal server error",
                    common_models["error_model"],
                ),
            },
        )
        @instruments_ns.expect(instrument_models["instrument_create_request"])
        def post(self):
            """Create a new instrument from FIRDS data"""
            from werkzeug.exceptions import BadRequest

            from ...interfaces.factory.services_factory import ServicesFactory
            from ...models.utils.cfi_instrument_manager import (
                get_valid_instrument_types,
                normalize_instrument_type_from_cfi,
                validate_cfi_code,
                validate_instrument_type,
            )

            try:
                # Handle JSON parsing errors specifically
                try:
                    data = request.json
                except BadRequest as json_error:
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.BAD_REQUEST),
                            ResponseFields.MESSAGE: f"Invalid JSON format: {str(json_error)}",
                        },
                    }, HTTPStatus.BAD_REQUEST
                if not data:
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.BAD_REQUEST),
                            ResponseFields.MESSAGE: "No data provided",
                        },
                    }, HTTPStatus.BAD_REQUEST

                # Required fields - ISIN and type
                if "isin" not in data or "type" not in data:
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.BAD_REQUEST),
                            ResponseFields.MESSAGE: "isin and type are required",
                        },
                    }, HTTPStatus.BAD_REQUEST

                instrument_type = data["type"]

                # Use CFI-based validation
                if not validate_instrument_type(instrument_type):
                    valid_types = get_valid_instrument_types()
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.BAD_REQUEST),
                            ResponseFields.MESSAGE: f"Invalid instrument type '{instrument_type}'. Must be one of: {', '.join(valid_types)}",
                        },
                    }, HTTPStatus.BAD_REQUEST

                # If CFI code is provided, validate it and ensure consistency
                cfi_code = data.get("cfi_code")
                if cfi_code:
                    is_valid, error_msg = validate_cfi_code(cfi_code)
                    if not is_valid:
                        return {
                            ResponseFields.STATUS: "error",
                            ResponseFields.ERROR: {
                                "code": str(HTTPStatus.BAD_REQUEST),
                                ResponseFields.MESSAGE: f"Invalid CFI code: {error_msg}",
                            },
                        }, HTTPStatus.BAD_REQUEST

                    # Ensure CFI code matches the provided instrument type
                    normalized_type = normalize_instrument_type_from_cfi(cfi_code)
                    if normalized_type != instrument_type:
                        return {
                            ResponseFields.STATUS: "error",
                            ResponseFields.ERROR: {
                                "code": str(HTTPStatus.BAD_REQUEST),
                                ResponseFields.MESSAGE: f"CFI code '{cfi_code}' indicates type '{normalized_type}' but '{instrument_type}' was specified",
                            },
                        }, HTTPStatus.BAD_REQUEST

                # Use factory pattern for service access
                service = ServicesFactory.get_instrument_service()

                # Use the create_instrument method that gets data from FIRDS
                instrument = service.create_instrument(data["isin"], instrument_type)

                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.MESSAGE: "Instrument created successfully",
                    ResponseFields.DATA: {
                        "id": instrument.id,
                        "isin": instrument.isin,
                        "instrument_type": instrument.instrument_type,
                    },
                }, HTTPStatus.CREATED

            except Exception as e:
                # Check if it's an InstrumentNotFoundError
                if "not found in local FIRDS data" in str(e):
                    logger.warning(f"Instrument not found in FIRDS data: {str(e)}")
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.NOT_FOUND),
                            ResponseFields.MESSAGE: str(e),
                        },
                    }, HTTPStatus.NOT_FOUND

                logger.error(f"Error in create_instrument: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @instruments_ns.route("/<string:isin>")
    @instruments_ns.param("isin", "International Securities Identification Number")
    class InstrumentDetail(Resource):
        @instruments_ns.doc(
            description="Retrieves detailed information about a specific instrument by its ISIN",
            responses={
                HTTPStatus.OK: ("Success", instrument_models["instrument_detail_response"]),
                HTTPStatus.NOT_FOUND: ("Instrument not found", common_models["error_model"]),
                HTTPStatus.UNAUTHORIZED: ("Unauthorized", common_models["error_model"]),
            },
        )
        def get(self, isin):
            """Retrieves detailed information about a specific instrument by its ISIN"""
            from ...interfaces.factory.services_factory import ServicesFactory

            try:
                service = ServicesFactory.get_instrument_service()
                session, instrument = service.get_instrument(isin)

                if not instrument:
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.NOT_FOUND),
                            ResponseFields.MESSAGE: ErrorMessages.INSTRUMENT_NOT_FOUND,
                        },
                    }, HTTPStatus.NOT_FOUND

                # Build detailed response using CLI-pattern response builder
                from ..utils.type_specific_responses import build_detailed_instrument_response

                result = build_detailed_instrument_response(instrument)
                session.close()

                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: result,
                }

            except Exception as e:
                logger.error(f"Error in swagger get_instrument: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @instruments_ns.route("/<string:isin>/raw")
    @instruments_ns.param("isin", "International Securities Identification Number")
    class InstrumentRawData(Resource):
        @instruments_ns.doc(
            description="Retrieves raw model data for a specific instrument by its ISIN for comparison with normalized outputs",
            responses={
                HTTPStatus.OK: ("Success", common_models["success_model"]),
                HTTPStatus.NOT_FOUND: ("Instrument not found", common_models["error_model"]),
                HTTPStatus.UNAUTHORIZED: ("Unauthorized", common_models["error_model"]),
            },
        )
        def get(self, isin):
            """Retrieves raw model data for a specific instrument - useful for comparing with normalized API responses"""
            from ...interfaces.factory.services_factory import ServicesFactory

            try:
                service = ServicesFactory.get_instrument_service()
                session, instrument = service.get_instrument(isin)

                if not instrument:
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.NOT_FOUND),
                            ResponseFields.MESSAGE: ErrorMessages.INSTRUMENT_NOT_FOUND,
                        },
                    }, HTTPStatus.NOT_FOUND

                # Get raw data directly from model - no normalization or presentation logic
                raw_data = instrument.to_raw_data()
                session.close()

                # Convert datetime objects and SQLAlchemy objects to JSON-serializable format
                def serialize_for_json(data):
                    """Recursively convert objects to JSON-serializable format"""
                    if isinstance(data, dict):
                        return {k: serialize_for_json(v) for k, v in data.items()}
                    elif isinstance(data, list):
                        return [serialize_for_json(item) for item in data]
                    elif hasattr(data, 'isoformat'):  # datetime, date objects
                        return data.isoformat()
                    elif hasattr(data, '__dict__'):  # SQLAlchemy objects, etc.
                        return str(data)  # Convert to string representation
                    elif data is None:
                        return None
                    else:
                        return data
                
                # Serialize the raw data for JSON response
                serialized_raw_data = serialize_for_json(raw_data)

                # Add metadata about the raw data structure for development reference
                metadata = {
                    "description": "Raw model data - compare with normalized /api/v1/instruments/{isin} response",
                    "instrument_type": serialized_raw_data.get("instrument_type"),
                    "total_fields": len(serialized_raw_data),
                    "firds_fields_count": len(serialized_raw_data.get("firds_data", {}) or {}),
                    "processed_attributes_count": len(serialized_raw_data.get("processed_attributes", {}) or {}),
                    "has_trading_venues": bool(instrument.trading_venues),
                    "has_figi_mappings": bool(instrument.figi_mappings),
                    "has_legal_entity": bool(instrument.legal_entity),
                }

                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: serialized_raw_data,
                    ResponseFields.META: metadata,
                }

            except Exception as e:
                logger.error(f"Error in raw data endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @instruments_ns.route("/<string:identifier>/venues")
    @instruments_ns.param("identifier", "Instrument identifier (ISIN, ID, or symbol)")
    class InstrumentVenues(Resource):
        @instruments_ns.doc(
            description="Retrieves trading venues for a specific instrument",
            responses={
                HTTPStatus.OK: ("Success", instrument_models["instrument_venues_response"]),
                HTTPStatus.NOT_FOUND: ("Instrument not found", common_models["error_model"]),
                HTTPStatus.UNAUTHORIZED: ("Unauthorized", common_models["error_model"]),
            },
        )
        def get(self, identifier):
            """Retrieves trading venues for a specific instrument"""
            from ...interfaces.factory.services_factory import ServicesFactory

            try:
                service = ServicesFactory.get_instrument_service()
                session, instrument = service.get_instrument(identifier)

                if not instrument:
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.NOT_FOUND),
                            ResponseFields.MESSAGE: ErrorMessages.INSTRUMENT_NOT_FOUND,
                        },
                    }, HTTPStatus.NOT_FOUND

                # Get venues for this instrument
                venues = []
                if hasattr(instrument, "trading_venues") and instrument.trading_venues:
                    for venue in instrument.trading_venues:
                        venues.append(
                            {
                                "venue_id": venue.venue_id,
                                "mic_code": venue.mic_code,
                                "venue_full_name": venue.venue_full_name,
                                "venue_short_name": venue.venue_short_name,
                                "first_trade_date": (
                                    venue.first_trade_date.isoformat()
                                    if venue.first_trade_date
                                    else None
                                ),
                                "termination_date": (
                                    venue.termination_date.isoformat()
                                    if venue.termination_date
                                    else None
                                ),
                                "venue_currency": venue.venue_currency,
                                "classification_type": venue.classification_type,
                            }
                        )

                session.close()

                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: {
                        "instrument_id": instrument.id,
                        "isin": instrument.isin,
                        "venues": venues,
                    },
                }

            except Exception as e:
                logger.error(f"Error in swagger get_instrument_venues: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @instruments_ns.route("/types")
    class InstrumentTypes(Resource):
        @instruments_ns.doc(
            description="Retrieves all available instrument types",
            responses={
                HTTPStatus.OK: ("Success", instrument_models["valid_types_response"]),
                HTTPStatus.UNAUTHORIZED: ("Unauthorized", common_models["error_model"]),
            },
        )
        def get(self):
            """Retrieves all available instrument types"""
            from ...models.utils.cfi_instrument_manager import get_valid_instrument_types

            try:
                instrument_types = get_valid_instrument_types()

                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: {"instrument_types": instrument_types},
                }

            except Exception as e:
                logger.error(f"Error in swagger get_instrument_types: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @instruments_ns.route("/cfi/<string:cfi_code>")
    @instruments_ns.param("cfi_code", "CFI classification code")
    class CFIDetails(Resource):
        @instruments_ns.doc(
            description="Retrieves detailed information about a CFI code",
            responses={
                HTTPStatus.OK: ("Success", instrument_models["cfi_info_response"]),
                HTTPStatus.NOT_FOUND: ("CFI code not found", common_models["error_model"]),
                HTTPStatus.UNAUTHORIZED: ("Unauthorized", common_models["error_model"]),
            },
        )
        def get(self, cfi_code):
            """Retrieves detailed information about a CFI code"""
            from ...models.utils.cfi import CFI

            try:
                cfi = CFI(cfi_code)

                if not cfi.is_valid():
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.NOT_FOUND),
                            ResponseFields.MESSAGE: f"Invalid CFI code: {cfi_code}",
                        },
                    }, HTTPStatus.NOT_FOUND

                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: {
                        "cfi_code": cfi_code,
                        "category": cfi.get_category(),
                        "group": cfi.get_group(),
                        "attributes": cfi.get_attributes(),
                        "description": cfi.get_description(),
                    },
                }

            except Exception as e:
                logger.error(f"Error in swagger get_cfi_details: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @instruments_ns.route("/<string:isin>/cfi")
    @instruments_ns.param("isin", "International Securities Identification Number")
    class InstrumentCFI(Resource):
        @instruments_ns.doc(
            description="Retrieves CFI information for a specific instrument",
            responses={
                HTTPStatus.OK: ("Success", instrument_models["instrument_cfi_classification"]),
                HTTPStatus.NOT_FOUND: ("Instrument not found", common_models["error_model"]),
                HTTPStatus.UNAUTHORIZED: ("Unauthorized", common_models["error_model"]),
            },
        )
        def get(self, isin):
            """Retrieves CFI information for a specific instrument"""
            from ...interfaces.factory.services_factory import ServicesFactory
            from ...models.utils.cfi import CFI

            try:
                service = ServicesFactory.get_instrument_service()
                session, instrument = service.get_instrument(isin)

                if not instrument:
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.NOT_FOUND),
                            ResponseFields.MESSAGE: ErrorMessages.INSTRUMENT_NOT_FOUND,
                        },
                    }, HTTPStatus.NOT_FOUND

                cfi_info = {}
                if instrument.cfi_code:
                    cfi = CFI(instrument.cfi_code)
                    cfi_info = {
                        "cfi_code": instrument.cfi_code,
                        "category": cfi.get_category(),
                        "group": cfi.get_group(),
                        "attributes": cfi.get_attributes(),
                        "description": cfi.get_description(),
                        "is_valid": cfi.is_valid(),
                    }

                session.close()

                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: {
                        "instrument_id": instrument.id,
                        "isin": instrument.isin,
                        "cfi_info": cfi_info,
                    },
                }

            except Exception as e:
                logger.error(f"Error in swagger get_instrument_cfi: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    return instruments_ns
