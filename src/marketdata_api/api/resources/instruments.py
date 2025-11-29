"""
Instrument API Resources

This module contains the actual working instrument endpoints with business logic,
migrated from the old swagger.py but organized in the new modular structure.
"""

import logging

from flask import current_app, request
from flask_restx import Namespace, Resource
from sqlalchemy import func, distinct
from sqlalchemy.orm import sessionmaker

from ...constants import ErrorMessages, HTTPStatus, Pagination, ResponseFields
from ...database import get_session
from ...config import DatabaseConfig

# Import database-agnostic services
from ...services import InstrumentService

# Dynamic model imports based on database type
def _get_models():
    """Get appropriate model classes based on database configuration."""
    db_type = DatabaseConfig.get_database_type()
    
    if db_type == 'sqlite':
        from ...models.sqlite.instrument import Instrument
        from ...models.sqlite.legal_entity import LegalEntity
        from ...models.sqlite.figi import FigiMapping
        from ...models.sqlite.transparency import TransparencyCalculation
    elif db_type in ['azure_sql', 'sqlserver', 'sql_server', 'mssql']:
        from ...models.sqlserver.instrument import SqlServerInstrument as Instrument
        from ...models.sqlserver.legal_entity import SqlServerLegalEntity as LegalEntity
        from ...models.sqlserver.figi import SqlServerFigiMapping as FigiMapping
        from ...models.sqlserver.transparency import SqlServerTransparencyCalculation as TransparencyCalculation
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    return Instrument, LegalEntity, FigiMapping, TransparencyCalculation

