"""SQLite instrument models preserving polymorphic inheritance."""

import uuid
from typing import Dict, Any, Optional
from sqlalchemy import Column, String, JSON, DateTime, Float, Date, Enum, ForeignKey, Boolean, Integer, Index
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from .base_model import Base
from ...models.interfaces.instrument_interface import InstrumentInterface

# Create the actual instrument models using the imported Base
class Instrument(Base, InstrumentInterface):
    __tablename__ = "instruments"
    __table_args__ = {'extend_existing': True}  # Allow table redefinition
    __mapper_args__ = {
        'polymorphic_identity': 'instrument',
        'polymorphic_on': 'type',
        'with_polymorphic': '*'
    }

    # Base identification fields
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String(50), nullable=False)
    isin = Column(String(12), unique=True)
    full_name = Column(String(255))
    short_name = Column(String(100))
    symbol = Column(String(50))  # Increased from 20
    figi = Column(String(12))
    
    # Common FIRDS fields
    cfi_code = Column(String(6))  # Classification of Financial Instruments  
    currency = Column(String(3))  # Currency code
    commodity_derivative = Column(Boolean)
    trading_venue = Column(String(100))
    issuer_req = Column(String(100))
    first_trade_date = Column(DateTime)
    termination_date = Column(DateTime)
    relevant_authority = Column(String(100))
    relevant_venue = Column(String(100))
    from_date = Column(DateTime)
    lei_id = Column(String(20), ForeignKey('legal_entities.lei', ondelete='SET NULL'))  # Foreign key to legal entities
    additional_data = Column(String)  # JSON data
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))
    technical_from_date = Column(DateTime)
    
    # Relationships - using lambda for forward references
    figi_mapping = relationship("marketdata_api.models.sqlite.figi.FigiMapping", back_populates="instrument", uselist=False)
    legal_entity = relationship("marketdata_api.models.sqlite.legal_entity.LegalEntity", back_populates="instruments", foreign_keys=[lei_id])
    transparency_calculations = relationship(
        "marketdata_api.models.sqlite.transparency.TransparencyCalculation", 
        back_populates="instrument",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # Methods required by InstrumentInterface
    def get_id(self) -> str:
        return self.id
    
    def get_isin(self) -> Optional[str]:
        return self.isin
    
    def get_type(self) -> str:
        return self.type
    
    def get_name(self) -> Optional[str]:
        return self.full_name
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'id': self.id,
            'type': self.type,
            'isin': self.isin,
            'full_name': self.full_name,
            'short_name': self.short_name,
            'symbol': self.symbol,
            'figi': self.figi,
            'cfi': self.cfi,
            'nominal_value': self.nominal_value,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'maturity_date': self.maturity_date.isoformat() if self.maturity_date else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'legal_entity_lei': self.legal_entity_lei
        }

class Equity(Instrument):
    __tablename__ = 'equities'
    __table_args__ = {'extend_existing': True}  # Allow table redefinition
    __mapper_args__ = {
        'polymorphic_identity': 'equity',
        'polymorphic_load': 'inline'
    }

    id = Column(String(36), ForeignKey('instruments.id', ondelete='CASCADE'), primary_key=True)
    
    # Equity-specific fields that match the actual database schema
    admission_approval_date = Column(Date)
    admission_request_date = Column(Date)
    price_multiplier = Column(Float)
    asset_class = Column(String(100))
    commodity_product = Column(String(100))
    energy_type = Column(String(100))
    oil_type = Column(String(100))
    base_product = Column(String(100))
    sub_product = Column(String(100))
    additional_sub_product = Column(String(100))
    metal_type = Column(String(100))
    precious_metal = Column(String(100))
    shares_outstanding = Column(Float)
    market_cap = Column(Float)
    exchange = Column(String(100))
    sector = Column(String(100))
    industry = Column(String(100))
    underlying_isins = Column(String)  # TEXT field
    basket_isin = Column(String(12))
    basket_lei = Column(String(20))
    underlying_index_isin = Column(String(12))
    underlying_single_isin = Column(String(12))
    underlying_single_index_name = Column(String(255))
    additional_metal_product = Column(String(100))

