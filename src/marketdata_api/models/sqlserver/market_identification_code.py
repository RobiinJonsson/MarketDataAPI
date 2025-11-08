"""SQL Server MIC code models."""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, Text

from .base_model import SqlServerBaseModel


class SqlServerMarketIdentificationCode(SqlServerBaseModel):
    """SQL Server MIC code model."""
    
    __tablename__ = "market_identification_codes"
    
    # Primary identification
    mic = Column(String(4), primary_key=True)
    
    # Basic information
    market_name = Column(String(200), nullable=True)
    market_category_code = Column(String(10), nullable=True)
    acronym = Column(String(50), nullable=True)
    
    # Geographic information
    iso_country_code = Column(String(2), nullable=True)
    city = Column(String(100), nullable=True)
    website = Column(String(200), nullable=True)
    
    # Status information
    status = Column(String(20), nullable=True, default='ACTIVE')
    status_date = Column(DateTime, nullable=True)
    
    # Operational information
    operating_mic = Column(String(4), nullable=True)
    segment_mic = Column(String(4), nullable=True)
    
    # Additional details
    legal_entity_name = Column(String(200), nullable=True)
    legal_entity_identifier = Column(String(20), nullable=True)
    market_type = Column(String(50), nullable=True)
    
    # Comments and notes
    comments = Column(Text, nullable=True)
    
    # Data source tracking
    last_update_date = Column(DateTime, nullable=True, default=datetime.utcnow)
    data_source = Column(String(50), nullable=True, default='ISO_REGISTRY')