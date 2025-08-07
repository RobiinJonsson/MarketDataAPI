"""SQLite venue model for storing trading venue information."""

import uuid
from typing import Dict, Any, Optional
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from .base_model import Base


class TradingVenue(Base):
    """Model for storing trading venue information for instruments."""
    __tablename__ = "trading_venues"
    
    # Primary identification
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    instrument_id = Column(String(36), ForeignKey('instruments.id', ondelete='CASCADE'), nullable=False)
    
    # Venue-specific fields from FIRDS data
    venue_id = Column(String(100), nullable=False)  # TradgVnRltdAttrbts_Id
    issuer_requested = Column(String(100))  # TradgVnRltdAttrbts_IssrReq
    first_trade_date = Column(DateTime)  # TradgVnRltdAttrbts_FrstTradDt
    admission_approval_date = Column(DateTime)  # TradgVnRltdAttrbts_AdmssnApprvlDtByIssr
    termination_date = Column(DateTime)  # TradgVnRltdAttrbts_TermntnDt
    request_for_admission_date = Column(DateTime)  # TradgVnRltdAttrbts_ReqForAdmssnDt
    
    # Technical attributes
    competent_authority = Column(String(100))  # TechAttrbts_RlvntCmptntAuthrty
    publication_from_date = Column(DateTime)  # TechAttrbts_PblctnPrd_FrDt
    relevant_trading_venue = Column(String(100))  # TechAttrbts_RlvntTradgVn
    
    # Instrument attributes specific to this venue
    full_name = Column(String(500))  # FinInstrmGnlAttrbts_FullNm
    short_name = Column(String(200))  # FinInstrmGnlAttrbts_ShrtNm
    classification_type = Column(String(100))  # FinInstrmGnlAttrbts_ClssfctnTp
    currency = Column(String(3))  # FinInstrmGnlAttrbts_NtnlCcy
    
    # Record metadata
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))
    
    # Relationships
    instrument = relationship("marketdata_api.models.sqlite.instrument.Instrument", back_populates="trading_venues")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_trading_venues_instrument_id', 'instrument_id'),
        Index('idx_trading_venues_venue_id', 'venue_id'),
        Index('idx_trading_venues_instrument_venue', 'instrument_id', 'venue_id'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'venue_id': self.venue_id,
            'issuer_requested': self.issuer_requested,
            'first_trade_date': self.first_trade_date.isoformat() if self.first_trade_date else None,
            'admission_approval_date': self.admission_approval_date.isoformat() if self.admission_approval_date else None,
            'termination_date': self.termination_date.isoformat() if self.termination_date else None,
            'request_for_admission_date': self.request_for_admission_date.isoformat() if self.request_for_admission_date else None,
            'competent_authority': self.competent_authority,
            'publication_from_date': self.publication_from_date.isoformat() if self.publication_from_date else None,
            'relevant_trading_venue': self.relevant_trading_venue,
            'full_name': self.full_name,
            'short_name': self.short_name,
            'classification_type': self.classification_type,
            'currency': self.currency,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
