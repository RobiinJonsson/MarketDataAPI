"""SQL Server optimized instrument model using single table design."""

import json
import uuid
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from sqlalchemy import DECIMAL, Boolean, Column, Date, DateTime, Index, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base_model import SqlServerBaseModel
from ...models.interfaces.instrument_interface import InstrumentInterface


class SqlServerInstrument(SqlServerBaseModel, InstrumentInterface):
    """
    SQL Server optimized instrument model using single table design.

    This approach avoids the complex polymorphic inheritance issues that caused
    problems with SQL Server by storing all instrument types in a single table
    with nullable fields for type-specific data.
    """

    __tablename__ = "instruments"

    # Core identification fields
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    isin = Column(String(12), nullable=False, index=True)
    instrument_type = Column(String(50), nullable=False, index=True)
    
    # Essential fields (matching SQLite structure)
    full_name = Column(String(500), nullable=True)
    short_name = Column(String(200), nullable=True)
    currency = Column(String(3), nullable=True)
    cfi_code = Column(String(6), nullable=True)
    commodity_derivative_indicator = Column(Boolean, nullable=True)
    lei_id = Column(String(20), ForeignKey("legal_entities.lei", ondelete="SET NULL"), nullable=True)
    
    # Publication and regulatory fields
    publication_from_date = Column(DateTime, nullable=True)
    competent_authority = Column(String(10), nullable=True)
    relevant_trading_venue = Column(String(100), nullable=True)
    
    # Document storage (SQL Server compatible JSON)
    firds_data = Column(Text, nullable=True)  # JSON as Text for SQL Server
    processed_attributes = Column(Text, nullable=True)  # JSON as Text for SQL Server
    
    # Relationships
    legal_entity = relationship("SqlServerLegalEntity", back_populates="instruments")
    trading_venues = relationship("SqlServerTradingVenue", back_populates="instrument", cascade="all, delete-orphan")

    # Indexes for performance
    __table_args__ = (
        Index('idx_isin_type', 'isin', 'instrument_type'),
        Index('idx_cfi_code', 'cfi_code'),
        Index('idx_currency', 'currency'),
        Index('idx_competent_authority', 'competent_authority'),
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses (matches SQLite interface)."""
        import json
        
        return {
            "id": self.id,
            "isin": self.isin,
            "instrument_type": self.instrument_type,
            "full_name": self.full_name,
            "short_name": self.short_name,
            "currency": self.currency,
            "cfi_code": self.cfi_code,
            "commodity_derivative_indicator": self.commodity_derivative_indicator,
            "lei_id": self.lei_id,
            "publication_from_date": self.publication_from_date.isoformat() if self.publication_from_date else None,
            "competent_authority": self.competent_authority,
            "relevant_trading_venue": self.relevant_trading_venue,
            "firds_data": json.loads(self.firds_data) if self.firds_data else None,
            "processed_attributes": json.loads(self.processed_attributes) if self.processed_attributes else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def to_raw_data(self) -> Dict[str, Any]:
        """Return raw data including relationships (matches SQLite interface)."""
        return {
            **self.to_dict(),
            "legal_entity": self.legal_entity,
            "trading_venues": self.trading_venues,
        }


class SqlServerTradingVenue(SqlServerBaseModel):
    """SQL Server trading venue model."""
    
    __tablename__ = "trading_venues"
    
    # Primary identification
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    instrument_id = Column(String(36), ForeignKey("instruments.id", ondelete="CASCADE"), nullable=False)
    
    # Core venue fields
    venue_id = Column(String(100), nullable=False)
    isin = Column(String(12), nullable=False)  # Denormalized for easier querying
    
    # MIC integration
    mic_code = Column(String(4), ForeignKey("market_identification_codes.mic", ondelete="SET NULL"), nullable=True)
    
    # Trading dates and status
    first_trade_date = Column(DateTime, nullable=True)
    termination_date = Column(DateTime, nullable=True)
    admission_approval_date = Column(DateTime, nullable=True)
    request_for_admission_date = Column(DateTime, nullable=True)
    issuer_requested = Column(Boolean, nullable=True)
    
    # Venue-specific instrument data
    venue_full_name = Column(String(500), nullable=True)
    venue_short_name = Column(String(200), nullable=True)
    classification_type = Column(String(100), nullable=True)
    venue_currency = Column(String(3), nullable=True)
    
    # Administrative fields
    competent_authority = Column(String(100), nullable=True)
    relevant_trading_venue = Column(String(100), nullable=True)
    publication_from_date = Column(DateTime, nullable=True)
    
    # Venue-specific attributes (JSON as Text for SQL Server)
    venue_attributes = Column(Text, nullable=True)
    original_firds_record = Column(Text, nullable=True)  # JSON as Text in SQL Server
    
    # Relationships
    instrument = relationship("SqlServerInstrument", back_populates="trading_venues")
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_trading_venues_instrument_id", "instrument_id"),
        Index("idx_trading_venues_venue_id", "venue_id"),
        Index("idx_trading_venues_isin", "isin"),
        Index("idx_trading_venues_isin_venue", "isin", "venue_id"),
        Index("idx_trading_venues_dates", "first_trade_date", "termination_date"),
        Index("idx_trading_venues_mic_code", "mic_code"),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (matches SQLite interface)."""
        import json
        
        return {
            "id": self.id,
            "venue_id": self.venue_id,
            "isin": self.isin,
            "first_trade_date": self.first_trade_date.isoformat() if self.first_trade_date else None,
            "termination_date": self.termination_date.isoformat() if self.termination_date else None,
            "admission_approval_date": self.admission_approval_date.isoformat() if self.admission_approval_date else None,
            "request_for_admission_date": self.request_for_admission_date.isoformat() if self.request_for_admission_date else None,
            "venue_full_name": self.venue_full_name,
            "venue_short_name": self.venue_short_name,
            "classification_type": self.classification_type,
            "venue_currency": self.venue_currency,
            "issuer_requested": self.issuer_requested,
            "competent_authority": self.competent_authority,
            "relevant_trading_venue": self.relevant_trading_venue,
            "publication_from_date": self.publication_from_date.isoformat() if self.publication_from_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "venue_attributes": json.loads(self.venue_attributes) if self.venue_attributes else None,
        }
