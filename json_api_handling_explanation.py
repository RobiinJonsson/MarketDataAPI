"""
JSON Handling in APIs - Schema-Based Approach

The proposed design uses JSON for storage flexibility but maintains structured APIs
through well-defined schemas and serialization methods.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


# 1. PYDANTIC SCHEMAS FOR API RESPONSES
# These define the exact structure of API responses, regardless of internal JSON storage

class AssetClassSchema(BaseModel):
    """Schema for asset class attributes."""
    oil_type: Optional[str] = None
    sub_product: Optional[str] = None
    metal_type: Optional[str] = None
    precious_metal: Optional[str] = None
    

class EquityAttributesSchema(BaseModel):
    """Schema for equity-specific attributes."""
    price_multiplier: Optional[float] = None
    underlying_isin: Optional[str] = None
    underlying_index: Optional[str] = None
    asset_class: Optional[AssetClassSchema] = None


class DebtAttributesSchema(BaseModel):
    """Schema for debt-specific attributes."""
    maturity_date: Optional[str] = None
    total_issued_nominal: Optional[float] = None
    nominal_value_per_unit: Optional[float] = None
    debt_seniority: Optional[str] = None
    interest_rate: Optional[Dict[str, Any]] = None


class FutureAttributesSchema(BaseModel):
    """Schema for future-specific attributes."""
    expiration_date: Optional[str] = None
    delivery_type: Optional[str] = None
    price_multiplier: Optional[float] = None
    underlying_assets: Optional[List[str]] = None
    commodity_details: Optional[Dict[str, Any]] = None


class InstrumentResponseSchema(BaseModel):
    """Main instrument API response schema."""
    id: str
    isin: str
    instrument_type: str
    full_name: str
    short_name: Optional[str] = None
    currency: Optional[str] = None
    cfi_code: Optional[str] = None
    lei_id: Optional[str] = None
    created_at: str
    updated_at: str
    
    # Type-specific attributes (dynamically populated based on instrument_type)
    equity_attributes: Optional[EquityAttributesSchema] = None
    debt_attributes: Optional[DebtAttributesSchema] = None
    future_attributes: Optional[FutureAttributesSchema] = None
    
    # Relationships
    figi_mapping: Optional[Dict[str, Any]] = None
    legal_entity: Optional[Dict[str, Any]] = None
    trading_venues_count: Optional[int] = None


class VenueResponseSchema(BaseModel):
    """Trading venue API response schema."""
    id: str
    venue_id: str
    isin: str
    first_trade_date: Optional[str] = None
    termination_date: Optional[str] = None
    admission_approval_date: Optional[str] = None
    request_for_admission_date: Optional[str] = None
    venue_full_name: Optional[str] = None
    venue_short_name: Optional[str] = None
    classification_type: Optional[str] = None
    venue_currency: Optional[str] = None
    issuer_requested: Optional[str] = None
    competent_authority: Optional[str] = None
    relevant_trading_venue: Optional[str] = None
    publication_from_date: Optional[str] = None
    created_at: str
    updated_at: str


# 2. MODEL SERIALIZATION METHODS
# These convert JSON storage to structured API responses

class Instrument(Base):
    """Instrument model with JSON storage but structured API responses."""
    
    def to_api_response(self) -> Dict[str, Any]:
        """Convert to structured API response based on instrument type."""
        
        # Base response structure
        response = {
            'id': self.id,
            'isin': self.isin,
            'instrument_type': self.instrument_type,
            'full_name': self.full_name,
            'short_name': self.short_name,
            'currency': self.currency,
            'cfi_code': self.cfi_code,
            'lei_id': self.lei_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
        # Add type-specific attributes in structured format
        if self.processed_attributes:
            if self.instrument_type == 'equity':
                response['equity_attributes'] = self._format_equity_attributes()
            elif self.instrument_type == 'debt':
                response['debt_attributes'] = self._format_debt_attributes()
            elif self.instrument_type == 'future':
                response['future_attributes'] = self._format_future_attributes()
        
        return response
    
    def _format_equity_attributes(self) -> Dict[str, Any]:
        """Format equity attributes from JSON to structured response."""
        attrs = self.processed_attributes or {}
        
        equity_attrs = {}
        
        if 'price_multiplier' in attrs:
            equity_attrs['price_multiplier'] = attrs['price_multiplier']
        
        if 'underlying_isin' in attrs:
            equity_attrs['underlying_isin'] = attrs['underlying_isin']
        
        if 'asset_class' in attrs:
            equity_attrs['asset_class'] = attrs['asset_class']
        
        return equity_attrs if equity_attrs else None
    
    def _format_debt_attributes(self) -> Dict[str, Any]:
        """Format debt attributes from JSON to structured response."""
        attrs = self.processed_attributes or {}
        
        debt_attrs = {}
        
        if 'maturity_date' in attrs:
            debt_attrs['maturity_date'] = attrs['maturity_date']
        
        if 'total_issued_nominal' in attrs:
            debt_attrs['total_issued_nominal'] = attrs['total_issued_nominal']
        
        if 'interest_rate' in attrs:
            debt_attrs['interest_rate'] = attrs['interest_rate']
        
        return debt_attrs if debt_attrs else None
    
    def _format_future_attributes(self) -> Dict[str, Any]:
        """Format future attributes from JSON to structured response."""
        attrs = self.processed_attributes or {}
        
        future_attrs = {}
        
        if 'expiration_date' in attrs:
            future_attrs['expiration_date'] = attrs['expiration_date']
        
        if 'delivery_type' in attrs:
            future_attrs['delivery_type'] = attrs['delivery_type']
        
        if 'commodity_details' in attrs:
            future_attrs['commodity_details'] = attrs['commodity_details']
        
        return future_attrs if future_attrs else None


# 3. API ENDPOINT IMPLEMENTATION
# Shows how structured responses are returned

from flask import jsonify
from flask_restx import Resource, fields

class InstrumentAPI(Resource):
    """API endpoint returning structured responses."""
    
    def get(self, instrument_id):
        """Get instrument with structured response."""
        
        # Get instrument from database (JSON stored internally)
        instrument = get_instrument_by_id(instrument_id)
        if not instrument:
            return {'error': 'Instrument not found'}, 404
        
        # Convert to structured API response (no raw JSON exposed)
        response = instrument.to_api_response()
        
        # Validate against schema
        try:
            validated_response = InstrumentResponseSchema(**response)
            return validated_response.dict(), 200
        except ValidationError as e:
            logger.error(f"Response validation failed: {e}")
            return {'error': 'Internal server error'}, 500


class VenuesAPI(Resource):
    """API endpoint for venue data."""
    
    def get(self, instrument_id):
        """Get all venues for an instrument."""
        
        # Query database directly (no file I/O)
        venues = get_instrument_venues_from_db(instrument_id)
        if not venues:
            return {'venues': []}, 200
        
        # Convert to structured responses
        venue_responses = []
        for venue in venues:
            response = venue.to_dict()  # Structured method
            validated = VenueResponseSchema(**response)
            venue_responses.append(validated.dict())
        
        return {'venues': venue_responses}, 200


# 4. SWAGGER/OPENAPI SCHEMA GENERATION
# Automatic documentation from Pydantic schemas

from flask_restx import fields

# Flask-RESTX models for Swagger documentation
instrument_response_model = api.model('InstrumentResponse', {
    'id': fields.String(required=True, description='Instrument ID'),
    'isin': fields.String(required=True, description='ISIN identifier'),
    'instrument_type': fields.String(required=True, description='Type of instrument'),
    'full_name': fields.String(description='Full instrument name'),
    'short_name': fields.String(description='Short instrument name'),
    'currency': fields.String(description='Currency code'),
    'cfi_code': fields.String(description='CFI classification code'),
    'lei_id': fields.String(description='Legal Entity Identifier'),
    'equity_attributes': fields.Raw(description='Equity-specific attributes'),
    'debt_attributes': fields.Raw(description='Debt-specific attributes'),
    'future_attributes': fields.Raw(description='Future-specific attributes'),
    'figi_mapping': fields.Raw(description='FIGI mapping data'),
    'legal_entity': fields.Raw(description='Legal entity information'),
    'trading_venues_count': fields.Integer(description='Number of trading venues'),
})

venue_response_model = api.model('VenueResponse', {
    'id': fields.String(required=True, description='Venue record ID'),
    'venue_id': fields.String(required=True, description='Trading venue identifier'),
    'isin': fields.String(required=True, description='ISIN identifier'),
    'first_trade_date': fields.String(description='First trading date'),
    'venue_full_name': fields.String(description='Full instrument name at venue'),
    'venue_currency': fields.String(description='Trading currency at venue'),
    'competent_authority': fields.String(description='Regulatory authority'),
})


"""
KEY POINTS:

1. JSON is used for STORAGE flexibility, not API responses
2. All API responses follow strict Pydantic schemas
3. Internal JSON is converted to structured data via serialization methods
4. No raw JSON or FIRDS data exposed to API consumers
5. Swagger documentation is auto-generated from schemas
6. Type-specific attributes are properly structured per instrument type

BENEFITS:
- Storage flexibility for varying FIRDS structures
- Consistent, typed API responses
- Automatic API documentation
- Schema validation
- Frontend can rely on predictable response structure
"""
