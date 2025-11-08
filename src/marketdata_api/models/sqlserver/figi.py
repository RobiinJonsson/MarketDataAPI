"""SQL Server FIGI mapping models."""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, Index

from .base_model import SqlServerBaseModel


class SqlServerFigiMapping(SqlServerBaseModel):
    """SQL Server FIGI mapping model."""
    
    __tablename__ = "figi_mappings"
    
    # Primary key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # FIGI identification
    figi = Column(String(12), nullable=False, index=True)
    composite_figi = Column(String(12), nullable=True, index=True)
    share_class_figi = Column(String(12), nullable=True, index=True)
    
    # Instrument identification
    isin = Column(String(12), nullable=True, index=True)
    ticker = Column(String(50), nullable=True)
    name = Column(String(500), nullable=True)
    
    # Market information
    exchange_code = Column(String(10), nullable=True)
    mic_code = Column(String(4), nullable=True)
    currency = Column(String(3), nullable=True)
    
    # Security details
    security_type = Column(String(50), nullable=True)
    security_type2 = Column(String(50), nullable=True)
    security_description = Column(String(500), nullable=True)
    
    # Status and metadata
    is_active = Column(Boolean, default=True)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Indexes for common queries
    __table_args__ = (
        Index('idx_figi_isin', 'figi', 'isin'),
        Index('idx_composite_figi_active', 'composite_figi', 'is_active'),
        Index('idx_exchange_ticker', 'exchange_code', 'ticker'),
    )