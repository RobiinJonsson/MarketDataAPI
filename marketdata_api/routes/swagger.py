from flask import Blueprint, render_template, send_from_directory, send_file, current_app, jsonify
from flask import Blueprint
from flask_restx import Api, Resource, fields

# Import transparency routes to register endpoints
from .transparency_routes import transparency_bp

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
         doc='/swagger/',
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
transparency_ns = api.namespace('transparency', description='Transparency calculation operations')

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

# Add address model
entity_address_model = api.model('EntityAddress', {
    'type': fields.String(description="Address type"),
    'address_lines': fields.String(description="Address lines"),
    'country': fields.String(description="Country code"),
    'city': fields.String(description="City"),
    'region': fields.String(description="Region/State"),
    'postal_code': fields.String(description="Postal code")
})

# Add registration model
entity_registration_model = api.model('EntityRegistration', {
    'status': fields.String(description="Registration status"),
    'initial_date': fields.DateTime(description="Initial registration date"),
    'last_update': fields.DateTime(description="Last update date"),
    'next_renewal': fields.DateTime(description="Next renewal date"),
    'managing_lou': fields.String(description="Managing LOU"),
    'validation_sources': fields.String(description="Validation sources")
})

legal_entity_detailed = api.inherit('LegalEntityDetailed', legal_entity_base, {
    'registered_as': fields.String(description="How the entity is registered"),
    'bic': fields.String(description="Business Identifier Code"),
    'next_renewal_date': fields.DateTime(description="Next renewal date for LEI"),
    'registration_status': fields.String(description="Registration status"),
    'managing_lou': fields.String(description="Managing Local Operating Unit"),
    'creation_date': fields.DateTime(description="Entity creation date"),
    'addresses': fields.List(fields.Nested(entity_address_model), description="Entity addresses"),
    'registration': fields.Nested(entity_registration_model, description="Registration details")
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

# Transparency models
transparency_base = api.model('TransparencyBase', {
    'id': fields.String(required=True, description="Unique identifier"),
    'isin': fields.String(required=True, description="International Securities Identification Number"),
    'calculation_type': fields.String(required=True, description="Type of calculation", enum=['EQUITY', 'NON_EQUITY']),
    'tech_record_id': fields.String(description="Technical record identifier"),
    'from_date': fields.DateTime(description="From date"),
    'to_date': fields.DateTime(description="To date"),
    'liquidity': fields.Boolean(description="Liquidity indicator"),
    'total_transactions_executed': fields.Integer(description="Total number of transactions executed"),
    'total_volume_executed': fields.Float(description="Total volume of transactions executed"),
    'created_at': fields.DateTime(description="Creation timestamp"),
    'updated_at': fields.DateTime(description="Last update timestamp")
})

# Updated details models to match the actual response format
transparency_details = api.model('TransparencyDetails', {
    'type': fields.String(required=True, description="Type of transparency details", enum=['equity', 'debt', 'futures', 'non_equity', 'unknown']),
    'financial_instrument_classification': fields.String(description="Financial instrument classification (equity only)"),
    'methodology': fields.String(description="Methodology used (equity only)"),
    'average_daily_turnover': fields.Float(description="Average daily turnover (equity only)"),
    'large_in_scale': fields.Float(description="Large in scale threshold (equity only)"),
    'average_daily_number_of_transactions': fields.Float(description="Average daily number of transactions (equity only)"),
    'average_transaction_value': fields.Float(description="Average transaction value (equity only)"),
    'standard_market_size': fields.Float(description="Standard market size (equity only)"),
    'description': fields.String(description="Description (non-equity only)"),
    'bond_type': fields.String(description="Bond type (debt only)"),
    'is_liquid': fields.Boolean(description="Liquidity indicator (debt only)"),
    'underlying_isin': fields.String(description="Underlying instrument ISIN (futures only)"),
    'is_stock_dividend_future': fields.Boolean(description="Stock dividend future indicator (futures only)"),
    'pre_trade_large_in_scale_threshold': fields.Float(description="Pre-trade large in scale threshold (non-equity)"),
    'post_trade_large_in_scale_threshold': fields.Float(description="Post-trade large in scale threshold (non-equity)"),
    'criterion_name': fields.String(description="Criterion name (non-equity)"),
    'criterion_value': fields.String(description="Criterion value (non-equity)")
})

transparency_detailed = api.inherit('TransparencyDetailed', transparency_base, {
    'details': fields.Nested(transparency_details, description="Type-specific transparency details")
})

transparency_list_response = api.model('TransparencyListResponse', {
    'status': fields.String(required=True, description="Response status", enum=["success"]),
    'data': fields.List(fields.Nested(transparency_detailed)),
    'meta': fields.Nested(pagination_meta)
})

# Update the transparency create request model
transparency_create_request = api.model('TransparencyCreateRequest', {
    'isin': fields.String(required=True, description="International Securities Identification Number"),
    'instrument_type': fields.String(required=True, description="Type of instrument", enum=['equity', 'debt', 'futures', 'fund', 'derivative'])
})

batch_transparency_request = api.model('BatchTransparencyRequest', {
    'calculation_type': fields.String(required=True, description="Type of calculation", enum=['EQUITY', 'NON_EQUITY']),
    'isin_prefix': fields.String(description="ISIN prefix filter (e.g., 'NL' for Netherlands)"),
    'limit': fields.Integer(description="Maximum number of calculations to create", default=10),
    'cfi_type': fields.String(description="CFI type filter (D, F, E)", enum=['D', 'F', 'E'])
})

batch_create_transparency_request = api.model('BatchCreateTransparencyRequest', {
    'records': fields.List(fields.Nested(transparency_create_request), required=True, description="List of transparency records to create")
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
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:            # Query parameters for filtering
            instrument_type = request.args.get('type')
            currency = request.args.get('currency')
            limit = request.args.get('limit', Pagination.DEFAULT_LIMIT, type=int)
            offset = request.args.get('offset', Pagination.DEFAULT_OFFSET, type=int)
            page = request.args.get('page', Pagination.DEFAULT_PAGE, type=int)
            per_page = min(request.args.get('per_page', Pagination.DEFAULT_PER_PAGE, type=int), Pagination.MAX_PER_PAGE)
            
            # Get models directly instead of using factory
            from ..models.sqlite import Instrument
            
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
        from ..interfaces.factory.services_factory import ServicesFactory
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            service = ServicesFactory.get_instrument_service()
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

@instruments_ns.route('/<string:identifier>/venues')
@instruments_ns.param('identifier', 'Instrument identifier (ISIN, ID, or symbol)')
class InstrumentVenues(Resource):
    @instruments_ns.doc(
        description='Get all venue records where this instrument trades. Shows venue count and detailed venue information for trading optimization and venue-aware enrichment strategies.',
        params={
            'type': 'Instrument type for venue lookup (default: equity)',
        },
        responses={
            HTTPStatus.OK: 'Successfully retrieved venue information',
            HTTPStatus.NOT_FOUND: 'No venue records found for the specified instrument',
            HTTPStatus.INTERNAL_SERVER_ERROR: 'Internal server error'
        }
    )
    def get(self, identifier):
        '''Get all venue records for a specific instrument'''
        from flask import request
        from ..interfaces.factory.services_factory import ServicesFactory
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            # Get instrument type from query parameter (default to equity)
            instrument_type = request.args.get('type', 'equity')
            
            service = ServicesFactory.get_instrument_service()
            venues = service.get_instrument_venues(identifier, instrument_type)
            
            if not venues:
                return {
                    ResponseFields.STATUS: "error", 
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.NOT_FOUND), 
                        ResponseFields.MESSAGE: f"No venue records found for {identifier}"
                    }
                }, HTTPStatus.NOT_FOUND
            
            return {
                ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                ResponseFields.DATA: {
                    "isin": identifier,
                    "instrument_type": instrument_type,
                    "venue_count": len(venues),
                    "venues": venues
                }
            }
            
        except Exception as e:
            logger.error(f"Error in get_instrument_venues: {str(e)}")
            return {
                ResponseFields.STATUS: "error", 
                ResponseFields.ERROR: {
                    "code": str(HTTPStatus.INTERNAL_SERVER_ERROR), 
                    ResponseFields.MESSAGE: str(e)
                }
            }, HTTPStatus.INTERNAL_SERVER_ERROR

@instruments_ns.route('/<string:identifier>/enrich')
@instruments_ns.param('identifier', 'Instrument identifier (ISIN, ID, or symbol)')
class InstrumentEnrich(Resource):
    @instruments_ns.doc(
        description='Enrich an existing instrument by fetching FIGI data from OpenFIGI API and LEI data from GLEIF API. Uses venue-aware strategy for optimal OpenFIGI results and validates LEI relationships.',
        responses={
            HTTPStatus.OK: 'Successfully enriched instrument',
            HTTPStatus.NOT_FOUND: 'Instrument not found',
            HTTPStatus.INTERNAL_SERVER_ERROR: 'Enrichment failed due to external API errors or internal issues'
        }
    )
    def post(self, identifier):
        '''Enrich an instrument with FIGI and LEI data'''
        from ..interfaces.factory.services_factory import ServicesFactory
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            service = ServicesFactory.get_instrument_service()
            session, instrument = service.get_instrument(identifier)
            
            if not instrument:
                return {
                    ResponseFields.STATUS: "error", 
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.NOT_FOUND), 
                        ResponseFields.MESSAGE: ErrorMessages.INSTRUMENT_NOT_FOUND
                    }
                }, HTTPStatus.NOT_FOUND
                
            # Track current enrichment state
            pre_figi = True if instrument.figi_mapping else False
            pre_lei = True if instrument.legal_entity else False
            
            # Perform enrichment
            session, enriched = service.enrich_instrument(instrument)
            
            # Track post-enrichment state
            post_figi = True if enriched.figi_mapping else False
            post_lei = True if enriched.legal_entity else False
            
            session.close()
            
            return {
                ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                ResponseFields.MESSAGE: "Instrument enriched successfully",
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
            }
            
        except Exception as e:
            logger.error(f"Error in enrich_instrument: {str(e)}")
            return {
                ResponseFields.STATUS: "error", 
                ResponseFields.ERROR: {
                    "code": str(HTTPStatus.INTERNAL_SERVER_ERROR), 
                    ResponseFields.MESSAGE: f"Failed to enrich instrument: {str(e)}"
                }
            }, HTTPStatus.INTERNAL_SERVER_ERROR

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
        from ..interfaces.factory.services_factory import ServicesFactory
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
            
            service = ServicesFactory.get_legal_entity_service()
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
    # Remove the marshal_with decorator to prevent field filtering
    def get(self, lei):
        '''Retrieves detailed information about a specific legal entity by its LEI'''
        from ..interfaces.factory.services_factory import ServicesFactory
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            service = ServicesFactory.get_legal_entity_service()
            session, entity = service.get_entity(lei)
            
            if not entity:
                return {ResponseFields.STATUS: "error", ResponseFields.ERROR: {"code": str(HTTPStatus.NOT_FOUND), ResponseFields.MESSAGE: ErrorMessages.ENTITY_NOT_FOUND}}, HTTPStatus.NOT_FOUND
            
            # Build comprehensive response - same logic as entity_routes.py
            result = {
                "lei": entity.lei,
                "name": entity.name,
                "jurisdiction": entity.jurisdiction,
                "legal_form": entity.legal_form,
                "registered_as": entity.registered_as,
                "status": entity.status,
                "bic": entity.bic,
                "next_renewal_date": entity.next_renewal_date.isoformat() if entity.next_renewal_date else None,
                "registration_status": entity.registration_status,
                "managing_lou": entity.managing_lou,
                "creation_date": entity.creation_date.isoformat() if entity.creation_date else None
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
                    "initial_date": entity.registration.initial_date.isoformat() if entity.registration.initial_date else None,
                    "last_update": entity.registration.last_update.isoformat() if entity.registration.last_update else None,
                    "next_renewal": entity.registration.next_renewal.isoformat() if entity.registration.next_renewal else None,
                    "managing_lou": entity.registration.managing_lou,
                    "validation_sources": entity.registration.validation_sources
                }
            
            session.close()
            
            return {
                ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                ResponseFields.DATA: result
            }
            
        except Exception as e:
            logger.error(f"Error in swagger get_entity: {str(e)}")
            return {ResponseFields.STATUS: "error", ResponseFields.ERROR: {"code": str(HTTPStatus.INTERNAL_SERVER_ERROR), ResponseFields.MESSAGE: str(e)}}, HTTPStatus.INTERNAL_SERVER_ERROR

