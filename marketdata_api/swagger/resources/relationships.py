"""
Relationships API Resources

This module contains Flask-RESTx resource definitions for entity relationship endpoints.
"""

from flask import request, current_app
from flask_restx import Resource, Namespace
from ...constants import HTTPStatus, Pagination, ResponseFields, ErrorMessages
import logging

logger = logging.getLogger(__name__)

def create_relationship_resources(api, models):
    """
    Create and register relationship-related API resources.
    
    Args:
        api: Flask-RESTx API instance
        models: Dictionary of registered models
        
    Returns:
        Namespace: Relationships namespace with registered resources
    """
    
    # Create namespace
    relationships_ns = api.namespace('relationships', description='Entity relationship operations')
    
    # Get model references
    relationship_models = models['relationships']
    common_models = models['common']
    
    @relationships_ns.route('/<string:lei>')
    @relationships_ns.param('lei', 'Legal Entity Identifier (20 characters)')
    class EntityRelationships(Resource):
        @relationships_ns.doc(
            description='Retrieves all relationships for a specific legal entity',
            params={
                'relationship_type': 'Filter by relationship type ("DIRECT", "ULTIMATE")',
                'relationship_status': 'Filter by relationship status ("ACTIVE", "INACTIVE")',
                'direction': 'Filter by relationship direction ("PARENT", "CHILD")',
                'include_hierarchy': 'Include hierarchical structure (true/false, default: false)',
                'page': f'Page number for paginated results (default: {Pagination.DEFAULT_PAGE})',
                'per_page': f'Number of records per page (default: {Pagination.DEFAULT_PER_PAGE}, max: {Pagination.MAX_PER_PAGE})'
            },
            responses={
                HTTPStatus.OK: ('Success', relationship_models['relationship_list_response']),
                HTTPStatus.NOT_FOUND: ('Legal entity not found', common_models['error_model']),
                HTTPStatus.INTERNAL_SERVER_ERROR: ('Internal server error', common_models['error_model'])
            }
        )
        @relationships_ns.marshal_with(relationship_models['relationship_list_response'])
        def get(self, lei):
            """Retrieves all relationships for a specific legal entity"""
            try:
                from ...interfaces.factory.services_factory import ServicesFactory
                from ...database.session import get_session
                
                # First check if the entity exists
                service = ServicesFactory.get_legal_entity_service()
                session, entity = service.get_entity(lei)
                
                if not entity:
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.NOT_FOUND),
                            ResponseFields.MESSAGE: ErrorMessages.ENTITY_NOT_FOUND
                        }
                    }, HTTPStatus.NOT_FOUND
                
                # Get query parameters
                relationship_type = request.args.get('relationship_type')
                relationship_status = request.args.get('relationship_status')
                direction = request.args.get('direction')
                include_hierarchy = request.args.get('include_hierarchy', 'false').lower() == 'true'
                page = request.args.get('page', Pagination.DEFAULT_PAGE, type=int)
                per_page = min(request.args.get('per_page', Pagination.DEFAULT_PER_PAGE, type=int), Pagination.MAX_PER_PAGE)
                
                # Get models directly
                from ...models.sqlite.legal_entity import EntityRelationship
                
                # Query relationships where this entity is either parent or child
                with get_session() as rel_session:
                    query = rel_session.query(EntityRelationship).filter(
                        (EntityRelationship.parent_lei == lei) | (EntityRelationship.child_lei == lei)
                    )
                    
                    # Apply filters
                    if relationship_type:
                        query = query.filter(EntityRelationship.relationship_type == relationship_type)
                    if relationship_status:
                        query = query.filter(EntityRelationship.relationship_status == relationship_status)
                    if direction:
                        if direction.upper() == 'PARENT':
                            query = query.filter(EntityRelationship.child_lei == lei)
                        elif direction.upper() == 'CHILD':
                            query = query.filter(EntityRelationship.parent_lei == lei)
                    
                    relationships = query.all()
                    
                    # Build response
                    relationship_data = []
                    for rel in relationships:
                        relationship_data.append({
                            "relationship_type": rel.relationship_type,
                            "relationship_status": rel.relationship_status,
                            "parent_lei": rel.parent_lei,
                            "parent_name": rel.parent.name if rel.parent else None,
                            "parent_jurisdiction": rel.parent.jurisdiction if rel.parent else None,
                            "child_lei": rel.child_lei,
                            "child_name": rel.child.name if rel.child else None,
                            "child_jurisdiction": rel.child.jurisdiction if rel.child else None,
                            "relationship_period_start": rel.relationship_period_start.isoformat() if rel.relationship_period_start else None,
                            "relationship_period_end": rel.relationship_period_end.isoformat() if rel.relationship_period_end else None,
                            "percentage_ownership": rel.percentage_of_ownership
                        })
                
                result = {
                    "entity": {
                        "lei": entity.lei,
                        "name": entity.name,
                        "jurisdiction": entity.jurisdiction,
                        "legal_form": entity.legal_form,
                        "status": entity.status
                    },
                    "relationships": relationship_data
                }
                
                session.close()
                
                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: result,
                    ResponseFields.META: {
                        ResponseFields.PAGE: page,
                        ResponseFields.PER_PAGE: per_page,
                        ResponseFields.TOTAL: len(relationship_data)
                    }
                }
                
            except Exception as e:
                logger.error(f"Error in entity relationships endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e)
                    }
                }, HTTPStatus.INTERNAL_SERVER_ERROR
        
        @relationships_ns.doc(
            description='Create a new relationship for this entity',
            responses={
                HTTPStatus.CREATED: ('Relationship created successfully', relationship_models['relationship_list_response']),
                HTTPStatus.BAD_REQUEST: ('Invalid request', common_models['error_model']),
                HTTPStatus.NOT_FOUND: ('Entity not found', common_models['error_model']),
                HTTPStatus.CONFLICT: ('Relationship already exists', common_models['error_model']),
                HTTPStatus.INTERNAL_SERVER_ERROR: ('Internal server error', common_models['error_model'])
            }
        )
        @relationships_ns.expect(relationship_models['relationship_create_request'])
        def post(self, lei):
            """Create a new relationship for this entity"""
            try:
                # This would call the relationship creation logic from routes
                # For now, return a placeholder response
                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.MESSAGE: "Relationship creation endpoint - implementation pending"
                }, HTTPStatus.CREATED
                
            except Exception as e:
                logger.error(f"Error in relationship creation endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e)
                    }
                }, HTTPStatus.INTERNAL_SERVER_ERROR
    
    @relationships_ns.route('/hierarchy/<string:lei>')
    @relationships_ns.param('lei', 'Legal Entity Identifier for hierarchy root')
    class EntityHierarchy(Resource):
        @relationships_ns.doc(
            description='Get complete entity hierarchy starting from the specified entity',
            params={
                'max_depth': 'Maximum depth to traverse (default: 10)',
                'relationship_type': 'Filter by relationship type ("DIRECT", "ULTIMATE")',
                'include_inactive': 'Include inactive relationships (true/false, default: false)'
            },
            responses={
                HTTPStatus.OK: ('Success', relationship_models['relationship_hierarchy_response']),
                HTTPStatus.NOT_FOUND: ('Entity not found', common_models['error_model']),
                HTTPStatus.INTERNAL_SERVER_ERROR: ('Internal server error', common_models['error_model'])
            }
        )
        @relationships_ns.marshal_with(relationship_models['relationship_hierarchy_response'])
        def get(self, lei):
            """Get complete entity hierarchy"""
            try:
                # This would implement hierarchy traversal logic
                # For now, return a placeholder response
                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: {
                        "root_entity": {
                            "lei": lei,
                            "name": "Entity hierarchy endpoint - implementation pending",
                            "jurisdiction": None,
                            "legal_form": None,
                            "status": None
                        },
                        "hierarchy": {},
                        "total_entities": 0,
                        "max_depth": 0
                    }
                }
                
            except Exception as e:
                logger.error(f"Error in entity hierarchy endpoint: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e)
                    }
                }, HTTPStatus.INTERNAL_SERVER_ERROR
    
    return relationships_ns
