from flask import Blueprint, render_template, send_from_directory, send_file, current_app
from flask import Blueprint
from flask_restx import Api, Resource, fields
from ..constants import (
    HTTPStatus, Pagination, API as APIConstants, ResponseFields,
    ErrorMessages, Endpoints
)
import os

# Create a blueprint for Swagger documentation
swagger_bp = Blueprint('swagger', __name__, url_prefix=APIConstants.PREFIX)

# Initialize Flask-RESTx API
api = Api(swagger_bp,
         version=APIConstants.VERSION,
         title='MarketDataAPI',
         description='API for financial market data, instrument details, and legal entity information',
         doc='/swagger',
         authorizations={
            'apikey': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            }
         },
         security='apikey')

# Define namespaces for API resources
instruments_ns = api.namespace('instruments', description='Instrument operations')
legal_entities_ns = api.namespace('legal-entities', description='Legal entity operations')
relationships_ns = api.namespace('relationships', description='Entity relationship operations')
schemas_ns = api.namespace('schemas', description='Schema management operations')

# Define response models
error_model = api.model('Error', {
    ResponseFields.STATUS: fields.String(required=True, description="Error status", enum=["error"]),
    ResponseFields.ERROR: fields.Nested(api.model('ErrorDetails', {
        'code': fields.String(required=True, description="Error code"),
        ResponseFields.MESSAGE: fields.String(required=True, description="Error message description")
    }))
})

pagination_meta = api.model('PaginationMeta', {
    ResponseFields.PAGE: fields.Integer(description="Current page number"),
    ResponseFields.PER_PAGE: fields.Integer(description="Items per page"),
    ResponseFields.TOTAL: fields.Integer(description="Total number of items")
})

# Instrument models
instrument_base = api.model('InstrumentBase', {
    'id': fields.String(required=True, description="Unique identifier"),
    'isin': fields.String(required=True, description="International Securities Identification Number"),
    'type': fields.String(description="Instrument type (equity, debt, future, etc.)"),
    'full_name': fields.String(required=True, description="Full name of the instrument"),
    'symbol': fields.String(description="Symbol or short name"),
    'currency': fields.String(description="Currency code (ISO 4217)"),
    'cfi_code': fields.String(description="CFI code")
})

instrument_detailed = api.inherit('InstrumentDetailed', instrument_base, {
    'cfi_code': fields.String(description="CFI code"),
    'figi': fields.String(description="FIGI code"),
    'market_identifier_code': fields.String(description="Market identifier code"),
    'trading_venues': fields.List(fields.String, description="Trading venues"),
    'price_multiplier': fields.String(description="Price multiplier"),
    'classification': fields.Nested(api.model('Classification', {
        'cfi_category': fields.String(description="CFI category"),
        'cfi_group': fields.String(description="CFI group"),
        'description': fields.String(description="Description")
    })),
    'issuer': fields.Nested(api.model('Issuer', {
        'lei': fields.String(description="Legal Entity Identifier"),
        'name': fields.String(description="Legal name of the entity"),
        'jurisdiction': fields.String(description="Jurisdiction code (ISO 3166-1)"),
        'legal_form': fields.String(description="Legal form of the entity")
    }))
})

instrument_list_response = api.model('InstrumentListResponse', {
    'status': fields.String(required=True, description="Response status", enum=["success"]),
    'data': fields.List(fields.Nested(instrument_base)),
    'meta': fields.Nested(pagination_meta)
})

instrument_detail_response = api.model('InstrumentDetailResponse', {
    'status': fields.String(required=True, description="Response status", enum=["success"]),
    'data': fields.Nested(instrument_detailed)
})

# Legal Entity models
legal_entity_base = api.model('LegalEntityBase', {
    'lei': fields.String(required=True, description="Legal Entity Identifier (20 characters)"),
    'name': fields.String(required=True, description="Legal name of the entity"),
    'jurisdiction': fields.String(description="Jurisdiction code (ISO 3166-1)"),
    'legal_form': fields.String(description="Legal form of the entity"),
    'status': fields.String(description="Current status (Active, Inactive, Pending)")
})

legal_entity_detailed = api.inherit('LegalEntityDetailed', legal_entity_base, {
    'registered_as': fields.String(description="How the entity is registered"),
    'bic': fields.String(description="Business Identifier Code"),
    'next_renewal_date': fields.DateTime(description="Next renewal date for LEI"),
    'registration_status': fields.String(description="Registration status"),
    'managing_lou': fields.String(description="Managing Local Operating Unit")
})

