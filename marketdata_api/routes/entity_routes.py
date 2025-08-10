import logging
from flask import Blueprint, jsonify, request
from ..interfaces.factory.services_factory import ServicesFactory
from ..constants import (
    HTTPStatus, Pagination, API, ErrorMessages, SuccessMessages,
    ResponseFields, Endpoints, QueryParams, FormFields, DbFields
)
from typing import Dict, Any

# Setup logging
logger = logging.getLogger(__name__)

# Create blueprint for entity operations
entity_bp = Blueprint("entity", __name__, url_prefix=API.PREFIX)

@entity_bp.route(Endpoints.ENTITIES, methods=["GET"])
def list_entities():
    """Get all legal entities with optional filtering"""
    try:
        # Query parameters for filtering
        status = request.args.get(QueryParams.STATUS)
        jurisdiction = request.args.get(QueryParams.JURISDICTION)
        limit = request.args.get(QueryParams.LIMIT, Pagination.DEFAULT_LIMIT, type=int)
        offset = request.args.get(QueryParams.OFFSET, Pagination.DEFAULT_OFFSET, type=int)
        page = request.args.get(QueryParams.PAGE, Pagination.DEFAULT_PAGE, type=int)
        per_page = min(request.args.get(QueryParams.PER_PAGE, Pagination.DEFAULT_PER_PAGE, type=int), Pagination.MAX_PER_PAGE)
        
        # Create filters dictionary only if we have filters to apply
        filters = {}
        if status:
            filters[QueryParams.STATUS] = status
        if jurisdiction:
            filters[QueryParams.JURISDICTION] = jurisdiction
        
        service = ServicesFactory.get_legal_entity_service()
        session, entities = service.get_all_entities(
            limit=limit,
            offset=offset,
            filters=filters if filters else None
        )
        
        result = []
        for entity in entities:
            result.append({
                DbFields.LEI: entity.lei,
                DbFields.NAME: entity.name,
                DbFields.JURISDICTION: entity.jurisdiction,
                "legal_form": entity.legal_form,
                DbFields.STATUS: entity.status
            })
                
        session.close()
        
        # Return in the new standardized format
        return jsonify({
            ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS, 
            ResponseFields.DATA: result,
            ResponseFields.META: {
                ResponseFields.PAGE: page,
                ResponseFields.PER_PAGE: per_page,
                ResponseFields.TOTAL: len(result)
            }
        })
            
    except Exception as e:
        logger.error(f"Error in list_entities: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@entity_bp.route(f"{Endpoints.ENTITIES}/<string:lei>", methods=["GET"])
def get_entity(lei):
    """Get legal entity by LEI code with comprehensive details"""
    try:
        service = ServicesFactory.get_legal_entity_service()
        session, entity = service.get_entity(lei)
        
        if not entity:
            return jsonify({ResponseFields.ERROR: ErrorMessages.ENTITY_NOT_FOUND}), HTTPStatus.NOT_FOUND
        
        # Use the comprehensive API response method
        result = {
            ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
            ResponseFields.DATA: entity.to_api_response(
                include_relationships=True,
                include_addresses=True,
                include_registration=True
            )
        }
        
        session.close()
        return jsonify(result)        
    except Exception as e:
        logger.error(f"Error in get_entity: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@entity_bp.route(f"{Endpoints.ENTITIES}/<string:lei>", methods=["PUT", "POST"])
def create_or_update_entity(lei):
    """Create or update a legal entity"""
    try:
        service = ServicesFactory.get_legal_entity_service()
        session, entity = service.create_or_update_entity(lei)
        
        if not entity:
            return jsonify({ResponseFields.ERROR: ErrorMessages.FAILED_TO_CREATE_ENTITY}), HTTPStatus.INTERNAL_SERVER_ERROR
            
        session.close()
        return jsonify({
            ResponseFields.MESSAGE: f"Legal entity {'updated' if request.method == 'PUT' else 'created'} successfully",
            DbFields.LEI: entity.lei,
            DbFields.NAME: entity.name
        }), HTTPStatus.CREATED if request.method == 'POST' else HTTPStatus.OK
        
    except Exception as e:
        logger.error(f"Error in create_or_update_entity: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@entity_bp.route(f"{Endpoints.ENTITIES}/<string:lei>", methods=["DELETE"])
def delete_entity(lei):
    """Delete a legal entity"""
    try:
        service = ServicesFactory.get_legal_entity_service()
        result = service.delete_entity(lei)
        
        if not result:
            return jsonify({ResponseFields.ERROR: ErrorMessages.ENTITY_NOT_FOUND}), HTTPStatus.NOT_FOUND
            
        return jsonify({
            ResponseFields.MESSAGE: SuccessMessages.ENTITY_DELETED,
            DbFields.LEI: lei
        })
        
    except Exception as e:
        logger.error(f"Error in delete_entity: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@entity_bp.route(Endpoints.ENTITIES, methods=["POST"])
def create_entity():
    """Create a new legal entity"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({ResponseFields.ERROR: "No data provided"}), HTTPStatus.BAD_REQUEST
        
        # Extract LEI from data if provided
        lei = data.get('lei')
        if not lei:
            return jsonify({ResponseFields.ERROR: "LEI is required"}), HTTPStatus.BAD_REQUEST
        
        # Use the existing create_or_update_entity logic
        return create_or_update_entity(lei)
        
    except Exception as e:
        logger.error(f"Error in create_entity: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