# Get models for this module
Instrument, LegalEntity, FigiMapping, TransparencyCalculation = _get_models()

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
                "search": "Search by ISIN or instrument name (partial matching supported)",
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
                    'search': str,  # Search by ISIN or instrument name
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
                    
                    if 'search' in filters:
                        # Search by ISIN (exact or partial) or instrument name
                        search_term = filters['search']
                        query = query.filter(
                            (Instrument.isin.ilike(f'%{search_term}%')) |
                            (Instrument.short_name.ilike(f'%{search_term}%')) |
                            (Instrument.full_name.ilike(f'%{search_term}%'))
                        )
                        count = query.count()
                        logger.debug(f"Swagger: Found {count} instruments matching search='{search_term}'")

                    # Get total count for pagination
                    total_count = query.count()

                    # Apply pagination with ORDER BY for SQL Server compatibility
                    limit = pagination['limit'] or pagination['per_page']
                    offset = pagination['offset'] or (pagination['page'] - 1) * pagination['per_page']
                    instruments = query.order_by(Instrument.isin).limit(limit).offset(offset).all()

                    # Use rich instrument response builder following CLI pattern
                    from ..utils.type_specific_responses import build_instrument_response, build_raw_instrument_response
                    
                    logger.debug(f"Building rich responses for {len(instruments)} instruments")
                    result = []
                    for instrument in instruments:
                        try:
                            rich_response = build_instrument_response(instrument, include_rich_details=True)
                            logger.debug(f"Rich response for {instrument.isin} has keys: {list(rich_response.keys())}")
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

                # Use database-agnostic service
                service = InstrumentService()

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
                
                # Check if it's a duplicate key constraint violation
                if "UNIQUE KEY constraint" in str(e) or "duplicate key" in str(e):
                    isin = data.get("isin", "unknown")
                    logger.info(f"Attempt to create existing instrument: {isin}")
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.CONFLICT),
                            ResponseFields.MESSAGE: f"Instrument with ISIN '{isin}' already exists. Use the update endpoint or retrieve the existing instrument.",
                            "error_type": "duplicate_instrument",
                            "suggestion": "To view the existing instrument, use GET /api/v1/instruments/{isin}"
                        },
                    }, HTTPStatus.CONFLICT

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
            try:
                service = InstrumentService()
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
            try:
                service = InstrumentService()
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

    @instruments_ns.route("/<string:isin>/enrich")
    @instruments_ns.param("isin", "International Securities Identification Number")
    class InstrumentEnrich(Resource):
        @instruments_ns.doc(
            description="Enrich an existing instrument with additional data from external sources (FIGI, legal entities)",
            responses={
                HTTPStatus.OK: ("Enrichment successful", instrument_models["instrument_detailed"]),
                HTTPStatus.NOT_FOUND: ("Instrument not found", common_models["error_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Server error", common_models["error_model"]),
            },
        )
        def post(self, isin):
            """Enrich instrument with FIGI mappings and legal entity data"""
            try:
                # Use database-agnostic service
                service = InstrumentService()
                
                # First, get the instrument
                session, instrument = service.get_instrument(isin)
                if not instrument:
                    session.close()
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.NOT_FOUND),
                            ResponseFields.MESSAGE: f"Instrument with ISIN {isin} not found",
                        },
                    }, HTTPStatus.NOT_FOUND

                # Close the first session since enrich_instrument creates its own
                session.close()
                
                # Enrich the instrument
                session, enriched_instrument = service.enrich_instrument(instrument)
                
                # Build detailed response using CLI-pattern response builder
                from ..utils.type_specific_responses import build_detailed_instrument_response
                result = build_detailed_instrument_response(enriched_instrument)
                
                session.close()
                
                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.MESSAGE: "Instrument enriched successfully",
                    ResponseFields.DATA: result,
                }, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error in instrument enrichment: {str(e)}")
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
            try:
                service = InstrumentService()
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
                    ResponseFields.DATA: cfi.describe(),
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
            from ...models.utils.cfi import CFI

            try:
                service = InstrumentService()
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
                logger.debug(f"Instrument CFI code: '{instrument.cfi_code}', type: {type(instrument.cfi_code)}")
                if instrument.cfi_code:
                    try:
                        cfi = CFI(instrument.cfi_code)
                        cfi_info = {
                            "cfi_code": instrument.cfi_code,
                            "category": cfi.get_category(),
                            "group": cfi.get_group(),
                            "attributes": cfi.get_attributes(),
                            "description": cfi.get_description(),
                            "is_valid": cfi.is_valid(),
                        }
                        logger.debug(f"Generated CFI info: {cfi_info}")
                    except Exception as cfi_error:
                        logger.error(f"Error processing CFI code '{instrument.cfi_code}': {str(cfi_error)}")
                else:
                    logger.debug(f"No CFI code found for instrument {instrument.isin}")

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

    @instruments_ns.route("/batch")
    class BatchInstruments(Resource):
        @instruments_ns.doc(
            description="Create multiple instruments using three different batch import methods",
            responses={
                HTTPStatus.OK: ("Success", common_models["success_model"]),
                HTTPStatus.BAD_REQUEST: ("Bad Request", common_models["error_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Server Error", common_models["error_model"]),
            },
        )
        def post(self):
            """
            Create multiple instruments using batch import methods:
            
            Method 1 - Full Type Import (Resource Intensive):
            {
                "method": "full_type",
                "instrument_type": "equity",
                "confirmed": true
            }
            
            Method 2 - Segmented Import:
            {
                "method": "segmented",
                "instrument_type": "equity", 
                "filters": {
                    "competent_authority": "SE",
                    "relevant_trading_venue": "XSTO",
                    "limit": 1000
                }
            }
            
            Method 3 - ISIN List Import:
            {
                "method": "isin_list",
                "instruments": [
                    {"isin": "SE0000108656", "type": "equity"},
                    {"isin": "SE0000148884", "type": "equity"}
                ]
            }
            
            All methods use BatchDataExtractor for performance and disable enrichment.
            """
            try:
                data = request.get_json()
                if not data:
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.BAD_REQUEST),
                            ResponseFields.MESSAGE: "Request body is required"
                        }
                    }, HTTPStatus.BAD_REQUEST

                method = data.get("method")
                if not method or method not in ["full_type", "segmented", "isin_list"]:
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.BAD_REQUEST),
                            ResponseFields.MESSAGE: "Method must be one of: full_type, segmented, isin_list"
                        }
                    }, HTTPStatus.BAD_REQUEST

                from ...services.utils.esma_utils import BatchDataExtractor
                from ...models.utils.cfi_instrument_manager import get_valid_instrument_types, validate_instrument_type

                instrument_service = InstrumentService()
                
                # Method 1: Full Type Import (Resource Intensive)
                if method == "full_type":
                    instrument_type = data.get("instrument_type")
                    confirmed = data.get("confirmed", False)
                    
                    if not instrument_type or not validate_instrument_type(instrument_type):
                        valid_types = get_valid_instrument_types()
                        return {
                            ResponseFields.STATUS: "error",
                            ResponseFields.ERROR: {
                                "code": str(HTTPStatus.BAD_REQUEST),
                                ResponseFields.MESSAGE: f"Valid instrument_type required. Options: {', '.join(valid_types)}"
                            }
                        }, HTTPStatus.BAD_REQUEST
                    
                    if not confirmed:
                        return {
                            ResponseFields.STATUS: "warning",
                            ResponseFields.MESSAGE: "Full type import is resource intensive and may take significant time. Set confirmed=true to proceed.",
                            "warning_type": "resource_intensive",
                            "estimated_impact": "High CPU/Memory usage, long execution time"
                        }, HTTPStatus.OK
                    
                    # Use create_instruments_bulk with no limits for full import
                    results = instrument_service.create_instruments_bulk(
                        competent_authority="ALL",  # Process all competent authorities
                        instrument_type=instrument_type,
                        limit=None,  # No limit
                        skip_existing=True,
                        enable_enrichment=False,  # Disable enrichment for performance
                        batch_size=100  # Increased batch size for bulk operations
                    )
                    
                    return {
                        ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                        ResponseFields.MESSAGE: f"Full {instrument_type} import completed",
                        ResponseFields.DATA: results
                    }, HTTPStatus.OK

                # Method 2: Segmented Import 
                elif method == "segmented":
                    instrument_type = data.get("instrument_type")
                    filters = data.get("filters", {})
                    
                    if not instrument_type or not validate_instrument_type(instrument_type):
                        valid_types = get_valid_instrument_types()
                        return {
                            ResponseFields.STATUS: "error",
                            ResponseFields.ERROR: {
                                "code": str(HTTPStatus.BAD_REQUEST),
                                ResponseFields.MESSAGE: f"Valid instrument_type required. Options: {', '.join(valid_types)}"
                            }
                        }, HTTPStatus.BAD_REQUEST
                    
                    # Extract filter parameters
                    competent_authority = filters.get("competent_authority", "SE")
                    limit = filters.get("limit", 1000)  # Default reasonable limit
                    venue = filters.get("relevant_trading_venue")
                    
                    # Validate limit
                    if limit and (not isinstance(limit, int) or limit < 1 or limit > 10000):
                        return {
                            ResponseFields.STATUS: "error", 
                            ResponseFields.ERROR: {
                                "code": str(HTTPStatus.BAD_REQUEST),
                                ResponseFields.MESSAGE: "Limit must be between 1 and 10000"
                            }
                        }, HTTPStatus.BAD_REQUEST
                    
                    # Use create_instruments_bulk with filters
                    results = instrument_service.create_instruments_bulk(
                        competent_authority=competent_authority,
                        instrument_type=instrument_type,
                        limit=limit,
                        skip_existing=True,
                        enable_enrichment=False,  # Disable enrichment for performance
                        batch_size=100  # Increased batch size for bulk operations
                    )
                    
                    # If venue filtering was requested, we'd need to implement post-processing
                    # For now, note this in the response
                    response_data = results.copy()
                    if venue:
                        response_data["note"] = f"Venue filtering ({venue}) applied during FIRDS extraction"
                    
                    return {
                        ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                        ResponseFields.MESSAGE: f"Segmented {instrument_type} import completed",
                        ResponseFields.DATA: response_data
                    }, HTTPStatus.OK

                # Method 3: ISIN List Import
                elif method == "isin_list":
                    instruments_list = data.get("instruments", [])
                    
                    if not instruments_list or not isinstance(instruments_list, list):
                        return {
                            ResponseFields.STATUS: "error",
                            ResponseFields.ERROR: {
                                "code": str(HTTPStatus.BAD_REQUEST),
                                ResponseFields.MESSAGE: "instruments array is required for isin_list method"
                            }
                        }, HTTPStatus.BAD_REQUEST
                    
                    if len(instruments_list) > 1000:
                        return {
                            ResponseFields.STATUS: "error",
                            ResponseFields.ERROR: {
                                "code": str(HTTPStatus.BAD_REQUEST),
                                ResponseFields.MESSAGE: "Maximum 1000 instruments per batch for isin_list method"
                            }
                        }, HTTPStatus.BAD_REQUEST
                    
                    # Validate instrument data structure
                    valid_instruments = []
                    validation_errors = []
                    
                    for idx, instr in enumerate(instruments_list):
                        if not isinstance(instr, dict):
                            validation_errors.append(f"Item {idx}: Must be an object with isin and type")
                            continue
                            
                        isin = instr.get("isin")
                        instr_type = instr.get("type")
                        
                        if not isin or not isinstance(isin, str) or len(isin) != 12:
                            validation_errors.append(f"Item {idx}: Invalid ISIN format")
                            continue
                            
                        if not instr_type or not validate_instrument_type(instr_type):
                            validation_errors.append(f"Item {idx}: Invalid instrument type '{instr_type}'")
                            continue
                            
                        valid_instruments.append({"isin": isin.upper(), "type": instr_type})
                    
                    if validation_errors:
                        return {
                            ResponseFields.STATUS: "error",
                            ResponseFields.ERROR: {
                                "code": str(HTTPStatus.BAD_REQUEST),
                                ResponseFields.MESSAGE: f"Validation errors: {'; '.join(validation_errors[:5])}"  # Limit error messages
                            }
                        }, HTTPStatus.BAD_REQUEST
                    
                    if not valid_instruments:
                        return {
                            ResponseFields.STATUS: "error",
                            ResponseFields.ERROR: {
                                "code": str(HTTPStatus.BAD_REQUEST),
                                ResponseFields.MESSAGE: "No valid instruments found after validation"
                            }
                        }, HTTPStatus.BAD_REQUEST
                    
                    # Use BatchDataExtractor for optimized ISIN list processing
                    logger.info(f"Starting batch ISIN list processing for {len(valid_instruments)} instruments")
                    
                    # Group ISINs by type for optimized processing
                    isin_groups = {}
                    for instr in valid_instruments:
                        instr_type = instr["type"]
                        if instr_type not in isin_groups:
                            isin_groups[instr_type] = []
                        isin_groups[instr_type].append(instr["isin"])
                    
                    # Process each instrument type group using batch extractor
                    total_results = {
                        "total_requested": len(valid_instruments),
                        "total_created": 0,
                        "total_skipped": 0,
                        "total_failed": 0,
                        "failed_instruments": [],
                        "created_instruments": [],
                        "type_breakdown": {}
                    }
                    
                    for instr_type, isins in isin_groups.items():
                        logger.info(f"Processing {len(isins)} {instr_type} instruments")
                        
                        try:
                            # Create instruments for this type batch
                            type_results = []
                            failed_isins = []
                            
                            # Use fast bulk creation for performance (no enrichment for isin_list method)
                            try:
                                bulk_result = instrument_service.bulk_create_instruments_fast(isins, instr_type)
                                
                                # Add successful creations to results
                                for isin in bulk_result.get("created_instruments", []):
                                    type_results.append(isin)
                                    total_results["created_instruments"].append({
                                        "isin": isin,
                                        "type": instr_type,
                                        "id": None  # Bulk creation doesn't return individual IDs
                                    })
                                
                                # Add failures 
                                failed_isins.extend(bulk_result.get("failed_instruments", []))
                                
                            except Exception as bulk_error:
                                logger.error(f"Bulk creation failed for {instr_type}: {str(bulk_error)}")
                                failed_isins.extend(isins)
                            
                            total_results["total_created"] += len(type_results)
                            total_results["total_failed"] += len(failed_isins)
                            total_results["type_breakdown"][instr_type] = {
                                "requested": len(isins),
                                "created": len(type_results),
                                "failed": len(failed_isins)
                            }
                            
                        except Exception as e:
                            logger.error(f"Error processing {instr_type} batch: {str(e)}")
                            total_results["total_failed"] += len(isins)
                            for isin in isins:
                                total_results["failed_instruments"].append({
                                    "isin": isin,
                                    "type": instr_type,
                                    "error": f"Batch processing error: {str(e)}"
                                })
                    
                    return {
                        ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                        ResponseFields.MESSAGE: f"ISIN list import completed: {total_results['total_created']} created, {total_results['total_failed']} failed",
                        ResponseFields.DATA: total_results
                    }, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error in batch instrument creation: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: f"Internal server error: {str(e)}"
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @instruments_ns.route("/figi/batch")
    class BatchFigi(Resource):
        @instruments_ns.doc(
            description="Map ISINs to Bloomberg FIGIs for unmapped instruments",
            responses={
                HTTPStatus.OK: ("Success", common_models["success_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Server Error", common_models["error_model"]),
            },
        )
        def post(self):
            """Map ISINs to Bloomberg FIGIs using OpenFIGI API"""
            try:
                data = request.get_json()
                isins = data.get("isins", []) if data else None
                
                # Use service layer for business logic
                instrument_service = InstrumentService()
                results = instrument_service.batch_enrich_figi(isins=isins, batch_size=50)
                
                return {
                    ResponseFields.STATUS: "success",
                    ResponseFields.MESSAGE: f"FIGI mapping completed: {results['mapped']} instruments mapped to FIGIs ({results['processed']} processed, {results['failed']} failed, {results.get('skipped', 0)} skipped)",
                    "processed": results["processed"],
                    "mapped": results["mapped"],
                    "failed": results["failed"],
                    "total": results["total"],
                    "skipped": results.get("skipped", 0)
                }, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error in batch FIGI mapping: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @instruments_ns.route("/stats")
    class InstrumentStats(Resource):
        @instruments_ns.doc(
            description="Get general instrument statistics",
            responses={
                HTTPStatus.OK: ("Success", common_models["success_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Server Error", common_models["error_model"]),
            },
        )
        def get(self):
            """Get general instrument statistics"""
            try:
                instrument_service = InstrumentService()
                
                # Get basic count statistics
                from ...database.session import get_session
                with get_session() as session:
                    total_instruments = session.query(instrument_service.Instrument).count()
                    
                    # Count by CFI type (first letter of CFI code)
                    cfi_type_counts = {}
                    cfi_types = ['C', 'D', 'E', 'F', 'H', 'I', 'J', 'O', 'R', 'S']
                    
                    for cfi_type in cfi_types:
                        count = session.query(instrument_service.Instrument).filter(
                            instrument_service.Instrument.cfi_code.like(f'{cfi_type}%')
                        ).count()
                        if count > 0:
                            cfi_type_counts[cfi_type] = count
                    
                    # Also count by instrument type for backward compatibility
                    type_counts = {}
                    from ...models.utils.cfi_instrument_manager import get_valid_instrument_types
                    valid_types = get_valid_instrument_types()
                    
                    for instrument_type in valid_types:
                        count = session.query(instrument_service.Instrument).filter(
                            instrument_service.Instrument.instrument_type == instrument_type
                        ).count()
                        if count > 0:
                            type_counts[instrument_type] = count
                    
                    # Count with/without LEI
                    with_lei = session.query(instrument_service.Instrument).filter(
                        instrument_service.Instrument.lei_id.isnot(None),
                        instrument_service.Instrument.lei_id != ""
                    ).count()
                    
                    # Count with FIGI mappings
                    with_figi = session.query(instrument_service.Instrument).filter(
                        instrument_service.Instrument.figi_mappings.any()
                    ).count()
                
                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: {
                        "total_instruments": total_instruments,
                        "cfi_type_breakdown": cfi_type_counts,
                        "type_breakdown": type_counts,
                        "lei_coverage": {
                            "with_lei": with_lei,
                            "without_lei": total_instruments - with_lei,
                            "percentage": round((with_lei / total_instruments * 100) if total_instruments > 0 else 0, 1)
                        },
                        "figi_coverage": {
                            "with_figi": with_figi,
                            "without_figi": total_instruments - with_figi,
                            "percentage": round((with_figi / total_instruments * 100) if total_instruments > 0 else 0, 1)
                        }
                    },
                    ResponseFields.MESSAGE: "Instrument statistics retrieved successfully"
                }, HTTPStatus.OK
            
            except Exception as e:
                logger.error(f"Error getting instrument statistics: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @instruments_ns.route("/stats/coverage")
    class DataCoverageStats(Resource):
        @instruments_ns.doc(
            description="Get data coverage statistics for instruments",
            responses={
                HTTPStatus.OK: ("Success", common_models["success_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Server Error", common_models["error_model"]),
            },
        )
        def get(self):
            """Get statistics on data coverage (entities, FIGIs, transparency)"""
            try:
                with get_session() as session:
                    # Get total number of instruments
                    total_instruments = session.query(func.count(distinct(Instrument.isin))).scalar() or 0
                    
                    if total_instruments == 0:
                        # Return zeros if no instruments
                        coverage_stats = {
                            "total_instruments": 0,
                            "entity_coverage": {"covered": 0, "percentage": 0.0},
                            "figi_coverage": {"covered": 0, "percentage": 0.0},
                            "transparency_coverage": {"covered": 0, "percentage": 0.0}
                        }
                    else:
                        # Count instruments with actual legal entity records linked
                        instruments_with_entities = session.query(
                            func.count(distinct(Instrument.isin))
                        ).join(
                            LegalEntity, Instrument.lei_id == LegalEntity.lei
                        ).scalar() or 0
                        
                        # Count instruments with FIGI mappings
                        instruments_with_figis = session.query(
                            func.count(distinct(FigiMapping.isin))
                        ).scalar() or 0
                        
                        # Count instruments with transparency data
                        instruments_with_transparency = session.query(
                            func.count(distinct(TransparencyCalculation.isin))
                        ).scalar() or 0
                        
                        # Calculate percentages
                        entity_percentage = (instruments_with_entities / total_instruments) * 100
                        figi_percentage = (instruments_with_figis / total_instruments) * 100
                        transparency_percentage = (instruments_with_transparency / total_instruments) * 100
                        
                        coverage_stats = {
                            "total_instruments": total_instruments,
                            "entity_coverage": {
                                "covered": instruments_with_entities,
                                "percentage": round(entity_percentage, 1)
                            },
                            "figi_coverage": {
                                "covered": instruments_with_figis,
                                "percentage": round(figi_percentage, 1)
                            },
                            "transparency_coverage": {
                                "covered": instruments_with_transparency,
                                "percentage": round(transparency_percentage, 1)
                            }
                        }
                    
                    return {
                        ResponseFields.STATUS: "success",
                        "data": coverage_stats
                    }, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error getting coverage statistics: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    return instruments_ns
