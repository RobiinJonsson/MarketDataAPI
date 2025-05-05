import uuid
from sqlalchemy import Column, String, JSON, DateTime, Float, Date, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database.base import Base
import enum
from .base_model import BaseModel
from datetime import datetime, UTC

class InstrumentType(enum.Enum):
    EQUITY = "equity"
    DEBT = "debt"
    DERIVATIVE = "derivative"
    COMMODITY = "commodity"
    CURRENCY = "currency"
    # Add more types as needed


class Instrument(BaseModel):
    __tablename__ = "instruments"
    __mapper_args__ = {
        'polymorphic_identity': 'instrument',
        'polymorphic_on': 'type',
        'with_polymorphic': '*'
    }

    # Base identification fields
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String, nullable=False)
    isin = Column(String, unique=True)
    full_name = Column(String)
    short_name = Column(String)
    symbol = Column(String, unique=True)
    figi = Column(String)
    
    # Common FIRDS fields
    cfi_code = Column(String)
    currency = Column(String)
    commodity_derivative = Column(Boolean)
    trading_venue = Column(String)
    issuer_req = Column(String)
    first_trade_date = Column(DateTime)
    termination_date = Column(DateTime)
    
    # Technical fields
    relevant_authority = Column(String)
    relevant_venue = Column(String)
    from_date = Column(DateTime)
    
    # Relationships
    lei_id = Column(String, ForeignKey('legal_entities.lei'))
    legal_entity = relationship("LegalEntity", back_populates="instruments")
    figi_mapping = relationship("FigiMapping", back_populates="instrument", uselist=False)
    
    # Additional data for flexibility
    additional_data = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


class Equity(Instrument):
    __tablename__ = 'equities'
    __mapper_args__ = {
        'polymorphic_identity': 'equity',
        'polymorphic_load': 'inline'
    }

    id = Column(String, ForeignKey('instruments.id', ondelete='CASCADE'), primary_key=True)
    
    # FIRDS specific fields
    admission_approval_date = Column(Date)
    admission_request_date = Column(Date)
    price_multiplier = Column(Float)
    
    # Asset class specific attributes
    asset_class = Column(String)
    commodity_product = Column(String)
    energy_type = Column(String)
    oil_type = Column(String)
    base_product = Column(String)
    sub_product = Column(String)
    additional_sub_product = Column(String)
    metal_type = Column(String)
    precious_metal = Column(String)
    
    # Keep existing fields
    shares_outstanding = Column(Float)
    market_cap = Column(Float)
    exchange = Column(String)
    sector = Column(String)
    industry = Column(String)
    
    # Underlying instrument references (JSON field to store multiple ISINs)
    underlying_isins = Column(JSON)


class Debt(Instrument):
    __tablename__ = 'debts'
    __mapper_args__ = {
        'polymorphic_identity': 'debt',
        'polymorphic_load': 'inline'
    }

    id = Column(String, ForeignKey('instruments.id', ondelete='CASCADE'), primary_key=True)
    
    # Debt-specific FIRDS fields
    total_issued_nominal = Column(Float)
    maturity_date = Column(Date)
    nominal_value_per_unit = Column(Float)
    fixed_interest_rate = Column(Float)
    debt_seniority = Column(String)
    
    # Additional debt fields from your schema
    coupon_frequency = Column(String)
    credit_rating = Column(String)
