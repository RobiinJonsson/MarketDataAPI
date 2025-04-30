from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database.db import Base
from datetime import datetime

class FigiMapping(Base):
    __tablename__ = 'isin_figi_map'

    isin = Column(String, ForeignKey('instruments.isin'), primary_key=True)
    figi = Column(String)
    composite_figi = Column('CompositeFIGI', String)
    share_class_figi = Column('ShareClassFIGI', String)
    ticker = Column(String)
    security_type = Column(String)
    market_sector = Column(String)
    security_description = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Relationship with instrument
    instrument = relationship("Instrument", back_populates="figi_data")
