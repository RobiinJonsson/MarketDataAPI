import uuid
from sqlalchemy import Column, String, DateTime, Float, Date, ForeignKey, Boolean, Integer, Index
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, UTC

class TransparencyCalculation(Base):
    """Base class for transparency calculations from FITRS data"""
    __tablename__ = "transparency_calculations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tech_record_id = Column(Integer)  # TechRcrdId
    isin = Column(String, ForeignKey('instruments.isin', ondelete='CASCADE'), nullable=False)
    calculation_type = Column(String, nullable=False)  # 'EQUITY' or 'NON_EQUITY'
    
    # Common fields across both types
    from_date = Column(Date)  # FrDt
    to_date = Column(Date)  # ToDt
    liquidity = Column(Boolean)  # Lqdty
    total_transactions_executed = Column(Integer)  # TtlNbOfTxsExctd
    total_volume_executed = Column(Float)  # TtlVolOfTxsExctd
    statistics = Column(String)  # Sttstcs (only in equity)
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    
    # Relationship to instrument
    instrument = relationship(
        "Instrument",
        back_populates="transparency_calculations",
        passive_deletes=True
    )
    
    # Relationship to equity transparency - no conflicts here
    equity_transparency = relationship(
        "EquityTransparency", 
        back_populates="parent_calculation",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    
    # Relationships that need overlaps
    non_equity_transparency = relationship(
        "NonEquityTransparency", 
        back_populates="parent_calculation",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        overlaps="debt_transparency,futures_transparency"
    )
    
    debt_transparency = relationship(
        "DebtTransparency", 
        back_populates="parent_calculation",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        overlaps="non_equity_transparency"
    )
    
    futures_transparency = relationship(
        "FuturesTransparency", 
        back_populates="parent_calculation",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        overlaps="non_equity_transparency"
    )
    
    __table_args__ = (
        Index('idx_transparency_isin', 'isin'),
        Index('idx_transparency_type', 'calculation_type'),
        Index('idx_transparency_dates', 'from_date', 'to_date'),
    )

class EquityTransparency(Base):
    """Equity instrument transparency data from FULECR files"""
    __tablename__ = "equity_transparency"
    
    id = Column(String, ForeignKey('transparency_calculations.id', ondelete='CASCADE'), primary_key=True)
    
    # Equity-specific fields from FULECR
    financial_instrument_classification = Column(String)  # FinInstrmClssfctn
    methodology = Column(String)  # Mthdlgy
    average_daily_turnover = Column(Float)  # AvrgDalyTrnvr
    large_in_scale = Column(Float)  # LrgInScale
    average_daily_number_of_transactions = Column(Float)  # AvrgDalyNbOfTxs
    
    # Secondary identifier and transactions (Id_2, AvrgDalyNbOfTxs_2)
    secondary_id = Column(String)  # Id_2
    average_daily_transactions_secondary = Column(Float)  # AvrgDalyNbOfTxs_2
    
    # Additional equity metrics
    average_transaction_value = Column(Float)  # AvrgTxVal
    standard_market_size = Column(Float)  # StdMktSz
    
    # Reference back to parent calculation
    parent_calculation = relationship(
        "TransparencyCalculation",
        back_populates="equity_transparency",
        passive_deletes=True
    )

class NonEquityTransparency(Base):
    """Non-equity instrument transparency data from FULNCR files"""
    __tablename__ = "non_equity_transparency"
    
    id = Column(String, ForeignKey('transparency_calculations.id', ondelete='CASCADE'), primary_key=True)
    
    # Non-equity specific fields from FULNCR
    description = Column(String)  # Desc - e.g., "Corporate bond", "Securitised derivatives"
    criterion_name = Column(String)  # CritNm - e.g., "SACL"
    criterion_value = Column(String)  # CritVal - e.g., "BOND5", "SDRV"
    financial_instrument_classification = Column(String)  # FinInstrmClssfctn - e.g., "BOND", "SDRV"
    
    # Threshold amounts for pre and post trade
    pre_trade_large_in_scale_threshold = Column(Float)  # PreTradLrgInScaleThrshld_Amt
    post_trade_large_in_scale_threshold = Column(Float)  # PstTradLrgInScaleThrshld_Amt
    pre_trade_instrument_size_specific_threshold = Column(Float)  # PreTradInstrmSzSpcfcThrshld_Amt
    post_trade_instrument_size_specific_threshold = Column(Float)  # PstTradInstrmSzSpcfcThrshld_Amt
    
    # Secondary criterion (CritNm_2, CritVal_2)
    criterion_name_secondary = Column(String)  # CritNm_2
    criterion_value_secondary = Column(String)  # CritVal_2
    
    # Reference back to parent calculation
    parent_calculation = relationship(
        "TransparencyCalculation",
        back_populates="non_equity_transparency",
        passive_deletes=True,
        overlaps="debt_transparency,futures_transparency"
    )
    
    # Add discriminator column for inheritance
    type = Column(String)
    
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'non_equity'
    }

