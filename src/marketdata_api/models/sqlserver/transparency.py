"""SQL Server transparency calculation models."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, DateTime, Boolean, Text, DECIMAL, Index

from .base_model import SqlServerBaseModel


class SqlServerTransparencyCalculation(SqlServerBaseModel):
    """SQL Server transparency calculation model."""
    
    __tablename__ = "transparency_calculations"
    
    # Primary identification
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    isin = Column(String(12), nullable=False, index=True)
    calculation_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Calculation results
    is_transparent = Column(Boolean, nullable=True)
    transparency_percentage = Column(DECIMAL(5, 2), nullable=True)
    
    # Calculation metadata
    calculation_method = Column(String(50), nullable=True)
    data_sources = Column(Text, nullable=True)  # JSON string of sources used
    
    # FITRS file information
    fitrs_file_name = Column(String(200), nullable=True)
    fitrs_file_date = Column(DateTime, nullable=True)
    fitrs_record_count = Column(String(10), nullable=True)  # Keep as String to match SQLite
    
    # Processing status
    status = Column(String(20), nullable=True, default='PENDING')
    error_message = Column(Text, nullable=True)
    processing_duration_ms = Column(String(10), nullable=True)  # Keep as String to match SQLite
    
    # Additional transparency metrics
    liquidity_assessment = Column(Text, nullable=True)  # JSON string
    market_making_assessment = Column(Text, nullable=True)  # JSON string
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_isin_calc_date', 'isin', 'calculation_date'),
        Index('idx_calc_date_status', 'calculation_date', 'status'),
        Index('idx_fitrs_file', 'fitrs_file_name'),
    )