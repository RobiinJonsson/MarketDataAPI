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
    """Unified instrument model with core fields + JSON document storage."""
    __tablename__ = "instruments"
    
    # Core identification (always present)
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    isin = Column(String(12), unique=True, nullable=False)
    instrument_type = Column(String(50), nullable=False)  # equity, debt, future, etc.
    
    # Essential fields (common across all types)
    full_name = Column(String(500))
    short_name = Column(String(200))
    currency = Column(String(3))
    cfi_code = Column(String(6))
    lei_id = Column(String(20), ForeignKey('legal_entities.lei', ondelete='SET NULL'))
    
    # Document storage for type-specific and varying attributes
    firds_data = Column(JSON)  # Original FIRDS record for reference
    processed_attributes = Column(JSON)  # Cleaned/processed attributes
    
    # Record metadata
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))
    
    # Relationships
    legal_entity = relationship("LegalEntity", back_populates="instruments")
    trading_venues = relationship("TradingVenue", back_populates="instrument", cascade="all, delete-orphan")
    figi_mapping = relationship("FigiMapping", back_populates="instrument", uselist=False)
    transparency_calculations = relationship("TransparencyCalculation", back_populates="instrument", cascade="all, delete-orphan")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_instruments_unified_isin', 'isin'),
        Index('idx_instruments_unified_type', 'instrument_type'),
        Index('idx_instruments_unified_lei', 'lei_id'),
        Index('idx_instruments_unified_created', 'created_at'),
    )
    
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
            # Merge processed attributes into response
            response.update(self.processed_attributes)
        
        return response


class TradingVenue(Base):
    """Trading venue records for instruments - stores ALL venue data."""
    __tablename__ = "trading_venues"
    
    # Primary identification
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    instrument_id = Column(String(36), ForeignKey('instruments.id', ondelete='CASCADE'), nullable=False)
    
    # Core venue fields (always present)
    venue_id = Column(String(100), nullable=False)
    isin = Column(String(12), nullable=False)  # Denormalized for easier querying
    
    # Trading dates and status
    first_trade_date = Column(DateTime)
    termination_date = Column(DateTime)
    admission_approval_date = Column(DateTime)
    request_for_admission_date = Column(DateTime)
    
    # Venue-specific instrument data
    venue_full_name = Column(String(500))
    venue_short_name = Column(String(200))
    classification_type = Column(String(100))
    venue_currency = Column(String(3))
    
    # Administrative fields
    issuer_requested = Column(String(100))
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
