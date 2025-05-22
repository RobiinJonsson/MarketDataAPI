import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, UTC

class FigiMapping(Base):
    __tablename__ = "figi_mappings"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    isin = Column(String, ForeignKey('instruments.isin', ondelete='CASCADE'), unique=True, nullable=False)
    figi = Column(String)
    composite_figi = Column(String)
    share_class_figi = Column(String)
    ticker = Column(String)
    security_type = Column(String)
    market_sector = Column(String)
    security_description = Column(String)
    last_updated = Column(DateTime, default=lambda: datetime.now(UTC))
    
    instrument = relationship(
        "Instrument",
        back_populates="figi_mapping",
        passive_deletes=True
    )
