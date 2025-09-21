"""
Market Identification Code (MIC) model based on ISO 20022 standard.

Implements local storage of ISO 10383 MIC codes for performance and reliability.
Integrates with instrument models via venue_id foreign key relationships.
"""

import uuid
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Index, String, Text
from sqlalchemy.orm import relationship

from .base_model import Base


class MICStatus(Enum):
    """MIC status enumeration."""

    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    SUSPENDED = "SUSPENDED"
    UPDATED = "UPDATED"  # Some MICs have UPDATED status


class MICType(Enum):
    """MIC operation type enumeration."""

    OPRT = "OPRT"  # Operating MIC
    SGMT = "SGMT"  # Segment MIC


class MarketCategoryCode(Enum):
    """Market category code enumeration based on ISO 20022."""

    APPA = "APPA"  # Approved Publication Arrangement
    ATSS = "ATSS"  # Alternative Trading System - Systematic
    CASP = "CASP"  # Crypto Asset Service Provider
    DCMS = "DCMS"  # Derivatives Contract Market - Systematic
    IDQS = "IDQS"  # Investment Data Quality System
    MLTF = "MLTF"  # Multilateral Trading Facility
    NSPD = "NSPD"  # Not Specified
    OTFS = "OTFS"  # Organized Trading Facility - Systematic
    OTHR = "OTHR"  # Other
    RMOS = "RMOS"  # Regulated Market - Order System
    RMKT = "RMKT"  # Regulated Market
    SEFS = "SEFS"  # Systematic Electronic Financial System
    SINT = "SINT"  # Systematic Internaliser
    TRFS = "TRFS"  # Trade Reporting Facility System


class MarketIdentificationCode(Base):
    """
    Market Identification Code (MIC) model implementing ISO 10383 standard.

    Provides comprehensive market venue information for integration with
    instrument trading venue relationships via venue_id foreign keys.

    Based on ISO 20022 specification and ESMA MIC registry.
    """

    __tablename__ = "market_identification_codes"

    # Primary identification (ISO 10383 standard)
    mic = Column(String(4), primary_key=True)  # Market Identification Code
    operating_mic = Column(String(4), nullable=False)  # Parent Operating MIC

    # Core market information
    operation_type = Column(SQLEnum(MICType), nullable=False)  # OPRT/SGMT
    market_name = Column(String(500), nullable=False)  # Market name/institution description
    legal_entity_name = Column(String(500))  # Legal entity operating the market
    lei = Column(String(20))  # Legal Entity Identifier (ISO 17442)

    # Market classification
    market_category_code = Column(SQLEnum(MarketCategoryCode))  # Market category
    acronym = Column(String(50))  # Market acronym/short name

    # Geographic information
    iso_country_code = Column(String(2), nullable=False)  # ISO 3166 country code
    city = Column(String(100))  # Market location city

    # Contact and reference information
    website = Column(String(500))  # Official website URL
    comments = Column(Text)  # Additional comments/notes

    # Status and lifecycle management
    status = Column(SQLEnum(MICStatus), nullable=False, default=MICStatus.ACTIVE)
    creation_date = Column(DateTime)  # MIC creation date
    last_update_date = Column(DateTime)  # Last modification date
    last_validation_date = Column(DateTime)  # Last validation date
    expiry_date = Column(DateTime)  # Expiry date (for expired MICs)

    # Record metadata
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))
    data_source_version = Column(String(50))  # Version of ISO data used

    # Relationships
    trading_venues = relationship("TradingVenue", back_populates="market_identification_code")

    # Performance indexes
    __table_args__ = (
        Index("idx_mic_operating_mic", "operating_mic"),
        Index("idx_mic_country", "iso_country_code"),
        Index("idx_mic_status", "status"),
        Index("idx_mic_category", "market_category_code"),
        Index("idx_mic_lei", "lei"),
        Index("idx_mic_name_search", "market_name"),
        Index("idx_mic_entity_search", "legal_entity_name"),
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "mic": self.mic,
            "operating_mic": self.operating_mic,
            "operation_type": self.operation_type.value if self.operation_type else None,
            "market_name": self.market_name,
            "legal_entity_name": self.legal_entity_name,
            "lei": self.lei,
            "market_category_code": (
                self.market_category_code.value if self.market_category_code else None
            ),
            "acronym": self.acronym,
            "iso_country_code": self.iso_country_code,
            "city": self.city,
            "website": self.website,
            "status": self.status.value,
            "creation_date": self.creation_date.isoformat() if self.creation_date else None,
            "last_update_date": (
                self.last_update_date.isoformat() if self.last_update_date else None
            ),
            "last_validation_date": (
                self.last_validation_date.isoformat() if self.last_validation_date else None
            ),
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "comments": self.comments,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def to_summary_dict(self) -> Dict[str, Any]:
        """Convert to summary dictionary for lightweight responses."""
        return {
            "mic": self.mic,
            "market_name": self.market_name,
            "iso_country_code": self.iso_country_code,
            "city": self.city,
            "status": self.status.value,
            "market_category_code": (
                self.market_category_code.value if self.market_category_code else None
            ),
        }

    @property
    def is_active(self) -> bool:
        """Check if MIC is currently active."""
        return self.status == MICStatus.ACTIVE and (
            self.expiry_date is None or self.expiry_date > datetime.now(UTC)
        )

    @property
    def is_operating_mic(self) -> bool:
        """Check if this is an operating MIC (not a segment)."""
        return self.operation_type == MICType.OPRT

    @property
    def is_segment_mic(self) -> bool:
        """Check if this is a segment MIC."""
        return self.operation_type == MICType.SGMT

    @classmethod
    def get_operating_mics(cls, session) -> List["MarketIdentificationCode"]:
        """Get all operating MICs (parent markets)."""
        return (
            session.query(cls)
            .filter(cls.operation_type == MICType.OPRT, cls.status == MICStatus.ACTIVE)
            .all()
        )

    @classmethod
    def get_segments_for_operating_mic(
        cls, session, operating_mic: str
    ) -> List["MarketIdentificationCode"]:
        """Get all segment MICs for a given operating MIC."""
        return (
            session.query(cls)
            .filter(
                cls.operating_mic == operating_mic,
                cls.operation_type == MICType.SGMT,
                cls.status == MICStatus.ACTIVE,
            )
            .all()
        )

    @classmethod
    def search_by_name(cls, session, name_pattern: str) -> List["MarketIdentificationCode"]:
        """Search MICs by market name pattern."""
        pattern = f"%{name_pattern}%"
        return (
            session.query(cls)
            .filter(cls.market_name.ilike(pattern), cls.status == MICStatus.ACTIVE)
            .all()
        )

    @classmethod
    def get_by_country(cls, session, country_code: str) -> List["MarketIdentificationCode"]:
        """Get all MICs for a specific country."""
        return (
            session.query(cls)
            .filter(cls.iso_country_code == country_code.upper(), cls.status == MICStatus.ACTIVE)
            .all()
        )

    def __repr__(self):
        return f"<MIC(mic='{self.mic}', name='{self.market_name}', country='{self.iso_country_code}', status='{self.status.value}')>"
