import uuid
from sqlalchemy import Column, String, JSON, DateTime, Float, Date, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database.base import Base
import enum

class InstrumentType(enum.Enum):
    EQUITY = "equity"
    DEBT = "debt"
    DERIVATIVE = "derivative"
    COMMODITY = "commodity"
    CURRENCY = "currency"
    # Add more types as needed


class Instrument(Base):
    __tablename__ = "instruments"
    __mapper_args__ = {
        'polymorphic_identity': 'instrument',
        'polymorphic_on': 'type'
    }

    # Base identification fields
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String)
    isin = Column(String, index=True)  # FinInstrmGnlAttrbts_Id
    full_name = Column(String)         # FinInstrmGnlAttrbts_FullNm
    short_name = Column(String)        # FinInstrmGnlAttrbts_ShrtNm
    symbol = Column(String, index=True)
    figi = Column(String, index=True)  # Figi code
    
    # Common FIRDS fields
    cfi_code = Column(String)          # FinInstrmGnlAttrbts_ClssfctnTp
    currency = Column(String)          # FinInstrmGnlAttrbts_NtnlCcy
    commodity_derivative = Column(Boolean)  # FinInstrmGnlAttrbts_CmmdtyDerivInd
    trading_venue = Column(String)     # TradgVnRltdAttrbts_Id
    issuer_req = Column(Boolean)       # TradgVnRltdAttrbts_IssrReq
    first_trade_date = Column(Date)    # TradgVnRltdAttrbts_FrstTradDt
    termination_date = Column(Date)    # TradgVnRltdAttrbts_TermntnDt
    
    # Technical fields
    relevant_authority = Column(String)  # TechAttrbts_RlvntCmptntAuthrty
    relevant_venue = Column(String)      # TechAttrbts_RlvntTradgVn
    from_date = Column(Date)            # PblctnPrd_FrDt
    
    # Relationships
    lei_id = Column(String, ForeignKey('legal_entities.lei'))  # Issr
    legal_entity = relationship("LegalEntity", back_populates="instruments")
    
    # Fix duplicate FIGI relationship - remove duplicate
    figi_mapping = relationship("FigiMapping", uselist=False, back_populates="instrument")
    
    # Additional data for flexibility
    additional_data = Column(JSON)
    last_updated = Column(DateTime)

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
    
    # Debt-specific FIRDS fields
    total_issued_nominal = Column(Float)    # DebtInstrmAttrbts_TtlIssdNmnlAmt
    maturity_date = Column(Date)            # DebtInstrmAttrbts_MtrtyDt
    nominal_value_per_unit = Column(Float)  # DebtInstrmAttrbts_NmnlValPerUnit
    fixed_interest_rate = Column(Float)     # DebtInstrmAttrbts_IntrstRate_Fxd
    debt_seniority = Column(String)         # DebtInstrmAttrbts_DebtSnrty
    
    # Additional debt fields from your schema
    coupon_frequency = Column(String)
    credit_rating = Column(String)
