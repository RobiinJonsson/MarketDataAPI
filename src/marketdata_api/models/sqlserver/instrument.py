"""SQL Server optimized instrument model using single table design."""

import json
import uuid
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from sqlalchemy import DECIMAL, Boolean, Column, Date, DateTime, Index, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

from ...database.base import Base  # Use shared Base
from ...models.interfaces.instrument_interface import InstrumentInterface

# Use shared Base instead of creating new one
SqlServerBase = Base


class SqlServerInstrument(SqlServerBase, InstrumentInterface):
    """
    SQL Server optimized instrument model using single table design.

    This approach avoids the complex polymorphic inheritance issues that caused
    problems with SQL Server by storing all instrument types in a single table
    with nullable fields for type-specific data.
    """

    __tablename__ = "instruments"

    # Core identification fields
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    instrument_type = Column(String(50), nullable=False, index=True)
    isin = Column(
        String(12), nullable=True, index=True
    )  # Removed unique constraint per migration plan
    full_name = Column(String(500), nullable=True)  # Increased to 500 per plan
    short_name = Column(String(255), nullable=True)
    symbol = Column(String(50), nullable=True)  # Increased from 20 to 50+ per migration plan
    figi = Column(String(12), nullable=True)

    # Common FIRDS fields
    cfi_code = Column(String(6), nullable=True)
    currency = Column(String(3), nullable=True)
    commodity_derivative = Column(Boolean, nullable=True)
    trading_venue = Column(String(255), nullable=True)
    issuer_req = Column(String(255), nullable=True)
    first_trade_date = Column(DateTime, nullable=True)
    termination_date = Column(DateTime, nullable=True)

    # Technical fields
    relevant_authority = Column(String(255), nullable=True)
    relevant_venue = Column(String(255), nullable=True)
    from_date = Column(DateTime, nullable=True)
    technical_from_date = Column(DateTime, nullable=True)

    # Foreign key relationships
    lei_id = Column(String(20), nullable=True)  # LEI foreign key

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Equity-specific fields (nullable when not equity) - using DECIMAL per migration plan
    shares_outstanding = Column(DECIMAL(20, 0), nullable=True)
    market_cap = Column(DECIMAL(20, 2), nullable=True)
    voting_rights_per_share = Column(DECIMAL(10, 6), nullable=True)
    admission_approval_date = Column(Date, nullable=True)
    admission_request_date = Column(Date, nullable=True)
    price_multiplier = Column(DECIMAL(10, 6), nullable=True)
    exchange = Column(String(100), nullable=True)
    sector = Column(String(100), nullable=True)
    industry = Column(String(100), nullable=True)

    # Debt-specific fields (nullable when not debt) - using DECIMAL per migration plan
    total_issued_nominal = Column(DECIMAL(20, 2), nullable=True)
    maturity_date = Column(Date, nullable=True)
    nominal_value_per_unit = Column(DECIMAL(20, 6), nullable=True)
    fixed_interest_rate = Column(DECIMAL(10, 6), nullable=True)  # coupon_rate from plan
    debt_seniority = Column(String(50), nullable=True)
    coupon_frequency = Column(String(20), nullable=True)
    credit_rating = Column(String(10), nullable=True)
    floating_rate_reference = Column(String(255), nullable=True)
    floating_rate_term_unit = Column(String(10), nullable=True)
    floating_rate_term_value = Column(DECIMAL(10, 6), nullable=True)
    floating_rate_basis_points_spread = Column(DECIMAL(10, 6), nullable=True)

    # Future-specific fields (nullable when not future)
    expiry_date = Column(Date, nullable=True)  # expiry_date from plan
    expiration_date = Column(Date, nullable=True)  # Keep both for compatibility
    final_settlement_date = Column(Date, nullable=True)
    delivery_type = Column(String(50), nullable=True)
    settlement_method = Column(String(50), nullable=True)
    contract_size = Column(DECIMAL(20, 6), nullable=True)
    contract_unit = Column(String(20), nullable=True)
    settlement_currency = Column(String(3), nullable=True)
    final_price_type = Column(String(50), nullable=True)
    transaction_type = Column(String(50), nullable=True)
    underlying_asset = Column(String(200), nullable=True)  # From plan

    # Common derivative/complex instrument fields
    asset_class = Column(String(50), nullable=True)
    commodity_product = Column(String(255), nullable=True)
    energy_type = Column(String(50), nullable=True)
    oil_type = Column(String(50), nullable=True)
    base_product = Column(String(255), nullable=True)
    sub_product = Column(String(255), nullable=True)
    additional_sub_product = Column(String(255), nullable=True)
    metal_type = Column(String(50), nullable=True)
    precious_metal = Column(String(50), nullable=True)
    additional_metal_product = Column(String(255), nullable=True)

    # Underlying instrument references
    underlying_single_isin = Column(String(12), nullable=True)
    underlying_index_isin = Column(String(12), nullable=True)
    basket_isin = Column(String(12), nullable=True)
    underlying_single_lei = Column(String(20), nullable=True)
    basket_lei = Column(String(20), nullable=True)
    underlying_single_index_name = Column(String(500), nullable=True)
    underlying_index_name_term_unit = Column(String(10), nullable=True)
    underlying_index_name_term_value = Column(String(50), nullable=True)

    # Flexible data storage for complex or future fields
    additional_data = Column(Text, nullable=True)  # JSON as TEXT in SQL Server

    # Indexes for performance - following SQL Server best practices
    __table_args__ = (
        Index("idx_instruments_type", "instrument_type"),
        Index("idx_instruments_isin", "isin"),
        Index("idx_instruments_symbol", "symbol"),
        Index("idx_instruments_lei", "lei_id"),
        Index("idx_instruments_trading_venue", "trading_venue"),
        Index("idx_instruments_created_at", "created_at"),
        Index("idx_instruments_type_isin", "instrument_type", "isin"),  # Composite index
    )

    # Implement the interface properties using direct attribute access
    @property
    def instrument_type(self) -> str:
        return getattr(self, "instrument_type", "unknown")

    def get_equity_fields(self) -> Dict[str, Any]:
        """Return only equity-relevant fields if this is an equity (per migration plan)."""
        if self.instrument_type == "equity":
            return {
                "shares_outstanding": self.shares_outstanding,
                "market_cap": self.market_cap,
                "voting_rights_per_share": self.voting_rights_per_share,
                "admission_approval_date": self.admission_approval_date,
                "admission_request_date": self.admission_request_date,
                "price_multiplier": self.price_multiplier,
                "exchange": self.exchange,
                "sector": self.sector,
                "industry": self.industry,
            }
        return {}

    def get_debt_fields(self) -> Dict[str, Any]:
        """Get debt-specific fields if this is a debt instrument."""
        if self.instrument_type == "debt":
            return {
                "total_issued_nominal": self.total_issued_nominal,
                "maturity_date": self.maturity_date,
                "nominal_value_per_unit": self.nominal_value_per_unit,
                "fixed_interest_rate": self.fixed_interest_rate,  # coupon_rate equivalent
                "debt_seniority": self.debt_seniority,
                "coupon_frequency": self.coupon_frequency,
                "credit_rating": self.credit_rating,
            }
        return {}

    def get_future_fields(self) -> Dict[str, Any]:
        """Get future-specific fields if this is a future instrument."""
        if self.instrument_type == "future":
            return {
                "expiry_date": self.expiry_date,
                "underlying_asset": self.underlying_asset,
                "expiration_date": self.expiration_date,
                "final_settlement_date": self.final_settlement_date,
                "delivery_type": self.delivery_type,
                "settlement_method": self.settlement_method,
                "contract_size": self.contract_size,
                "contract_unit": self.contract_unit,
                "settlement_currency": self.settlement_currency,
            }
        return {}

    def set_equity_fields(self, data: Dict[str, Any]) -> None:
        """Set equity-specific fields."""
        equity_field_mapping = {
            "shares_outstanding": "shares_outstanding",
            "market_cap": "market_cap",
            "voting_rights_per_share": "voting_rights_per_share",
            "admission_approval_date": "admission_approval_date",
            "admission_request_date": "admission_request_date",
            "price_multiplier": "price_multiplier",
            "exchange": "exchange",
            "sector": "sector",
            "industry": "industry",
        }

        for field_name, attr_name in equity_field_mapping.items():
            if field_name in data:
                setattr(self, attr_name, data[field_name])

    def set_debt_fields(self, data: Dict[str, Any]) -> None:
        """Set debt-specific fields."""
        debt_field_mapping = {
            "total_issued_nominal": "total_issued_nominal",
            "maturity_date": "maturity_date",
            "nominal_value_per_unit": "nominal_value_per_unit",
            "fixed_interest_rate": "fixed_interest_rate",
            "coupon_rate": "fixed_interest_rate",  # Map coupon_rate to fixed_interest_rate
            "debt_seniority": "debt_seniority",
            "coupon_frequency": "coupon_frequency",
            "credit_rating": "credit_rating",
        }

        for field_name, attr_name in debt_field_mapping.items():
            if field_name in data:
                setattr(self, attr_name, data[field_name])

    def set_future_fields(self, data: Dict[str, Any]) -> None:
        """Set future-specific fields."""
        future_field_mapping = {
            "expiry_date": "expiry_date",
            "underlying_asset": "underlying_asset",
            "expiration_date": "expiration_date",
            "final_settlement_date": "final_settlement_date",
            "delivery_type": "delivery_type",
            "settlement_method": "settlement_method",
            "contract_size": "contract_size",
            "contract_unit": "contract_unit",
            "settlement_currency": "settlement_currency",
        }

        for field_name, attr_name in future_field_mapping.items():
            if field_name in data:
                setattr(self, attr_name, data[field_name])

    def to_dict(self) -> Dict[str, Any]:
        """Convert the model instance to a dictionary."""
        result = {
            "id": self.id,
            "instrument_type": self.instrument_type,
            "isin": self.isin,
            "full_name": self.full_name,
            "short_name": self.short_name,
            "symbol": self.symbol,
            "figi": self.figi,
            "cfi_code": self.cfi_code,
            "currency": self.currency,
            "trading_venue": self.trading_venue,
            "lei_id": self.lei_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        # Add type-specific fields based on instrument type
        result.update(self.get_equity_fields())
        result.update(self.get_debt_fields())
        result.update(self.get_future_fields())

        # Add additional data if present
        if self.additional_data:
            try:
                additional = (
                    json.loads(self.additional_data)
                    if isinstance(self.additional_data, str)
                    else self.additional_data
                )
                result.update(additional)
            except (json.JSONDecodeError, TypeError):
                pass  # Ignore malformed additional data

        return result

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Update the model instance from a dictionary."""
        # Update basic fields
        basic_fields = [
            "isin",
            "full_name",
            "short_name",
            "symbol",
            "figi",
            "cfi_code",
            "currency",
            "trading_venue",
            "lei_id",
        ]
        for field in basic_fields:
            if field in data:
                setattr(self, field, data[field])

        # Update instrument type
        if "instrument_type" in data:
            self.instrument_type = data["instrument_type"]

        # Update type-specific fields based on instrument type
        instrument_type = data.get("instrument_type", self.instrument_type)

        if instrument_type == "equity":
            self.set_equity_fields(data)
        elif instrument_type == "debt":
            self.set_debt_fields(data)
        elif instrument_type == "future":
            self.set_future_fields(data)

        # Store remaining fields as additional_data
        processed_fields = set(basic_fields + ["instrument_type", "id", "created_at", "updated_at"])
        additional = {k: v for k, v in data.items() if k not in processed_fields}
        if additional:
            self.additional_data = json.dumps(additional)

        # Update timestamp
        self.updated_at = datetime.now(UTC)