legal_entity_list_response = api.model('LegalEntityListResponse', {
    'status': fields.String(required=True, description="Response status", enum=["success"]),
    'data': fields.List(fields.Nested(legal_entity_base)),
    'meta': fields.Nested(pagination_meta)
})

legal_entity_detail_response = api.model('LegalEntityDetailResponse', {
    'status': fields.String(required=True, description="Response status", enum=["success"]),
    'data': fields.Nested(legal_entity_detailed)
})

# Relationship models
relationship_base = api.model('RelationshipBase', {
    'relationship_type': fields.String(required=True, description="Type of relationship (DIRECT, ULTIMATE)"),
    'relationship_status': fields.String(required=True, description="Status of the relationship (ACTIVE, INACTIVE)"),
    'parent_lei': fields.String(required=True, description="LEI of the parent entity"),
    'parent_name': fields.String(required=True, description="Name of the parent entity"),
    'child_lei': fields.String(required=True, description="LEI of the child entity"),
    'child_name': fields.String(required=True, description="Name of the child entity"),
    'relationship_period_start': fields.DateTime(description="Start date of the relationship"),
    'relationship_period_end': fields.DateTime(description="End date of the relationship"),
    'percentage_ownership': fields.Float(description="Percentage of ownership")
})

relationship_list_response = api.model('RelationshipListResponse', {
    'status': fields.String(required=True, description="Response status", enum=["success"]),
    'data': fields.Nested(api.model('RelationshipData', {
        'entity': fields.Nested(legal_entity_base),
        'relationships': fields.List(fields.Nested(relationship_base))
    })),
    'meta': fields.Nested(pagination_meta)
})

# Schema models
schema_base = api.model('SchemaBase', {
    'id': fields.String(required=True, description="Unique identifier for the schema"),
    'name': fields.String(required=True, description="Display name for the schema"),
    'description': fields.String(description="Description of the schema and its purpose"),
    'type': fields.String(required=True, description="Type of the schema (instrument, legal_entity, relationship)"),
    'status': fields.String(description="Status of the schema (active, draft, deprecated)"),
    'version': fields.String(description="Version of the schema"),
    'created_at': fields.DateTime(description="Creation date"),
    'updated_at': fields.DateTime(description="Last update date")
})

schema_detailed = api.inherit('SchemaDetailed', schema_base, {
    'mapping_rules': fields.List(fields.Nested(api.model('MappingRule', {
        'source_field': fields.String(required=True, description="Source field in the original data"),
        'target_field': fields.String(required=True, description="Target field in the transformed data"),
        'transformation': fields.Raw(description="Transformation rule to apply")
    })))
})

schema_list_response = api.model('SchemaListResponse', {
    'status': fields.String(required=True, description="Response status", enum=["success"]),
    'data': fields.List(fields.Nested(schema_base)),
    'meta': fields.Nested(pagination_meta)
})

schema_detail_response = api.model('SchemaDetailResponse', {
    'status': fields.String(required=True, description="Response status", enum=["success"]),
    'data': fields.Nested(schema_detailed)
})

