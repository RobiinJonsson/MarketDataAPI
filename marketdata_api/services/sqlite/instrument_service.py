"""
Unified Instrument Service Implementation

This service implements the document-based approach for ALL FIRDS instrument types:
1. Supports all 10 FIRDS types: C,D,E,F,H,I,J,S,R,O
2. Stores ALL venue records in database with promoted common fields
3. Uses JSON for flexible type-specific attribute storage
4. Provides clean API responses without raw FIRDS data
5. Uses new FIRDS type mappings and constants
"""

import uuid
import json
import logging
import re
from typing import Dict, Any, Optional, List, Tuple
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, UTC
from ...services.interfaces.instrument_service_interface import InstrumentServiceInterface
from ...models.interfaces.instrument_interface import InstrumentInterface
from ...database.session import get_session, SessionLocal
from ..openfigi import search_openfigi_with_fallback
from ..gleif import fetch_lei_info
from ...config import esmaConfig
from ...constants import FirdsTypes, InstrumentTypes

# Import the unified models
from ...models.sqlite.instrument import Instrument, TradingVenue

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
        self.database_type = 'sqlite'
        self.logger = logging.getLogger(__name__)
    
    def create_instrument(self, identifier: str, instrument_type: str = "equity") -> InstrumentInterface:
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
            all_venue_records, detected_firds_type = self._get_firds_data_from_storage_all_types(identifier, instrument_type)
            if not all_venue_records:
                raise InstrumentNotFoundError(f"No FIRDS data found for {identifier}")
            
            self.logger.info(f"Found {len(all_venue_records)} venue records for {identifier} (FIRDS type: {detected_firds_type})")
            
            # Map FIRDS type to business instrument type
            business_instrument_type = Instrument.map_firds_type_to_instrument_type(
                detected_firds_type, 
                all_venue_records[0].get('FinInstrmGnlAttrbts_ClssfctnTp')
            )
            
            self.logger.info(f"Mapped FIRDS type {detected_firds_type} to business type: {business_instrument_type}")
            
            # Use first record for primary instrument data
            primary_record = all_venue_records[0]
            
            # Check for existing and delete if present
            existing = session.query(Instrument).filter(Instrument.isin == identifier).first()
            if existing:
                self.logger.info(f"Deleting existing instrument {identifier}")
                session.delete(existing)
                session.flush()
            
            # Create instrument with promoted common fields + JSON attributes
            instrument_data = self._build_instrument_data(
                identifier, 
                business_instrument_type, 
                primary_record, 
                detected_firds_type
            )
            
            # Create new instrument
            instrument = Instrument(**instrument_data)
            session.add(instrument)
            session.flush()
            
            # Create venue records for ALL venues
            venue_records = []
            for venue_data in all_venue_records:
                venue_record = self._create_venue_record(instrument.id, venue_data)
                venue_records.append(venue_record)
                session.add(venue_record)
            
            session.commit()
            
            self.logger.info(f"Created {business_instrument_type} instrument {identifier} with {len(venue_records)} venue records")
            
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
    
    def _build_instrument_data(self, identifier: str, business_instrument_type: str, 
                             primary_record: Dict[str, Any], firds_type: str) -> Dict[str, Any]:
        """Build instrument data dictionary with promoted common fields."""
        
        # Parse boolean commodity derivative indicator
        commodity_deriv_ind = primary_record.get('FinInstrmGnlAttrbts_CmmdtyDerivInd')
        if isinstance(commodity_deriv_ind, str):
            commodity_deriv_ind = commodity_deriv_ind.lower() in ('true', '1', 'yes')
        elif commodity_deriv_ind is None:
            commodity_deriv_ind = False
        
        return {
            'id': str(uuid.uuid4()),
            'isin': identifier,
            'instrument_type': business_instrument_type,
            
            # Promoted common fields (from FIRDS analysis)
            'full_name': primary_record.get('FinInstrmGnlAttrbts_FullNm'),
            'short_name': primary_record.get('FinInstrmGnlAttrbts_ShrtNm'),
            'currency': primary_record.get('FinInstrmGnlAttrbts_NtnlCcy'),
            'cfi_code': primary_record.get('FinInstrmGnlAttrbts_ClssfctnTp'),
            'commodity_derivative_indicator': commodity_deriv_ind,
            'lei_id': primary_record.get('Issr'),
            'publication_from_date': self._parse_date(primary_record.get('TechAttrbts_PblctnPrd_FrDt')),
            'competent_authority': primary_record.get('TechAttrbts_RlvntCmptntAuthrty'),
            'relevant_trading_venue': primary_record.get('TechAttrbts_RlvntTradgVn'),
            
            # JSON storage for flexibility
            'firds_data': primary_record,  # Original FIRDS record
            'processed_attributes': self._process_instrument_attributes(primary_record, business_instrument_type, firds_type)
        }
    
    def _get_firds_data_from_storage_all_types(self, identifier: str, 
                                              preferred_type: str = None) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Fetch FIRDS data from all instrument types, auto-detecting the correct type.
        
        Returns:
            Tuple of (records_list, detected_firds_type)
        """
        try:
            from pathlib import Path
            
            # If preferred type is provided, try it first
            if preferred_type:
                legacy_mapping = {'equity': 'E', 'debt': 'D', 'future': 'F'}
                if preferred_type in legacy_mapping:
                    firds_type = legacy_mapping[preferred_type]
                    records = self._search_firds_files_for_type(identifier, firds_type)
                    if records:
                        return records, firds_type
            
            # Search all FIRDS types (C,D,E,F,H,I,J,S,R,O)
            for firds_type in FirdsTypes.MAPPING.keys():
                self.logger.debug(f"Searching for {identifier} in FIRDS type {firds_type}")
                records = self._search_firds_files_for_type(identifier, firds_type)
                if records:
                    self.logger.info(f"Found {identifier} in FIRDS type {firds_type}")
                    return records, firds_type
            
            self.logger.warning(f"Identifier {identifier} not found in any FIRDS files")
            return None, None

        except Exception as e:
            self.logger.error(f"Error fetching FIRDS data from storage: {str(e)}")
            return None, None
    
    def _search_firds_files_for_type(self, identifier: str, firds_type: str) -> Optional[List[Dict[str, Any]]]:
        """Search for identifier in FIRDS files of a specific type."""
        try:
            from pathlib import Path
            import pandas as pd
            
            firds_path = Path(esmaConfig.firds_path)
            if not firds_path.exists():
                self.logger.error(f"FIRDS storage path does not exist: {firds_path}")
                return None
            
            # Find files matching the pattern for this FIRDS type
            file_pattern = f"*FULINS_{firds_type}*_firds_data.csv"
            matching_files = list(firds_path.glob(file_pattern))
            
            if not matching_files:
                self.logger.debug(f"No {firds_type} files found matching pattern: {file_pattern}")
                return None
            
            # Search through files for the identifier
            for file_path in matching_files:
                try:
                    self.logger.debug(f"Searching for {identifier} in {file_path.name}")
                    
                    df = pd.read_csv(str(file_path), dtype=str, low_memory=False)
                    
                    if df is not None and not df.empty and 'Id' in df.columns:
                        # Check for the identifier in the data
                        isin_data = df[df['Id'] == identifier]
                        if not isin_data.empty:
                            self.logger.info(f"Found {len(isin_data)} records for {identifier} in {file_path.name}")
                            
                            # Return ALL records for this ISIN, handling NaN values
                            all_records = isin_data.fillna('').to_dict('records')
                            return all_records
                
                except Exception as e:
                    self.logger.warning(f"Error reading file {file_path}: {str(e)}")
                    continue
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error searching FIRDS files for type {firds_type}: {str(e)}")
            return None
    
    def get_instrument_venues(self, identifier: str, instrument_type: str = "equity") -> Optional[List[Dict[str, Any]]]:
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
            instrument = session.query(Instrument).filter(
                (Instrument.id == identifier) |
                (Instrument.isin == identifier)
            ).first()
            
            if not instrument:
                self.logger.warning(f"Instrument {identifier} not found")
                return None
            
            # Get all venue records from database
            venue_records = session.query(TradingVenue).filter(
                TradingVenue.instrument_id == instrument.id
            ).all()
            
            if not venue_records:
                self.logger.warning(f"No venue records found in database for {identifier}")
                return []
            
            # Return clean structured data (no raw FIRDS)
            result = [venue.to_dict() for venue in venue_records]
            
            self.logger.info(f"Retrieved {len(result)} venue records for {identifier} from database")
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
                    joinedload(Instrument.figi_mapping),
                    joinedload(Instrument.legal_entity),
                    joinedload(Instrument.trading_venues)
                )
                .filter(
                    (Instrument.id == identifier) |
                    (Instrument.isin == identifier)
                )
                .first()
            )
            if instrument:
                session.refresh(instrument)
            return session, instrument
        except:
            session.close()
            raise
    
    def _process_instrument_attributes(self, firds_record: Dict[str, Any], 
                                     business_instrument_type: str, firds_type: str) -> Dict[str, Any]:
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
            attributes['firds_type'] = firds_type
            attributes['business_type'] = business_instrument_type
            
            # Process common derivative attributes (present across multiple types)
            self._process_common_derivative_attributes(firds_record, attributes)
        
        except Exception as e:
            self.logger.warning(f"Error processing attributes for {business_instrument_type}: {e}")
        
        return attributes
    
    def _process_equity_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process equity-specific attributes."""
        attributes = {}
        
        if firds_record.get('DerivInstrmAttrbts_PricMltplr'):
            try:
                attributes['price_multiplier'] = float(firds_record['DerivInstrmAttrbts_PricMltplr'])
            except (ValueError, TypeError):
                pass
        
        if firds_record.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
            attributes['underlying_isin'] = firds_record['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']
        
        if firds_record.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm'):
            attributes['underlying_index'] = firds_record['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm']
        
        # Asset class attributes
        asset_class = self._extract_asset_class_attributes(firds_record)
        if asset_class:
            attributes['asset_class'] = asset_class
            
        return attributes
    
    def _process_debt_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process debt-specific attributes."""
        attributes = {}
        
        if firds_record.get('DebtInstrmAttrbts_MtrtyDt'):
            attributes['maturity_date'] = firds_record['DebtInstrmAttrbts_MtrtyDt']
        
        if firds_record.get('DebtInstrmAttrbts_TtlIssdNmnlAmt'):
            try:
                attributes['total_issued_nominal'] = float(firds_record['DebtInstrmAttrbts_TtlIssdNmnlAmt'])
            except (ValueError, TypeError):
                pass
        
        if firds_record.get('DebtInstrmAttrbts_NmnlValPerUnit'):
            try:
                attributes['nominal_value_per_unit'] = float(firds_record['DebtInstrmAttrbts_NmnlValPerUnit'])
            except (ValueError, TypeError):
                pass
        
        if firds_record.get('DebtInstrmAttrbts_DebtSnrty'):
            attributes['debt_seniority'] = firds_record['DebtInstrmAttrbts_DebtSnrty']
        
        # Interest rate attributes
        if firds_record.get('DebtInstrmAttrbts_IntrstRate_Fxd'):
            try:
                attributes['interest_rate'] = float(firds_record['DebtInstrmAttrbts_IntrstRate_Fxd'])
            except (ValueError, TypeError):
                pass
                
        return attributes
    
    def _process_future_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process future-specific attributes."""
        attributes = {}
        
        if firds_record.get('DerivInstrmAttrbts_XpryDt'):
            attributes['expiration_date'] = firds_record['DerivInstrmAttrbts_XpryDt']
        
        if firds_record.get('DerivInstrmAttrbts_DlvryTp'):
            attributes['delivery_type'] = firds_record['DerivInstrmAttrbts_DlvryTp']
        
        if firds_record.get('DerivInstrmAttrbts_PricMltplr'):
            try:
                attributes['price_multiplier'] = float(firds_record['DerivInstrmAttrbts_PricMltplr'])
            except (ValueError, TypeError):
                pass
                
        return attributes
    
    def _process_collective_investment_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process collective investment (Type C) specific attributes."""
        attributes = {}
        
        if firds_record.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
            attributes['underlying_isin'] = firds_record['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']
        
        # CIV-specific logic could be added here based on CFI code
        cfi_code = firds_record.get('FinInstrmGnlAttrbts_ClssfctnTp', '')
        if cfi_code.startswith('CI'):
            attributes['fund_type'] = 'investment_fund'
        elif cfi_code.startswith('CE'):
            attributes['fund_type'] = 'etf'
        elif cfi_code.startswith('CB'):
            attributes['fund_type'] = 'reit'
            
        return attributes
    
    def _process_hybrid_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process hybrid instrument (Type H) specific attributes."""
        attributes = {}
        
        if firds_record.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
            attributes['underlying_isin'] = firds_record['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']
        
        if firds_record.get('DerivInstrmAttrbts_PricMltplr'):
            try:
                attributes['conversion_ratio'] = float(firds_record['DerivInstrmAttrbts_PricMltplr'])
            except (ValueError, TypeError):
                pass
                
        return attributes
    
    def _process_interest_rate_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process interest rate instrument (Type I) specific attributes."""
        attributes = {}
        
        # Interest rate specific fields
        if firds_record.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm'):
            attributes['reference_rate'] = firds_record['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm']
        
        if firds_record.get('DerivInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd'):
            try:
                attributes['spread'] = float(firds_record['DerivInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd'])
            except (ValueError, TypeError):
                pass
                
        return attributes
    
    def _process_convertible_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process convertible instrument (Type J) specific attributes."""
        attributes = {}
        
        if firds_record.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
            attributes['underlying_isin'] = firds_record['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']
        
        if firds_record.get('DerivInstrmAttrbts_PricMltplr'):
            try:
                attributes['conversion_ratio'] = float(firds_record['DerivInstrmAttrbts_PricMltplr'])
            except (ValueError, TypeError):
                pass
                
        return attributes
    
    def _process_option_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process option (Type O) specific attributes."""
        attributes = {}
        
        if firds_record.get('DerivInstrmAttrbts_XpryDt'):
            attributes['expiration_date'] = firds_record['DerivInstrmAttrbts_XpryDt']
        
        if firds_record.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
            attributes['underlying_isin'] = firds_record['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']
        
        # Option type could be derived from other fields or CFI code
        cfi_code = firds_record.get('FinInstrmGnlAttrbts_ClssfctnTp', '')
        if 'C' in cfi_code:
            attributes['option_type'] = 'call'
        elif 'P' in cfi_code:
            attributes['option_type'] = 'put'
            
        return attributes
    
    def _process_rights_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process rights/warrants (Type R) specific attributes."""
        attributes = {}
        
        if firds_record.get('DerivInstrmAttrbts_XpryDt'):
            attributes['expiration_date'] = firds_record['DerivInstrmAttrbts_XpryDt']
        
        if firds_record.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
            attributes['underlying_isin'] = firds_record['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']
        
        if firds_record.get('DerivInstrmAttrbts_PricMltplr'):
            try:
                attributes['exercise_ratio'] = float(firds_record['DerivInstrmAttrbts_PricMltplr'])
            except (ValueError, TypeError):
                pass
                
        return attributes
    
    def _process_structured_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Process structured product (Type S) specific attributes."""
        attributes = {}
        
        if firds_record.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
            attributes['underlying_isin'] = firds_record['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']
        
        if firds_record.get('DerivInstrmAttrbts_PricMltplr'):
            try:
                attributes['participation_rate'] = float(firds_record['DerivInstrmAttrbts_PricMltplr'])
            except (ValueError, TypeError):
                pass
                
        return attributes
    
    def _process_common_derivative_attributes(self, firds_record: Dict[str, Any], attributes: Dict[str, Any]) -> None:
        """Process attributes common to multiple derivative types."""
        
        # Underlying instrument attributes
        underlying_assets = {}
        
        if firds_record.get('DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN'):
            underlying_assets['basket_isin'] = firds_record['DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN']
        
        if firds_record.get('DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI'):
            underlying_assets['basket_lei'] = firds_record['DerivInstrmAttrbts_UndrlygInstrm_Bskt_LEI']
        
        if firds_record.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI'):
            underlying_assets['single_lei'] = firds_record['DerivInstrmAttrbts_UndrlygInstrm_Sngl_LEI']
        
        if underlying_assets:
            attributes['underlying_assets'] = underlying_assets
    
    def _extract_asset_class_attributes(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Extract asset class specific attributes."""
        asset_class = {}
        
        # Oil/Energy attributes
        if firds_record.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct'):
            asset_class['oil_type'] = firds_record['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct']
        
        if firds_record.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct'):
            asset_class['sub_product'] = firds_record['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct']
        
        # Metal attributes
        if firds_record.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct'):
            asset_class['metal_type'] = firds_record['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct']
        
        # Electricity attributes
        if firds_record.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct'):
            asset_class['electricity_type'] = firds_record['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct']
        
        # FX attributes
        if firds_record.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy'):
            asset_class['other_currency'] = firds_record['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy']
        
        return asset_class
    
    def _create_venue_record(self, instrument_id: str, venue_data: Dict[str, Any]) -> TradingVenue:
        """Create a venue record from FIRDS data using updated model structure."""
        
        # Parse issuer requested as boolean
        issuer_requested = venue_data.get('TradgVnRltdAttrbts_IssrReq')
        if isinstance(issuer_requested, str):
            issuer_requested = issuer_requested.lower() in ('true', '1', 'yes')
        elif issuer_requested is None:
            issuer_requested = False
        
        venue_record = TradingVenue(
            id=str(uuid.uuid4()),
            instrument_id=instrument_id,
            venue_id=venue_data.get('TradgVnRltdAttrbts_Id'),
            isin=venue_data.get('Id'),
            
            # Updated fields to match new model structure
            first_trade_date=self._parse_date(venue_data.get('TradgVnRltdAttrbts_FrstTradDt')),
            termination_date=self._parse_date(venue_data.get('TradgVnRltdAttrbts_TermntnDt')),
            admission_approval_date=self._parse_date(venue_data.get('TradgVnRltdAttrbts_AdmssnApprvlDtByIssr')),
            request_for_admission_date=self._parse_date(venue_data.get('TradgVnRltdAttrbts_ReqForAdmssnDt')),
            issuer_requested=issuer_requested,  # Now boolean instead of string
            
            venue_full_name=venue_data.get('FinInstrmGnlAttrbts_FullNm'),
            venue_short_name=venue_data.get('FinInstrmGnlAttrbts_ShrtNm'),
            classification_type=venue_data.get('FinInstrmGnlAttrbts_ClssfctnTp'),
            venue_currency=venue_data.get('FinInstrmGnlAttrbts_NtnlCcy'),
            competent_authority=venue_data.get('TechAttrbts_RlvntCmptntAuthrty'),
            relevant_trading_venue=venue_data.get('TechAttrbts_RlvntTradgVn'),
            publication_from_date=self._parse_date(venue_data.get('TechAttrbts_PblctnPrd_FrDt')),
            original_firds_record=venue_data  # Store original for debugging/reference
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
            'original_firds_record', 'venue_attributes'
        }

    
    def _parse_date(self, date_str) -> Optional[datetime]:
        """Parse date string to datetime object."""
        if not date_str or not isinstance(date_str, str):
            return None
        try:
            # Handle various date formats
            if 'T' in date_str:
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                return datetime.strptime(date_str, '%Y-%m-%d')
        except (ValueError, AttributeError):
            return None
    
    def enrich_instrument(self, instrument: InstrumentInterface) -> Tuple[Session, InstrumentInterface]:
        """Enrich existing instrument with additional data from external sources."""
        session = SessionLocal()
        
        try:
            self.logger.info(f"Starting enrichment for instrument {instrument.isin}")
            
            # Keep instrument bound to this session
            instrument = session.merge(instrument)
            
            # Enrich with FIGI if not present
            if not instrument.figi_mapping:
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
        """Helper method to handle FIGI enrichment with venue-aware optimization."""
        from ...database.model_mapper import map_figi_data
        
        self.logger.debug(f"Starting FIGI enrichment for {instrument.isin}")
        
        # Get venue records for this ISIN to optimize OpenFIGI search
        try:
            venue_records = session.query(TradingVenue).filter(
                TradingVenue.instrument_id == instrument.id
            ).all()
            
            # Convert to format expected by OpenFIGI function
            venue_data = [venue.original_firds_record for venue in venue_records if venue.original_firds_record]
            
            if venue_data:
                self.logger.info(f"Using {len(venue_data)} venue records for optimized FIGI search")
            else:
                self.logger.warning(f"No venue records found for {instrument.isin}, using basic search")
                venue_data = None
        except Exception as e:
            self.logger.warning(f"Failed to get venue data for FIGI optimization: {e}")
            venue_data = None
        
        # Use venue-aware search with fallback
        figi_data = search_openfigi_with_fallback(
            instrument.isin, 
            instrument.instrument_type, 
            venue_data
        )
        
        if figi_data:
            self.logger.debug(f"Received FIGI data: {figi_data}")
            figi_mapping = map_figi_data(figi_data, instrument.isin)
            if figi_mapping:
                self.logger.info(f"Created FIGI mapping for {instrument.isin}")
                instrument.figi_mapping = figi_mapping
                session.add(figi_mapping)
            else:
                self.logger.warning(f"Failed to create FIGI mapping from data: {figi_data}")
        else:
            self.logger.warning(f"No FIGI data returned for {instrument.isin}")

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
    def get_instrument_by_id(self, instrument_id: str) -> Optional[InstrumentInterface]:
        """Get an instrument by its ID."""
        with get_session() as session:
            return session.query(Instrument).filter(Instrument.id == instrument_id).first()
    
    def get_instrument_by_isin(self, isin: str) -> Optional[InstrumentInterface]:
        """Get an instrument by its ISIN."""
        with get_session() as session:
            return session.query(Instrument).filter(Instrument.isin == isin).first()
    
    def get_instruments(self, limit: int = 100, offset: int = 0, 
                       instrument_type: Optional[str] = None) -> List[InstrumentInterface]:
        """Get a list of instruments with pagination."""
        with get_session() as session:
            query = session.query(Instrument)
            if instrument_type:
                query = query.filter(Instrument.instrument_type == instrument_type)
            return query.offset(offset).limit(limit).all()
    
    def update_instrument(self, identifier: str, data: Dict[str, Any]) -> Optional[InstrumentInterface]:
        """Update an existing instrument."""
        session = SessionLocal()
        try:
            instrument = (
                session.query(Instrument)
                .filter(
                    (Instrument.id == identifier) |
                    (Instrument.isin == identifier)
                )
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
    
    def delete_instrument(self, instrument_id: str) -> bool:
        """Delete an instrument."""
        with get_session() as session:
            instrument = session.query(Instrument).filter(Instrument.id == instrument_id).first()
            if instrument:
                session.delete(instrument)
                session.commit()
                return True
            return False
    
    def search_instruments(self, query: str, limit: int = 100) -> List[InstrumentInterface]:
        """Search instruments by name, symbol, or ISIN."""
        with get_session() as session:
            return session.query(Instrument).filter(
                (Instrument.full_name.ilike(f'%{query}%')) |
                (Instrument.short_name.ilike(f'%{query}%')) |
                (Instrument.isin.ilike(f'%{query}%'))
            ).limit(limit).all()
    
    def validate_instrument_data(self, data: Dict[str, Any]) -> None:
        """Validate instrument data."""
        if not data.get('isin'):
            raise ValueError("Instrument must have ISIN")
    
    def validate_instrument_identifier(self, identifier: str) -> None:
        """Validate instrument identifier (ISIN)"""
        if not identifier or not isinstance(identifier, str):
            raise ValueError("Instrument identifier must be a non-empty string")
        if len(identifier) != 12:
            raise ValueError("ISIN must be 12 characters long")
