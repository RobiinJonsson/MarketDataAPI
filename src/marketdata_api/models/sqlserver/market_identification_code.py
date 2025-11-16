"""SQL Server MIC code models - EXACT copy of SQLite schema."""

import uuid
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from sqlalchemy import Boolean, Column, DateTime, Index, String, Text, CheckConstraint
from sqlalchemy.orm import relationship

from .base_model import SqlServerBaseModel


class SqlServerMICStatus(Enum):
    """MIC status enumeration."""

    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    SUSPENDED = "SUSPENDED"
    UPDATED = "UPDATED"  # Some MICs have UPDATED status


class SqlServerMICType(Enum):
    """MIC operation type enumeration."""

    OPRT = "OPRT"  # Operating MIC
    SGMT = "SGMT"  # Segment MIC


class SqlServerMarketCategoryCode(Enum):
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


class SqlServerMarketIdentificationCode(SqlServerBaseModel):
    """
    SQL Server Market Identification Code (MIC) model - EXACT match to SQLite.
    
    Market Identification Code (MIC) model implementing ISO 10383 standard.
    Provides comprehensive market venue information for integration with
    instrument trading venue relationships via venue_id foreign keys.
    """

    __tablename__ = "market_identification_codes"

    # Primary identification (ISO 10383 standard) - EXACT match to SQLite
    mic = Column(String(4), primary_key=True)  # Market Identification Code
    operating_mic = Column(String(4), nullable=False)  # Parent Operating MIC

    # Core market information
    operation_type = Column(String(4), nullable=False)  # OPRT/SGMT (using String instead of Enum)
    market_name = Column(String(500), nullable=False)  # Market name/institution description
    legal_entity_name = Column(String(500))  # Legal entity operating the market
    lei = Column(String(20))  # Legal Entity Identifier (ISO 17442)

    # Market classification
    market_category_code = Column(String(4))  # Market category (using String instead of Enum)
    acronym = Column(String(50))  # Market acronym/short name

    # Geographic information
    iso_country_code = Column(String(2), nullable=False)  # ISO 3166 country code
    city = Column(String(100))  # Market location city

    # Contact and reference information
    website = Column(String(500))  # Official website URL
    comments = Column(Text)  # Additional comments/notes

    # Status and lifecycle management
    status = Column(String(20), nullable=False, default='ACTIVE')  # Using String instead of Enum
    creation_date = Column(DateTime)  # MIC creation date
    last_update_date = Column(DateTime)  # Last modification date
    last_validation_date = Column(DateTime)  # Last validation date
    expiry_date = Column(DateTime)  # Expiry date (for expired MICs)

    # Record metadata
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))
    data_source_version = Column(String(50))  # Version of ISO data used

    # Relationships (SQL Server version)
    # trading_venues = relationship("SqlServerTradingVenue", back_populates="market_identification_code")

    # Performance indexes - EXACT match to SQLite
    __table_args__ = (
        Index("idx_mic_operating_mic", "operating_mic"),
        Index("idx_mic_country", "iso_country_code"),
        Index("idx_mic_status", "status"),
        Index("idx_mic_category", "market_category_code"),
        Index("idx_mic_lei", "lei"),
        Index("idx_mic_name_search", "market_name"),
        Index("idx_mic_entity_search", "legal_entity_name"),
        # Add constraints for enum-like behavior
        CheckConstraint("operation_type IN ('OPRT', 'SGMT')", name="ck_operation_type"),
        CheckConstraint("status IN ('ACTIVE', 'EXPIRED', 'SUSPENDED', 'UPDATED')", name="ck_status"),
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses. EXACT copy from SQLite."""
        return {
            "mic": self.mic,
            "operating_mic": self.operating_mic,
            "operation_type": self.operation_type,
            "market_name": self.market_name,
            "legal_entity_name": self.legal_entity_name,
            "lei": self.lei,
            "market_category_code": self.market_category_code,
            "acronym": self.acronym,
            "iso_country_code": self.iso_country_code,
            "city": self.city,
            "website": self.website,
            "comments": self.comments,
            "status": self.status,
            "creation_date": self.creation_date.isoformat() if self.creation_date else None,
            "last_update_date": self.last_update_date.isoformat() if self.last_update_date else None,
            "last_validation_date": self.last_validation_date.isoformat() if self.last_validation_date else None,
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "data_source_version": self.data_source_version,
        }