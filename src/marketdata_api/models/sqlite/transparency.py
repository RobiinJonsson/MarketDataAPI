"""
Unified Transparency Models for FITRS Data

This module provides a simplified, unified approach to storing transparency data
from all FITRS file types (FULECR_E, FULNCR_C, FULNCR_D, FULNCR_F) using
JSON storage instead of complex polymorphic inheritance.

Based on the successful FIRDS unification pattern.
"""

import uuid
from datetime import UTC, datetime
from typing import Any, Dict

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .base_model import Base


class TransparencyCalculation(Base):
    """
    Unified transparency calculation model for all FITRS data types.

    Stores common fields directly and file-specific data in JSON format.
    This replaces the complex polymorphic inheritance with a simpler approach.
    """

    __tablename__ = "transparency_calculations"

    # Core identification
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tech_record_id = Column(Integer)  # TechRcrdId from FITRS

    # Instrument reference
    isin = Column(String, ForeignKey("instruments.isin", ondelete="CASCADE"), nullable=True)

    # Core transparency fields present across file types
    from_date = Column(Date)  # FrDt
    to_date = Column(Date)  # ToDt
    liquidity = Column(Boolean)  # Lqdty

    # Transaction statistics (present in some file types)
    total_transactions_executed = Column(Integer)  # TtlNbOfTxsExctd
    total_volume_executed = Column(Float)  # TtlVolOfTxsExctd

    # File type and source tracking
    file_type = Column(String, nullable=False)
    """
    FITRS file types based on instrument categories:
    - FULECR_C: ETFs/ETCs (equity files)
    - FULECR_E: Equities/Shares (equity files) 
    - FULECR_R: Rights (equity files)
    - FULNCR_C: Corporate/Certificates (non-equity)
    - FULNCR_D: Debt/Bonds (non-equity)
    - FULNCR_E: ETFs (non-equity category)
    - FULNCR_F: Funds/Derivatives (non-equity)
    - FULNCR_H: Structured Products (non-equity)
    - FULNCR_I: Index-linked (non-equity)
    - FULNCR_J: Warrants (non-equity)
    - FULNCR_O: Options (non-equity)
    """
    source_file = Column(String)  # Original filename for tracking

    # JSON storage for all file-specific data
    raw_data = Column(JSON, nullable=False, default=dict)
    """
    Raw data JSON structure examples:
    
    FULECR_E (Equity):
    {
        "Id": "US8793601050",
        "FinInstrmClssfctn": "SHRS",
        "Mthdlgy": "SINT",
        "AvrgDalyTrnvr": 1234.56,
        "LrgInScale": 567.89,
        "AvrgDalyNbOfTxs": 123.45,
        "Id_2": "secondary_id",
        "AvrgDalyNbOfTxs_2": 67.89,
        "AvrgTxVal": 234.56,
        "StdMktSz": 345.67,
        "Sttstcs": "statistics_data"
    }
    
    FULNCR_C/D/F (Non-Equity):
    {
        "ISIN": "XS2675718998",
        "Desc": "Corporate bond",
        "FinInstrmClssfctn": "BOND",
        "CritNm": "SACL",
        "CritVal": "BOND5",
        "CritNm_2": "ISIN",
        "CritVal_2": "XS2675718998",
        ... (up to CritNm_7/CritVal_7 for futures)
    }
    """

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )

    # Relationships
    instrument = relationship(
        "marketdata_api.models.sqlite.instrument.Instrument",
        back_populates="transparency_calculations",
        passive_deletes=True,
    )

    thresholds = relationship(
        "TransparencyThreshold",
        back_populates="transparency",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # Indexes for efficient querying
    __table_args__ = (
        Index("idx_transparency_isin", "isin"),
        Index("idx_transparency_file_type", "file_type"),
        Index("idx_transparency_dates", "from_date", "to_date"),
        Index("idx_transparency_tech_id", "tech_record_id"),
        {"extend_existing": True},
    )

    def get_field(self, field_name: str, default=None):
        """
        Get a field from raw_data JSON with fallback to direct attribute.
        Handles null/empty values appropriately based on FITRS analysis findings.
        """
        # First check if it's a direct attribute
        attr_name = field_name.lower()
        if hasattr(self, attr_name):
            value = getattr(self, attr_name)
            # Return default if value is None or empty string
            if value is None or value == "":
                return default
            return value

        # Then check raw_data, handling various null representations
        if field_name in self.raw_data:
            value = self.raw_data[field_name]
            # Handle pandas-style null values and empty strings
            if value is None or value == "" or str(value).lower() in ["nan", "null", "none"]:
                return default
            return value

        return default

    def has_valid_data(self, field_name: str) -> bool:
        """Check if a field has valid (non-null, non-empty) data"""
        value = self.get_field(field_name)
        return (
            value is not None and value != "" and str(value).lower() not in ["nan", "null", "none"]
        )

    def get_transaction_data(self) -> Dict[str, Any]:
        """
        Get transaction data with proper null handling.
        Based on FITRS analysis: ~25% fill rate for transaction fields.
        """
        return {
            "total_transactions": (
                self.get_field("TtlNbOfTxsExctd", 0)
                if self.has_valid_data("TtlNbOfTxsExctd")
                else None
            ),
            "total_volume": (
                self.get_field("TtlVolOfTxsExctd", 0.0)
                if self.has_valid_data("TtlVolOfTxsExctd")
                else None
            ),
            "has_transaction_data": self.has_valid_data("TtlNbOfTxsExctd")
            or self.has_valid_data("TtlVolOfTxsExctd"),
        }

    def get_threshold_data(self) -> Dict[str, Any]:
        """
        Get threshold data with proper null handling.
        Based on FITRS analysis: ~31% fill rate for threshold amount fields.
        """
        return {
            "pre_trade_large_scale_amt": (
                self.get_field("PreTradLrgInScaleThrshld_Amt")
                if self.has_valid_data("PreTradLrgInScaleThrshld_Amt")
                else None
            ),
            "post_trade_large_scale_amt": (
                self.get_field("PstTradLrgInScaleThrshld_Amt")
                if self.has_valid_data("PstTradLrgInScaleThrshld_Amt")
                else None
            ),
            "pre_trade_instrument_specific_amt": (
                self.get_field("PreTradInstrmSzSpcfcThrshld_Amt")
                if self.has_valid_data("PreTradInstrmSzSpcfcThrshld_Amt")
                else None
            ),
            "post_trade_instrument_specific_amt": (
                self.get_field("PstTradInstrmSzSpcfcThrshld_Amt")
                if self.has_valid_data("PstTradInstrmSzSpcfcThrshld_Amt")
                else None
            ),
            "has_threshold_data": any(
                [
                    self.has_valid_data("PreTradLrgInScaleThrshld_Amt"),
                    self.has_valid_data("PstTradLrgInScaleThrshld_Amt"),
                    self.has_valid_data("PreTradInstrmSzSpcfcThrshld_Amt"),
                    self.has_valid_data("PstTradInstrmSzSpcfcThrshld_Amt"),
                ]
            ),
        }

    def get_criteria_pairs(self):
        """Extract all criteria name/value pairs from raw_data"""
        criteria = []
        for i in range(1, 8):  # Up to 7 criteria pairs in futures
            suffix = "" if i == 1 else f"_{i}"
            name_key = f"CritNm{suffix}"
            value_key = f"CritVal{suffix}"

            if name_key in self.raw_data and value_key in self.raw_data:
                criteria.append(
                    {"name": self.raw_data[name_key], "value": self.raw_data[value_key]}
                )
        return criteria

    @property
    def is_equity(self):
        """Check if this is equity transparency data (FULECR files)"""
        return self.file_type.startswith("FULECR_")

    @property
    def is_non_equity(self):
        """Check if this is non-equity transparency data (FULNCR files)"""
        return self.file_type.startswith("FULNCR_")

    @property
    def instrument_category(self):
        """Get the specific instrument category (C, D, E, F, H, I, J, O, R)"""
        if "_" in self.file_type:
            return self.file_type.split("_")[1]
        return None

    @property
    def is_debt_instrument(self):
        """Check if this is specifically a debt instrument (FULNCR_D)"""
        return self.file_type == "FULNCR_D"

    @property
    def is_derivatives_or_complex(self):
        """Check if this is derivatives or complex instruments (F, H, I, J, O)"""
        return self.instrument_category in ["F", "H", "I", "J", "O"]

    @property
    def instrument_classification(self):
        """Get financial instrument classification"""
        return self.get_field("FinInstrmClssfctn")

    @property
    def description(self):
        """Get instrument description (non-equity only)"""
        return self.get_field("Desc")


class TransparencyThreshold(Base):
    """
    Threshold data for transparency calculations.

    Normalizes all the various threshold types (pre/post trade, large scale,
    instrument specific, by amount or number) into a single table.
    """

    __tablename__ = "transparency_thresholds"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    transparency_id = Column(
        String, ForeignKey("transparency_calculations.id", ondelete="CASCADE"), nullable=False
    )

    # Threshold classification
    threshold_type = Column(String, nullable=False)
    """
    Threshold types:
    - 'pre_trade_large_scale'
    - 'post_trade_large_scale'  
    - 'pre_trade_instrument_specific'
    - 'post_trade_instrument_specific'
    """

    # Threshold values
    amount_value = Column(Float)  # For amount-based thresholds
    number_value = Column(Float)  # For number-based thresholds (futures)

    # Additional threshold metadata
    raw_data = Column(JSON, default=dict)
    """
    Additional metadata about the threshold, such as:
    - currency
    - calculation method
    - validity period
    - source field name
    """

    # Relationships
    transparency = relationship(
        "TransparencyCalculation", back_populates="thresholds", passive_deletes=True
    )

    # Indexes
    __table_args__ = (
        Index("idx_threshold_transparency_id", "transparency_id"),
        Index("idx_threshold_type", "threshold_type"),
        {"extend_existing": True},
    )

    @classmethod
    def create_from_fitrs_data(cls, transparency_id: str, fitrs_data: dict):
        """
        Create threshold records from FITRS data.

        Extracts all threshold fields and creates appropriate records.
        """
        thresholds = []

        # Amount-based thresholds
        threshold_mappings = {
            "PreTradLrgInScaleThrshld_Amt": ("pre_trade_large_scale", "amount_value"),
            "PstTradLrgInScaleThrshld_Amt": ("post_trade_large_scale", "amount_value"),
            "PreTradInstrmSzSpcfcThrshld_Amt": ("pre_trade_instrument_specific", "amount_value"),
            "PstTradInstrmSzSpcfcThrshld_Amt": ("post_trade_instrument_specific", "amount_value"),
            # Number-based thresholds (futures)
            "PreTradLrgInScaleThrshld_Nb": ("pre_trade_large_scale", "number_value"),
            "PstTradLrgInScaleThrshld_Nb": ("post_trade_large_scale", "number_value"),
            "PreTradInstrmSzSpcfcThrshld_Nb": ("pre_trade_instrument_specific", "number_value"),
            "PstTradInstrmSzSpcfcThrshld_Nb": ("post_trade_instrument_specific", "number_value"),
        }

        for field_name, (threshold_type, value_type) in threshold_mappings.items():
            if field_name in fitrs_data and fitrs_data[field_name] is not None:
                # Get the value and handle NaN for cross-database compatibility
                raw_value = fitrs_data[field_name]
                
                # Skip if value is NaN (ensures consistent behavior across databases)
                import math
                if isinstance(raw_value, (int, float)) and math.isnan(raw_value):
                    continue
                    
                threshold = cls(
                    transparency_id=transparency_id,
                    threshold_type=threshold_type,
                    raw_data={"source_field": field_name},
                )

                if value_type == "amount_value":
                    threshold.amount_value = raw_value
                else:
                    threshold.number_value = raw_value

                thresholds.append(threshold)

        return thresholds
