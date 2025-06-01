import logging
from flask import Blueprint, jsonify, request
from ..services.instrument_service import InstrumentService
from ..services.legal_entity_service import LegalEntityService
from ..database.session import get_session
from ..models.instrument import Instrument, Equity, Debt, Future
from ..models.legal_entity import LegalEntity
from ..models.utils.cfi import CFI
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, Any, List, Optional
import traceback

# Setup logging
logger = logging.getLogger(__name__)

# Create blueprint for CRUD operations
crud_bp = Blueprint("crud", __name__, url_prefix="/api/v1")

# Error handler for database errors
@crud_bp.errorhandler(SQLAlchemyError)
def handle_db_error(error):
    logger.error(f"Database error: {str(error)}")
    return jsonify({"error": "A database error occurred", "details": str(error)}), 500

# Root endpoint to provide API information
@crud_bp.route("/", methods=["GET"])
def api_info():
    """Root endpoint with API information"""
    return jsonify({
        "api": "MarketDataAPI CRUD API",
        "version": "1.0",
        "endpoints": {
            "instruments": "/api/v1/instruments",
            "entities": "/api/v1/entities",
            "cfi": "/api/v1/cfi/{cfi_code}"
        }
    })

# Instruments endpoints
@crud_bp.route("/instruments", methods=["GET"])
def list_instruments():
    """Get all instruments with optional filtering"""
    try:
        # Query parameters for filtering
        instrument_type = request.args.get('type')
        currency = request.args.get('currency')
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
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
                "status": "success", 
                "data": result,
                "meta": {
                    "page": page,
                    "per_page": per_page,
                    "total": total_count
                }
            })
            
    except Exception as e:
        logger.error(f"Error in list_instruments: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@crud_bp.route("/instruments/<string:identifier>", methods=["GET"])
def get_instrument(identifier):
    """Get instrument details by ID or ISIN"""
    try:
        service = InstrumentService()
        session, instrument = service.get_instrument(identifier)
        
        if not instrument:
            return jsonify({"error": "Instrument not found"}), 404
        
        # Build detailed response including relationships
        result = build_instrument_response(instrument)
        session.close()
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in get_instrument: {str(e)}")
        return jsonify({"error": str(e)}), 500

@crud_bp.route("/instruments", methods=["POST"])
def create_instrument():
    """Create a new instrument"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Required fields
        if "isin" not in data or "type" not in data:
            return jsonify({"error": "ISIN and type are required"}), 400
            
        instrument_type = data["type"]
        valid_types = ["equity", "debt", "future"]
        if instrument_type not in valid_types:
            return jsonify({"error": f"Invalid instrument type. Must be one of: {', '.join(valid_types)}"}), 400
            
        service = InstrumentService()
        instrument = service.create_instrument(data, instrument_type)
        
        return jsonify({
            "message": "Instrument created successfully",
            "id": instrument.id,
            "isin": instrument.isin,
            "type": instrument.type
        }), 201
        
    except Exception as e:
        logger.error(f"Error in create_instrument: {str(e)}")
        return jsonify({"error": str(e)}), 500

@crud_bp.route("/instruments/<string:identifier>", methods=["PUT"])
def update_instrument(identifier):
    """Update an existing instrument"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        service = InstrumentService()
        instrument = service.update_instrument(identifier, data)
        
        if not instrument:
            return jsonify({"error": "Instrument not found"}), 404
            
        return jsonify({
            "message": "Instrument updated successfully",
            "id": instrument.id,
            "isin": instrument.isin,
            "type": instrument.type
        })
        
    except Exception as e:
        logger.error(f"Error in update_instrument: {str(e)}")
        return jsonify({"error": str(e)}), 500

@crud_bp.route("/instruments/<string:identifier>", methods=["DELETE"])
def delete_instrument(identifier):
    """Delete an instrument"""
    try:
        service = InstrumentService()
        result = service.delete_instrument(identifier)
        
        if not result:
            return jsonify({"error": "Instrument not found"}), 404
            
        return jsonify({
            "message": "Instrument deleted successfully",
            "identifier": identifier
        })
        
    except Exception as e:
        logger.error(f"Error in delete_instrument: {str(e)}")
        return jsonify({"error": str(e)}), 500

@crud_bp.route("/instruments/<string:identifier>/enrich", methods=["POST"])
def enrich_instrument(identifier):
    """Enrich an instrument with FIGI and LEI data"""
    try:
        service = InstrumentService()
        session, instrument = service.get_instrument(identifier)
        
        if not instrument:
            return jsonify({"error": "Instrument not found"}), 404
            
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
            "message": "Instrument enriched successfully",
            "id": enriched.id,
            "isin": enriched.isin,
            "enrichment_results": {
                "figi": {
                    "before": pre_figi,
                    "after": post_figi,
                    "changed": post_figi != pre_figi
                },
                "lei": {
                    "before": pre_lei,
                    "after": post_lei,
                    "changed": post_lei != pre_lei
                }
            }
        })
        
    except Exception as e:
        logger.error(f"Error in enrich_instrument: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Legal Entity endpoints
@crud_bp.route("/entities", methods=["GET"])
def list_entities():
    """Get all legal entities with optional filtering"""
    try:
        # Query parameters for filtering
        status = request.args.get('status')
        jurisdiction = request.args.get('jurisdiction')
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        # Create filters dictionary only if we have filters to apply
        filters = {}
        if status:
            filters['status'] = status
        if jurisdiction:
            filters['jurisdiction'] = jurisdiction
        
        service = LegalEntityService()
        session, entities = service.get_all_entities(
            limit=limit,
            offset=offset,
            filters=filters if filters else None
        )
        
        result = []
        for entity in entities:
            result.append({
                "lei": entity.lei,
                "name": entity.name,
                "jurisdiction": entity.jurisdiction,
                "legal_form": entity.legal_form,
                "status": entity.status
            })
                
        session.close()
        
        # Return in the new standardized format
        return jsonify({
            "status": "success", 
            "data": result,
            "meta": {
                "page": page,
                "per_page": per_page,
                "total": len(result)
            }
        })
            
    except Exception as e:
        logger.error(f"Error in list_entities: {str(e)}")
        return jsonify({"error": str(e)}), 500

@crud_bp.route("/entities/<string:lei>", methods=["GET"])
def get_entity(lei):
    """Get legal entity by LEI code"""
    try:
        service = LegalEntityService()
        session, entity = service.get_entity(lei)
        
        if not entity:
            return jsonify({"error": "Legal entity not found"}), 404
        
        # Build comprehensive response
        result = {
            "lei": entity.lei,
            "name": entity.name,
            "jurisdiction": entity.jurisdiction,
            "legal_form": entity.legal_form,
            "registered_as": entity.registered_as,
            "status": entity.status,
            "creation_date": entity.creation_date.isoformat() if entity.creation_date else None,
            "next_renewal_date": entity.next_renewal_date.isoformat() if entity.next_renewal_date else None
        }
        
        # Add addresses
        if entity.addresses:
            result["addresses"] = []
            for address in entity.addresses:
                result["addresses"].append({
                    "type": address.type,
                    "address_lines": address.address_lines,
                    "country": address.country,
                    "city": address.city,
                    "region": address.region,
                    "postal_code": address.postal_code
                })
        
        # Add registration details
        if entity.registration:
            result["registration"] = {
                "status": entity.registration.status,
                "last_update": entity.registration.last_update.isoformat() if entity.registration.last_update else None,
                "next_renewal": entity.registration.next_renewal.isoformat() if entity.registration.next_renewal else None,
                "managing_lou": entity.registration.managing_lou,
                "validation_sources": entity.registration.validation_sources
            }
        
        session.close()
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in get_entity: {str(e)}")
        return jsonify({"error": str(e)}), 500

@crud_bp.route("/entities/<string:lei>", methods=["PUT", "POST"])
def create_or_update_entity(lei):
    """Create or update a legal entity"""
    try:
        service = LegalEntityService()
        session, entity = service.create_or_update_entity(lei)
        
        if not entity:
            return jsonify({"error": "Failed to create or update entity"}), 500
            
        session.close()
        return jsonify({
            "message": f"Legal entity {'updated' if request.method == 'PUT' else 'created'} successfully",
            "lei": entity.lei,
            "name": entity.name
        }), 201 if request.method == 'POST' else 200
        
    except Exception as e:
        logger.error(f"Error in create_or_update_entity: {str(e)}")
        return jsonify({"error": str(e)}), 500

@crud_bp.route("/entities/<string:lei>", methods=["DELETE"])
def delete_entity(lei):
    """Delete a legal entity"""
    try:
        service = LegalEntityService()
        result = service.delete_entity(lei)
        
        if not result:
            return jsonify({"error": "Legal entity not found"}), 404
            
        return jsonify({
            "message": "Legal entity deleted successfully",
            "lei": lei
        })
        
    except Exception as e:
        logger.error(f"Error in delete_entity: {str(e)}")
        return jsonify({"error": str(e)}), 500

# CFI code decoding endpoint
@crud_bp.route("/cfi/<string:cfi_code>", methods=["GET"])
def decode_cfi(cfi_code):
    """Decode a CFI code and return human-readable attributes"""
    try:
        cfi_code = cfi_code.upper()
        
        if len(cfi_code) != 6:
            return jsonify({"error": "CFI code must be 6 characters"}), 400
            
        cfi = CFI(cfi_code)
        result = cfi.describe()
        
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in decode_cfi: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Batch operations endpoint
@crud_bp.route("/batch/instruments", methods=["POST"])
def batch_process_instruments():
    """Batch process instruments (create or enrich)"""
    try:
        data = request.json
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Invalid data format"}), 400
            
        operation = data.get("operation")
        if operation not in ["create", "enrich"]:
            return jsonify({"error": "Invalid operation, must be 'create' or 'enrich'"}), 400
            
        identifiers = data.get("identifiers")
        if not identifiers or not isinstance(identifiers, list):
            return jsonify({"error": "Missing or invalid 'identifiers' list"}), 400
            
        instrument_type = data.get("type", "equity")
        if instrument_type not in ["equity", "debt", "future"]:
            return jsonify({"error": "Invalid instrument type"}), 400
            
        service = InstrumentService()
        results = {"successful": [], "failed": []}
        
        for isin in identifiers:
            try:
                if operation == "create":
                    instrument = service.get_or_create_instrument(isin, instrument_type)
                    if instrument:
                        results["successful"].append({
                            "isin": isin,
                            "id": instrument.id,
                            "type": instrument.type
                        })
                    else:
                        results["failed"].append({
                            "isin": isin,
                            "error": "Failed to create instrument"
                        })
                elif operation == "enrich":
                    session, instrument = service.get_instrument(isin)
                    if instrument:
                        session, enriched = service.enrich_instrument(instrument)
                        results["successful"].append({
                            "isin": isin,
                            "id": enriched.id,
                            "type": enriched.type,
                            "figi": enriched.figi_mapping.figi if enriched.figi_mapping else None,
                            "lei": enriched.legal_entity.lei if enriched.legal_entity else None
                        })
                    else:
                        results["failed"].append({
                            "isin": isin,
                            "error": "Instrument not found"
                        })
            except Exception as e:
                results["failed"].append({
                    "isin": isin,
                    "error": str(e)
                })
                
        return jsonify({
            "operation": operation,
            "type": instrument_type,
            "total": len(identifiers),
            "successful": len(results["successful"]),
            "failed": len(results["failed"]),
            "results": results
        })
        
    except Exception as e:
        logger.error(f"Error in batch_process_instruments: {str(e)}")
        return jsonify({"error": str(e)}), 500

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