# Swagger documentation for instrument endpoints
@instruments_ns.route('/')
class InstrumentList(Resource):
    @instruments_ns.doc(
        description='Retrieves a paginated list of instruments',
        params={
            'type': 'Filter by instrument type (e.g., "equity", "debt", "future")',
            'currency': 'Filter by currency code',
            'page': f'Page number for paginated results (default: {Pagination.DEFAULT_PAGE})',
            'per_page': f'Number of records per page (default: {Pagination.DEFAULT_PER_PAGE}, max: {Pagination.MAX_PER_PAGE})',
            'limit': 'Maximum number of records to return',
            'offset': 'Number of records to skip'
        },
        responses={
            HTTPStatus.OK: 'Success',
            HTTPStatus.BAD_REQUEST: 'Invalid request',
            HTTPStatus.UNAUTHORIZED: 'Unauthorized'
        }
    )
    @instruments_ns.marshal_with(instrument_list_response)
    def get(self):
        '''Retrieves a paginated list of instruments'''
        from flask import request
        from ..database.session import get_session
        from ..models.instrument import Instrument
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:            # Query parameters for filtering
            instrument_type = request.args.get('type')
            currency = request.args.get('currency')
            limit = request.args.get('limit', Pagination.DEFAULT_LIMIT, type=int)
            offset = request.args.get('offset', Pagination.DEFAULT_OFFSET, type=int)
            page = request.args.get('page', Pagination.DEFAULT_PAGE, type=int)
            per_page = min(request.args.get('per_page', Pagination.DEFAULT_PER_PAGE, type=int), Pagination.MAX_PER_PAGE)
            
            with get_session() as session:
                query = session.query(Instrument)
                
                # Apply filters
                logger.debug(f"Swagger: Filtering instruments with type={instrument_type}, currency={currency}")
                if instrument_type:
                    query = query.filter(Instrument.type == instrument_type)
                    count = query.count()
                    logger.debug(f"Swagger: Found {count} instruments with type={instrument_type}")
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
                  # Return in the standardized format
                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS, 
                    ResponseFields.DATA: result,
                    ResponseFields.META: {
                        ResponseFields.PAGE: page,
                        ResponseFields.PER_PAGE: per_page,
                        ResponseFields.TOTAL: total_count
                    }
                }
                
        except Exception as e:
            logger.error(f"Error in swagger list_instruments: {str(e)}")
            return {ResponseFields.STATUS: "error", ResponseFields.ERROR: {"code": str(HTTPStatus.INTERNAL_SERVER_ERROR), ResponseFields.MESSAGE: str(e)}}, HTTPStatus.INTERNAL_SERVER_ERROR
    
@instruments_ns.route('/<string:isin>')
@instruments_ns.param('isin', 'International Securities Identification Number')
class InstrumentDetail(Resource):
    @instruments_ns.doc(
        description='Retrieves detailed information about a specific instrument by its ISIN',
        responses={
            HTTPStatus.OK: 'Success',
            HTTPStatus.NOT_FOUND: 'Instrument not found',
            HTTPStatus.UNAUTHORIZED: 'Unauthorized'
        }
    )
    #@instruments_ns.marshal_with(instrument_detail_response)
    def get(self, isin):
        '''Retrieves detailed information about a specific instrument by its ISIN'''
        from ..services.instrument_service import InstrumentService
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            service = InstrumentService()
            session, instrument = service.get_instrument(isin)
            
            if not instrument:
                return {ResponseFields.STATUS: "error", ResponseFields.ERROR: {"code": str(HTTPStatus.NOT_FOUND), ResponseFields.MESSAGE: ErrorMessages.INSTRUMENT_NOT_FOUND}}, HTTPStatus.NOT_FOUND
            
            # Build detailed response using the helper function from instrument_routes
            from ..routes.instrument_routes import build_instrument_response
            result = build_instrument_response(instrument)
            session.close()
            
            return {
                ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                ResponseFields.DATA: result
            }
            
        except Exception as e:
            logger.error(f"Error in swagger get_instrument: {str(e)}")
            return {ResponseFields.STATUS: "error", ResponseFields.ERROR: {"code": str(HTTPStatus.INTERNAL_SERVER_ERROR), ResponseFields.MESSAGE: str(e)}}, HTTPStatus.INTERNAL_SERVER_ERROR

# Similarly add swagger documentation for other endpoints...

# Legal entities endpoints
@legal_entities_ns.route('/')
class LegalEntityList(Resource):
    @legal_entities_ns.doc(
        description='Retrieves a paginated list of legal entities',
        params={
            'status': 'Filter by entity status (e.g., "ACTIVE", "INACTIVE", "PENDING")',
            'jurisdiction': 'Filter by jurisdiction code (ISO 3166-1)',
            'page': f'Page number for paginated results (default: {Pagination.DEFAULT_PAGE})',
            'per_page': f'Number of records per page (default: {Pagination.DEFAULT_PER_PAGE}, max: {Pagination.MAX_PER_PAGE})',
            'limit': 'Maximum number of records to return',
            'offset': 'Number of records to skip'
        },
        responses={
            HTTPStatus.OK: 'Success',
            HTTPStatus.BAD_REQUEST: 'Invalid request',
            HTTPStatus.UNAUTHORIZED: 'Unauthorized'
        }
    )
    @legal_entities_ns.marshal_with(legal_entity_list_response)
    def get(self):
        '''Retrieves a paginated list of legal entities'''
        from flask import request
        from ..services.legal_entity_service import LegalEntityService
        import logging
        
        logger = logging.getLogger(__name__)        
        try:
            # Query parameters for filtering
            status = request.args.get('status')
            jurisdiction = request.args.get('jurisdiction')
            limit = request.args.get('limit', Pagination.DEFAULT_LIMIT, type=int)
            offset = request.args.get('offset', Pagination.DEFAULT_OFFSET, type=int)
            page = request.args.get('page', Pagination.DEFAULT_PAGE, type=int)
            per_page = min(request.args.get('per_page', Pagination.DEFAULT_PER_PAGE, type=int), Pagination.MAX_PER_PAGE)
            
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
            return {
                ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS, 
                ResponseFields.DATA: result,
                ResponseFields.META: {
                    ResponseFields.PAGE: page,
                    ResponseFields.PER_PAGE: per_page,
                    ResponseFields.TOTAL: len(result)
                }
            }
                
        except Exception as e:
            logger.error(f"Error in swagger list_entities: {str(e)}")
            return {ResponseFields.STATUS: "error", ResponseFields.ERROR: {"code": str(HTTPStatus.INTERNAL_SERVER_ERROR), ResponseFields.MESSAGE: str(e)}}, HTTPStatus.INTERNAL_SERVER_ERROR
    
