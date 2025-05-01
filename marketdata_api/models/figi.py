from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from ..database.base import Base

class FigiMapping(Base):
    __tablename__ = 'isin_figi_map'

    isin = Column(String, ForeignKey('instruments.isin', ondelete='CASCADE'), primary_key=True)
    figi = Column(String)
    composite_figi = Column(String)
    share_class_figi = Column(String)
    ticker = Column(String)
    security_type = Column(String)
    market_sector = Column(String)
    security_description = Column(String)
    last_updated = Column(DateTime, default=lambda: datetime.now(UTC))

    # Relationship with instrument
    instrument = relationship(
        "Instrument",
        back_populates="figi_mapping",
        passive_deletes=True,
        single_parent=True
    )
