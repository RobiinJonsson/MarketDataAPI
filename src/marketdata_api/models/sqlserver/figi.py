"""SQL Server FIGI mapping models - EXACT copy of SQLite schema."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from .base_model import SqlServerBaseModel


class SqlServerFigiMapping(SqlServerBaseModel):
    """SQL Server FIGI mapping model - EXACT match to SQLite FigiMapping."""
    
    __tablename__ = "figi_mappings"
    __table_args__ = {}  # Allow table redefinition, like SQLite

    # EXACT column match to SQLite
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    isin = Column(
        String(12), ForeignKey("instruments.isin", ondelete="CASCADE"), nullable=False
    )  # Removed unique=True to allow multiple FIGIs per ISIN
    figi = Column(
        String(12), unique=True
    )  # FIGI is always 12 characters and must be unique across all instruments
    composite_figi = Column(String(12))
    share_class_figi = Column(String(12))
    ticker = Column(String(100))  # Increased size to handle longer ticker symbols
    security_type = Column(String(50))
    market_sector = Column(String(50))
    security_description = Column(String(255))
    last_updated = Column(DateTime, default=lambda: datetime.now(UTC))

    # Relationships (SQL Server version)
    instrument = relationship("SqlServerInstrument", back_populates="figi_mappings")