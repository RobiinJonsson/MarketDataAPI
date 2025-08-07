"""SQLite instrument service preserving existing functionality."""

import logging
import uuid
import math
from typing import Dict, Any, Optional, List, Tuple
from sqlalchemy.orm import sessionmaker, Session
from ...services.interfaces.instrument_service_interface import InstrumentServiceInterface
from ...models.interfaces.instrument_interface import InstrumentInterface
from ...database.session import get_session, SessionLocal
from ...database.model_mapper import map_to_model, map_figi_data
from ..esma_data_loader import EsmaDataLoader
from ..openfigi import search_openfigi
from ..gleif import fetch_lei_info
from datetime import datetime, UTC
from ...config import esmaConfig

# Direct model imports at module level - importing only what this service needs
from ...models.sqlite.instrument import Instrument, Equity, Debt, Future
from ...models.sqlite.legal_entity import LegalEntity  # Only what's needed
from ...models.sqlite.figi import FigiMapping  # Ensure FIGI relationships work
from ...models.sqlite.figi import FigiMapping
from ...models.sqlite.transparency import TransparencyCalculation

logger = logging.getLogger(__name__)


class InstrumentServiceError(Exception):
    """Base exception for instrument service errors"""
    pass


class InstrumentNotFoundError(InstrumentServiceError):
    """Raised when an instrument cannot be found"""
    pass


class InstrumentValidationError(InstrumentServiceError):
    """Raised when instrument data validation fails"""
    pass


