import uuid
from sqlalchemy import Column, String, JSON, DateTime, Float, Date, Enum, ForeignKey, Boolean, Integer, Index
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


class IsinRelationType(enum.Enum):
    PRIMARY = "primary"      # For ISIN_1
    SECONDARY = "secondary"  # For ISIN_2-10 (31-4 occurrences)
    TERTIARY = "tertiary"   # For ISIN_11-38 (3-2 occurrences)
    OTHER = "other"         # For ISIN_39-100 (1 occurrence)


class RelatedIsin(Base):
    __tablename__ = "related_isins"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    primary_instrument_id = Column(String(36), ForeignKey('instruments.id', ondelete='CASCADE'))
    related_isin = Column(String(12), nullable=False)  # ISIN is always 12 characters
    sequence_number = Column(Integer, nullable=False)
    relationship_type = Column(Enum(IsinRelationType), nullable=False)
    
    # Relationship back to the primary instrument
    primary_instrument = relationship("Instrument", back_populates="related_isins")
    
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    # Add indexes for better query performance
    __table_args__ = (
        Index('idx_related_isins_primary_instrument', 'primary_instrument_id'),
        Index('idx_related_isins_isin', 'related_isin'),
        Index('idx_related_isins_type', 'relationship_type'),
    )


class Instrument(BaseModel):
    __tablename__ = "instruments"
    __mapper_args__ = {
        'polymorphic_identity': 'instrument',
        'polymorphic_on': 'type',
        'with_polymorphic': '*'
    }

    # Base identification fields
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String(50), nullable=False)
    isin = Column(String(12), unique=True)  # ISIN is always 12 characters
    full_name = Column(String(255))
    short_name = Column(String(100))
    symbol = Column(String(20))  # Removed unique=True
    figi = Column(String(12))  # FIGI is always 12 characters
    
    # Common FIRDS fields
    cfi_code = Column(String(6))  # CFI codes are 6 characters
    currency = Column(String(3))  # Currency codes are 3 characters
    commodity_derivative = Column(Boolean)
    trading_venue = Column(String(100))
    issuer_req = Column(String(100))
    first_trade_date = Column(DateTime)
    termination_date = Column(DateTime)
    
    # Technical fields
    relevant_authority = Column(String(100))
    relevant_venue = Column(String(100))
    from_date = Column(DateTime)
    technical_from_date = Column(DateTime)  # TechAttrbts_PblctnPrd_FrDt
    
    # Relationships
    lei_id = Column(String(20), ForeignKey('legal_entities.lei', ondelete='CASCADE'))
    legal_entity = relationship(
        "LegalEntity",
        back_populates="instruments",
        passive_deletes=True
    )
    figi_mapping = relationship(
        "FigiMapping",
        back_populates="instrument",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    
    # Additional data for flexibility
    additional_data = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    
    # Add relationship to related ISINs
    related_isins = relationship(
        "RelatedIsin",
        back_populates="primary_instrument",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    
    # Add relationship to transparency calculations
    transparency_calculations = relationship(
        "TransparencyCalculation",
        back_populates="instrument",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class Equity(Instrument):
    __tablename__ = 'equities'
    __mapper_args__ = {
        'polymorphic_identity': 'equity',
        'polymorphic_load': 'inline'
    }

    id = Column(String(36), ForeignKey('instruments.id', ondelete='CASCADE'), primary_key=True)
    
    # FIRDS specific fields
    admission_approval_date = Column(Date)
    admission_request_date = Column(Date)
    price_multiplier = Column(Float)
    
    # Asset class specific attributes
    asset_class = Column(String(50))
    commodity_product = Column(String(100))
    energy_type = Column(String(50))
    oil_type = Column(String(50))
    base_product = Column(String(100))
    sub_product = Column(String(100))
    additional_sub_product = Column(String(100))
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

    # Add missing FULINS_E fields
    basket_isin = Column(String)  # DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN
    basket_lei = Column(String)  # DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI
    underlying_index_isin = Column(String)  # DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN
    underlying_single_isin = Column(String)  # DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN
    underlying_single_index_name = Column(String)  # DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm
    additional_metal_product = Column(String(100))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct

class Debt(Instrument):
    __tablename__ = 'debts'
    __mapper_args__ = {
        'polymorphic_identity': 'debt',
        'polymorphic_load': 'inline'
    }

    id = Column(String(36), ForeignKey('instruments.id', ondelete='CASCADE'), primary_key=True)
    
    # Debt-specific FIRDS fields
    total_issued_nominal = Column(Float)
    maturity_date = Column(Date)
    nominal_value_per_unit = Column(Float)
    fixed_interest_rate = Column(Float)
    debt_seniority = Column(String(50))
    
    # Additional debt fields from your schema
    coupon_frequency = Column(String(20))
    credit_rating = Column(String(10))
    floating_rate_reference = Column(String(100))  # DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm
    floating_rate_term_unit = Column(String(10))  # DebtInstrmAttrbts_IntrstRate_Fltg_Term_Unit
    floating_rate_term_value = Column(Float)  # DebtInstrmAttrbts_IntrstRate_Fltg_Term_Val
    floating_rate_basis_points_spread = Column(Float)  # DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd
    interest_rate_floating_reference_index = Column(String(100))  # DerivInstrmAttrbts_IntrstRate_Fltg_RefRate_Indx
    interest_rate_floating_reference_isin = Column(String(12))  # DerivInstrmAttrbts_IntrstRate_Fltg_RefRate_ISIN

    # Add missing FULINS_D fields
    underlying_single_isin = Column(String(12))  # DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN
    basket_isin = Column(String(12))  # DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN
    underlying_index_isin = Column(String(12))  # DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN
    underlying_single_index_name = Column(String(255))  # DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm
    underlying_single_lei = Column(String(20))  # DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI
    additional_metal_product = Column(String(100))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct
    oil_type = Column(String(50))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct
    sub_product = Column(String(100))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct
    additional_sub_product = Column(String(100))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct
    metal_type = Column(String(50))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct
    precious_metal = Column(String(50))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct
    other_commodity_base_product = Column(String(100))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Othr_BasePdct
    underlying_index_name_term_unit = Column(String(10))  # DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit
    underlying_index_name_term_value = Column(String(50))  # DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val

class Future(Instrument):
    __tablename__ = 'futures'
    __mapper_args__ = {
        'polymorphic_identity': 'future',
        'polymorphic_load': 'inline'
    }

    id = Column(String(36), ForeignKey('instruments.id', ondelete='CASCADE'), primary_key=True)
    
    # Future-specific fields from FIRDS
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
    contract_details = Column(JSON)  # Add proper JSON column type
    final_price_type = Column(String(50))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp
    transaction_type = Column(String(50))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_TxTp
    underlying_index_name = Column(String(255))  # DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm

    # Add missing FULINS_F fields
    underlying_single_isin = Column(String(12))  # DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN
    basket_isin = Column(String(12))  # DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN
    underlying_index_isin = Column(String(12))  # DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN
    underlying_single_index_name = Column(String(255))  # DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm
    underlying_single_lei = Column(String(20))  # DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI
    basket_lei = Column(String(20))  # DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI
    additional_metal_product = Column(String(100))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_AddtlSubPdct
    oil_type = Column(String(50))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct
    sub_product = Column(String(100))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct
    additional_sub_product = Column(String(100))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_AddtlSubPdct
    metal_type = Column(String(50))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct
    precious_metal = Column(String(50))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_SubPdct
    multi_commodity_base_product = Column(String(100))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_MultiCmmdtyExtc_BasePdct
    other_c10_nondeliverable_base_product = Column(String(100))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_BasePdct
    other_c10_nondeliverable_sub_product = Column(String(100))  # DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_OthrC10_NonDlvrbl_SubPdct
    underlying_index_name_term_unit = Column(String(10))  # DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit
    underlying_index_name_term_value = Column(String(50))  # DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val