class DebtTransparency(NonEquityTransparency):
    """Debt-specific transparency data - extends NonEquityTransparency for debt instruments"""
    __tablename__ = "debt_transparency"
    
    id = Column(String, ForeignKey('non_equity_transparency.id', ondelete='CASCADE'), primary_key=True)
    
    # Debt-specific fields based on the terminal output
    bond_type = Column(String)  # Derived from criterion_value - "BOND5", "SDRV", etc.
    security_type = Column(String)  # Derived from description - "Corporate bond", "Securitised derivatives"
    
    # Additional debt characteristics that might be present
    is_securitised_derivative = Column(Boolean, default=False)  # True if CritVal = "SDRV"
    is_corporate_bond = Column(Boolean, default=False)  # True if Desc = "Corporate bond"
    
    # Liquidity flag (from Lqdty field)
    is_liquid = Column(Boolean)  # Lqdty field from FITRS data
    
    # Reference back to parent calculation
    parent_calculation = relationship(
        "TransparencyCalculation",
        back_populates="debt_transparency",
        passive_deletes=True,
        overlaps="non_equity_transparency"
    )
    
    __mapper_args__ = {
        'polymorphic_identity': 'debt',
        'inherit_condition': id == NonEquityTransparency.id
    }
    
    def __post_init__(self):
        """Set derived fields based on criterion values and descriptions"""
        if self.criterion_value == "SDRV":
            self.is_securitised_derivative = True
            self.bond_type = "Securitised Derivative"
        elif self.criterion_value and "BOND" in self.criterion_value:
            self.is_corporate_bond = True
            self.bond_type = "Corporate Bond"
            
        if self.description:
            self.security_type = self.description

class FuturesTransparency(NonEquityTransparency):
    """Futures-specific transparency data - extends NonEquityTransparency for futures instruments"""
    __tablename__ = "futures_transparency"
    
    id = Column(String, ForeignKey('non_equity_transparency.id', ondelete='CASCADE'), primary_key=True)
    
    # Additional futures-specific fields from terminal output
    # These are additional criterion pairs beyond the base CritNm/CritVal
    criterion_name_3 = Column(String)  # CritNm_3
    criterion_value_3 = Column(String)  # CritVal_3
    criterion_name_4 = Column(String)  # CritNm_4  
    criterion_value_4 = Column(String)  # CritVal_4
    criterion_name_5 = Column(String)  # CritNm_5
    criterion_value_5 = Column(String)  # CritVal_5
    criterion_name_6 = Column(String)  # CritNm_6
    criterion_value_6 = Column(String)  # CritVal_6
    criterion_name_7 = Column(String)  # CritNm_7
    criterion_value_7 = Column(String)  # CritVal_7
    
    # Futures have number-based thresholds in addition to amount-based
    pre_trade_large_in_scale_threshold_nb = Column(Float)  # PreTradLrgInScaleThrshld_Nb
    post_trade_large_in_scale_threshold_nb = Column(Float)  # PstTradLrgInScaleThrshld_Nb
    pre_trade_instrument_size_specific_threshold_nb = Column(Float)  # PreTradInstrmSzSpcfcThrshld_Nb
    post_trade_instrument_size_specific_threshold_nb = Column(Float)  # PstTradInstrmSzSpcfcThrshld_Nb
    
    # Futures classification fields
    is_stock_dividend_future = Column(Boolean, default=False)  # Based on "Stock dividend futures/forwards"
    underlying_isin = Column(String)  # Extracted from CritVal_2 if CritNm_2 = "UINS"
    
    # Reference back to parent calculation
    parent_calculation = relationship(
        "TransparencyCalculation",
        back_populates="futures_transparency",
        passive_deletes=True,
        overlaps="non_equity_transparency"
    )
    
    __mapper_args__ = {
        'polymorphic_identity': 'futures',
        'inherit_condition': id == NonEquityTransparency.id
    }
    
    def __post_init__(self):
        """Set derived fields based on criterion values and descriptions"""
        # Classify based on description
        if self.description and "Stock dividend" in self.description:
            self.is_stock_dividend_future = True
        
        # Extract underlying ISIN if available
        if self.criterion_name_secondary == "UINS":
            self.underlying_isin = self.criterion_value_secondary
