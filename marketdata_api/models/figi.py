from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime

class FigiMapping(Base):
    __tablename__ = 'isin_figi_map'

    isin = Column(String, ForeignKey('instruments.isin'), primary_key=True)
    figi = Column(String)
    composite_figi = Column(String)
    share_class_figi = Column(String)
    ticker = Column(String)
    security_type = Column(String)
    market_sector = Column(String)
    security_description = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)

    instrument = relationship("Instrument", back_populates="figi_mapping")
