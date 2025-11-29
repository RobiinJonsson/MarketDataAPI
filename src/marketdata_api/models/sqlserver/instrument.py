"""SQL Server optimized instrument model using single table design."""

import json
import uuid
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from sqlalchemy import DECIMAL, Boolean, Column, Date, DateTime, Index, Integer, String, Text, ForeignKey
from sqlalchemy.dialects.mssql import NVARCHAR
from sqlalchemy.types import TypeDecorator, NVARCHAR as NVARCHAR_BASE
from sqlalchemy.orm import relationship

from .base_model import SqlServerBaseModel
from ...models.interfaces.instrument_interface import InstrumentInterface


class LegacyCompatibleText(TypeDecorator):
    """Custom text type for legacy SQL Server ODBC driver compatibility."""
    
    impl = Text
    cache_ok = True
    
    def load_dialect_impl(self, dialect):
        # For SQL Server, use Text instead of NVARCHAR to avoid precision issues
        return dialect.type_descriptor(Text())


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
    lei_id = Column(String(20), nullable=True)  # Removed FK constraint - lei_id can exist without legal entity
    
    # Publication and regulatory fields
    publication_from_date = Column(DateTime, nullable=True)
    competent_authority = Column(String(10), nullable=True)
    relevant_trading_venue = Column(String(100), nullable=True)
    
    # Document storage (SQL Server compatible JSON) 
    # Using custom type for legacy ODBC driver compatibility
    _firds_data = Column('firds_data', LegacyCompatibleText, nullable=True)  
    _processed_attributes = Column('processed_attributes', LegacyCompatibleText, nullable=True)
    
    @property
    def firds_data(self):
        """Get firds_data as dict (deserialize from JSON)."""
        import json
        return json.loads(self._firds_data) if self._firds_data else None
    
    @firds_data.setter
    def firds_data(self, value):
        """Set firds_data from dict (serialize to JSON)."""
        import json
        self._firds_data = json.dumps(value) if value is not None else None
    
    @property
    def processed_attributes(self):
        """Get processed_attributes as dict (deserialize from JSON)."""
        import json
        return json.loads(self._processed_attributes) if self._processed_attributes else None
    
    @processed_attributes.setter
    def processed_attributes(self, value):
        """Set processed_attributes from dict (serialize to JSON)."""
        import json
        self._processed_attributes = json.dumps(value) if value is not None else None
    
    # Relationships
    legal_entity = relationship(
        "SqlServerLegalEntity", 
        back_populates="instruments",
        primaryjoin="SqlServerInstrument.lei_id == SqlServerLegalEntity.lei",
        foreign_keys="SqlServerInstrument.lei_id"
    )
    trading_venues = relationship("SqlServerTradingVenue", back_populates="instrument", cascade="all, delete-orphan")
    figi_mappings = relationship(
        "SqlServerFigiMapping", 
        back_populates="instrument", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    transparency_calculations = relationship(
        "SqlServerTransparencyCalculation", 
        back_populates="instrument", 
        cascade="all, delete-orphan"
    )

    # Indexes for performance
    __table_args__ = (
        Index('idx_isin_type', 'isin', 'instrument_type'),
        Index('idx_cfi_code', 'cfi_code'),
        Index('idx_currency', 'currency'),
        Index('idx_competent_authority', 'competent_authority'),
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses (matches SQLite interface)."""
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
            "firds_data": self.firds_data,  # Property already deserializes
            "processed_attributes": self.processed_attributes,  # Property already deserializes
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

    @classmethod
    def map_firds_type_to_instrument_type(
        cls, firds_type: str, cfi_code: Optional[str] = None
    ) -> str:
        """Map FIRDS instrument type letter to business instrument type using CFI standards.

        This method now uses the CFI model as the single source of truth.
        FIRDS file letters directly map to CFI categories following ISO 10962.

        Args:
            firds_type: Single letter FIRDS type (C, D, E, F, H, I, J, O, R, S)
            cfi_code: Optional CFI code for validation and refinement

        Returns:
            String representing the business instrument type
        """
        from marketdata_api.models.utils.cfi_instrument_manager import CFIInstrumentTypeManager

        # Use CFI code if available (primary source of truth)
        if cfi_code:
            # Validate consistency between FIRDS type and CFI code
            is_consistent, error_msg = CFIInstrumentTypeManager.validate_cfi_consistency(
                cfi_code, firds_type
            )
            if not is_consistent:
                # Log warning but continue - data might have inconsistencies
                import logging

                logger = logging.getLogger(__name__)
                logger.warning(f"CFI-FIRDS inconsistency for {firds_type}/{cfi_code}: {error_msg}")

            # Use CFI-based type determination
            return CFIInstrumentTypeManager.get_business_type_from_cfi(cfi_code)

        # Fallback to FIRDS-based determination (still CFI-compliant)
        return CFIInstrumentTypeManager.get_business_type_from_firds_file(firds_type)


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
    
    # JSON property setters/getters for compatibility with SQLite
    @property 
    def venue_attributes_json(self):
        """Get venue_attributes as parsed JSON object."""
        import json
        return json.loads(self.venue_attributes) if self.venue_attributes else None
    
    @venue_attributes_json.setter
    def venue_attributes_json(self, value):
        """Set venue_attributes from JSON object."""
        import json
        self.venue_attributes = json.dumps(value) if value is not None else None
    
    @property
    def original_firds_record_json(self):
        """Get original_firds_record as parsed JSON object."""
        import json
        return json.loads(self.original_firds_record) if self.original_firds_record else None
        
    @original_firds_record_json.setter
    def original_firds_record_json(self, value):
        """Set original_firds_record from JSON object."""
        import json
        self.original_firds_record = json.dumps(value) if value is not None else None
    
    def __setattr__(self, name, value):
        """Override setattr to handle automatic JSON conversion for compatibility with SQLite."""
        if name in ('venue_attributes', 'original_firds_record') and isinstance(value, dict):
            import json
            value = json.dumps(value)
        super().__setattr__(name, value)
    
    # Relationships
    instrument = relationship("SqlServerInstrument", back_populates="trading_venues")
    market_identification_code = relationship("SqlServerMarketIdentificationCode", back_populates="trading_venues")
    
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
