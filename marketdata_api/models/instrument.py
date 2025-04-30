from sqlalchemy import Column, String, JSON, DateTime, Float, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..database.db import Base
import enum

class InstrumentType(enum.Enum):
    EQUITY = "equity"
    DEBT = "debt"

class Instrument(Base):
    __tablename__ = "instruments"
    __mapper_args__ = {
        'polymorphic_identity': 'instrument',
        'polymorphic_on': 'type'
    }

    id = Column(String, primary_key=True)
    type = Column(String)
    symbol = Column(String, index=True)
    isin = Column(String, index=True)
    name = Column(String)
    additional_data = Column(JSON)
    last_updated = Column(DateTime)
    lei_id = Column(String, ForeignKey('legal_entities.lei'))
    legal_entity = relationship("LegalEntity", back_populates="instruments")

class Equity(Instrument):
    __tablename__ = 'equities'
    __mapper_args__ = {
        'polymorphic_identity': 'equity'
    }

    id = Column(String, ForeignKey('instruments.id'), primary_key=True)
    shares_outstanding = Column(Float)
    market_cap = Column(Float)
    exchange = Column(String)
    sector = Column(String)
    industry = Column(String)

class Debt(Instrument):
    __tablename__ = 'debts'
    __mapper_args__ = {
        'polymorphic_identity': 'debt'
    }

    id = Column(String, ForeignKey('instruments.id'), primary_key=True)
    maturity_date = Column(Date)
    coupon_rate = Column(Float)
    face_value = Column(Float)
    coupon_frequency = Column(String)
    credit_rating = Column(String)