class Debt(Instrument):
    __tablename__ = 'debts'  # Changed from 'bonds' to 'debts'
    __table_args__ = {'extend_existing': True}  # Allow table redefinition
    __mapper_args__ = {
        'polymorphic_identity': 'debt',  # Changed from 'bond' to match data
        'polymorphic_load': 'inline'
    }

    id = Column(String(36), ForeignKey('instruments.id', ondelete='CASCADE'), primary_key=True)
    
    # Debt-specific fields that match the actual database schema
    total_issued_nominal = Column(Float)
    maturity_date = Column(Date)
    nominal_value_per_unit = Column(Float)
    fixed_interest_rate = Column(Float)
    debt_seniority = Column(String(100))
    coupon_frequency = Column(String(100))
    credit_rating = Column(String(10))
    floating_rate_reference = Column(String(100))
    floating_rate_term_unit = Column(String(100))
    floating_rate_term_value = Column(Float)
    floating_rate_basis_points_spread = Column(Float)
    interest_rate_floating_reference_index = Column(String(100))
    interest_rate_floating_reference_isin = Column(String(12))
    underlying_single_isin = Column(String(12))
    basket_isin = Column(String(12))
    underlying_index_isin = Column(String(12))
    underlying_single_index_name = Column(String(255))
    underlying_single_lei = Column(String(20))
    additional_metal_product = Column(String(100))
    oil_type = Column(String(100))
    sub_product = Column(String(100))
    additional_sub_product = Column(String(100))
    metal_type = Column(String(100))
    precious_metal = Column(String(100))
    other_commodity_base_product = Column(String(100))
    underlying_index_name_term_unit = Column(String(100))
    underlying_index_name_term_value = Column(String(100))

class Future(Instrument):
    __tablename__ = 'futures'
    __table_args__ = {'extend_existing': True}  # Allow table redefinition
    __mapper_args__ = {
        'polymorphic_identity': 'future',
        'polymorphic_load': 'inline'
    }

    id = Column(String(36), ForeignKey('instruments.id', ondelete='CASCADE'), primary_key=True)
    
    # Future-specific fields that match the actual database schema
    admission_approval_date = Column(Date)
    admission_request_date = Column(Date)
    expiration_date = Column(Date)
    final_settlement_date = Column(Date)
    delivery_type = Column(String(50))
    settlement_method = Column(String(50))
    contract_size = Column(Float)
    contract_unit = Column(String(20))
    price_multiplier = Column(Float)
    settlement_currency = Column(String(3))
    contract_details = Column(String)  # TEXT field
    final_price_type = Column(String(100))
    transaction_type = Column(String(100))
    underlying_index_name = Column(String(255))
    agricultural_attributes = Column(String)  # JSON field
    natural_gas_attributes = Column(String)  # JSON field
    electricity_attributes = Column(String)  # JSON field
    renewable_energy_attributes = Column(String)  # JSON field
    paper_attributes = Column(String)  # JSON field
    environmental_attributes = Column(String)  # JSON field
    freight_attributes = Column(String)  # JSON field
    fx_type = Column(String(100))
    other_notional_currency = Column(String(3))
    interest_rate_reference = Column(String(100))
    interest_rate_term_unit = Column(String(100))
    interest_rate_term_value = Column(Float)
    index_reference_rate = Column(String(100))
    underlying_single_isin = Column(String(12))
    basket_isin = Column(String(12))
    underlying_index_isin = Column(String(12))
    underlying_single_index_name = Column(String(255))
    underlying_single_lei = Column(String(20))
    basket_lei = Column(String(20))
    additional_metal_product = Column(String(100))
    oil_type = Column(String(100))
    sub_product = Column(String(100))
    additional_sub_product = Column(String(100))
    metal_type = Column(String(100))
    precious_metal = Column(String(100))
    multi_commodity_base_product = Column(String(100))
    other_c10_nondeliverable_base_product = Column(String(100))
    other_c10_nondeliverable_sub_product = Column(String(100))
    underlying_index_name_term_unit = Column(String(100))
    underlying_index_name_term_value = Column(String(100))