# Relationships endpoints
@relationships_ns.route('/<string:lei>')
@relationships_ns.param('lei', 'Legal Entity Identifier (20 characters)')
class EntityRelationships(Resource):
    @relationships_ns.doc(
        description='Retrieves all relationships for a specific legal entity',
        params={
            'relationship_type': 'Filter by relationship type ("DIRECT", "ULTIMATE")',
            'relationship_status': 'Filter by relationship status ("ACTIVE", "INACTIVE")',
            'direction': 'Filter by relationship direction ("PARENT", "CHILD")',
            'page': f'Page number for paginated results (default: {Pagination.DEFAULT_PAGE})',
            'per_page': f'Number of records per page (default: {Pagination.DEFAULT_PER_PAGE}, max: {Pagination.MAX_PER_PAGE})'
        },
        responses={
            HTTPStatus.OK: 'Success',
            HTTPStatus.NOT_FOUND: 'Legal entity not found',
            HTTPStatus.UNAUTHORIZED: 'Unauthorized'
        }
    )
    def get(self, lei):
        '''Retrieves all relationships for a specific legal entity'''
        from flask import request
        from ..interfaces.factory.services_factory import ServicesFactory
        from ..database.session import get_session
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            # First check if the entity exists
            service = ServicesFactory.get_legal_entity_service()
            session, entity = service.get_entity(lei)
            
            if not entity:
                return {ResponseFields.STATUS: "error", ResponseFields.ERROR: {"code": str(HTTPStatus.NOT_FOUND), ResponseFields.MESSAGE: ErrorMessages.ENTITY_NOT_FOUND}}, HTTPStatus.NOT_FOUND
            
            # Get query parameters
            relationship_type = request.args.get('relationship_type')
            relationship_status = request.args.get('relationship_status')
            direction = request.args.get('direction')
            page = request.args.get('page', Pagination.DEFAULT_PAGE, type=int)
            per_page = min(request.args.get('per_page', Pagination.DEFAULT_PER_PAGE, type=int), Pagination.MAX_PER_PAGE)
            
            # Get models directly instead of using factory
            from ..models.sqlite.legal_entity import EntityRelationship
            
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
                    # Determine if this entity is parent or child in this relationship
                    is_parent = rel.parent_lei == lei
                    
                    relationship_data.append({
                        "relationship_type": rel.relationship_type,
                        "relationship_status": rel.relationship_status,
                        "parent_lei": rel.parent_lei,
                        "parent_name": rel.parent.name if rel.parent else None,
                        "child_lei": rel.child_lei,
                        "child_name": rel.child.name if rel.child else None,
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
            logger.error(f"Error in swagger get_relationships: {str(e)}")
            return {ResponseFields.STATUS: "error", ResponseFields.ERROR: {"code": str(HTTPStatus.INTERNAL_SERVER_ERROR), ResponseFields.MESSAGE: str(e)}}, HTTPStatus.INTERNAL_SERVER_ERROR

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

# Import the transparency routes blueprint to ensure endpoints are registered
from . import transparency_routes

# Add transparency endpoints to the API
@transparency_ns.route('')
class TransparencyList(Resource):
    @api.doc('list_transparency_calculations')
    @api.marshal_with(transparency_list_response)
    @api.param('calculation_type', 'Filter by calculation type', enum=['EQUITY', 'NON_EQUITY'])
    @api.param('instrument_type', 'Filter by instrument type', enum=['equity', 'debt', 'futures'])
    @api.param('isin', 'Filter by ISIN')
    @api.param('page', 'Page number', type='integer', default=1)
    @api.param('per_page', 'Items per page', type='integer', default=20)
    def get(self):
        """Get all transparency calculations with optional filtering"""
        # Don't try to call the blueprint function directly - this causes issues
        # with how Flask handles the request context
        from flask import request
        from sqlalchemy.orm import joinedload
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            # Get query parameters
            calculation_type = request.args.get('calculation_type')
            instrument_type = request.args.get('instrument_type')
            isin = request.args.get('isin')
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 20, type=int), 100)
            
            # Use factory pattern for models
            # Get models directly instead of using factory
            from ..models.sqlite.transparency import TransparencyCalculation
            
            # Create a new session
            from ..database.session import SessionLocal
            session = SessionLocal()
            try:
                # Build query - unified model no longer needs joinedload for polymorphic relationships
                query = session.query(TransparencyCalculation)
                
                # Apply filters
                if calculation_type:
                    query = query.filter(TransparencyCalculation.calculation_type == calculation_type)
                if isin:
                    query = query.filter(TransparencyCalculation.isin == isin)
                
                # Get total count
                total_count = query.count()
                
                # Apply pagination
                offset = (page - 1) * per_page
                calculations = query.offset(offset).limit(per_page).all()
                
                # Use the formatting function from transparency_routes
                from .transparency_routes import format_unified_transparency
                
                # Format each calculation
                result = []
                for calc in calculations:
                    formatted_calc = format_unified_transparency(calc)
                    if formatted_calc:
                        result.append(formatted_calc)
                
                # Return in the expected format
                return {
                    'status': '200 OK',
                    'data': result,
                    'meta': {
                        'page': page,
                        'per_page': per_page,
                        'total': total_count
                    }
                }
            finally:
                session.close()
        except Exception as e:
            logger.error(f"Error in swagger transparency list: {str(e)}")
            logger.exception(e)
            return {'status': '500 Internal Server Error', 'error': str(e)}, 500
    
    @api.doc('create_transparency_calculation')
    @api.expect(transparency_create_request)
    @api.response(201, 'Transparency calculations created from FITRS data')
    @api.response(400, 'Bad request - missing required fields', error_model)
    @api.response(404, 'No transparency data found in FITRS for the given ISIN', error_model)
    def post(self):
        """Create transparency calculations from FITRS data for a given ISIN"""
        # Import here to avoid circular imports
        from flask import request, jsonify
        from ..interfaces.factory.services_factory import ServicesFactory
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            data = request.get_json()
            if not data:
                return {'status': '400 Bad Request', 'error': 'No data provided'}, 400
            
            # Get required parameters
            isin = data.get('isin')
            instrument_type = data.get('instrument_type')
            
            if not isin:
                return {'status': '400 Bad Request', 'error': 'ISIN is required'}, 400
            
            if not instrument_type:
                return {'status': '400 Bad Request', 'error': 'instrument_type is required'}, 400
            
            logger.info(f"Creating transparency calculations for ISIN={isin}, instrument_type={instrument_type}")
            
            # 1. Check if instrument exists, if not create it
            instrument_service = ServicesFactory.get_instrument_service()
            
            # First check if instrument exists
            session, instrument = instrument_service.get_instrument(isin)
            if session:
                session.close()
            
            if not instrument:
                logger.info(f"Instrument {isin} not found, creating from FITRS data")
                # Create instrument using FITRS data
                instrument = instrument_service.get_or_create_instrument(
                    isin=isin,
                    instrument_type=instrument_type,
                    create_from_fitrs=True
                )
                
                if not instrument:
                    return {
                        'status': '400 Bad Request',
                        'error': f'Failed to create instrument {isin} from FITRS data'
                    }, 400
            
            # 2. Derive calculation_type from instrument_type
            calculation_type = "EQUITY" if instrument_type.lower() == "equity" else "NON_EQUITY"
            logger.info(f"Derived calculation_type={calculation_type} from instrument_type={instrument_type}")
            
            # 3. Use TransparencyService to get transparency data
            service = ServicesFactory.get_transparency_service()
            
            # Get or create transparency calculations
            try:
                created_calculations = service.create_transparency(
                    isin=isin,
                    instrument_type=instrument_type
                )
            except Exception as e:
                if "does not exist in the database" in str(e):
                    return {
                        'status': '404 Not Found',
                        'error': f'ISIN {isin} does not exist in the database'
                    }, 404
                else:
                    return {
                        'status': '500 Internal Server Error',
                        'error': str(e)
                    }, 500
            
            # Ensure we have a list
            if not isinstance(created_calculations, list):
                created_calculations = [created_calculations] if created_calculations else []
            
            # Filter out None values
            created_calculations = [calc for calc in created_calculations if calc is not None]
            
            if not created_calculations:
                return {
                    'status': '404 Not Found',
                    'error': f'No transparency data found for ISIN {isin}'
                }, 404
            
            # 4. Format response with created calculations
            from .transparency_routes import format_unified_transparency
            
            result = []
            for calc in created_calculations:
                formatted_calc = format_unified_transparency(calc)
                if formatted_calc:
                    result.append(formatted_calc)
            
            logger.info(f"Successfully created {len(result)} transparency calculations for ISIN {isin}")
            
            return {
                'status': '201 Created',
                'message': f'Successfully created {len(result)} transparency calculations',
                'data': result,
                'meta': {
                    'isin': isin,
                    'instrument_type': instrument_type,
                    'calculation_type': calculation_type,
                    'total_created': len(result)
                }
            }, 201
            
        except Exception as e:
            logger.error(f"Error in swagger create transparency: {str(e)}")
            logger.exception(e)
            return {'status': '500 Internal Server Error', 'error': str(e)}, 500

