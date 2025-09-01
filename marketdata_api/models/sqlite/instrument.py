"""
Unified SQLite models with document-based approach.

This replaces the complex polymorphic inheritance with a clean, flexible design.
"""

import uuid
from typing import Dict, Any, Optional
from sqlalchemy import Column, String, JSON, DateTime, Boolean, ForeignKey, Index, Text
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from .base_model import Base


class Instrument(Base):
    """Unified instrument model with core fields + JSON document storage.
    
    Updated to support all FIRDS instrument types (C,D,E,F,H,I,J,S,R,O) with
    common FIRDS columns promoted to dedicated database fields for performance.
    """
    __tablename__ = "instruments"
    
    # Core identification (always present)
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    isin = Column(String(12), unique=True, nullable=False)
    instrument_type = Column(String(50), nullable=False)  # collective_investment, debt, equity, future, etc.
    
    # Essential fields (common across all FIRDS types - promoted from JSON)
    full_name = Column(String(500))  # FinInstrmGnlAttrbts_FullNm
    short_name = Column(String(200))  # FinInstrmGnlAttrbts_ShrtNm
    currency = Column(String(3))  # FinInstrmGnlAttrbts_NtnlCcy
    cfi_code = Column(String(6))  # FinInstrmGnlAttrbts_ClssfctnTp
    commodity_derivative_indicator = Column(Boolean)  # FinInstrmGnlAttrbts_CmmdtyDerivInd
    lei_id = Column(String(20), ForeignKey('legal_entities.lei', ondelete='SET NULL'))  # Issr
    
    # Publication and regulatory fields (common to all FIRDS types)
    publication_from_date = Column(DateTime)  # TechAttrbts_PblctnPrd_FrDt
    competent_authority = Column(String(10))  # TechAttrbts_RlvntCmptntAuthrty
    relevant_trading_venue = Column(String(100))  # TechAttrbts_RlvntTradgVn
    
    # Document storage for type-specific and varying attributes
    firds_data = Column(JSON)  # Original FIRDS record for reference
    processed_attributes = Column(JSON)  # Cleaned/processed attributes
    
    # Record metadata
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))
    
    # Relationships
    legal_entity = relationship("LegalEntity", back_populates="instruments")
    trading_venues = relationship("TradingVenue", back_populates="instrument", cascade="all, delete-orphan")
    figi_mapping = relationship("FigiMapping", back_populates="instrument", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    transparency_calculations = relationship("TransparencyCalculation", back_populates="instrument", cascade="all, delete-orphan")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_instruments_unified_isin', 'isin'),
        Index('idx_instruments_unified_type', 'instrument_type'),
        Index('idx_instruments_unified_lei', 'lei_id'),
        Index('idx_instruments_unified_cfi', 'cfi_code'),
        Index('idx_instruments_unified_currency', 'currency'),
        Index('idx_instruments_unified_competent_auth', 'competent_authority'),
        Index('idx_instruments_unified_created', 'created_at'),
    )
    
    def to_api_response(self) -> Dict[str, Any]:
        """Convert to structured API response based on instrument type."""
        
        # Base response structure with promoted FIRDS fields
        response = {
            'id': self.id,
            'isin': self.isin,
            'instrument_type': self.instrument_type,
            'full_name': self.full_name,
            'short_name': self.short_name,
            'currency': self.currency,
            'cfi_code': self.cfi_code,
            'commodity_derivative_indicator': self.commodity_derivative_indicator,
            'lei_id': self.lei_id,
            'publication_from_date': self.publication_from_date.isoformat() if self.publication_from_date else None,
            'competent_authority': self.competent_authority,
            'relevant_trading_venue': self.relevant_trading_venue,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
        # Add type-specific attributes in structured format
        if self.processed_attributes:
            # Clean and merge processed attributes into response
            cleaned_attributes = self._clean_json_attributes(self.processed_attributes)
            
            # Structure type-specific attributes based on FIRDS instrument type
            if self.instrument_type == 'collective_investment':  # Type C
                civ_attrs = self._format_collective_investment_attributes(cleaned_attributes)
                if civ_attrs:
                    response['collective_investment_attributes'] = civ_attrs
            elif self.instrument_type == 'debt':  # Type D
                debt_attrs = self._format_debt_attributes(cleaned_attributes)
                if debt_attrs:
                    response['debt_attributes'] = debt_attrs
            elif self.instrument_type == 'equity':  # Type E
                equity_attrs = self._format_equity_attributes(cleaned_attributes)
                if equity_attrs:
                    response['equity_attributes'] = equity_attrs
            elif self.instrument_type == 'future':  # Type F
                future_attrs = self._format_future_attributes(cleaned_attributes)
                if future_attrs:
                    response['future_attributes'] = future_attrs
            elif self.instrument_type == 'hybrid':  # Type H
                hybrid_attrs = self._format_hybrid_attributes(cleaned_attributes)
                if hybrid_attrs:
                    response['hybrid_attributes'] = hybrid_attrs
            elif self.instrument_type == 'interest_rate':  # Type I
                ir_attrs = self._format_interest_rate_attributes(cleaned_attributes)
                if ir_attrs:
                    response['interest_rate_attributes'] = ir_attrs
            elif self.instrument_type == 'convertible':  # Type J
                conv_attrs = self._format_convertible_attributes(cleaned_attributes)
                if conv_attrs:
                    response['convertible_attributes'] = conv_attrs
            elif self.instrument_type == 'option':  # Type O
                option_attrs = self._format_option_attributes(cleaned_attributes)
                if option_attrs:
                    response['option_attributes'] = option_attrs
            elif self.instrument_type == 'rights':  # Type R
                rights_attrs = self._format_rights_attributes(cleaned_attributes)
                if rights_attrs:
                    response['rights_attributes'] = rights_attrs
            elif self.instrument_type == 'structured':  # Type S
                struct_attrs = self._format_structured_attributes(cleaned_attributes)
                if struct_attrs:
                    response['structured_attributes'] = struct_attrs
            
            # Also include any remaining unstructured attributes
            remaining_attrs = {k: v for k, v in cleaned_attributes.items() 
                             if not self._is_structured_attribute(k)}
            if remaining_attrs:
                response.update(remaining_attrs)
        
        return response
    
    def _format_equity_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format equity-specific attributes into structured schema."""
        equity_attrs = {}
        
        if 'price_multiplier' in attrs:
            equity_attrs['price_multiplier'] = attrs['price_multiplier']
        
        if 'underlying_isin' in attrs:
            equity_attrs['underlying_isin'] = attrs['underlying_isin']
    def _format_collective_investment_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format collective investment (Type C) specific attributes."""
        civ_attrs = {}
        
        # Common CIV attributes from FIRDS analysis
        if 'underlying_isin' in attrs:
            civ_attrs['underlying_isin'] = attrs['underlying_isin']
        
        if 'fund_type' in attrs:
            civ_attrs['fund_type'] = attrs['fund_type']
            
        if 'investment_strategy' in attrs:
            civ_attrs['investment_strategy'] = attrs['investment_strategy']
        
        return civ_attrs if civ_attrs else None
        
    def _format_hybrid_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format hybrid instrument (Type H) specific attributes."""
        hybrid_attrs = {}
        
        if 'underlying_assets' in attrs:
            hybrid_attrs['underlying_assets'] = attrs['underlying_assets']
            
        if 'conversion_ratio' in attrs:
            hybrid_attrs['conversion_ratio'] = attrs['conversion_ratio']
            
        if 'barrier_level' in attrs:
            hybrid_attrs['barrier_level'] = attrs['barrier_level']
        
        return hybrid_attrs if hybrid_attrs else None
    
    def _format_interest_rate_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format interest rate instrument (Type I) specific attributes."""
        ir_attrs = {}
        
        if 'reference_rate' in attrs:
            ir_attrs['reference_rate'] = attrs['reference_rate']
            
        if 'spread' in attrs:
            ir_attrs['spread'] = attrs['spread']
            
        if 'payment_frequency' in attrs:
            ir_attrs['payment_frequency'] = attrs['payment_frequency']
        
        return ir_attrs if ir_attrs else None
    
    def _format_convertible_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format convertible instrument (Type J) specific attributes."""
        conv_attrs = {}
        
        if 'conversion_price' in attrs:
            conv_attrs['conversion_price'] = attrs['conversion_price']
            
        if 'conversion_ratio' in attrs:
            conv_attrs['conversion_ratio'] = attrs['conversion_ratio']
            
        if 'underlying_isin' in attrs:
            conv_attrs['underlying_isin'] = attrs['underlying_isin']
        
        return conv_attrs if conv_attrs else None
    
    def _format_option_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format option (Type O) specific attributes."""
        option_attrs = {}
        
        if 'option_type' in attrs:
            option_attrs['option_type'] = attrs['option_type']  # Call/Put
            
        if 'strike_price' in attrs:
            option_attrs['strike_price'] = attrs['strike_price']
            
        if 'expiration_date' in attrs:
            option_attrs['expiration_date'] = attrs['expiration_date']
            
        if 'underlying_assets' in attrs:
            option_attrs['underlying_assets'] = attrs['underlying_assets']
        
        return option_attrs if option_attrs else None
    
    def _format_rights_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format rights/warrants (Type R) specific attributes."""
        rights_attrs = {}
        
        if 'exercise_price' in attrs:
            rights_attrs['exercise_price'] = attrs['exercise_price']
            
        if 'exercise_ratio' in attrs:
            rights_attrs['exercise_ratio'] = attrs['exercise_ratio']
            
        if 'expiration_date' in attrs:
            rights_attrs['expiration_date'] = attrs['expiration_date']
            
        if 'underlying_isin' in attrs:
            rights_attrs['underlying_isin'] = attrs['underlying_isin']
        
        return rights_attrs if rights_attrs else None
    
    def _format_structured_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format structured product (Type S) specific attributes."""
        struct_attrs = {}
        
        if 'underlying_assets' in attrs:
            struct_attrs['underlying_assets'] = attrs['underlying_assets']
            
        if 'protection_level' in attrs:
            struct_attrs['protection_level'] = attrs['protection_level']
            
        if 'participation_rate' in attrs:
            struct_attrs['participation_rate'] = attrs['participation_rate']
            
        if 'barrier_level' in attrs:
            struct_attrs['barrier_level'] = attrs['barrier_level']
        
        return struct_attrs if struct_attrs else None
    
    def _format_debt_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format debt-specific attributes into structured schema."""
        debt_attrs = {}
        
        if 'maturity_date' in attrs:
            debt_attrs['maturity_date'] = attrs['maturity_date']
        
        if 'total_issued_nominal' in attrs:
            debt_attrs['total_issued_nominal'] = attrs['total_issued_nominal']
        
        if 'nominal_value_per_unit' in attrs:
            debt_attrs['nominal_value_per_unit'] = attrs['nominal_value_per_unit']
        
        # Map potential debt-specific FIRDS fields
        if 'debt_seniority' in attrs:
            debt_attrs['debt_seniority'] = attrs['debt_seniority']
        
        if 'interest_rate' in attrs:
            debt_attrs['interest_rate'] = attrs['interest_rate']
        
        return debt_attrs if debt_attrs else None
    
    def _format_future_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format future-specific attributes into structured schema."""
        future_attrs = {}
        
        if 'expiration_date' in attrs:
            future_attrs['expiration_date'] = attrs['expiration_date']
        
        if 'delivery_type' in attrs:
            future_attrs['delivery_type'] = attrs['delivery_type']
        
        if 'price_multiplier' in attrs:
            future_attrs['price_multiplier'] = attrs['price_multiplier']
        
        if 'underlying_assets' in attrs:
            future_attrs['underlying_assets'] = attrs['underlying_assets']
        
        if 'commodity_details' in attrs:
            future_attrs['commodity_details'] = attrs['commodity_details']
        
        return future_attrs if future_attrs else None
    
    def _is_structured_attribute(self, key: str) -> bool:
        """Check if an attribute is already handled in structured sections."""
        structured_keys = {
            # Equity attributes
            'price_multiplier', 'underlying_isin', 'underlying_index', 'asset_class',
            # Debt attributes  
            'maturity_date', 'total_issued_nominal', 'nominal_value_per_unit', 
            'debt_seniority', 'interest_rate',
            # Future attributes
            'expiration_date', 'delivery_type', 'underlying_assets', 'commodity_details',
            # Collective Investment attributes
            'fund_type', 'investment_strategy',
            # Hybrid attributes
            'conversion_ratio', 'barrier_level',
            # Interest Rate attributes
            'reference_rate', 'spread', 'payment_frequency',
            # Convertible attributes
            'conversion_price',
            # Option attributes
            'option_type', 'strike_price',
            # Rights attributes
            'exercise_price', 'exercise_ratio',
            # Structured product attributes
            'protection_level', 'participation_rate'
        }
        return key in structured_keys
    
    @classmethod
    def map_firds_type_to_instrument_type(cls, firds_type: str, cfi_code: Optional[str] = None) -> str:
        """Map FIRDS instrument type letter to business instrument type.
        
        Args:
            firds_type: Single letter FIRDS type (C, D, E, F, H, I, J, O, R, S)
            cfi_code: Optional CFI code for additional classification context
            
        Returns:
            String representing the business instrument type
        """
        firds_mapping = {
            'C': 'collective_investment',  # Collective Investment Vehicles
            'D': 'debt',                  # Debt Securities  
            'E': 'equity',                # Equities
            'F': 'future',                # Futures
            'H': 'hybrid',                # Hybrid/Structured instruments
            'I': 'interest_rate',         # Interest Rate derivatives
            'J': 'convertible',           # Convertible instruments
            'O': 'option',                # Options
            'R': 'rights',                # Rights/Warrants
            'S': 'structured',            # Structured Products/Swaps
        }
        
        base_type = firds_mapping.get(firds_type, 'other')
        
        # Refine based on CFI code if available
        if cfi_code and len(cfi_code) >= 1:
            cfi_category = cfi_code[0].upper()
            
            # Override FIRDS mapping with CFI-based classification if they differ
            if cfi_category == 'E' and base_type != 'equity':
                return 'equity'
            elif cfi_category == 'D' and base_type != 'debt':
                return 'debt'
            elif cfi_category == 'C' and base_type != 'collective_investment':
                return 'collective_investment'
            elif cfi_category in ['F', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'S', 'T'] and base_type not in ['future', 'option', 'structured']:
                # These are various derivative types
                if firds_type == 'F':
                    return 'future'
                elif firds_type == 'O':
                    return 'option'
                else:
                    return 'structured'
        
        return base_type
    
    def _clean_json_attributes(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Clean JSON attributes, removing NaN values and empty objects."""
        import math
        
        def clean_value(value):
            if isinstance(value, float) and math.isnan(value):
                return None
            elif isinstance(value, dict):
                cleaned = {k: clean_value(v) for k, v in value.items()}
                # Remove keys with None values or empty dicts
                return {k: v for k, v in cleaned.items() if v is not None and v != {}}
            elif isinstance(value, list):
                return [clean_value(item) for item in value if not (isinstance(item, float) and math.isnan(item))]
            else:
                return value
        
        cleaned = {}
        for key, value in attributes.items():
            cleaned_value = clean_value(value)
            if cleaned_value is not None and cleaned_value != {}:
                cleaned[key] = cleaned_value
        
        return cleaned


class TradingVenue(Base):
    """Trading venue records for instruments - stores ALL venue data."""
    __tablename__ = "trading_venues"
    
    # Primary identification
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    instrument_id = Column(String(36), ForeignKey('instruments.id', ondelete='CASCADE'), nullable=False)
    
    # Core venue fields (always present)
    venue_id = Column(String(100), nullable=False)  # TradgVnRltdAttrbts_Id
    isin = Column(String(12), nullable=False)  # Denormalized for easier querying
    
    # Trading dates and status (common FIRDS fields promoted)
    first_trade_date = Column(DateTime)  # TradgVnRltdAttrbts_FrstTradDt
    termination_date = Column(DateTime)  # TradgVnRltdAttrbts_TermntnDt
    admission_approval_date = Column(DateTime)  # TradgVnRltdAttrbts_AdmssnApprvlDtByIssr
    request_for_admission_date = Column(DateTime)  # TradgVnRltdAttrbts_ReqForAdmssnDt
    issuer_requested = Column(Boolean)  # TradgVnRltdAttrbts_IssrReq
    
    # Venue-specific instrument data
    venue_full_name = Column(String(500))
    venue_short_name = Column(String(200))
    classification_type = Column(String(100))
    venue_currency = Column(String(3))
    
    # Administrative fields
    issuer_requested = Column(Boolean)  # TradgVnRltdAttrbts_IssrReq
    competent_authority = Column(String(100))
    relevant_trading_venue = Column(String(100))
    publication_from_date = Column(DateTime)
    
    # Document storage for venue-specific attributes
    venue_attributes = Column(JSON)  # Any additional venue-specific data
    original_firds_record = Column(JSON)  # Original FIRDS record for this venue
    
    # Record metadata
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))
    
    # Relationships
    instrument = relationship("Instrument", back_populates="trading_venues")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_trading_venues_unified_instrument_id', 'instrument_id'),
        Index('idx_trading_venues_unified_venue_id', 'venue_id'),
        Index('idx_trading_venues_unified_isin', 'isin'),
        Index('idx_trading_venues_unified_isin_venue', 'isin', 'venue_id'),
        Index('idx_trading_venues_unified_dates', 'first_trade_date', 'termination_date'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses - NO raw FIRDS data."""
        return {
            'id': self.id,
            'venue_id': self.venue_id,
            'isin': self.isin,
            'first_trade_date': self.first_trade_date.isoformat() if self.first_trade_date else None,
            'termination_date': self.termination_date.isoformat() if self.termination_date else None,
            'admission_approval_date': self.admission_approval_date.isoformat() if self.admission_approval_date else None,
            'request_for_admission_date': self.request_for_admission_date.isoformat() if self.request_for_admission_date else None,
            'venue_full_name': self.venue_full_name,
            'venue_short_name': self.venue_short_name,
            'classification_type': self.classification_type,
            'venue_currency': self.venue_currency,
            'issuer_requested': self.issuer_requested,
            'competent_authority': self.competent_authority,
            'relevant_trading_venue': self.relevant_trading_venue,
            'publication_from_date': self.publication_from_date.isoformat() if self.publication_from_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            # Include venue-specific attributes if present (but not raw FIRDS)
            **(self.venue_attributes or {})
        }
