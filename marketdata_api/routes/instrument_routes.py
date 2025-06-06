import logging
import traceback
from flask import Blueprint, jsonify, request
from ..services.instrument_service import InstrumentService
from ..database.session import get_session
from ..models.instrument import Instrument
from ..models.utils.cfi import CFI
from ..constants import (
    HTTPStatus, Pagination, API, InstrumentTypes, BatchOperations, 
    ErrorMessages, SuccessMessages, ResponseFields, Endpoints, 
    QueryParams, FormFields, DbFields
)
from typing import Dict, Any, List, Optional

# Setup logging
logger = logging.getLogger(__name__)

# Create blueprint for instrument operations
instrument_bp = Blueprint("instrument", __name__, url_prefix=API.PREFIX)

@instrument_bp.route(Endpoints.INSTRUMENTS, methods=["GET"])
def list_instruments():
    """Get all instruments with optional filtering"""
    try:
        # Query parameters for filtering
        instrument_type = request.args.get(QueryParams.TYPE)
        currency = request.args.get(QueryParams.CURRENCY)
        limit = request.args.get(QueryParams.LIMIT, Pagination.DEFAULT_LIMIT, type=int)
        offset = request.args.get(QueryParams.OFFSET, Pagination.DEFAULT_OFFSET, type=int)
        page = request.args.get(QueryParams.PAGE, Pagination.DEFAULT_PAGE, type=int)
        per_page = min(request.args.get(QueryParams.PER_PAGE, Pagination.DEFAULT_PER_PAGE, type=int), Pagination.MAX_PER_PAGE)
        
        with get_session() as session:
            query = session.query(Instrument)
            
            # Apply filters - Debug log to check the filter
            logger.debug(f"Filtering instruments with type={instrument_type}, currency={currency}")
            if instrument_type:
                query = query.filter(Instrument.type == instrument_type)
                # Additional debug to check if this filter matches anything
                count = query.count()
                logger.debug(f"Found {count} instruments with type={instrument_type}")
            if currency:
                query = query.filter(Instrument.currency == currency)
                
            # Get total count for pagination
            total_count = query.count()
            
            # Apply pagination
            instruments = query.limit(limit).offset(offset).all()
            
            result = []
            for instrument in instruments:
                result.append({
                    "id": instrument.id,
                    "type": instrument.type,
                    "isin": instrument.isin,
                    "symbol": instrument.symbol,
                    "full_name": instrument.full_name,
                    "currency": instrument.currency,
                    "cfi_code": instrument.cfi_code
                })
            # Match the expected response format from swagger
            return jsonify({
                ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS, 
                ResponseFields.DATA: result,
                ResponseFields.META: {
                    ResponseFields.PAGE: page,
                    ResponseFields.PER_PAGE: per_page,
                    ResponseFields.TOTAL: total_count
                }
            })
            
    except Exception as e:
        logger.error(f"Error in list_instruments: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@instrument_bp.route(f"{Endpoints.INSTRUMENTS}/<string:identifier>", methods=["GET"])
def get_instrument(identifier):
    """Get instrument details by ID or ISIN, create from FIRDS if not found"""
    try:
        service = InstrumentService()
        
        # First try to get existing instrument
        session, instrument = service.get_instrument(identifier)
        
        if not instrument:
            # If not found, try to get or create from FIRDS (assume equity type for now)
            instrument = service.get_or_create_instrument(identifier, "equity")
            if instrument:
                # Get fresh session for the new instrument
                session, instrument = service.get_instrument(instrument.id)
        
        if not instrument:
            return jsonify({ResponseFields.ERROR: ErrorMessages.INSTRUMENT_NOT_FOUND}), HTTPStatus.NOT_FOUND
        
        # Build detailed response including relationships
        result = build_instrument_response(instrument)
        session.close()
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in get_instrument: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@instrument_bp.route(Endpoints.INSTRUMENTS, methods=["POST"])
def create_instrument():
    """Create a new instrument or get from FIRDS if not found"""
    try:
        data = request.json
        if not data:
            return jsonify({ResponseFields.ERROR: ErrorMessages.NO_DATA_PROVIDED}), HTTPStatus.BAD_REQUEST
            
        # Required fields - use Id instead of isin to match service expectations
        if "Id" not in data or DbFields.TYPE not in data:
            return jsonify({ResponseFields.ERROR: "Id and type are required"}), HTTPStatus.BAD_REQUEST
            
        instrument_type = data[DbFields.TYPE]
        if instrument_type not in InstrumentTypes.VALID_TYPES:
            return jsonify({ResponseFields.ERROR: ErrorMessages.INVALID_INSTRUMENT_TYPE}), HTTPStatus.BAD_REQUEST
            
        service = InstrumentService()
        instrument = service.get_or_create_instrument(data["Id"], instrument_type)
        
        return jsonify({
            ResponseFields.MESSAGE: SuccessMessages.INSTRUMENT_CREATED,
            DbFields.ID: instrument.id,
            DbFields.ISIN: instrument.isin,
            DbFields.TYPE: instrument.type
        }), HTTPStatus.CREATED
        
    except Exception as e:
        logger.error(f"Error in create_instrument: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@instrument_bp.route(f"{Endpoints.INSTRUMENTS}/<string:identifier>", methods=["PUT"])
def update_instrument(identifier):
    """Update an existing instrument"""
    try:
        data = request.json
        if not data:
            return jsonify({ResponseFields.ERROR: ErrorMessages.NO_DATA_PROVIDED}), HTTPStatus.BAD_REQUEST
            
        service = InstrumentService()
        instrument = service.update_instrument(identifier, data)
        
        if not instrument:
            return jsonify({ResponseFields.ERROR: ErrorMessages.INSTRUMENT_NOT_FOUND}), HTTPStatus.NOT_FOUND
            
        return jsonify({
            ResponseFields.MESSAGE: SuccessMessages.INSTRUMENT_UPDATED,
            DbFields.ID: instrument.id,
            DbFields.ISIN: instrument.isin,
            DbFields.TYPE: instrument.type
        })
        
    except Exception as e:
        logger.error(f"Error in update_instrument: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@instrument_bp.route(f"{Endpoints.INSTRUMENTS}/<string:identifier>", methods=["DELETE"])
def delete_instrument(identifier):
    """Delete an instrument"""
    try:
        service = InstrumentService()
        result = service.delete_instrument(identifier)
        
        if not result:
            return jsonify({ResponseFields.ERROR: ErrorMessages.INSTRUMENT_NOT_FOUND}), HTTPStatus.NOT_FOUND
            
        return jsonify({
            ResponseFields.MESSAGE: SuccessMessages.INSTRUMENT_DELETED,
            "identifier": identifier
        })
        
    except Exception as e:
        logger.error(f"Error in delete_instrument: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@instrument_bp.route(f"{Endpoints.INSTRUMENTS}/<string:identifier>/enrich", methods=["POST"])
def enrich_instrument(identifier):
    """Enrich an instrument with FIGI and LEI data"""
    try:
        service = InstrumentService()
        session, instrument = service.get_instrument(identifier)
        
        if not instrument:
            return jsonify({ResponseFields.ERROR: ErrorMessages.INSTRUMENT_NOT_FOUND}), HTTPStatus.NOT_FOUND
            
        # Track current enrichment state
        pre_figi = True if instrument.figi_mapping else False
        pre_lei = True if instrument.legal_entity else False
        
        # Perform enrichment
        session, enriched = service.enrich_instrument(instrument)
        
        # Track post-enrichment state
        post_figi = True if enriched.figi_mapping else False
        post_lei = True if enriched.legal_entity else False
        
        session.close()
        
        return jsonify({
            ResponseFields.MESSAGE: SuccessMessages.INSTRUMENT_ENRICHED,
            DbFields.ID: enriched.id,
            DbFields.ISIN: enriched.isin,
            "enrichment_results": {
                DbFields.FIGI: {
                    "before": pre_figi,
                    "after": post_figi,
                    "changed": post_figi != pre_figi
                },
                DbFields.LEI: {
                    "before": pre_lei,
                    "after": post_lei,
                    "changed": post_lei != pre_lei
                }
            }
        })
        
    except Exception as e:
        logger.error(f"Error in enrich_instrument: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

# Batch operations endpoint
@instrument_bp.route(Endpoints.BATCH_INSTRUMENTS, methods=["POST"])
def batch_process_instruments():
    """Batch process instruments (create or enrich)"""
    try:
        data = request.json
        if not data or not isinstance(data, dict):
            return jsonify({ResponseFields.ERROR: ErrorMessages.INVALID_DATA_FORMAT}), HTTPStatus.BAD_REQUEST
            
        operation = data.get(FormFields.OPERATION)
        if operation not in BatchOperations.VALID_OPERATIONS:
            return jsonify({ResponseFields.ERROR: ErrorMessages.INVALID_BATCH_OPERATION}), HTTPStatus.BAD_REQUEST
            
        identifiers = data.get(FormFields.IDENTIFIERS)
        if not identifiers or not isinstance(identifiers, list):
            return jsonify({ResponseFields.ERROR: ErrorMessages.MISSING_IDENTIFIERS}), HTTPStatus.BAD_REQUEST
            
        instrument_type = data.get(QueryParams.TYPE, InstrumentTypes.EQUITY)
        if instrument_type not in InstrumentTypes.VALID_TYPES:
            return jsonify({ResponseFields.ERROR: ErrorMessages.INVALID_INSTRUMENT_TYPE}), HTTPStatus.BAD_REQUEST
            
        service = InstrumentService()
        results = {ResponseFields.SUCCESSFUL: [], ResponseFields.FAILED: []}
        
        for isin in identifiers:
            try:
                if operation == BatchOperations.CREATE:
                    instrument = service.get_or_create_instrument(isin, instrument_type)
                    if instrument:
                        results[ResponseFields.SUCCESSFUL].append({
                            DbFields.ISIN: isin,
                            DbFields.ID: instrument.id,
                            DbFields.TYPE: instrument.type
                        })
                    else:
                        results[ResponseFields.FAILED].append({
                            DbFields.ISIN: isin,
                            ResponseFields.ERROR: "Failed to create instrument"
                        })
                elif operation == BatchOperations.ENRICH:
                    session, instrument = service.get_instrument(isin)
                    if instrument:
                        session, enriched = service.enrich_instrument(instrument)
                        results[ResponseFields.SUCCESSFUL].append({
                            DbFields.ISIN: isin,
                            DbFields.ID: enriched.id,
                            DbFields.TYPE: enriched.type,
                            DbFields.FIGI: enriched.figi_mapping.figi if enriched.figi_mapping else None,
                            DbFields.LEI: enriched.legal_entity.lei if enriched.legal_entity else None
                        })
                    else:
                        results[ResponseFields.FAILED].append({
                            DbFields.ISIN: isin,
                            ResponseFields.ERROR: ErrorMessages.INSTRUMENT_NOT_FOUND
                        })
            except Exception as e:
                results[ResponseFields.FAILED].append({
                    DbFields.ISIN: isin,
                    ResponseFields.ERROR: str(e)
                })
                
        return jsonify({
            ResponseFields.OPERATION: operation,
            ResponseFields.TYPE: instrument_type,
            ResponseFields.TOTAL: len(identifiers),
            ResponseFields.SUCCESSFUL: len(results[ResponseFields.SUCCESSFUL]),
            ResponseFields.FAILED: len(results[ResponseFields.FAILED]),
            ResponseFields.RESULTS: results
        })
        
    except Exception as e:
        logger.error(f"Error in batch_process_instruments: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

# Helper function to build detailed instrument response
def build_instrument_response(instrument):
    """Build comprehensive response with all instrument details"""
    response = {
        "id": instrument.id,
        "type": instrument.type,
        "isin": instrument.isin,
        "full_name": instrument.full_name,
        "symbol": instrument.symbol,
        "cfi_code": instrument.cfi_code,
        "currency": instrument.currency,
        "trading_venue": instrument.trading_venue,
        "relevant_venue": instrument.relevant_venue,
        "relevant_authority": instrument.relevant_authority,
        "first_trade_date": instrument.first_trade_date.isoformat() if instrument.first_trade_date else None,
        "termination_date": instrument.termination_date.isoformat() if getattr(instrument, "termination_date", None) else None,
        "created_at": instrument.created_at.isoformat() if instrument.created_at else None,
        "updated_at": instrument.updated_at.isoformat() if instrument.updated_at else None
    }
    
    # Add CFI decoding if available
    if instrument.cfi_code and len(instrument.cfi_code) == 6:
        try:
            cfi = CFI(instrument.cfi_code)
            response["cfi_decoded"] = cfi.describe()
        except Exception as e:
            response["cfi_decoded"] = {"error": str(e)}
    
    # Add type-specific attributes
    instrument_type = instrument.type
    if instrument_type == "equity":
        response["equity_attributes"] = {
            "asset_class": instrument.asset_class,
            "shares_outstanding": instrument.shares_outstanding,
            "market_cap": instrument.market_cap,
            "sector": instrument.sector,
            "industry": instrument.industry
        }
    elif instrument_type == "debt":
        response["debt_attributes"] = {
            "maturity_date": instrument.maturity_date.isoformat() if instrument.maturity_date else None,
            "total_issued_nominal": instrument.total_issued_nominal,
            "nominal_value_per_unit": instrument.nominal_value_per_unit,
            "debt_seniority": instrument.debt_seniority
        }
    elif instrument_type == "future":
        response["future_attributes"] = {
            "expiration_date": instrument.expiration_date.isoformat() if instrument.expiration_date else None,
            "price_multiplier": instrument.price_multiplier,
            "delivery_type": instrument.delivery_type,
            "underlying_isin": (instrument.underlying_single_isin or 
                              instrument.basket_isin or 
                              instrument.underlying_index_isin)
        }
    
    # Add related entity info if available
    if instrument.legal_entity:
        response["legal_entity"] = {
            "lei": instrument.legal_entity.lei,
            "name": instrument.legal_entity.name,
            "jurisdiction": instrument.legal_entity.jurisdiction,
            "status": instrument.legal_entity.status
        }
    
    # Add FIGI mapping if available
    if instrument.figi_mapping:
        response["figi"] = {
            "figi": instrument.figi_mapping.figi,
            "composite_figi": instrument.figi_mapping.composite_figi,
            "share_class_figi": instrument.figi_mapping.share_class_figi,
            "security_type": instrument.figi_mapping.security_type,
            "market_sector": instrument.figi_mapping.market_sector
        }
    
    return response