@transparency_ns.route('/<string:transparency_id>')
@api.param('transparency_id', 'The transparency calculation identifier')
class TransparencyItem(Resource):
    @api.doc('get_transparency_calculation')
    # Remove the marshal_with decorator that might be causing issues
    @api.response(404, 'Transparency calculation not found', error_model)
    def get(self, transparency_id):
        """Get transparency calculation by ID"""
        # Implement the endpoint directly rather than calling the blueprint function
        from ..interfaces.factory.services_factory import ServicesFactory
        from flask import jsonify
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            service = ServicesFactory.get_transparency_service()
            session, calculation = service.get_transparency_by_id(transparency_id)
            
            if not calculation:
                session.close()
                return {'status': '404 Not Found', 'error': 'Transparency calculation not found'}, 404
            
            # Use the formatting function from transparency_routes
            from .transparency_routes import format_unified_transparency
            result = format_unified_transparency(calculation)
            session.close()
            
            return result
        except Exception as e:
            logger.error(f"Error in swagger get transparency: {str(e)}")
            logger.exception(e)
            return {'status': '500 Internal Server Error', 'error': str(e)}, 500
    
    @api.doc('update_transparency_calculation')
    @api.expect(transparency_create_request)
    @api.response(200, 'Transparency calculation updated')
    @api.response(404, 'Transparency calculation not found', error_model)
    def put(self, transparency_id):
        """Update an existing transparency calculation"""
        from .transparency_routes import update_transparency_calculation
        return update_transparency_calculation(transparency_id)
    
    @api.doc('delete_transparency_calculation')
    @api.response(200, 'Transparency calculation deleted')
    @api.response(404, 'Transparency calculation not found', error_model)
    def delete(self, transparency_id):
        """Delete a transparency calculation"""
        from .transparency_routes import delete_transparency_calculation
        return delete_transparency_calculation(transparency_id)