@legal_entities_ns.route('/<string:lei>')
@legal_entities_ns.param('lei', 'Legal Entity Identifier (20 characters)')
class LegalEntityDetail(Resource):
    @legal_entities_ns.doc(
        description='Retrieves detailed information about a specific legal entity by its LEI',
        responses={
            HTTPStatus.OK: 'Success',
            HTTPStatus.NOT_FOUND: 'Legal entity not found',
            HTTPStatus.UNAUTHORIZED: 'Unauthorized'
        }
    )
    @legal_entities_ns.marshal_with(legal_entity_detail_response)
    def get(self, lei):
        '''Retrieves detailed information about a specific legal entity by its LEI'''
        return None

# Relationships endpoints
@relationships_ns.route('/<string:lei>')
@relationships_ns.param('lei', 'Legal Entity Identifier (20 characters)')
class EntityRelationships(Resource):
    @relationships_ns.doc(
        description='Retrieves all relationships for a specific legal entity',
        params={
            'relationship_type': 'Filter by relationship type ("DIRECT", "ULTIMATE")',
            'relationship_status': 'Filter by relationship status ("ACTIVE", "INACTIVE")',
            'direction': 'Filter by relationship direction ("PARENT", "CHILD")',            'page': f'Page number for paginated results (default: {Pagination.DEFAULT_PAGE})',
            'per_page': f'Number of records per page (default: {Pagination.DEFAULT_PER_PAGE}, max: {Pagination.MAX_PER_PAGE})'
        },
        responses={
            HTTPStatus.OK: 'Success',
            HTTPStatus.NOT_FOUND: 'Legal entity not found',
            HTTPStatus.UNAUTHORIZED: 'Unauthorized'
        }
    )
    @relationships_ns.marshal_with(relationship_list_response)
    def get(self, lei):
        '''Retrieves all relationships for a specific legal entity'''
        return None

# Schema management endpoints
@schemas_ns.route('/')
class SchemaList(Resource):
    @schemas_ns.doc(
        description='Retrieves a list of all available schemas',
        params={
            'type': 'Filter by schema type ("instrument", "legal_entity", "relationship")',
            'status': 'Filter by schema status ("active", "draft", "deprecated")',
            'page': 'Page number for paginated results (default: 1)',
            'per_page': 'Number of records per page (default: 20, max: 100)'
        },
        responses={
            200: 'Success',
            400: 'Invalid request',
            401: 'Unauthorized'
        }
    )
    @schemas_ns.marshal_with(schema_list_response)
    def get(self):
        '''Retrieves a list of all available schemas'''
        return None

# Add a route to serve the OpenAPI specification
@swagger_bp.route('/openapi.yaml')
def serve_openapi_spec():
    # Get the absolute path to the openapi.yaml file
    openapi_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docs', 'openapi.yaml')
    return send_file(openapi_path, mimetype='text/yaml')

# Add a route to serve the Redoc documentation UI
@swagger_bp.route('/docs')
def serve_redoc_ui():
    return f'''
    <!DOCTYPE html>
    <html>
      <head>
        <title>MarketDataAPI Documentation</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
        <style>
          body {{
            margin: 0;
            padding: 0;
          }}
        </style>
      </head>
      <body>
        <redoc spec-url="{APIConstants.PREFIX}/openapi.yaml"></redoc>
        <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"></script>
      </body>
    </html>
    '''
