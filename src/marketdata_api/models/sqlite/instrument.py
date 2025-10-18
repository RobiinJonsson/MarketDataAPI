"""
Unified SQLite models with document-based approach.

This replaces the complex polymorphic inheritance with a clean, flexible design.
"""

import uuid
from datetime import UTC, datetime
from typing import Any, Dict, Optional

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import relationship

from .base_model import Base


class Instrument(Base):
    """Unified instrument model with core fields + JSON document storage.

    Updated to support all FIRDS instrument types (C,D,E,F,H,I,J,S,R,O) with
    common FIRDS columns promoted to dedicated database fields for performance.
    """

    __tablename__ = "instruments"

    # Core identification (always present)
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    isin = Column(String(12), unique=True, nullable=False)
    instrument_type = Column(
        String(50), nullable=False
    )  # collective_investment, debt, equity, future, etc.

    # Essential fields (common across all FIRDS types - promoted from JSON)
    full_name = Column(String(500))  # FinInstrmGnlAttrbts_FullNm
    short_name = Column(String(200))  # FinInstrmGnlAttrbts_ShrtNm
    currency = Column(String(3))  # FinInstrmGnlAttrbts_NtnlCcy
    cfi_code = Column(String(6))  # FinInstrmGnlAttrbts_ClssfctnTp
    commodity_derivative_indicator = Column(Boolean)  # FinInstrmGnlAttrbts_CmmdtyDerivInd
    lei_id = Column(String(20), ForeignKey("legal_entities.lei", ondelete="SET NULL"))  # Issr

    # Publication and regulatory fields (common to all FIRDS types)
    publication_from_date = Column(DateTime)  # TechAttrbts_PblctnPrd_FrDt
    competent_authority = Column(String(10))  # TechAttrbts_RlvntCmptntAuthrty
    relevant_trading_venue = Column(String(100))  # TechAttrbts_RlvntTradgVn

    # Document storage for type-specific and varying attributes
    firds_data = Column(JSON)  # Original FIRDS record for reference
    processed_attributes = Column(JSON)  # Cleaned/processed attributes

    # Record metadata
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))

    # Relationships
    legal_entity = relationship("LegalEntity", back_populates="instruments")
    trading_venues = relationship(
        "TradingVenue", back_populates="instrument", cascade="all, delete-orphan"
    )
    figi_mappings = relationship(
        "FigiMapping",
        back_populates="instrument",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )  # Changed to plural, removed uselist=False to allow multiple FIGIs
    transparency_calculations = relationship(
        "TransparencyCalculation", back_populates="instrument", cascade="all, delete-orphan"
    )

    # Indexes for performance
    __table_args__ = (
        Index("idx_instruments_unified_isin", "isin"),
        Index("idx_instruments_unified_type", "instrument_type"),
        Index("idx_instruments_unified_lei", "lei_id"),
        Index("idx_instruments_unified_cfi", "cfi_code"),
        Index("idx_instruments_unified_currency", "currency"),
        Index("idx_instruments_unified_competent_auth", "competent_authority"),
        Index("idx_instruments_unified_created", "created_at"),
    )

    def to_raw_data(self) -> Dict[str, Any]:
        """Extract raw model data for API layer processing. No presentation logic."""
        return {
            # Core database fields - raw values
            "id": self.id,
            "isin": self.isin, 
            "instrument_type": self.instrument_type,
            "full_name": self.full_name,
            "short_name": self.short_name,
            "currency": self.currency,
            "cfi_code": self.cfi_code,
            "commodity_derivative_indicator": self.commodity_derivative_indicator,
            "lei_id": self.lei_id,
            "publication_from_date": self.publication_from_date,
            "competent_authority": self.competent_authority,
            "relevant_trading_venue": self.relevant_trading_venue,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            
            # JSON data fields
            "processed_attributes": self.processed_attributes,
            "firds_data": self.firds_data,
            
            # Related data (for API layer to process)
            "legal_entity": self.legal_entity,
            "trading_venues": self.trading_venues,
            "figi_mappings": self.figi_mappings,
            "transparency_calculations": self.transparency_calculations,
        }

    def to_api_response(self) -> Dict[str, Any]:
        """Legacy method for backward compatibility. Use API layer response builders instead."""
        # Temporary fallback - will be removed once API layer is updated
        raw_data = self.to_raw_data()
        
        # Basic transformation for backward compatibility
        result = {}
        for key, value in raw_data.items():
            if key in ['created_at', 'updated_at', 'publication_from_date'] and value:
                result[key] = value.isoformat() if hasattr(value, 'isoformat') else str(value)
            elif key in ['legal_entity', 'trading_venues', 'figi_mappings', 'transparency_calculations']:
                # Skip related objects for now
                continue
            else:
                result[key] = value
        
        return result

    def _format_equity_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format equity-specific attributes into structured schema."""
        equity_attrs = {}

        if "price_multiplier" in attrs:
            equity_attrs["price_multiplier"] = attrs["price_multiplier"]

        if "underlying_isin" in attrs:
            equity_attrs["underlying_isin"] = attrs["underlying_isin"]

    def _format_collective_investment_attributes(
        self, attrs: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Format collective investment (Type C) specific attributes."""
        civ_attrs = {}

        # Common CIV attributes from FIRDS analysis
        if "underlying_isin" in attrs:
            civ_attrs["underlying_isin"] = attrs["underlying_isin"]

        if "fund_type" in attrs:
            civ_attrs["fund_type"] = attrs["fund_type"]

        if "investment_strategy" in attrs:
            civ_attrs["investment_strategy"] = attrs["investment_strategy"]

        return civ_attrs if civ_attrs else None

    def _format_hybrid_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format hybrid instrument (Type H) specific attributes."""
        hybrid_attrs = {}

        if "underlying_assets" in attrs:
            hybrid_attrs["underlying_assets"] = attrs["underlying_assets"]

        if "conversion_ratio" in attrs:
            hybrid_attrs["conversion_ratio"] = attrs["conversion_ratio"]

        if "barrier_level" in attrs:
            hybrid_attrs["barrier_level"] = attrs["barrier_level"]

        return hybrid_attrs if hybrid_attrs else None

    def _format_interest_rate_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format interest rate instrument (Type I) specific attributes."""
        ir_attrs = {}

        if "reference_rate" in attrs:
            ir_attrs["reference_rate"] = attrs["reference_rate"]

        if "spread" in attrs:
            ir_attrs["spread"] = attrs["spread"]

        if "payment_frequency" in attrs:
            ir_attrs["payment_frequency"] = attrs["payment_frequency"]

        return ir_attrs if ir_attrs else None

    def _format_convertible_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format convertible instrument (Type J) specific attributes."""
        conv_attrs = {}

        if "conversion_price" in attrs:
            conv_attrs["conversion_price"] = attrs["conversion_price"]

        if "conversion_ratio" in attrs:
            conv_attrs["conversion_ratio"] = attrs["conversion_ratio"]

        if "underlying_isin" in attrs:
            conv_attrs["underlying_isin"] = attrs["underlying_isin"]

        return conv_attrs if conv_attrs else None

    def _format_option_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format option (Type O) specific attributes."""
        option_attrs = {}

        if "option_type" in attrs:
            option_attrs["option_type"] = attrs["option_type"]  # Call/Put

        if "strike_price" in attrs:
            option_attrs["strike_price"] = attrs["strike_price"]

        if "expiration_date" in attrs:
            option_attrs["expiration_date"] = attrs["expiration_date"]

        if "underlying_assets" in attrs:
            option_attrs["underlying_assets"] = attrs["underlying_assets"]

        return option_attrs if option_attrs else None

    def _format_rights_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format rights/warrants (Type R) specific attributes."""
        rights_attrs = {}

        if "exercise_price" in attrs:
            rights_attrs["exercise_price"] = attrs["exercise_price"]

        if "exercise_ratio" in attrs:
            rights_attrs["exercise_ratio"] = attrs["exercise_ratio"]

        if "expiration_date" in attrs:
            rights_attrs["expiration_date"] = attrs["expiration_date"]

        if "underlying_isin" in attrs:
            rights_attrs["underlying_isin"] = attrs["underlying_isin"]

        return rights_attrs if rights_attrs else None

    def _format_structured_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format structured product (Type S) specific attributes."""
        struct_attrs = {}

        if "underlying_assets" in attrs:
            struct_attrs["underlying_assets"] = attrs["underlying_assets"]

        if "protection_level" in attrs:
            struct_attrs["protection_level"] = attrs["protection_level"]

        if "participation_rate" in attrs:
            struct_attrs["participation_rate"] = attrs["participation_rate"]

        if "barrier_level" in attrs:
            struct_attrs["barrier_level"] = attrs["barrier_level"]

        return struct_attrs if struct_attrs else None

    def _format_debt_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format debt-specific attributes into structured schema."""
        debt_attrs = {}

        if "maturity_date" in attrs:
            debt_attrs["maturity_date"] = attrs["maturity_date"]

        if "total_issued_nominal" in attrs:
            debt_attrs["total_issued_nominal"] = attrs["total_issued_nominal"]

        if "nominal_value_per_unit" in attrs:
            debt_attrs["nominal_value_per_unit"] = attrs["nominal_value_per_unit"]

        # Map potential debt-specific FIRDS fields
        if "debt_seniority" in attrs:
            debt_attrs["debt_seniority"] = attrs["debt_seniority"]

        if "interest_rate" in attrs:
            debt_attrs["interest_rate"] = attrs["interest_rate"]

        return debt_attrs if debt_attrs else None

    def _format_future_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format future-specific attributes into structured schema."""
        future_attrs = {}

        if "expiration_date" in attrs:
            future_attrs["expiration_date"] = attrs["expiration_date"]

        if "delivery_type" in attrs:
            future_attrs["delivery_type"] = attrs["delivery_type"]

        if "price_multiplier" in attrs:
            future_attrs["price_multiplier"] = attrs["price_multiplier"]

        if "underlying_assets" in attrs:
            future_attrs["underlying_assets"] = attrs["underlying_assets"]

        if "commodity_details" in attrs:
            future_attrs["commodity_details"] = attrs["commodity_details"]

        return future_attrs if future_attrs else None

    def _is_structured_attribute(self, key: str) -> bool:
        """Check if an attribute is already handled in structured sections."""
        structured_keys = {
            # Equity attributes
            "price_multiplier",
            "underlying_isin",
            "underlying_index",
            "asset_class",
            # Debt attributes
            "maturity_date",
            "total_issued_nominal",
            "nominal_value_per_unit",
            "debt_seniority",
            "interest_rate",
            # Future attributes
            "expiration_date",
            "delivery_type",
            "underlying_assets",
            "commodity_details",
            # Collective Investment attributes
            "fund_type",
            "investment_strategy",
            # Hybrid attributes
            "conversion_ratio",
            "barrier_level",
            # Interest Rate attributes
            "reference_rate",
            "spread",
            "payment_frequency",
            # Convertible attributes
            "conversion_price",
            # Option attributes
            "option_type",
            "strike_price",
            # Rights attributes
            "exercise_price",
            "exercise_ratio",
            # Structured product attributes
            "protection_level",
            "participation_rate",
        }
        return key in structured_keys

    @classmethod
    def map_firds_type_to_instrument_type(
        cls, firds_type: str, cfi_code: Optional[str] = None
    ) -> str:
        """Map FIRDS instrument type letter to business instrument type using CFI standards.

        This method now uses the CFI model as the single source of truth.
        FIRDS file letters directly map to CFI categories following ISO 10962.

        Args:
            firds_type: Single letter FIRDS type (C, D, E, F, H, I, J, O, R, S)
            cfi_code: Optional CFI code for validation and refinement

        Returns:
            String representing the business instrument type
        """
        from marketdata_api.models.utils.cfi_instrument_manager import CFIInstrumentTypeManager

        # Use CFI code if available (primary source of truth)
        if cfi_code:
            # Validate consistency between FIRDS type and CFI code
            is_consistent, error_msg = CFIInstrumentTypeManager.validate_cfi_consistency(
                cfi_code, firds_type
            )
            if not is_consistent:
                # Log warning but continue - data might have inconsistencies
                import logging

                logger = logging.getLogger(__name__)
                logger.warning(f"CFI-FIRDS inconsistency for {firds_type}/{cfi_code}: {error_msg}")

            # Use CFI-based type determination
            return CFIInstrumentTypeManager.get_business_type_from_cfi(cfi_code)

        # Fallback to FIRDS-based determination (still CFI-compliant)
        return CFIInstrumentTypeManager.get_business_type_from_firds_file(firds_type)

    def _clean_json_attributes(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Clean JSON attributes, removing NaN values and empty objects."""
        import math

        def clean_value(value):
            if isinstance(value, float) and math.isnan(value):
                return None
            elif isinstance(value, dict):
                cleaned = {k: clean_value(v) for k, v in value.items()}
                # Remove keys with None values or empty dicts
                return {k: v for k, v in cleaned.items() if v is not None and v != {}}
            elif isinstance(value, list):
                return [
                    clean_value(item)
                    for item in value
                    if not (isinstance(item, float) and math.isnan(item))
                ]
            else:
                return value

        cleaned = {}
        for key, value in attributes.items():
            cleaned_value = clean_value(value)
            if cleaned_value is not None and cleaned_value != {}:
                cleaned[key] = cleaned_value

        return cleaned

    def _format_spot_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format spot (index-linked) instrument attributes."""
        if not attrs:
            return None

        spot_attrs = {}

        # Index reference information
        if "underlying_index" in attrs:
            spot_attrs["underlying_index"] = attrs["underlying_index"]

        # Multiplier and adjustment factor
        if "index_multiplier" in attrs:
            spot_attrs["index_multiplier"] = attrs["index_multiplier"]

        return spot_attrs if spot_attrs else None

    def _format_forward_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format forward instrument attributes."""
        if not attrs:
            return None

        forward_attrs = {}

        # Forward contract details
        if "delivery_date" in attrs:
            forward_attrs["delivery_date"] = attrs["delivery_date"]

        if "settlement_type" in attrs:
            forward_attrs["settlement_type"] = attrs["settlement_type"]

        if "underlying_asset" in attrs:
            forward_attrs["underlying_asset"] = attrs["underlying_asset"]

        return forward_attrs if forward_attrs else None

    def _format_swap_attributes(self, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format swap instrument attributes from FIRDS data."""
        # For swaps, we need to extract from firds_data, not just processed_attributes
        firds = self.firds_data or {}
        
        swap_attrs = {}

        # Expiration and termination dates
        if firds.get('DerivInstrmAttrbts_XpryDt'):
            swap_attrs["expiration_date"] = firds['DerivInstrmAttrbts_XpryDt']
        
        if firds.get('TradgVnRltdAttrbts_TermntnDt'):
            swap_attrs["termination_date"] = firds['TradgVnRltdAttrbts_TermntnDt']

        # Settlement/Delivery type
        if firds.get('DerivInstrmAttrbts_DlvryTp'):
            swap_attrs["settlement_type"] = firds['DerivInstrmAttrbts_DlvryTp']

        # Price multiplier
        if firds.get('DerivInstrmAttrbts_PricMltplr'):
            swap_attrs["price_multiplier"] = firds['DerivInstrmAttrbts_PricMltplr']

        # Reference rate from index
        if firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx'):
            swap_attrs["reference_index"] = firds['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx']
        elif firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx'):
            swap_attrs["reference_index"] = firds['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx']

        # Floating term (combine value and unit from interest rate)
        term_val = firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val')
        term_unit = firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit')
        if term_val and term_unit:
            swap_attrs["floating_term"] = f"{term_val} {term_unit}"

        # Underlying index term (for reference rate frequency)
        underlying_val = firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val')
        underlying_unit = firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit')
        if underlying_val and underlying_unit:
            swap_attrs["reference_rate_frequency"] = f"{underlying_val} {underlying_unit}"

        # Fixed rate (first leg) - if available
        if firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd'):
            swap_attrs["fixed_rate"] = firds['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_FrstLegIntrstRate_Fxd']

        # Floating rate name (other leg) - if available
        if firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm'):
            swap_attrs["floating_reference_rate"] = firds['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrLegIntrstRate_Fltg_RefRate_Nm']

        # Other currency (for cross-currency swaps)
        if firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy'):
            swap_attrs["other_currency"] = firds['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_OthrNtnlCcy']

        # Underlying ISINs (basket or single)
        if firds.get('DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN'):
            swap_attrs["underlying_basket_isin"] = firds['DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN']
        elif firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
            swap_attrs["underlying_single_isin"] = firds['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']

        # Determine swap type based on available data
        if any(['IntrstRate' in key for key in firds.keys()]):
            swap_attrs["swap_type"] = "Interest Rate Swap"
        elif firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp'):
            swap_attrs["swap_type"] = "FX Swap"
        else:
            swap_attrs["swap_type"] = "Swap"

        # Add classification details for better understanding
        if swap_attrs.get("reference_index") and swap_attrs.get("floating_term"):
            swap_attrs["classification"] = f"Fixed-Float {swap_attrs['floating_term']} {swap_attrs['reference_index']}"

        return swap_attrs if swap_attrs else None


class TradingVenue(Base):
    """Trading venue records for instruments - stores ALL venue data."""

    __tablename__ = "trading_venues"

    # Primary identification
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    instrument_id = Column(
        String(36), ForeignKey("instruments.id", ondelete="CASCADE"), nullable=False
    )

    # Core venue fields (always present)
    venue_id = Column(String(100), nullable=False)  # TradgVnRltdAttrbts_Id
    isin = Column(String(12), nullable=False)  # Denormalized for easier querying

    # MIC integration (ISO 10383 Market Identification Code)
    mic_code = Column(
        String(4), ForeignKey("market_identification_codes.mic", ondelete="SET NULL")
    )  # Link to MIC registry

    # Trading dates and status (common FIRDS fields promoted)
    first_trade_date = Column(DateTime)  # TradgVnRltdAttrbts_FrstTradDt
    termination_date = Column(DateTime)  # TradgVnRltdAttrbts_TermntnDt
    admission_approval_date = Column(DateTime)  # TradgVnRltdAttrbts_AdmssnApprvlDtByIssr
    request_for_admission_date = Column(DateTime)  # TradgVnRltdAttrbts_ReqForAdmssnDt
    issuer_requested = Column(Boolean)  # TradgVnRltdAttrbts_IssrReq

    # Venue-specific instrument data
    venue_full_name = Column(String(500))
    venue_short_name = Column(String(200))
    classification_type = Column(String(100))
    venue_currency = Column(String(3))

    # Administrative fields
    issuer_requested = Column(Boolean)  # TradgVnRltdAttrbts_IssrReq
    competent_authority = Column(String(100))
    relevant_trading_venue = Column(String(100))
    publication_from_date = Column(DateTime)

    # Document storage for venue-specific attributes
    venue_attributes = Column(JSON)  # Any additional venue-specific data
    original_firds_record = Column(JSON)  # Original FIRDS record for this venue

    # Record metadata
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))

    # Relationships
    instrument = relationship("Instrument", back_populates="trading_venues")
    market_identification_code = relationship(
        "MarketIdentificationCode", back_populates="trading_venues"
    )

    # Indexes for performance
    __table_args__ = (
        Index("idx_trading_venues_unified_instrument_id", "instrument_id"),
        Index("idx_trading_venues_unified_venue_id", "venue_id"),
        Index("idx_trading_venues_unified_isin", "isin"),
        Index("idx_trading_venues_unified_isin_venue", "isin", "venue_id"),
        Index("idx_trading_venues_unified_dates", "first_trade_date", "termination_date"),
        Index("idx_trading_venues_unified_mic_code", "mic_code"),
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses - NO raw FIRDS data."""
        return {
            "id": self.id,
            "venue_id": self.venue_id,
            "isin": self.isin,
            "first_trade_date": (
                self.first_trade_date.isoformat() if self.first_trade_date else None
            ),
            "termination_date": (
                self.termination_date.isoformat() if self.termination_date else None
            ),
            "admission_approval_date": (
                self.admission_approval_date.isoformat() if self.admission_approval_date else None
            ),
            "request_for_admission_date": (
                self.request_for_admission_date.isoformat()
                if self.request_for_admission_date
                else None
            ),
            "venue_full_name": self.venue_full_name,
            "venue_short_name": self.venue_short_name,
            "classification_type": self.classification_type,
            "venue_currency": self.venue_currency,
            "issuer_requested": self.issuer_requested,
            "competent_authority": self.competent_authority,
            "relevant_trading_venue": self.relevant_trading_venue,
            "publication_from_date": (
                self.publication_from_date.isoformat() if self.publication_from_date else None
            ),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            # Include venue-specific attributes if present (but not raw FIRDS)
            **(self.venue_attributes or {}),
        }
