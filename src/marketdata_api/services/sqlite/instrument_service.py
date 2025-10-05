"""
Unified Instrument Service Implementation

This service implements the document-based approach for ALL FIRDS instrument types:
1. Supports all 10 FIRDS types: C,D,E,F,H,I,J,S,R,O
2. Stores ALL venue records in database with promoted common fields
3. Uses JSON for flexible type-specific attribute storage
4. Provides clean API responses without raw FIRDS data
5. Uses new FIRDS type mappings and constants
"""

import json
import logging
import re
import time
import uuid
from datetime import UTC, datetime
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

# Removed old OpenFIGI import - now using enhanced service for both primary and fallback
from ...config import esmaConfig
from ...constants import FirdsTypes
from ...database.session import SessionLocal, get_session
from ...models.interfaces.instrument_interface import InstrumentInterface
from ...models.sqlite.figi import FigiMapping

# Import the unified models
from ...models.sqlite.instrument import Instrument, TradingVenue
from ...models.utils.cfi_instrument_manager import CFIInstrumentTypeManager
from ...services.interfaces.instrument_service_interface import InstrumentServiceInterface

logger = logging.getLogger(__name__)


class InstrumentServiceError(Exception):
    """Base exception for instrument service errors"""

    pass


class InstrumentNotFoundError(InstrumentServiceError):
    """Raised when an instrument cannot be found"""

    pass


