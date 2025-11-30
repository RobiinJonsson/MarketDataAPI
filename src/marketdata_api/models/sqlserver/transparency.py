"""SQL Server transparency calculation models - Exact copy of SQLite schema."""

import uuid
from datetime import UTC, datetime
from typing import Any, Dict

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .base_model import SqlServerBaseModel


class SqlServerTransparencyCalculation(SqlServerBaseModel):
    """
    SQL Server transparency calculation model - EXACT match to SQLite TransparencyCalculation.
    
    Unified transparency calculation model for all FITRS data types.
    Stores common fields directly and file-specific data in JSON format.
    """

    __tablename__ = "transparency_calculations"

    # Core identification (EXACT match to SQLite)
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tech_record_id = Column(Integer)  # TechRcrdId from FITRS

    # Instrument reference
    isin = Column(String(12), ForeignKey("instruments.isin", ondelete="CASCADE"), nullable=True)

    # Core transparency fields present across file types
    from_date = Column(Date)  # FrDt
    to_date = Column(Date)  # ToDt
    liquidity = Column(Boolean)  # Lqdty

    # Transaction statistics (present in some file types)
    total_transactions_executed = Column(Integer)  # TtlNbOfTxsExctd
    total_volume_executed = Column(Float)  # TtlVolOfTxsExctd

    # File type and source tracking
    file_type = Column(String(50), nullable=False)
    source_file = Column(String(255))  # Original filename for tracking

    # JSON storage for all file-specific data (using Text instead of JSON for SQL Server compatibility)
    raw_data = Column(Text, nullable=False, default='{}')  # JSON as Text

    # Timestamps (EXACT match to SQLite)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )

    # Relationships (SQL Server version)
    instrument = relationship("SqlServerInstrument", back_populates="transparency_calculations")
    thresholds = relationship("SqlServerTransparencyThreshold", back_populates="transparency", cascade="all, delete-orphan")

    # Indexes for efficient querying (EXACT match to SQLite)
    __table_args__ = (
        Index("idx_transparency_isin", "isin"),
        Index("idx_transparency_file_type", "file_type"),
        Index("idx_transparency_dates", "from_date", "to_date"),
        Index("idx_transparency_tech_id", "tech_record_id"),
    )

    def get_field(self, field_name: str, default=None):
        """
        Get a field from raw_data JSON with fallback to direct attribute.
        Handles null/empty values appropriately based on FITRS analysis findings.
        EXACT copy from SQLite model.
        """
        import json
        
        # First check if it's a direct attribute
        attr_name = field_name.lower()
        if hasattr(self, attr_name):
            value = getattr(self, attr_name)
            # Return default if value is None or empty string
            if value is None or value == "":
                return default
            return value

        # Then check raw_data, handling various null representations
        try:
            raw_data_dict = json.loads(self.raw_data) if self.raw_data else {}
            if field_name in raw_data_dict:
                value = raw_data_dict[field_name]
                # Handle pandas-style null values and empty strings
                if value is None or value == "" or str(value).lower() in ["nan", "null", "none"]:
                    return default
                return value
        except (json.JSONDecodeError, AttributeError):
            pass

        return default

    def has_valid_data(self, field_name: str) -> bool:
        """Check if a field has valid (non-null, non-empty) data. EXACT copy from SQLite model."""
        value = self.get_field(field_name)
        return (
            value is not None and value != "" and str(value).lower() not in ["nan", "null", "none"]
        )

    def get_transaction_data(self) -> Dict[str, Any]:
        """
        Get transaction data with proper null handling.
        Based on FITRS analysis: ~25% fill rate for transaction fields.
        EXACT copy from SQLite model.
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
        EXACT copy from SQLite model.
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
        }
    
    # Indexes for performance (EXACT match to SQLite)
    __table_args__ = (
        Index("idx_transparency_isin", "isin"),
        Index("idx_transparency_file_type", "file_type"),
        Index("idx_transparency_dates", "from_date", "to_date"),
        Index("idx_transparency_tech_id", "tech_record_id"),
        {'extend_existing': True}
    )


class SqlServerTransparencyThreshold(SqlServerBaseModel):
    """
    SQL Server threshold data for transparency calculations - EXACT match to SQLite TransparencyThreshold.

    Normalizes all the various threshold types (pre/post trade, large scale,
    instrument specific, by amount or number) into a single table.
    """

    __tablename__ = "transparency_thresholds"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    transparency_id = Column(
        String(36), ForeignKey("transparency_calculations.id", ondelete="CASCADE"), nullable=False
    )

    # Threshold classification
    threshold_type = Column(String(100), nullable=False)
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
    raw_data = Column(Text, default='{}')  # JSON stored as text for SQL Server compatibility
    """
    Additional metadata about the threshold, such as:
    - currency
    - calculation method
    - validity period
    - source field name
    """

    # Relationships
    transparency = relationship(
        "SqlServerTransparencyCalculation", back_populates="thresholds", passive_deletes=True
    )

    # Indexes for performance
    __table_args__ = (
        Index("idx_threshold_transparency_id", "transparency_id"),
        Index("idx_threshold_type", "threshold_type"),
        {'extend_existing': True}
    )

    @classmethod
    def create_from_fitrs_data(cls, transparency_id: str, fitrs_data: dict):
        """
        Create threshold records from FITRS data.

        Extracts all threshold fields and creates appropriate records.
        """
        import json
        
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
                # Get the value and handle NaN for SQL Server compatibility
                raw_value = fitrs_data[field_name]
                
                # Skip if value is NaN (SQL Server doesn't support NaN in float columns)
                import math
                if isinstance(raw_value, (int, float)) and math.isnan(raw_value):
                    continue
                    
                threshold = cls(
                    transparency_id=transparency_id,
                    threshold_type=threshold_type,
                    raw_data=json.dumps({"source_field": field_name}),  # JSON as text for SQL Server
                )

                if value_type == "amount_value":
                    threshold.amount_value = raw_value
                else:
                    threshold.number_value = raw_value

                thresholds.append(threshold)

        return thresholds
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary with NaN handling"""
        import math
        
        def clean_value(value):
            """Clean individual values, converting NaN to None"""
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                return None
            elif isinstance(value, dict):
                return {k: clean_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [clean_value(item) for item in value]
            return value
        
        # Get all column values
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            result[column.name] = clean_value(value)
        
        return result