@transparency_ns.route('/isin/<string:isin>')
@api.param('isin', 'The ISIN to search for')
class TransparencyByIsin(Resource):
    @api.doc('get_transparency_by_isin')
    # Remove the marshal_with decorator that might be causing issues
    @api.param('calculation_type', 'Calculation type to get/create', enum=['EQUITY', 'NON_EQUITY'])
    @api.param('ensure_instrument', 'Ensure instrument exists before creating transparency data', type='boolean', default=True)
    def get(self, isin):
        """Get transparency calculations for a specific ISIN"""
        # Implement directly instead of calling blueprint function
        from flask import request
        from ..database.session import SessionLocal
        from sqlalchemy.orm import joinedload
        from ..interfaces.factory.services_factory import ServicesFactory
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            # Get query parameters
            calculation_type = request.args.get('calculation_type')
            ensure_instrument = request.args.get('ensure_instrument', 'false').lower() == 'true'
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 20, type=int), 100)
            
            # Get models directly instead of using factory
            from ..models.sqlite.transparency import TransparencyCalculation
            
            # Create a new session
            session = SessionLocal()
            try:
                # Build query - unified model no longer needs joinedload for polymorphic relationships
                query = session.query(TransparencyCalculation).filter(
                    TransparencyCalculation.isin == isin
                )
                
                # Apply filter for calculation type
                if calculation_type:
                    query = query.filter(TransparencyCalculation.calculation_type == calculation_type)
                
                # Execute query
                calculations = query.all()
                logger.info(f"Found {len(calculations)} transparency calculations for ISIN {isin}")
                
                # If no results and ensure_instrument is true, try to create
                if not calculations and ensure_instrument:
                    session.close()
                    service = ServicesFactory.get_transparency_service()
                    
                    try:
                        created_calcs = service.create_transparency(
                            isin=isin,
                            instrument_type=calculation_type or 'equity'
                        )
                    except Exception as e:
                        if "does not exist in the database" in str(e):
                            return {
                                'status': '404 Not Found',
                                'error': f'ISIN {isin} does not exist in the database'
                            }, 404
                        else:
                            return {
                                'status': '500 Internal Server Error',
                                'error': str(e)
                            }, 500
                    
                    # Ensure we have a list
                    if not isinstance(created_calcs, list):
                        created_calcs = [created_calcs] if created_calcs else []
                    
                    logger.info(f"Created {len(created_calcs)} new calculations")
                    calculations = created_calcs
                    
                # Format calculations
                from .transparency_routes import format_unified_transparency
                
                result = []
                for calc in calculations:
                    if calc:
                        formatted_calc = format_unified_transparency(calc)
                        if formatted_calc:
                            result.append(formatted_calc)
                
                # If still no results and ensure_instrument is true, return minimal response
                if not result and ensure_instrument:
                    calculation_type = calculation_type or "EQUITY"
                    minimal_response = {
                        "id": None,
                        "isin": isin,
                        "calculation_type": calculation_type,
                        "tech_record_id": None,
                        "from_date": None,
                        "to_date": None,
                        "liquidity": None,
                        "total_transactions_executed": None,
                        "total_volume_executed": None,
                        "created_at": None,
                        "updated_at": None
                    }
                    
                    # Add minimal details based on calculation_type
                    if calculation_type == "EQUITY":
                        minimal_response["details"] = {
                            "financial_instrument_classification": None,
                            "methodology": None,
                            "average_daily_turnover": None,
                            "large_in_scale": None,
                            "average_daily_number_of_transactions": None,
                            "average_transaction_value": None,
                            "standard_market_size": None,
                            "type": "equity"
                        }
                    else:
                        minimal_response["details"] = {
                            "description": None,
                            "criterion_name": None,
                            "criterion_value": None,
                            "pre_trade_large_in_scale_threshold": None,
                            "post_trade_large_in_scale_threshold": None,
                            "type": "non_equity"
                        }
                        
                    result = [minimal_response]
                
                # Return formatted response
                return {
                    'status': '200 OK',
                    'data': result,
                    'meta': {
                        'page': page,
                        'per_page': per_page,
                        'total': len(result)
                    }
                }
            finally:
                if session:
                    session.close()
        except Exception as e:
            logger.error(f"Error in swagger transparency by ISIN: {str(e)}")
            logger.exception(e)
            return {'status': '500 Internal Server Error', 'error': str(e)}, 500

# Add a route to serve the OpenAPI specification
@swagger_bp.route('/openapi.yaml')
def serve_openapi_spec():
    # Get the absolute path to the generated openapi.yaml file
    try:
        openapi_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docs', 'openapi', 'openapi.yaml')
        if os.path.exists(openapi_path):
            return send_file(openapi_path, mimetype='text/yaml')
        else:
            # If generated file doesn't exist, return basic error
            return jsonify({
                "error": "OpenAPI specification not found",
                "message": "Run 'python scripts/generate_docs.py' to generate the OpenAPI specification",
                "expected_path": openapi_path
            }), 404
    except Exception as e:
        return jsonify({"error": f"Failed to serve OpenAPI spec: {str(e)}"}), 500

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
        <redoc spec-url="/docs/openapi"></redoc>
        <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"></script>
      </body>
    </html>
    '''

