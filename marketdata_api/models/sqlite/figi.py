import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import Base
from datetime import datetime, UTC

class FigiMapping(Base):
    __tablename__ = "figi_mappings"
    __table_args__ = {'extend_existing': True}  # Allow table redefinition
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    isin = Column(String(12), ForeignKey('instruments.isin', ondelete='CASCADE'), unique=True, nullable=False)
    figi = Column(String(12))  # FIGI is always 12 characters
    composite_figi = Column(String(12))
    share_class_figi = Column(String(12))
    ticker = Column(String(20))
    security_type = Column(String(50))
    market_sector = Column(String(50))
    security_description = Column(String(255))
    last_updated = Column(DateTime, default=lambda: datetime.now(UTC))
    
    instrument = relationship(
        "marketdata_api.models.sqlite.instrument.Instrument",
        back_populates="figi_mapping",
        passive_deletes=True
    )
