"""
CONTROVERSIAL DESIGN PROPOSAL: Unified Document-Based Data Model

PROBLEMS WITH CURRENT APPROACH:
1. Polymorphic inheritance creates 120+ columns across 5 classes
2. Most columns are NULL for most records (sparse data)
3. Venue data not stored in database - always read from files
4. Complex field mapping with lots of overlaps
5. FIRDS has varying column structures (24-176 columns)

PROPOSED SOLUTION: Document-Based with Structured Relationships

1. SINGLE instruments table with core fields + JSON document
2. SEPARATE trading_venues table for all venue records  
3. SEPARATE instrument_attributes table for type-specific data
4. Clean relationships between tables

BENEFITS:
- Store ALL venue records in database
- Handle variable FIRDS column structures naturally
- Eliminate nullable column explosion
- Much simpler codebase
- Better performance (fewer JOINs)
- Easier to query venue data
- No raw FIRDS data in API responses

TABLE STRUCTURE:
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
    isin = Column(String(12), unique=True, nullable=False, index=True)
    instrument_type = Column(String(50), nullable=False, index=True)  # equity, debt, future, etc.
    
    # Essential fields (common across all types)
    full_name = Column(String(500))
    short_name = Column(String(200))
    currency = Column(String(3))
    cfi_code = Column(String(6))
    lei_id = Column(String(20), ForeignKey('legal_entities.lei', ondelete='SET NULL'))
    
    # Document storage for type-specific and varying attributes
    firds_data = Column(JSON)  # Original FIRDS record
    processed_attributes = Column(JSON)  # Cleaned/processed attributes
    
    # Record metadata
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))
    
    # Relationships
    legal_entity = relationship("LegalEntity", back_populates="instruments")
    trading_venues = relationship("TradingVenue", back_populates="instrument", cascade="all, delete-orphan")
    figi_mapping = relationship("FigiMapping", back_populates="instrument", uselist=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        result = {
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
        
        # Include processed attributes
        if self.processed_attributes:
            result.update(self.processed_attributes)
            
        return result


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
    
    # Record metadata
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))
    
    # Relationships
    instrument = relationship("Instrument", back_populates="trading_venues")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_trading_venues_instrument_id', 'instrument_id'),
        Index('idx_trading_venues_venue_id', 'venue_id'),
        Index('idx_trading_venues_isin', 'isin'),
        Index('idx_trading_venues_isin_venue', 'isin', 'venue_id'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        result = {
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
        }
        
        # Include venue-specific attributes
        if self.venue_attributes:
            result['venue_attributes'] = self.venue_attributes
            
        return result


"""
MIGRATION STRATEGY:

1. Create new tables alongside existing ones
2. Implement new service layer
3. Migrate data from old to new structure
4. Update API endpoints to use new structure
5. Drop old tables once validated

DATA FLOW:
1. create_instrument() stores primary instrument + ALL venue records
2. get_instrument_venues() queries database, not files
3. API responses use clean structured data, no raw FIRDS
4. Enrichment (FIGI/LEI) works the same way

QUERY EXAMPLES:
- All venues for an ISIN: SELECT * FROM trading_venues WHERE isin = ?
- Instruments by venue: SELECT DISTINCT instrument_id FROM trading_venues WHERE venue_id = ?
- Venue count per instrument: SELECT instrument_id, COUNT(*) FROM trading_venues GROUP BY instrument_id

JSON STRUCTURE EXAMPLES:
processed_attributes for equity:
{
  "price_multiplier": 1.0,
  "underlying_index": "S&P 500",
  "basket_isin": ["US...", "GB..."],
  "asset_class": {
    "oil_type": "crude",
    "sub_product": "WTI"
  }
}

venue_attributes:
{
  "local_symbol": "AAPL.XNAS",
  "trading_hours": "09:30-16:00",
  "settlement_period": "T+2"
}
"""
