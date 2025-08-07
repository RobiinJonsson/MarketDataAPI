"""
Unified Instrument Service Implementation

This service implements the new document-based approach:
1. Stores ALL venue records in database
2. Uses JSON for flexible attribute storage
3. Provides clean API responses without raw FIRDS data
4. Much simpler than the polymorphic inheritance approach
"""

import uuid
import json
import logging
from typing import Dict, Any, Optional, List, Tuple
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, UTC
from ...services.interfaces.instrument_service_interface import InstrumentServiceInterface
from ...models.interfaces.instrument_interface import InstrumentInterface
from ...database.session import get_session, SessionLocal
from ..openfigi import search_openfigi_with_fallback
from ..gleif import fetch_lei_info
from ...config import esmaConfig

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
        Create instrument and store ALL venue records in database.
        
        NEW BEHAVIOR:
        1. Gets ALL FIRDS records for the ISIN
        2. Creates single instrument with primary data
        3. Creates separate venue records for EACH venue
        4. Stores both original and processed data
        """
        session = SessionLocal()
        
        try:
            # Get ALL FIRDS data for this ISIN
            all_venue_records = self._get_firds_data_from_storage(identifier, instrument_type)
            if not all_venue_records:
                raise InstrumentNotFoundError(f"No FIRDS data found for {identifier}")
            
            self.logger.info(f"Found {len(all_venue_records)} venue records for {identifier}")
            
            # Use first record for primary instrument data
            primary_record = all_venue_records[0]
            
            # Check for existing and delete if present
            existing = session.query(Instrument).filter(Instrument.isin == identifier).first()
            if existing:
                self.logger.info(f"Deleting existing instrument {identifier}")
                session.delete(existing)
                session.flush()
            
            # Create instrument with core fields + JSON attributes
            instrument_data = {
                'id': str(uuid.uuid4()),
                'isin': identifier,
                'instrument_type': instrument_type,
                'full_name': primary_record.get('FinInstrmGnlAttrbts_FullNm'),
                'short_name': primary_record.get('FinInstrmGnlAttrbts_ShrtNm'),
                'currency': primary_record.get('FinInstrmGnlAttrbts_NtnlCcy'),
                'cfi_code': primary_record.get('FinInstrmGnlAttrbts_ClssfctnTp'),
                'lei_id': primary_record.get('Issr'),
                'firds_data': primary_record,  # Original FIRDS record
                'processed_attributes': self._process_instrument_attributes(primary_record, instrument_type)
            }
            
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
            
            self.logger.info(f"Created instrument {identifier} with {len(venue_records)} venue records")
            
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
    
    def _process_instrument_attributes(self, firds_record: Dict[str, Any], instrument_type: str) -> Dict[str, Any]:
        """Process type-specific attributes into clean JSON structure."""
        attributes = {}
        
        try:
            if instrument_type == "equity":
                # Extract equity-specific fields
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
                asset_class = {}
                if firds_record.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct'):
                    asset_class['oil_type'] = firds_record['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct']
                
                if firds_record.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct'):
                    asset_class['sub_product'] = firds_record['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct']
                
                if firds_record.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct'):
                    asset_class['metal_type'] = firds_record['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_Prcs_BasePdct']
                
                if asset_class:
                    attributes['asset_class'] = asset_class
                    
            elif instrument_type == "debt":
                # Extract debt-specific fields
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
                        
            elif instrument_type == "future":
                # Extract future-specific fields
                if firds_record.get('DerivInstrmAttrbts_XpryDt'):
                    attributes['expiration_date'] = firds_record['DerivInstrmAttrbts_XpryDt']
                
                if firds_record.get('DerivInstrmAttrbts_DlvryTp'):
                    attributes['delivery_type'] = firds_record['DerivInstrmAttrbts_DlvryTp']
                
                if firds_record.get('DerivInstrmAttrbts_PricMltplr'):
                    try:
                        attributes['price_multiplier'] = float(firds_record['DerivInstrmAttrbts_PricMltplr'])
                    except (ValueError, TypeError):
                        pass
        
        except Exception as e:
            self.logger.warning(f"Error processing attributes for {instrument_type}: {e}")
        
        return attributes
    
    def _create_venue_record(self, instrument_id: str, venue_data: Dict[str, Any]) -> TradingVenue:
        """Create a venue record from FIRDS data."""
        
        venue_record = TradingVenue(
            id=str(uuid.uuid4()),
            instrument_id=instrument_id,
            venue_id=venue_data.get('TradgVnRltdAttrbts_Id'),
            isin=venue_data.get('Id'),
            first_trade_date=self._parse_date(venue_data.get('TradgVnRltdAttrbts_FrstTradDt')),
            termination_date=self._parse_date(venue_data.get('TradgVnRltdAttrbts_TermntnDt')),
            admission_approval_date=self._parse_date(venue_data.get('TradgVnRltdAttrbts_AdmssnApprvlDtByIssr')),
            request_for_admission_date=self._parse_date(venue_data.get('TradgVnRltdAttrbts_ReqForAdmssnDt')),
            venue_full_name=venue_data.get('FinInstrmGnlAttrbts_FullNm'),
            venue_short_name=venue_data.get('FinInstrmGnlAttrbts_ShrtNm'),
            classification_type=venue_data.get('FinInstrmGnlAttrbts_ClssfctnTp'),
            venue_currency=venue_data.get('FinInstrmGnlAttrbts_NtnlCcy'),
            issuer_requested=venue_data.get('TradgVnRltdAttrbts_IssrReq'),
            competent_authority=venue_data.get('TechAttrbts_RlvntCmptntAuthrty'),
            relevant_trading_venue=venue_data.get('TechAttrbts_RlvntTradgVn'),
            publication_from_date=self._parse_date(venue_data.get('TechAttrbts_PblctnPrd_FrDt')),
            original_firds_record=venue_data  # Store original for debugging/reference
        )
        
        # Store any additional venue-specific attributes (excluding mapped fields)
        venue_attributes = {}
        mapped_fields = self._get_mapped_fields()
        
        for key, value in venue_data.items():
            if key not in mapped_fields and value is not None and value != "":
                venue_attributes[key] = value
        
        if venue_attributes:
            venue_record.venue_attributes = venue_attributes
        
        return venue_record
    
    def _get_mapped_fields(self) -> set:
        """Get list of fields that are already mapped to specific columns."""
        return {
            'Id', 'TradgVnRltdAttrbts_Id', 'TradgVnRltdAttrbts_FrstTradDt',
            'TradgVnRltdAttrbts_TermntnDt', 'TradgVnRltdAttrbts_AdmssnApprvlDtByIssr',
            'TradgVnRltdAttrbts_ReqForAdmssnDt', 'FinInstrmGnlAttrbts_FullNm',
            'FinInstrmGnlAttrbts_ShrtNm', 'FinInstrmGnlAttrbts_ClssfctnTp',
            'FinInstrmGnlAttrbts_NtnlCcy', 'TradgVnRltdAttrbts_IssrReq',
            'TechAttrbts_RlvntCmptntAuthrty', 'TechAttrbts_RlvntTradgVn',
            'TechAttrbts_PblctnPrd_FrDt', 'Issr', 'FinInstrmGnlAttrbts_CmmdtyDerivInd'
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
    
    def _get_firds_data_from_storage(self, identifier: str, instrument_type: str) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch ALL FIRDS data records from local storage for a given ISIN.
        This is the same as the current implementation but returns all records.
        """
        try:
            from pathlib import Path
            
            # Determine file type pattern
            file_type = ('FULINS_E' if instrument_type == 'equity' else
                        'FULINS_D' if instrument_type == 'debt' else
                        'FULINS_F' if instrument_type == 'future' else None)
            
            if not file_type:
                self.logger.error(f"Unsupported instrument type: {instrument_type}")
                return None
            
            # Look for files in local storage
            firds_path = Path(esmaConfig.firds_path)
            if not firds_path.exists():
                self.logger.error(f"FIRDS storage path does not exist: {firds_path}")
                return None
            
            # Find files matching the pattern for this instrument type
            matching_files = list(firds_path.glob(f"*{file_type}*_firds_data.csv"))
            
            if not matching_files:
                self.logger.warning(f"No {file_type} files found in local storage: {firds_path}")
                return None
            
            # Search through local files for the identifier
            for file_path in matching_files:
                try:
                    self.logger.debug(f"Searching for {identifier} in {file_path.name}")
                    
                    import pandas as pd
                    df = pd.read_csv(str(file_path), dtype=str, low_memory=False)
                    
                    if df is not None and not df.empty:
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
            
            self.logger.warning(f"Identifier {identifier} not found in any local {file_type} files")
            return None

        except Exception as e:
            self.logger.error(f"Error fetching FIRDS data from storage: {str(e)}")
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