class SqliteInstrumentService(InstrumentServiceInterface):
    """Unified instrument service using document-based approach."""

    def __init__(self):
        self.database_type = "sqlite"
        self.logger = logging.getLogger(__name__)

    def create_instrument(
        self, identifier: str, instrument_type: str = "equity"
    ) -> InstrumentInterface:
        """
        Create instrument with support for ALL FIRDS types and store venue records.

        UPDATED BEHAVIOR:
        1. Auto-detects FIRDS type from files or uses provided type
        2. Maps FIRDS type to business instrument type using new mappings
        3. Creates single instrument with promoted common fields
        4. Creates separate venue records for EACH venue
        5. Stores both original and processed data with new structure
        """
        session = SessionLocal()

        try:
            # Get ALL FIRDS data for this ISIN (auto-detect type if needed)
            all_venue_records, detected_firds_type = self._get_firds_data_from_storage_all_types(
                identifier, instrument_type
            )
            if not all_venue_records:
                raise InstrumentNotFoundError(f"No FIRDS data found for {identifier}")

            self.logger.info(
                f"Found {len(all_venue_records)} venue records for {identifier} (FIRDS type: {detected_firds_type})"
            )

            # Map FIRDS type to business instrument type
            business_instrument_type = Instrument.map_firds_type_to_instrument_type(
                detected_firds_type, all_venue_records[0].get("FinInstrmGnlAttrbts_ClssfctnTp")
            )

            self.logger.info(
                f"Mapped FIRDS type {detected_firds_type} to business type: {business_instrument_type}"
            )

            # Use first record for primary instrument data
            primary_record = all_venue_records[0]

            # Check for existing and delete if present (with transaction optimization)
            existing = session.query(Instrument).filter(Instrument.isin == identifier).first()
            if existing:
                self.logger.info(f"🗑️  Deleting existing instrument {identifier}")
                # Delete related venues first to avoid constraint issues
                session.query(TradingVenue).filter(
                    TradingVenue.instrument_id == existing.id
                ).delete()
                session.delete(existing)
                session.flush()  # Ensure deletion is processed before creating new

            # Create instrument with promoted common fields + JSON attributes
            instrument_data = self._build_instrument_data(
                identifier, business_instrument_type, primary_record, detected_firds_type
            )

            # Create new instrument
            instrument = Instrument(**instrument_data)
            session.add(instrument)
            session.flush()

            # Create venue records for ALL venues
            venue_creation_start = time.time()
            venue_records = []
            self.logger.info(f"🏢 Creating {len(all_venue_records)} venue records...")

            for i, venue_data in enumerate(all_venue_records, 1):
                venue_record = self._create_venue_record(instrument.id, venue_data)
                venue_records.append(venue_record)
                session.add(venue_record)
                if i % 10 == 0:  # Log progress every 10 venues
                    self.logger.debug(f"  📍 Created {i}/{len(all_venue_records)} venues...")

            venue_creation_elapsed = time.time() - venue_creation_start
            self.logger.info(
                f"✅ Created {len(venue_records)} venue records in {venue_creation_elapsed:.1f}s"
            )

            # Commit all changes
            commit_start = time.time()
            self.logger.info("💾 Committing to database...")
            session.commit()
            commit_elapsed = time.time() - commit_start
            self.logger.info(f"✅ Database commit completed in {commit_elapsed:.1f}s")

            self.logger.info(
                f"Created {business_instrument_type} instrument {identifier} with {len(venue_records)} venue records"
            )

            # Try enrichment
            try:
                enriched_session, enriched_instrument = self.enrich_instrument(instrument)
                enriched_session.close()

                # Return fresh copy
                return session.get(Instrument, instrument.id)
            except Exception as e:
                self.logger.warning(f"Enrichment failed: {e}")
                return instrument

        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to create instrument: {str(e)}")
            raise InstrumentServiceError(f"Failed to create instrument: {str(e)}") from e
        finally:
            session.close()

    def _build_instrument_data(
        self,
        identifier: str,
        business_instrument_type: str,
        primary_record: Dict[str, Any],
        firds_type: str,
    ) -> Dict[str, Any]:
        """Build instrument data dictionary with promoted common fields."""

        # Parse boolean commodity derivative indicator
        commodity_deriv_ind = primary_record.get("FinInstrmGnlAttrbts_CmmdtyDerivInd")
        if isinstance(commodity_deriv_ind, str):
            commodity_deriv_ind = commodity_deriv_ind.lower() in ("true", "1", "yes")
        elif commodity_deriv_ind is None:
            commodity_deriv_ind = False

        return {
            "id": str(uuid.uuid4()),
            "isin": identifier,
            "instrument_type": business_instrument_type,
            # Promoted common fields (from FIRDS analysis)
            "full_name": primary_record.get("FinInstrmGnlAttrbts_FullNm"),
            "short_name": primary_record.get("FinInstrmGnlAttrbts_ShrtNm"),
            "currency": primary_record.get("FinInstrmGnlAttrbts_NtnlCcy"),
            "cfi_code": primary_record.get("FinInstrmGnlAttrbts_ClssfctnTp"),
            "commodity_derivative_indicator": commodity_deriv_ind,
            "lei_id": primary_record.get("Issr"),
            "publication_from_date": self._parse_date(
                primary_record.get("TechAttrbts_PblctnPrd_FrDt")
            ),
            "competent_authority": primary_record.get("TechAttrbts_RlvntCmptntAuthrty"),
            "relevant_trading_venue": primary_record.get("TechAttrbts_RlvntTradgVn"),
            # JSON storage for flexibility
            "firds_data": primary_record,  # Original FIRDS record
            "processed_attributes": self._process_instrument_attributes(
                primary_record, business_instrument_type, firds_type
            ),
        }

    def _get_firds_data_from_storage_all_types(
        self, identifier: str, preferred_type: str = None
    ) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Fetch FIRDS data from all instrument types, auto-detecting the correct type.

        Returns:
            Tuple of (records_list, detected_firds_type)
        """
        try:
            from pathlib import Path

            self.logger.info(f"🔍 Starting FIRDS search for {identifier}")
            search_start = time.time()

            # If preferred type is provided, try it first
            if preferred_type:
                # Use CFI manager for consistent business type to FIRDS type mapping
                # Reverse lookup: business type -> FIRDS letter
                business_to_firds = {}
                for firds_letter, category in CFIInstrumentTypeManager.FIRDS_TO_CFI_MAPPING.items():
                    business_type = CFIInstrumentTypeManager.CFI_TO_BUSINESS_TYPE.get(category)
                    if business_type:
                        business_to_firds[business_type] = firds_letter

                if preferred_type in business_to_firds:
                    firds_type = business_to_firds[preferred_type]
                    self.logger.info(
                        f"🎯 Trying CFI-validated type: {preferred_type} → FIRDS {firds_type}"
                    )
                    records = self._search_firds_files_for_type(identifier, firds_type)
                    if records:
                        elapsed = time.time() - search_start
                        self.logger.info(f"✅ Found in CFI type {firds_type} in {elapsed:.1f}s")
                        return records, firds_type
                    else:
                        elapsed = time.time() - search_start
                        self.logger.warning(
                            f"❌ {identifier} not found in CFI-validated type {firds_type} ({elapsed:.1f}s)"
                        )
                        self.logger.info(
                            f"🚫 Stopping search - CFI type {firds_type} is definitive for business type '{preferred_type}'"
                        )
                        return None, None
                elif preferred_type in {"E", "D", "F", "C"}:  # Legacy direct FIRDS types
                    firds_type = preferred_type
                    self.logger.info(f"🎯 Trying legacy FIRDS type: {firds_type}")
                    records = self._search_firds_files_for_type(identifier, firds_type)
                    if records:
                        elapsed = time.time() - search_start
                        self.logger.info(f"✅ Found in legacy type {firds_type} in {elapsed:.1f}s")
                        return records, firds_type
                    else:
                        self.logger.info(
                            f"❌ Not found in legacy type {firds_type}, will try all types"
                        )
                else:
                    self.logger.warning(
                        f"❌ Unknown business type '{preferred_type}' - not in CFI mapping"
                    )

            # Only search all types if no preferred type was given OR it was a legacy/unknown type
            if not preferred_type or preferred_type not in business_to_firds:
                types_to_search = list(FirdsTypes.MAPPING.keys())
                self.logger.info(
                    f"🔄 Fallback: Searching {len(types_to_search)} FIRDS types: {types_to_search}"
                )

                for i, firds_type in enumerate(types_to_search, 1):
                    type_start = time.time()
                    self.logger.debug(
                        f"  📂 [{i}/{len(types_to_search)}] Searching type {firds_type}..."
                    )
                    records = self._search_firds_files_for_type(identifier, firds_type)
                    type_elapsed = time.time() - type_start

                    if records:
                        total_elapsed = time.time() - search_start
                        self.logger.info(
                            f"✅ Found {identifier} in FIRDS type {firds_type} (searched {i} types, {total_elapsed:.1f}s total)"
                        )
                        return records, firds_type
                    else:
                        self.logger.debug(
                            f"  ❌ Not found in type {firds_type} ({type_elapsed:.1f}s)"
                        )

            total_elapsed = time.time() - search_start
            self.logger.warning(
                f"❌ {identifier} not found in any FIRDS files after {total_elapsed:.1f}s"
            )
            return None, None

        except Exception as e:
            self.logger.error(f"💥 Error fetching FIRDS data from storage: {str(e)}")
            return None, None

    def _search_firds_files_for_type(
        self, identifier: str, firds_type: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Search for identifier in FIRDS files of a specific type with performance optimization."""
        try:
            from pathlib import Path

            import pandas as pd

            search_start = time.time()

            firds_path = Path(esmaConfig.firds_path)
            if not firds_path.exists():
                self.logger.error(f"❌ FIRDS storage path does not exist: {firds_path}")
                return None

            # Find files matching the pattern for this FIRDS type
            file_pattern = f"*FULINS_{firds_type}*_firds_data.csv"
            matching_files = list(firds_path.glob(file_pattern))

            if not matching_files:
                self.logger.debug(
                    f"    📁 No {firds_type} files found matching pattern: {file_pattern}"
                )
                return None

            self.logger.debug(f"    📁 Found {len(matching_files)} files for type {firds_type}")

            # Search through files for the identifier (newest files first for better cache hit)
            matching_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

            for file_idx, file_path in enumerate(matching_files, 1):
                try:
                    file_start = time.time()
                    self.logger.debug(
                        f"      📄 [{file_idx}/{len(matching_files)}] Reading {file_path.name}..."
                    )

                    # Read with optimizations
                    df = pd.read_csv(
                        str(file_path),
                        dtype=str,
                        low_memory=False,
                        usecols=lambda x: x == "Id"
                        or not x.startswith("Unnamed"),  # Skip unnamed columns
                    )

                    file_read_time = time.time() - file_start

                    if df is not None and not df.empty and "Id" in df.columns:
                        search_start_df = time.time()

                        # Optimized search - use pandas vectorized operations
                        isin_data = df[df["Id"] == identifier]

                        search_time = time.time() - search_start_df

                        if not isin_data.empty:
                            total_time = time.time() - search_start
                            self.logger.info(
                                f"      ✅ Found {len(isin_data)} records in {file_path.name} (read: {file_read_time:.1f}s, search: {search_time:.1f}s, total: {total_time:.1f}s)"
                            )

                            # Return ALL records for this ISIN, handling NaN values efficiently
                            all_records = isin_data.fillna("").to_dict("records")
                            return all_records
                        else:
                            self.logger.debug(
                                f"      ❌ Not in {file_path.name} ({len(df)} total records, read: {file_read_time:.1f}s, search: {search_time:.1f}s)"
                            )
                    else:
                        self.logger.warning(f"      ⚠️  Invalid file structure in {file_path.name}")

                except Exception as e:
                    self.logger.warning(f"      💥 Error reading file {file_path}: {str(e)}")
                    continue

            total_search_time = time.time() - search_start
            self.logger.debug(
                f"    ❌ Not found in any {firds_type} files ({total_search_time:.1f}s)"
            )
            return None

        except Exception as e:
            self.logger.error(f"💥 Error searching FIRDS files for type {firds_type}: {str(e)}")
            return None

    def get_instrument_venues(
        self, identifier: str, instrument_type: str = "equity"
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get ALL venue records from DATABASE (not files).

        NEW BEHAVIOR:
        1. Queries database trading_venues table
        2. Returns clean structured data
        3. No raw FIRDS data included
        4. Much faster than file access
        """
        session = SessionLocal()

        try:
            # Find instrument
            instrument = (
                session.query(Instrument)
                .filter((Instrument.id == identifier) | (Instrument.isin == identifier))
                .first()
            )

            if not instrument:
                self.logger.warning(f"Instrument {identifier} not found")
                return None

            # Get all venue records from database
            venue_records = (
                session.query(TradingVenue)
                .filter(TradingVenue.instrument_id == instrument.id)
                .all()
            )

            if not venue_records:
                self.logger.warning(f"No venue records found in database for {identifier}")
                return []

            # Return clean structured data (no raw FIRDS)
            result = [venue.to_dict() for venue in venue_records]

            self.logger.info(
                f"Retrieved {len(result)} venue records for {identifier} from database"
            )
            return result

        except Exception as e:
            self.logger.error(f"Error retrieving venues for {identifier}: {e}")
            return None
        finally:
            session.close()

    def get_instrument(self, identifier: str) -> Tuple[Session, Optional[InstrumentInterface]]:
        """
        Retrieve an instrument by its identifier with relationships loaded.
        """
        from sqlalchemy.orm import joinedload

        session = SessionLocal()
        try:
            instrument = (
                session.query(Instrument)
                .options(
                    joinedload(Instrument.figi_mappings),
                    joinedload(Instrument.legal_entity),
                    joinedload(Instrument.trading_venues),
                )
                .filter((Instrument.id == identifier) | (Instrument.isin == identifier))
                .first()
            )
            if instrument:
                session.refresh(instrument)
            return session, instrument
        except:
            session.close()
            raise

    def _process_instrument_attributes(
        self, firds_record: Dict[str, Any], business_instrument_type: str, firds_type: str
    ) -> Dict[str, Any]:
        """Process type-specific attributes into clean JSON structure for ALL FIRDS types."""
        attributes = {}

        try:
            # Process based on business instrument type (mapped from FIRDS type)
            if business_instrument_type == "equity":
                attributes.update(self._process_equity_attributes(firds_record))

            elif business_instrument_type == "debt":
                attributes.update(self._process_debt_attributes(firds_record))

            elif business_instrument_type == "future":
                attributes.update(self._process_future_attributes(firds_record))

            elif business_instrument_type == "collective_investment":
                attributes.update(self._process_collective_investment_attributes(firds_record))

            elif business_instrument_type == "hybrid":
                attributes.update(self._process_hybrid_attributes(firds_record))

            elif business_instrument_type == "interest_rate":
                attributes.update(self._process_interest_rate_attributes(firds_record))

            elif business_instrument_type == "convertible":
                attributes.update(self._process_convertible_attributes(firds_record))

            elif business_instrument_type == "option":
                attributes.update(self._process_option_attributes(firds_record))

            elif business_instrument_type == "rights":
                attributes.update(self._process_rights_attributes(firds_record))

            elif business_instrument_type == "structured":
                attributes.update(self._process_structured_attributes(firds_record))

            # Add FIRDS type metadata
            attributes["firds_type"] = firds_type
            attributes["business_type"] = business_instrument_type

            # Process common derivative attributes (present across multiple types)
            self._process_common_derivative_attributes(firds_record, attributes)

        except Exception as e:
            self.logger.warning(f"Error processing attributes for {business_instrument_type}: {e}")

        return attributes

    def _process_equity_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process equity-specific attributes."""
        attributes = {}

        if firds_record.get("DerivInstrmAttrbts_PricMltplr"):
            try:
                attributes["price_multiplier"] = float(
                    firds_record["DerivInstrmAttrbts_PricMltplr"]
                )
            except (ValueError, TypeError):
                pass

        if firds_record.get("DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN"):
            attributes["underlying_isin"] = firds_record[
                "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN"
            ]

        if firds_record.get("DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm"):
            attributes["underlying_index"] = firds_record[
                "DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm"
            ]

        # Asset class attributes
        asset_class = self._extract_asset_class_attributes(firds_record)
        if asset_class:
            attributes["asset_class"] = asset_class

        return attributes

    def _process_debt_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process debt-specific attributes."""
        attributes = {}

        if firds_record.get("DebtInstrmAttrbts_MtrtyDt"):
            attributes["maturity_date"] = firds_record["DebtInstrmAttrbts_MtrtyDt"]

        if firds_record.get("DebtInstrmAttrbts_TtlIssdNmnlAmt"):
            try:
                attributes["total_issued_nominal"] = float(
                    firds_record["DebtInstrmAttrbts_TtlIssdNmnlAmt"]
                )
            except (ValueError, TypeError):
                pass

        if firds_record.get("DebtInstrmAttrbts_NmnlValPerUnit"):
            try:
                attributes["nominal_value_per_unit"] = float(
                    firds_record["DebtInstrmAttrbts_NmnlValPerUnit"]
                )
            except (ValueError, TypeError):
                pass

        if firds_record.get("DebtInstrmAttrbts_DebtSnrty"):
            attributes["debt_seniority"] = firds_record["DebtInstrmAttrbts_DebtSnrty"]

        # Interest rate attributes
        if firds_record.get("DebtInstrmAttrbts_IntrstRate_Fxd"):
            try:
                attributes["interest_rate"] = float(
                    firds_record["DebtInstrmAttrbts_IntrstRate_Fxd"]
                )
            except (ValueError, TypeError):
                pass

        return attributes

    def _process_future_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process future-specific attributes."""
        attributes = {}

        if firds_record.get("DerivInstrmAttrbts_XpryDt"):
            attributes["expiration_date"] = firds_record["DerivInstrmAttrbts_XpryDt"]

        if firds_record.get("DerivInstrmAttrbts_DlvryTp"):
            attributes["delivery_type"] = firds_record["DerivInstrmAttrbts_DlvryTp"]

        if firds_record.get("DerivInstrmAttrbts_PricMltplr"):
            try:
                attributes["price_multiplier"] = float(
                    firds_record["DerivInstrmAttrbts_PricMltplr"]
                )
            except (ValueError, TypeError):
                pass

        return attributes

    def _process_collective_investment_attributes(
        self, firds_record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process collective investment (Type C) specific attributes."""
        attributes = {}

        if firds_record.get("DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN"):
            attributes["underlying_isin"] = firds_record[
                "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN"
            ]

        # CIV-specific logic could be added here based on CFI code
        cfi_code = firds_record.get("FinInstrmGnlAttrbts_ClssfctnTp", "")
        if cfi_code.startswith("CI"):
            attributes["fund_type"] = "investment_fund"
        elif cfi_code.startswith("CE"):
            attributes["fund_type"] = "etf"
        elif cfi_code.startswith("CB"):
            attributes["fund_type"] = "reit"

        return attributes

    def _process_hybrid_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process hybrid instrument (Type H) specific attributes."""
        attributes = {}

        if firds_record.get("DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN"):
            attributes["underlying_isin"] = firds_record[
                "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN"
            ]

        if firds_record.get("DerivInstrmAttrbts_PricMltplr"):
            try:
                attributes["conversion_ratio"] = float(
                    firds_record["DerivInstrmAttrbts_PricMltplr"]
                )
            except (ValueError, TypeError):
                pass

        return attributes

    def _process_interest_rate_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process interest rate instrument (Type I) specific attributes."""
        attributes = {}

        # Interest rate specific fields
        if firds_record.get("DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm"):
            attributes["reference_rate"] = firds_record[
                "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm"
            ]

        if firds_record.get("DerivInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd"):
            try:
                attributes["spread"] = float(
                    firds_record["DerivInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd"]
                )
            except (ValueError, TypeError):
                pass

        return attributes

    def _process_convertible_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process convertible instrument (Type J) specific attributes."""
        attributes = {}

        if firds_record.get("DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN"):
            attributes["underlying_isin"] = firds_record[
                "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN"
            ]

        if firds_record.get("DerivInstrmAttrbts_PricMltplr"):
            try:
                attributes["conversion_ratio"] = float(
                    firds_record["DerivInstrmAttrbts_PricMltplr"]
                )
            except (ValueError, TypeError):
                pass

        return attributes

    def _extract_clean_strike_price(self, firds_record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract and clean strike price information from FIRDS record."""
        import re
        
        strike_info = {}
        
        # Handle percentage strike price
        if firds_record.get("DerivInstrmAttrbts_StrkPric_Pric_Pctg"):
            pctg_value = firds_record["DerivInstrmAttrbts_StrkPric_Pric_Pctg"]
            try:
                if isinstance(pctg_value, bool):
                    # Convert boolean to numeric (True=1, False=0)
                    strike_info["percentage"] = 1.0 if pctg_value else 0.0
                elif isinstance(pctg_value, str):
                    # Try to parse as float, handling boolean strings
                    cleaned = re.sub(r'^(true|false)', '', pctg_value.lower())
                    if cleaned:
                        strike_info["percentage"] = float(cleaned)
                    else:
                        strike_info["percentage"] = 1.0 if pctg_value.lower().startswith('true') else 0.0
                else:
                    strike_info["percentage"] = float(pctg_value)
            except (ValueError, TypeError):
                pass

        # Handle monetary amount strike price  
        if firds_record.get("DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt"):
            amount_raw = firds_record["DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Amt"]
            sign = firds_record.get("DerivInstrmAttrbts_StrkPric_Pric_MntryVal_Sgn", "")
            
            try:
                if isinstance(amount_raw, str):
                    # Remove boolean prefixes like "true" or "false" 
                    amount_clean = re.sub(r'^(true|false)', '', str(amount_raw))
                    if amount_clean:
                        amount_numeric = float(amount_clean)
                        if amount_numeric != 0:
                            strike_info["monetary_amount"] = amount_numeric
                            if sign:
                                strike_info["monetary_sign"] = sign
                elif isinstance(amount_raw, (int, float)) and amount_raw != 0:
                    strike_info["monetary_amount"] = float(amount_raw)
                    if sign:
                        strike_info["monetary_sign"] = sign
            except (ValueError, TypeError):
                pass

        # Handle basis points strike price
        if firds_record.get("DerivInstrmAttrbts_StrkPric_Pric_BsisPts"):
            bps_value = firds_record["DerivInstrmAttrbts_StrkPric_Pric_BsisPts"]
            try:
                if isinstance(bps_value, (int, float)) and bps_value != 0:
                    strike_info["basis_points"] = float(bps_value)
            except (ValueError, TypeError):
                pass

        return strike_info if strike_info else None

    def _process_option_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process option (Type O) specific attributes."""
        attributes = {}

        if firds_record.get("DerivInstrmAttrbts_XpryDt"):
            attributes["expiration_date"] = firds_record["DerivInstrmAttrbts_XpryDt"]

        if firds_record.get("DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN"):
            attributes["underlying_isin"] = firds_record[
                "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN"
            ]

        # Option type could be derived from other fields or CFI code
        cfi_code = firds_record.get("FinInstrmGnlAttrbts_ClssfctnTp", "")
        if "C" in cfi_code:
            attributes["option_type"] = "call"
        elif "P" in cfi_code:
            attributes["option_type"] = "put"

        # Process strike price information - clean and validate data
        strike_price_info = self._extract_clean_strike_price(firds_record)
        if strike_price_info:
            attributes["strike_price"] = strike_price_info

        # Exercise style
        if firds_record.get("DerivInstrmAttrbts_OptnExrcStyle"):
            exercise_style = firds_record["DerivInstrmAttrbts_OptnExrcStyle"]
            if exercise_style == "AMER":
                attributes["exercise_style"] = "american"
            elif exercise_style == "EURO":
                attributes["exercise_style"] = "european"
            else:
                attributes["exercise_style"] = exercise_style.lower()

        # Settlement type
        if firds_record.get("DerivInstrmAttrbts_DlvryTp"):
            delivery_type = firds_record["DerivInstrmAttrbts_DlvryTp"]
            attributes["settlement_type"] = "physical" if delivery_type == "PHYS" else "cash"

        # Underlying index information
        if firds_record.get("DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm"):
            attributes["underlying_index"] = firds_record["DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm"]

        return attributes

    def _process_rights_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process rights/warrants (Type R) specific attributes."""
        attributes = {}

        if firds_record.get("DerivInstrmAttrbts_XpryDt"):
            attributes["expiration_date"] = firds_record["DerivInstrmAttrbts_XpryDt"]

        if firds_record.get("DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN"):
            attributes["underlying_isin"] = firds_record[
                "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN"
            ]

        if firds_record.get("DerivInstrmAttrbts_PricMltplr"):
            try:
                attributes["exercise_ratio"] = float(firds_record["DerivInstrmAttrbts_PricMltplr"])
            except (ValueError, TypeError):
                pass

        return attributes

    def _process_structured_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process structured product (Type S) specific attributes."""
        attributes = {}

        if firds_record.get("DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN"):
            attributes["underlying_isin"] = firds_record[
                "DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN"
            ]

        if firds_record.get("DerivInstrmAttrbts_PricMltplr"):
            try:
                attributes["participation_rate"] = float(
                    firds_record["DerivInstrmAttrbts_PricMltplr"]
                )
            except (ValueError, TypeError):
                pass

        return attributes

    def _process_common_derivative_attributes(
        self, firds_record: Dict[str, Any], attributes: Dict[str, Any]
    ) -> None:
        """Process attributes common to multiple derivative types."""

        # Underlying instrument attributes
        underlying_assets = {}

        if firds_record.get("DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN"):
            underlying_assets["basket_isin"] = firds_record[
                "DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN"
            ]

        if firds_record.get("DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI"):
            underlying_assets["basket_lei"] = firds_record[
                "DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI"
            ]

        if firds_record.get("DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI"):
            underlying_assets["single_lei"] = firds_record[
                "DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI"
            ]

        if underlying_assets:
            attributes["underlying_assets"] = underlying_assets

    def _extract_asset_class_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Extract asset class specific attributes."""
        asset_class = {}

        # Oil/Energy attributes
        if firds_record.get(
            "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct"
        ):
            asset_class["oil_type"] = firds_record[
                "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct"
            ]

        if firds_record.get("DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct"):
            asset_class["sub_product"] = firds_record[
                "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct"
            ]

        # Metal attributes
        if firds_record.get(
            "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct"
        ):
            asset_class["metal_type"] = firds_record[
                "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct"
            ]

        # Electricity attributes
        if firds_record.get(
            "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct"
        ):
            asset_class["electricity_type"] = firds_record[
                "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct"
            ]

        # FX attributes
        if firds_record.get("DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy"):
            asset_class["other_currency"] = firds_record[
                "DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy"
            ]

        return asset_class

    def _create_venue_record(self, instrument_id: str, venue_data: Dict[str, Any]) -> TradingVenue:
        """Create a venue record from FIRDS data using updated model structure."""

        # Parse issuer requested as boolean
        issuer_requested = venue_data.get("TradgVnRltdAttrbts_IssrReq")
        if isinstance(issuer_requested, str):
            issuer_requested = issuer_requested.lower() in ("true", "1", "yes")
        elif issuer_requested is None:
            issuer_requested = False

        venue_record = TradingVenue(
            id=str(uuid.uuid4()),
            instrument_id=instrument_id,
            venue_id=venue_data.get("TradgVnRltdAttrbts_Id"),
            isin=venue_data.get("Id"),
            # Updated fields to match new model structure
            first_trade_date=self._parse_date(venue_data.get("TradgVnRltdAttrbts_FrstTradDt")),
            termination_date=self._parse_date(venue_data.get("TradgVnRltdAttrbts_TermntnDt")),
            admission_approval_date=self._parse_date(
                venue_data.get("TradgVnRltdAttrbts_AdmssnApprvlDtByIssr")
            ),
            request_for_admission_date=self._parse_date(
                venue_data.get("TradgVnRltdAttrbts_ReqForAdmssnDt")
            ),
            issuer_requested=issuer_requested,  # Now boolean instead of string
            venue_full_name=venue_data.get("FinInstrmGnlAttrbts_FullNm"),
            venue_short_name=venue_data.get("FinInstrmGnlAttrbts_ShrtNm"),
            classification_type=venue_data.get("FinInstrmGnlAttrbts_ClssfctnTp"),
            venue_currency=venue_data.get("FinInstrmGnlAttrbts_NtnlCcy"),
            competent_authority=venue_data.get("TechAttrbts_RlvntCmptntAuthrty"),
            relevant_trading_venue=venue_data.get("TechAttrbts_RlvntTradgVn"),
            publication_from_date=self._parse_date(venue_data.get("TechAttrbts_PblctnPrd_FrDt")),
            original_firds_record=venue_data,  # Store original for debugging/reference
        )

        # Store any additional venue-specific attributes (excluding mapped fields)
        venue_attributes = {}
        mapped_fields = self._get_mapped_fields_updated()

        for key, value in venue_data.items():
            if key not in mapped_fields and value is not None and value != "":
                venue_attributes[key] = value

        if venue_attributes:
            venue_record.venue_attributes = venue_attributes

        return venue_record

    def _get_mapped_fields_updated(self) -> set:
        """Get updated list of fields that are mapped to specific columns."""
        return {
            # Use the FIRDS column mapping from constants
            *FirdsTypes.COLUMN_MAPPING.keys(),
            # Additional commonly mapped fields
            "original_firds_record",
            "venue_attributes",
        }

    def _parse_date(self, date_str) -> Optional[datetime]:
        """Parse date string to datetime object."""
        if not date_str or not isinstance(date_str, str):
            return None
        try:
            # Handle various date formats
            if "T" in date_str:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            else:
                return datetime.strptime(date_str, "%Y-%m-%d")
        except (ValueError, AttributeError):
            return None

    def enrich_instrument(
        self, instrument: InstrumentInterface
    ) -> Tuple[Session, InstrumentInterface]:
        """Enrich existing instrument with additional data from external sources."""
        session = SessionLocal()

        try:
            self.logger.info(f"Starting enrichment for instrument {instrument.isin}")

            # Keep instrument bound to this session
            instrument = session.merge(instrument)

            # Enrich with FIGI if not present
            if not instrument.figi_mappings:
                try:
                    self.logger.info("Starting FIGI enrichment...")
                    self._enrich_figi(session, instrument)
                except Exception as e:
                    self.logger.error(f"FIGI enrichment failed: {str(e)}")

            # Check for LEI
            if instrument.lei_id:
                self.logger.info(f"Found LEI {instrument.lei_id} for instrument {instrument.isin}")
                try:
                    self._enrich_legal_entity(session, instrument)
                except Exception as e:
                    self.logger.error(f"Legal entity enrichment failed: {str(e)}")
            else:
                self.logger.warning(f"No LEI found for instrument {instrument.isin}")

            session.commit()
            self.logger.info("Enrichment completed successfully")
            return session, instrument

        except Exception as e:
            self.logger.error(f"Enrichment failed for {instrument.id}: {str(e)}")
            session.rollback()
            raise InstrumentServiceError(f"Enrichment failed: {str(e)}")

    def _enrich_figi(self, session: Session, instrument: InstrumentInterface) -> None:
        """Helper method to handle FIGI enrichment with enhanced OpenFIGI service and multiple FIGI support."""
        from ...database.model_mapper import map_figi_data
        from ...models.sqlite.figi import FigiMapping

        self.logger.debug(f"Starting FIGI enrichment for {instrument.isin}")

        # Check if instrument already has FIGI mappings
        if instrument.figi_mappings:
            self.logger.info(
                f"FIGI mappings already exist for {instrument.isin} ({len(instrument.figi_mappings)} FIGIs)"
            )
            return

        # Use the new enhanced OpenFIGI service
        try:
            from ..openfigi import OpenFIGIService

            openfigi_service = OpenFIGIService()

            # Get MIC code by looking up the operating MIC from relevant_trading_venue
            mic_code = None
            if instrument.relevant_trading_venue:
                from ...models.sqlite.market_identification_code import MarketIdentificationCode
                
                # Look up the MIC record to get the operating MIC
                mic_record = session.query(MarketIdentificationCode).filter(
                    MarketIdentificationCode.mic == instrument.relevant_trading_venue
                ).first()
                
                if mic_record and mic_record.operating_mic:
                    mic_code = mic_record.operating_mic
                    self.logger.info(f"Mapped {instrument.relevant_trading_venue} to operating MIC: {mic_code}")
                elif mic_record:
                    # Use the MIC itself if no operating MIC is set
                    mic_code = mic_record.mic
                    self.logger.info(f"Using MIC directly: {mic_code}")
                else:
                    # Fallback to using relevant_trading_venue as-is
                    mic_code = instrument.relevant_trading_venue
                    self.logger.warning(f"No MIC record found for {instrument.relevant_trading_venue}, using as-is")
            else:
                self.logger.info("No relevant_trading_venue available for MIC lookup")

            if mic_code:
                self.logger.info(f"Using MIC code {mic_code} for enhanced FIGI search")
            else:
                self.logger.info(
                    f"No MIC code available, using ISIN-only search for {instrument.isin}"
                )
                mic_code = ""  # OpenFIGI service expects string, not None

            # Search for FIGIs using the enhanced service - unpack tuple return
            figi_results, search_strategy = openfigi_service.search_figi(instrument.isin, mic_code)

            if figi_results:
                self.logger.info(f"Found {len(figi_results)} FIGI(s) for {instrument.isin} using strategy: {search_strategy}")

                # Convert OpenFIGISearchResult objects to dictionary format for map_figi_data
                figi_data_list = []
                for result in figi_results:
                    figi_data_list.append({
                        "figi": result.figi,
                        "name": result.name,
                        "ticker": result.ticker,
                        "exchCode": result.exch_code,
                        "securityType": result.security_type,
                        "marketSector": result.market_sector,
                        "compositeFIGI": result.composite_figi,
                        "shareClassFIGI": result.share_class_figi,
                        "currency": result.currency,
                        "securityDescription": result.security_description,
                    })

                # Create FIGI mappings for all results
                figi_mappings = map_figi_data(figi_data_list, instrument.isin)
                if figi_mappings:
                    self.logger.info(
                        f"Created {len(figi_mappings)} FIGI mapping(s) for {instrument.isin}"
                    )

                    # Check for existing FIGIs and add only new ones
                    added_count = 0
                    for figi_mapping in figi_mappings:
                        # Check if this FIGI already exists in the database
                        existing_figi = (
                            session.query(FigiMapping)
                            .filter(FigiMapping.figi == figi_mapping.figi)
                            .first()
                        )

                        if existing_figi:
                            self.logger.info(
                                f"FIGI {figi_mapping.figi} already exists for ISIN {existing_figi.isin}, skipping"
                            )
                        else:
                            instrument.figi_mappings.append(figi_mapping)
                            session.add(figi_mapping)
                            added_count += 1

                    self.logger.info(
                        f"Added {added_count} new FIGI mapping(s) for {instrument.isin} (skipped {len(figi_mappings) - added_count} duplicates)"
                    )
                else:
                    self.logger.warning(
                        f"Failed to create FIGI mappings from results: {figi_results}"
                    )
            else:
                self.logger.warning(f"No FIGI data returned for {instrument.isin}")

        except Exception as e:
            self.logger.error(f"Error during FIGI enrichment: {e}")
            # Fallback to old service if new one fails
            self.logger.info("Falling back to original OpenFIGI service...")

            # Get venue records for this ISIN to optimize OpenFIGI search
            try:
                venue_records = (
                    session.query(TradingVenue)
                    .filter(TradingVenue.instrument_id == instrument.id)
                    .all()
                )

                # Convert to format expected by OpenFIGI function
                venue_data = [
                    venue.original_firds_record
                    for venue in venue_records
                    if venue.original_firds_record
                ]

                if venue_data:
                    self.logger.info(
                        f"Using {len(venue_data)} venue records for fallback FIGI search"
                    )
                else:
                    venue_data = None
            except Exception as fallback_e:
                self.logger.warning(f"Failed to get venue data for fallback: {fallback_e}")
                venue_data = None

            # Use enhanced service as final fallback with empty MIC (broad search)
            fallback_results, fallback_strategy = openfigi_service.search_figi(
                instrument.isin, ""
            )

            if fallback_results:
                self.logger.debug(f"Received fallback FIGI data: {len(fallback_results)} results")
                
                # Convert OpenFIGISearchResult objects to dictionary format
                figi_data_list = []
                for result in fallback_results:
                    figi_data_list.append({
                        "figi": result.figi,
                        "name": result.name,
                        "ticker": result.ticker,
                        "exchCode": result.exch_code,
                        "securityType": result.security_type,
                        "marketSector": result.market_sector,
                        "compositeFIGI": result.composite_figi,
                        "shareClassFIGI": result.share_class_figi,
                        "currency": result.currency,
                        "securityDescription": result.security_description,
                    })
                
                figi_mappings = map_figi_data(figi_data_list, instrument.isin)
                if figi_mappings:
                    self.logger.info(
                        f"Created {len(figi_mappings)} FIGI mapping(s) via fallback for {instrument.isin}"
                    )

                    # Check for existing FIGIs and add only new ones
                    added_count = 0
                    for figi_mapping in figi_mappings:
                        # Check if this FIGI already exists in the database
                        existing_figi = (
                            session.query(FigiMapping)
                            .filter(FigiMapping.figi == figi_mapping.figi)
                            .first()
                        )

                        if existing_figi:
                            self.logger.info(
                                f"FIGI {figi_mapping.figi} already exists for ISIN {existing_figi.isin}, skipping"
                            )
                        else:
                            instrument.figi_mappings.append(figi_mapping)
                            session.add(figi_mapping)
                            added_count += 1

                    self.logger.info(
                        f"Added {added_count} new FIGI mapping(s) via fallback for {instrument.isin} (skipped {len(figi_mappings) - added_count} duplicates)"
                    )
                else:
                    self.logger.warning(
                        f"Failed to create FIGI mappings from fallback data: received {len(fallback_results)} results but couldn't map them"
                    )
            else:
                self.logger.warning(f"No FIGI data returned from fallback for {instrument.isin}")

    def _enrich_legal_entity(self, session: Session, instrument: InstrumentInterface) -> None:
        """Helper method to handle legal entity enrichment"""
        from .legal_entity_service import LegalEntityService

        lei_service = LegalEntityService()

        self.logger.info(f"Starting legal entity enrichment for LEI: {instrument.lei_id}")

        lei_session, entity = lei_service.create_or_update_entity(instrument.lei_id)
        try:
            if entity:
                self.logger.info(f"Found legal entity data for LEI {instrument.lei_id}")
                entity = session.merge(entity)
                instrument.legal_entity = entity
                session.flush()
            else:
                self.logger.warning(f"No legal entity data found for LEI {instrument.lei_id}")
        finally:
            if lei_session:
                lei_session.close()

    # Implement required interface methods for backward compatibility
    def get_instruments(
        self, limit: int = 100, offset: int = 0, instrument_type: Optional[str] = None
    ) -> List[InstrumentInterface]:
        """Get a list of instruments with pagination."""
        with get_session() as session:
            query = session.query(Instrument)
            if instrument_type:
                query = query.filter(Instrument.instrument_type == instrument_type)
            return query.offset(offset).limit(limit).all()

    def update_instrument(
        self, identifier: str, data: Dict[str, Any]
    ) -> Optional[InstrumentInterface]:
        """Update an existing instrument."""
        session = SessionLocal()
        try:
            instrument = (
                session.query(Instrument)
                .filter((Instrument.id == identifier) | (Instrument.isin == identifier))
                .first()
            )
            if not instrument:
                return None

            # Update core fields
            for key, value in data.items():
                if hasattr(instrument, key):
                    setattr(instrument, key, value)

            # Update timestamp
            instrument.updated_at = datetime.now(UTC)

            session.commit()
            session.refresh(instrument)
            return instrument
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_instrument(self, identifier: str, cascade: bool = False) -> bool:
        """Delete an instrument by ISIN or ID, optionally with cascade deletion of related data."""
        with get_session() as session:
            try:
                # Try to find by ISIN first, then by ID
                instrument = session.query(Instrument).filter(Instrument.isin == identifier).first()
                if not instrument:
                    instrument = session.query(Instrument).filter(Instrument.id == identifier).first()
                
                if not instrument:
                    return False
                
                if cascade:
                    # Delete related data manually to ensure proper cleanup
                    from marketdata_api.models.sqlite.instrument import TradingVenue
                    from marketdata_api.models.sqlite.figi import FigiMapping
                    from marketdata_api.models.sqlite.transparency import TransparencyCalculation
                    
                    # Delete trading venues
                    session.query(TradingVenue).filter(TradingVenue.instrument_id == instrument.id).delete()
                    
                    # Delete FIGI mappings
                    session.query(FigiMapping).filter(FigiMapping.instrument_id == instrument.id).delete()
                    
                    # Delete transparency calculations
                    session.query(TransparencyCalculation).filter(TransparencyCalculation.instrument_id == instrument.id).delete()
                    
                    # Legal entity is handled by foreign key relationship
                
                # Delete the instrument itself
                session.delete(instrument)
                session.commit()
                return True
                
            except Exception as e:
                session.rollback()
                raise e

    def search_instruments(self, query: str, limit: int = 100) -> List[InstrumentInterface]:
        """Search instruments by name, symbol, or ISIN."""
        with get_session() as session:
            return (
                session.query(Instrument)
                .filter(
                    (Instrument.full_name.ilike(f"%{query}%"))
                    | (Instrument.short_name.ilike(f"%{query}%"))
                    | (Instrument.isin.ilike(f"%{query}%"))
                )
                .limit(limit)
                .all()
            )

    def validate_instrument_data(self, data: Dict[str, Any]) -> None:
        """Validate instrument data."""
        if not data.get("isin"):
            raise ValueError("Instrument must have ISIN")

    def validate_instrument_identifier(self, identifier: str) -> None:
        """Validate instrument identifier (ISIN)"""
        if not identifier or not isinstance(identifier, str):
            raise ValueError("Instrument identifier must be a non-empty string")
        if len(identifier) != 12:
            raise ValueError("ISIN must be 12 characters long")

    def create_instruments_bulk(
        self,
        jurisdiction: str = "SE",
        instrument_type: str = "equity",
        limit: Optional[int] = None,
        skip_existing: bool = True,
        enable_enrichment: bool = True,
        batch_size: int = 10,
    ) -> Dict[str, Any]:
        """
        Create multiple instruments in bulk with filtering and performance optimization.

        Args:
            jurisdiction: Filter by competent authority jurisdiction (default: "SE" for Sweden)
            instrument_type: Target instrument type to create (default: "equity")
            limit: Maximum number of instruments to create (None = no limit)
            skip_existing: Skip instruments already in database (default: True)
            enable_enrichment: Enable FIGI/LEI enrichment (default: True)
            batch_size: Number of instruments to process per batch (default: 10)

        Returns:
            Dict with creation results and statistics
        """
        start_time = time.time()
        results = {
            "total_found": 0,
            "total_created": 0,
            "total_skipped": 0,
            "total_failed": 0,
            "failed_instruments": [],
            "created_instruments": [],
            "batch_results": [],
            "elapsed_time": 0,
        }

        try:
            self.logger.info(f"🚀 Starting bulk instrument creation")
            self.logger.info(f"   Jurisdiction filter: {jurisdiction}")
            self.logger.info(f"   Instrument type: {instrument_type}")
            self.logger.info(f"   Limit: {limit or 'No limit'}")
            self.logger.info(f"   Skip existing: {skip_existing}")
            self.logger.info(f"   Enrichment: {enable_enrichment}")
            self.logger.info(f"   Batch size: {batch_size}")

            # Get ISINs matching the filters from FIRDS files
            isins_to_process = self._get_filtered_isins_from_firds(
                jurisdiction=jurisdiction, instrument_type=instrument_type, limit=limit
            )

            if not isins_to_process:
                self.logger.warning(f"❌ No instruments found matching filters")
                return results

            results["total_found"] = len(isins_to_process)
            self.logger.info(f"📊 Found {len(isins_to_process)} instruments matching filters")

            # Filter out existing instruments if requested
            if skip_existing:
                isins_to_process = self._filter_existing_instruments(isins_to_process)
                self.logger.info(
                    f"📊 After filtering existing: {len(isins_to_process)} instruments to create"
                )

            # Process in batches for better performance and error handling
            total_batches = (len(isins_to_process) + batch_size - 1) // batch_size

            for batch_idx in range(total_batches):
                batch_start_idx = batch_idx * batch_size
                batch_end_idx = min(batch_start_idx + batch_size, len(isins_to_process))
                batch_isins = isins_to_process[batch_start_idx:batch_end_idx]

                batch_start_time = time.time()
                self.logger.info(
                    f"🔄 Processing batch {batch_idx + 1}/{total_batches} ({len(batch_isins)} instruments)"
                )

                batch_result = self._process_instrument_batch(
                    batch_isins, instrument_type, enable_enrichment
                )

                # Update overall results
                results["total_created"] += batch_result["created"]
                results["total_failed"] += batch_result["failed"]
                results["failed_instruments"].extend(batch_result["failed_instruments"])
                results["created_instruments"].extend(batch_result["created_instruments"])

                batch_elapsed = time.time() - batch_start_time
                batch_result["elapsed_time"] = batch_elapsed
                results["batch_results"].append(batch_result)

                self.logger.info(
                    f"✅ Batch {batch_idx + 1} completed: {batch_result['created']} created, {batch_result['failed']} failed ({batch_elapsed:.1f}s)"
                )

                # Progress update
                total_processed = results["total_created"] + results["total_failed"]
                progress_pct = (total_processed / len(isins_to_process)) * 100
                self.logger.info(
                    f"📈 Overall progress: {total_processed}/{len(isins_to_process)} ({progress_pct:.1f}%)"
                )

            results["elapsed_time"] = time.time() - start_time

            # Final summary
            self.logger.info(f"🎉 Bulk creation completed!")
            self.logger.info(f"   Total found: {results['total_found']}")
            self.logger.info(f"   Total created: {results['total_created']}")
            self.logger.info(f"   Total failed: {results['total_failed']}")
            self.logger.info(f"   Total time: {results['elapsed_time']:.1f}s")

            if results["total_created"] > 0:
                avg_time = results["elapsed_time"] / results["total_created"]
                self.logger.info(f"   Average per instrument: {avg_time:.1f}s")

            return results

        except Exception as e:
            results["elapsed_time"] = time.time() - start_time
            self.logger.error(f"💥 Bulk creation failed: {str(e)}")
            raise InstrumentServiceError(f"Bulk creation failed: {str(e)}") from e

    def _get_filtered_isins_from_firds(
        self, jurisdiction: str, instrument_type: str, limit: Optional[int] = None
    ) -> List[str]:
        """Get ISINs from FIRDS files matching the specified filters."""
        try:
            from pathlib import Path

            import pandas as pd

            self.logger.info(
                f"🔍 Scanning FIRDS files for {jurisdiction} {instrument_type} instruments..."
            )

            firds_path = Path(esmaConfig.firds_path)
            if not firds_path.exists():
                raise InstrumentServiceError(f"FIRDS path does not exist: {firds_path}")

            # Use CFI manager for consistent business type to FIRDS type mapping
            # Reverse lookup: business type -> FIRDS letter
            business_to_firds = {}
            for firds_letter, category in CFIInstrumentTypeManager.FIRDS_TO_CFI_MAPPING.items():
                business_type = CFIInstrumentTypeManager.CFI_TO_BUSINESS_TYPE.get(category)
                if business_type:
                    business_to_firds[business_type] = firds_letter

            firds_type = business_to_firds.get(instrument_type, "E")
            self.logger.info(f"🎯 Mapped {instrument_type} → FIRDS type {firds_type}")

            # Find matching files
            file_pattern = f"*FULINS_{firds_type}*_firds_data.csv"
            matching_files = list(firds_path.glob(file_pattern))

            if not matching_files:
                self.logger.warning(f"❌ No FIRDS files found for type {firds_type}")
                return []

            self.logger.info(f"📁 Found {len(matching_files)} FIRDS files for type {firds_type}")

            # Collect ISINs from all files
            all_isins = set()

            for file_idx, file_path in enumerate(matching_files, 1):
                try:
                    self.logger.info(
                        f"📄 [{file_idx}/{len(matching_files)}] Processing {file_path.name}..."
                    )

                    # Read with jurisdiction filter
                    df = pd.read_csv(
                        str(file_path),
                        dtype=str,
                        low_memory=False,
                        usecols=["Id", "TechAttrbts_RlvntCmptntAuthrty"],
                    )

                    if df is not None and not df.empty:
                        # Filter by jurisdiction
                        jurisdiction_filtered = df[
                            df["TechAttrbts_RlvntCmptntAuthrty"] == jurisdiction
                        ]

                        if not jurisdiction_filtered.empty:
                            file_isins = set(jurisdiction_filtered["Id"].dropna().unique())
                            all_isins.update(file_isins)
                            self.logger.info(
                                f"   ✅ Found {len(file_isins)} {jurisdiction} ISINs in {file_path.name}"
                            )
                        else:
                            self.logger.debug(f"   ⚪ No {jurisdiction} ISINs in {file_path.name}")

                except Exception as e:
                    self.logger.warning(f"   💥 Error processing {file_path.name}: {str(e)}")
                    continue

            isin_list = list(all_isins)

            # Apply limit if specified
            if limit and len(isin_list) > limit:
                isin_list = isin_list[:limit]
                self.logger.info(
                    f"🔢 Applied limit: {limit} ISINs selected from {len(all_isins)} total"
                )

            self.logger.info(f"✅ Collection complete: {len(isin_list)} ISINs ready for processing")
            return isin_list

        except Exception as e:
            self.logger.error(f"💥 Error collecting ISINs from FIRDS: {str(e)}")
            raise

    def _filter_existing_instruments(self, isins: List[str]) -> List[str]:
        """Remove ISINs that already exist in the database."""
        try:
            session = SessionLocal()

            try:
                # Query existing ISINs in batches for performance
                batch_size = 1000
                existing_isins = set()

                for i in range(0, len(isins), batch_size):
                    batch = isins[i : i + batch_size]
                    existing_batch = (
                        session.query(Instrument.isin).filter(Instrument.isin.in_(batch)).all()
                    )
                    existing_isins.update([isin for (isin,) in existing_batch])

                filtered_isins = [isin for isin in isins if isin not in existing_isins]

                self.logger.info(f"🔍 Filtering existing instruments:")
                self.logger.info(f"   Total ISINs: {len(isins)}")
                self.logger.info(f"   Already exist: {len(existing_isins)}")
                self.logger.info(f"   To create: {len(filtered_isins)}")

                return filtered_isins

            finally:
                session.close()

        except Exception as e:
            self.logger.error(f"💥 Error filtering existing instruments: {str(e)}")
            return isins  # Return all if filtering fails

    def _process_instrument_batch(
        self, isins: List[str], instrument_type: str, enable_enrichment: bool
    ) -> Dict[str, Any]:
        """Process a batch of instruments with error handling."""
        batch_result = {
            "created": 0,
            "failed": 0,
            "failed_instruments": [],
            "created_instruments": [],
        }

        for isin in isins:
            try:
                self.logger.debug(f"   🔨 Creating {isin}...")

                # Create instrument (enrichment is handled inside create_instrument)
                if enable_enrichment:
                    instrument = self.create_instrument(isin, instrument_type)
                else:
                    # Create without enrichment (would need separate method)
                    instrument = self.create_instrument(isin, instrument_type)

                if instrument:
                    batch_result["created"] += 1
                    batch_result["created_instruments"].append(isin)
                    self.logger.debug(f"   ✅ Created {isin}")
                else:
                    batch_result["failed"] += 1
                    batch_result["failed_instruments"].append(
                        {"isin": isin, "error": "Creation returned None"}
                    )
                    self.logger.warning(f"   ❌ Failed to create {isin}: No instrument returned")

            except Exception as e:
                batch_result["failed"] += 1
                error_msg = str(e)
                batch_result["failed_instruments"].append({"isin": isin, "error": error_msg})
                self.logger.warning(f"   ❌ Failed to create {isin}: {error_msg}")

        return batch_result