class SqliteInstrumentService(InstrumentServiceInterface):
    """SQLite instrument service using direct imports with legacy functionality."""
    
    def __init__(self):
        self.database_type = 'sqlite'
        self.logger = logging.getLogger(__name__)
        self.esma_loader = EsmaDataLoader(esmaConfig.start_date, esmaConfig.end_date)
    
    def _get_instrument_model(self):
        """Get the appropriate instrument model."""
        return Instrument
    
    def validate_instrument_identifier(self, identifier: str) -> None:
        """Validate instrument identifier (ISIN)"""
        if not identifier or not isinstance(identifier, str):
            raise InstrumentValidationError("Instrument identifier must be a non-empty string")
        if len(identifier) != 12:
            raise InstrumentValidationError("ISIN must be 12 characters long")
    
    def create_instrument(self, identifier: str, instrument_type: str = "equity") -> InstrumentInterface:
        """
        Create a new instrument from FIRDS data stored locally.
        
        Behavior:
        1. Always create from FIRDS files in storage (never download new files)
        2. No manual inputs - always use FIRDS data
        3. If instrument exists, override current data
        4. Try to enrich with OpenFIGI and GLEIF information
        
        Args:
            identifier: ISIN identifier for the instrument
            instrument_type: Type of instrument to create ('equity', 'debt', or 'future')
            
        Returns:
            Created Instrument instance
            
        Raises:
            InstrumentNotFoundError: If instrument not found in FIRDS data
            InstrumentServiceError: If creation fails
        """
        session = SessionLocal()
        
        try:
            # Get FIRDS data from local storage only
            instrument_records = self._get_firds_data_from_storage(identifier, instrument_type)
            if not instrument_records:
                raise InstrumentNotFoundError(f"Instrument {identifier} not found in local FIRDS data for type {instrument_type}")

            # For basic instrument creation, use the first record but log all available venues
            primary_record = instrument_records[0]
            venues = [record.get('TradgVnRltdAttrbts_Id', 'Unknown') for record in instrument_records]
            logger.info(f"Creating instrument {identifier} from {len(instrument_records)} records across venues: {venues}")

            model_data = map_to_model(primary_record, instrument_type)
            model_data['id'] = str(uuid.uuid4())
            model_data['type'] = instrument_type

            # Check for existing instrument and delete if exists (override behavior)
            isin = model_data.get('isin') or model_data.get('Id')
            existing = session.query(Instrument).filter(
                Instrument.isin == isin
            ).first()
            if existing:
                logger.info(f"Instrument with ISIN {isin} exists. Overriding as requested.")
                session.delete(existing)
                session.flush()

            # Get the appropriate model class
            if instrument_type == "equity":
                model_cls = Equity
            elif instrument_type == "debt":
                model_cls = Debt
            elif instrument_type == "future":
                model_cls = Future
            else:
                model_cls = Instrument

            valid_keys = set(c.name for c in model_cls.__table__.columns)
            # Also include parent columns (Instrument) for subclasses
            if model_cls is not Instrument:
                valid_keys |= set(c.name for c in Instrument.__table__.columns)

            filtered_model_data = {k: v for k, v in model_data.items() if k in valid_keys}

            unmapped = {k: v for k, v in model_data.items() if k not in valid_keys}
            # Remove unmapped fields that are None, NaN, or empty dicts
            def is_empty(val):
                if val is None:
                    return True
                if isinstance(val, float) and math.isnan(val):
                    return True
                if isinstance(val, dict) and all(is_empty(v) for v in val.values()):
                    return True
                return False
            unmapped = {k: v for k, v in unmapped.items() if not is_empty(v)}
            if unmapped:
                logger.warning(f"Unmapped fields for {instrument_type} instrument: {unmapped}")

            instrument = model_cls(**filtered_model_data)

            session.add(instrument)
            session.flush()
            session.refresh(instrument)
            session.commit()

            logger.info(f"Created new {instrument_type} instrument with ID: {instrument.id}")
            
            # Try to enrich with external data
            try:
                enriched_session, enriched_instrument = self.enrich_instrument(instrument)
                enriched_session.close()
                
                # Get a fresh copy of the instrument from the original session
                # to avoid session binding issues
                fresh_instrument = session.get(type(instrument), instrument.id)
                return fresh_instrument
            except Exception as e:
                logger.warning(f"Failed to enrich instrument {identifier}: {str(e)}")
                # Return the basic instrument even if enrichment fails
                return session.get(type(instrument), instrument.id)

        except Exception as e:
            session.rollback()
            logger.error(f"Failed to create instrument: {str(e)}")
            raise InstrumentServiceError(f"Failed to create instrument: {str(e)}") from e
        finally:
            session.close()
    
    def get_instrument_by_id(self, instrument_id: str) -> Optional[InstrumentInterface]:
        """Get an instrument by its ID."""
        Instrument = self._get_instrument_model()
        with get_session() as session:
            return session.query(Instrument).filter(Instrument.id == instrument_id).first()
    
    def get_instrument_by_isin(self, isin: str) -> Optional[InstrumentInterface]:
        """Get an instrument by its ISIN."""
        Instrument = self._get_instrument_model()
        with get_session() as session:
            return session.query(Instrument).filter(Instrument.isin == isin).first()
    
    def get_instruments(self, limit: int = 100, offset: int = 0, 
                       instrument_type: Optional[str] = None) -> List[InstrumentInterface]:
        """Get a list of instruments with pagination."""
        Instrument = self._get_instrument_model()
        with get_session() as session:
            query = session.query(Instrument)
            if instrument_type:
                query = query.filter(Instrument.type == instrument_type)
            return query.offset(offset).limit(limit).all()
    
    def update_instrument(self, identifier: str, data: Dict[str, Any]) -> Optional[InstrumentInterface]:
        """
        Update an existing instrument in the database.
        
        Args:
            identifier: The unique identifier of the instrument
            data: Dictionary containing updated instrument data
            
        Returns:
            The updated Instrument instance if successful, otherwise None
        """
        Instrument = self._get_instrument_model()
        session = SessionLocal()
        try:
            instrument = (
                session.query(Instrument)
                .filter(
                    (Instrument.id == identifier) |
                    (Instrument.isin == identifier) |
                    (Instrument.symbol == identifier)
                )
                .first()
            )
            if not instrument:
                logger.warning(f"Instrument with ID {identifier} not found")
                return None
                
            mapped_data = map_to_model(data, instrument.type)
            for key, value in mapped_data.items():
                setattr(instrument, key, value)
            
            session.commit()
            session.refresh(instrument)
            logger.info(f"Updated instrument with ID: {identifier}")
            return instrument
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()
    
    def delete_instrument(self, instrument_id: str) -> bool:
        """Delete an instrument."""
        Instrument = self._get_instrument_model()
        with get_session() as session:
            instrument = session.query(Instrument).filter(Instrument.id == instrument_id).first()
            if instrument:
                session.delete(instrument)
                session.commit()
                return True
            return False
    
    def get_instrument_venues(self, identifier: str, instrument_type: str = "equity") -> Optional[List[Dict[str, Any]]]:
        """
        Get all venue records for a specific ISIN.
        
        Args:
            identifier: ISIN identifier for the instrument
            instrument_type: Type of instrument ('equity', 'debt', or 'future')
            
        Returns:
            List of venue records with trading information, dates, etc.
        """
        try:
            records = self._get_firds_data_from_storage(identifier, instrument_type)
            if not records:
                self.logger.warning(f"No venue records found for {identifier}")
                return None
                
            # Format the records for API consumption
            formatted_records = []
            for record in records:
                venue_info = {
                    'isin': record.get('Id'),
                    'venue_id': record.get('TradgVnRltdAttrbts_Id'),
                    'issuer_requested': record.get('TradgVnRltdAttrbts_IssrReq'),
                    'first_trade_date': record.get('TradgVnRltdAttrbts_FrstTradDt'),
                    'admission_approval_date': record.get('TradgVnRltdAttrbts_AdmssnApprvlDtByIssr'),
                    'termination_date': record.get('TradgVnRltdAttrbts_TermntnDt'),
                    'request_for_admission_date': record.get('TradgVnRltdAttrbts_ReqForAdmssnDt'),
                    'competent_authority': record.get('TechAttrbts_RlvntCmptntAuthrty'),
                    'publication_from_date': record.get('TechAttrbts_PblctnPrd_FrDt'),
                    'relevant_trading_venue': record.get('TechAttrbts_RlvntTradgVn'),
                    'full_name': record.get('FinInstrmGnlAttrbts_FullNm'),
                    'short_name': record.get('FinInstrmGnlAttrbts_ShrtNm'),
                    'classification_type': record.get('FinInstrmGnlAttrbts_ClssfctnTp'),
                    'currency': record.get('FinInstrmGnlAttrbts_NtnlCcy'),
                    'lei': record.get('Issr'),
                    # Include raw record for advanced use cases
                    'raw_record': record
                }
                formatted_records.append(venue_info)
                
            self.logger.info(f"Retrieved {len(formatted_records)} venue records for {identifier}")
            return formatted_records
            
        except Exception as e:
            self.logger.error(f"Error retrieving venue records for {identifier}: {str(e)}")
            return None

    def search_instruments(self, query: str, limit: int = 100) -> List[InstrumentInterface]:
        """Search instruments by name, symbol, or ISIN."""
        Instrument = self._get_instrument_model()
        with get_session() as session:
            return session.query(Instrument).filter(
                (Instrument.full_name.ilike(f'%{query}%')) |
                (Instrument.short_name.ilike(f'%{query}%')) |
                (Instrument.symbol.ilike(f'%{query}%')) |
                (Instrument.isin.ilike(f'%{query}%'))
            ).limit(limit).all()
    
    def validate_instrument_data(self, data: Dict[str, Any]) -> None:
        """
        Legacy method for backward compatibility. 
        New create_instrument method uses validate_instrument_identifier instead.
        """
        # Basic validation
        if not data.get('isin') and not data.get('symbol'):
            raise ValueError("Instrument must have either ISIN or symbol")
    
    def enrich_with_figi(self, instrument: InstrumentInterface) -> InstrumentInterface:
        """Enrich instrument with FIGI data."""
        # Placeholder implementation
        self.logger.info(f"FIGI enrichment not implemented for {instrument.id}")
        return instrument
    
    def enrich_with_lei(self, instrument: InstrumentInterface) -> InstrumentInterface:
        """Enrich instrument with LEI data."""
        # Placeholder implementation
        self.logger.info(f"LEI enrichment not implemented for {instrument.id}")
        return instrument
    
    def get_instrument(self, identifier: str) -> Tuple[Session, Optional[InstrumentInterface]]:
        """
        Retrieve an instrument by its identifier with relationships loaded.
        
        Args:
            identifier: The unique identifier of the instrument
            
        Returns:
            Tuple of (Session, Instrument): Active session and instrument if found
        """
        from sqlalchemy.orm import joinedload
        
        Instrument = self._get_instrument_model()
        session = SessionLocal()
        try:
            instrument = (
                session.query(Instrument)
                .options(
                    joinedload(Instrument.figi_mapping),
                    joinedload(Instrument.legal_entity)
                )
                .filter(
                    (Instrument.id == identifier) |
                    (Instrument.isin == identifier) |
                    (Instrument.symbol == identifier)
                )
                .first()
            )
            if instrument:
                session.refresh(instrument)
            return session, instrument
        except:
            session.close()
            raise
            raise
    
    def _get_firds_data_from_storage(self, identifier: str, instrument_type: str) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch ALL FIRDS data records from local storage for a given ISIN.
        
        Args:
            identifier: ISIN identifier for the instrument
            instrument_type: Type of instrument ('equity', 'debt', or 'future')
            
        Returns:
            List of dictionaries containing all instrument records if found, None otherwise
        """
        try:
            from pathlib import Path
            from ...config import esmaConfig
            
            # Determine file type pattern for different instrument types
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
                    
                    # Load the file - these are CSV files with specific dtype handling
                    import pandas as pd
                    df = pd.read_csv(str(file_path), dtype=str, low_memory=False)
                    
                    if df is not None and not df.empty:
                        # Check for the identifier in the data
                        isin_data = df[df['Id'] == identifier]
                        if not isin_data.empty:
                            self.logger.info(f"Found {len(isin_data)} records for {identifier} in {file_path.name}")
                            
                            # Return all records for this ISIN, not just one
                            # This allows API layer to handle venue selection, date filtering, etc.
                            all_records = isin_data.to_dict('records')  # Convert to list of dicts
                            self.logger.info(f"Returning all {len(all_records)} records for {identifier}")
                            return all_records
                
                except Exception as e:
                    self.logger.warning(f"Error reading file {file_path}: {str(e)}")
                    continue
            
            self.logger.warning(f"Identifier {identifier} not found in any local {file_type} files")
            return None

        except Exception as e:
            self.logger.error(f"Error fetching FIRDS data from storage: {str(e)}")
            return None

    def _get_firds_data(self, identifier: str, instrument_type: str) -> Optional[Dict[str, Any]]:
        """Helper method to fetch FIRDS data."""
        try:
            list_files = self.esma_loader.load_mifid_file_list(['firds'])
            # Add Future file type
            file_type = ('FULINS_E' if instrument_type == 'equity' else
                        'FULINS_D' if instrument_type == 'debt' else
                        'FULINS_F' if instrument_type == 'future' else None)
            
            if not file_type:
                self.logger.error(f"Unsupported instrument type: {instrument_type}")
                return None
                
            fulins_files = list_files[list_files['download_link'].str.contains(file_type, na=False)]
            
            if fulins_files.empty:
                return None

            for _, file_info in fulins_files.iterrows():
                df = self.esma_loader.download_file(file_info['download_link'])
                if not df.empty:
                    isin_data = df[df['Id'] == identifier]
                    if not isin_data.empty:
                        return isin_data.iloc[0].to_dict()
                        
            return None

        except Exception as e:
            self.logger.error(f"Error fetching FIRDS data: {str(e)}")
            return None
    
    def enrich_instrument(self, instrument: InstrumentInterface) -> Tuple[Session, InstrumentInterface]:
        """Enrich existing instrument with additional data from external sources."""
        session = SessionLocal()
        
        try:
            self.logger.info(f"Starting enrichment for instrument {instrument.isin}")
            self.logger.debug(f"Initial instrument state: {instrument.__dict__}")
            
            # Keep instrument bound to this session
            self.logger.info("Merging instrument into session...")
            instrument = session.merge(instrument)
            self.logger.debug(f"Post-merge instrument state: {instrument.__dict__}")
            
            # Log session state
            self.logger.debug(f"Session identity map: {session.identity_map.keys()}")
            
            # Verify session binding
            self.logger.debug(f"Is instrument in session: {instrument in session}")
            self.logger.debug(f"Instrument session: {session.object_session(instrument)}")
            
            # Enrich with FIGI if not present
            if not instrument.figi_mapping:
                try:
                    self.logger.info("Starting FIGI enrichment...")
                    self._enrich_figi(session, instrument)
                except Exception as e:
                    self.logger.error(f"FIGI enrichment failed: {str(e)}")
            
            # Check for LEI
            self.logger.debug(f"Checking LEI. Current lei_id: {getattr(instrument, 'lei_id', None)}")
            if instrument.lei_id:
                self.logger.info(f"Found LEI {instrument.lei_id} for instrument {instrument.isin}")
                try:
                    self._enrich_legal_entity(session, instrument)
                    self.logger.debug(f"Post-LEI enrichment state: {instrument.__dict__}")
                except Exception as e:
                    self.logger.error(f"Legal entity enrichment failed: {str(e)}")
                    self.logger.exception(e)  # This will log the full stack trace
                    raise
            else:
                self.logger.warning(f"No LEI found for instrument {instrument.isin}")
                self.logger.debug(f"Full instrument state: {instrument.__dict__}")
            
            self.logger.info("Committing changes...")
            session.commit()
            self.logger.info("Enrichment completed successfully")
            return session, instrument
            
        except Exception as e:
            self.logger.error(f"Enrichment failed for {instrument.id}: {str(e)}")
            self.logger.exception(e)  # Log full stack trace
            session.rollback()
            raise InstrumentServiceError(f"Enrichment failed: {str(e)}")

    def _enrich_figi(self, session: Session, instrument: InstrumentInterface) -> None:
        """
        Helper method to handle FIGI enrichment with venue-aware optimization.
        
        Uses intelligent venue selection from FIRDS data for better OpenFIGI results.
        """
        self.logger.debug(f"Starting FIGI enrichment for {instrument.isin}")
        
        # Import the enhanced search function
        from ...services.openfigi import search_openfigi_with_fallback
        
        # Get venue records for this ISIN to optimize OpenFIGI search
        try:
            venue_records = self._get_firds_data_from_storage(instrument.isin, instrument.type)
            if venue_records:
                self.logger.info(f"Using {len(venue_records)} venue records for optimized FIGI search")
            else:
                self.logger.warning(f"No venue records found for {instrument.isin}, using basic search")
        except Exception as e:
            self.logger.warning(f"Failed to get venue data for FIGI optimization: {e}")
            venue_records = None
        
        # Use venue-aware search with fallback
        figi_data = search_openfigi_with_fallback(
            instrument.isin, 
            instrument.type, 
            venue_records
        )
        
        if figi_data:
            self.logger.debug(f"Received FIGI data: {figi_data}")
            figi_mapping = map_figi_data(figi_data, instrument.isin)
            if figi_mapping:
                self.logger.info(f"Created FIGI mapping for {instrument.isin}")
                instrument.figi_mapping = figi_mapping
                session.add(figi_mapping)
                self.logger.debug(f"FIGI mapping added to session")
            else:
                self.logger.warning(f"Failed to create FIGI mapping from data: {figi_data}")
        else:
            self.logger.warning(f"No FIGI data returned for {instrument.isin}")

    def _enrich_legal_entity(self, session: Session, instrument: InstrumentInterface) -> None:
        """Helper method to handle legal entity enrichment"""
        from .legal_entity_service import LegalEntityService
        lei_service = LegalEntityService()
        
        self.logger.info(f"Starting legal entity enrichment for LEI: {instrument.lei_id}")
        self.logger.debug(f"Current instrument state: {instrument.__dict__}")
        
        lei_session, entity = lei_service.create_or_update_entity(instrument.lei_id)
        try:
            if entity:
                self.logger.info(f"Found legal entity data for LEI {instrument.lei_id}")
                self.logger.debug(f"Entity data: {entity.__dict__}")
                entity = session.merge(entity)
                instrument.legal_entity = entity
                session.flush()
                self.logger.debug(f"Post-enrichment instrument state: {instrument.__dict__}")
            else:
                self.logger.warning(f"No legal entity data found for LEI {instrument.lei_id}")
        finally:
            if lei_session:
                lei_session.close()
