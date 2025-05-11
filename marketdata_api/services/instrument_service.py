import uuid
import logging
from typing import Dict, Any, Optional, NoReturn, Tuple
from sqlalchemy.orm import Session
from ..database.session import get_session, SessionLocal
from ..database.model_mapper import map_to_model, map_figi_data
from ..models.instrument import Instrument, Equity, Debt
from ..models.figi import FigiMapping  # Assuming this is the model for FIGI mapping
from .esma_data_loader import EsmaDataLoader
from .openfigi import search_openfigi
from .gleif import fetch_lei_info
from datetime import datetime, UTC
from ..config import esmaConfig

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

class InstrumentService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.esma_loader = EsmaDataLoader(esmaConfig.start_date, esmaConfig.end_date)

    def validate_instrument_data(self, data: Dict[str, Any]) -> None:
        """Validate required instrument data fields"""
        required_fields = ['Id']  # Changed from 'FinInstrmGnlAttrbts_Id' to match model_mapper
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise InstrumentValidationError(f"Missing required fields: {', '.join(missing)}")
    
    
    def create_instrument(self, data: Dict[str, Any], instrument_type: str = "equity") -> Instrument:
        """
        Create a new instrument in the database.
        
        Args:
            data: Dictionary containing instrument data
            instrument_type: Type of instrument to create ('equity' or 'debt')
            
        Returns:
            Created Instrument instance
            
        Raises:
            InstrumentValidationError: If required data is missing
            InstrumentServiceError: If creation fails
        """
        self.validate_instrument_data(data)
        session = SessionLocal()
        
        try:
            model_data = map_to_model(data, instrument_type)
            model_data['id'] = str(uuid.uuid4())
            model_data['type'] = instrument_type
            
            instrument = (Equity if instrument_type == "equity" else 
                        Debt if instrument_type == "debt" else 
                        Instrument)(**model_data)
            
            unmapped = {k: v for k, v in data.items() if k not in model_data}
            if unmapped:
                instrument.additional_data = unmapped
            
            session.add(instrument)
            session.flush()
            session.refresh(instrument)
            session.commit()
            
            logger.info(f"Created new {instrument_type} instrument with ID: {instrument.id}")
            return session.get(Instrument, instrument.id)
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to create instrument: {str(e)}")
            raise InstrumentServiceError(f"Failed to create instrument: {str(e)}") from e
        finally:
            session.close()

    def get_instrument(self, identifier: str) -> tuple[Session, Optional[Instrument]]:
        """
        Retrieve an instrument by its identifier.
        
        Args:
            identifier: The unique identifier of the instrument
            
        Returns:
            Tuple of (Session, Instrument): Active session and instrument if found
        """
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
            if instrument:
                session.refresh(instrument)
            return session, instrument
        except:
            session.close()
            raise

    def update_instrument(self, identifier: str, data: Dict[str, Any]) -> Optional[Instrument]:
        """
        Update an existing instrument in the database.
        
        Args:
            identifier: The unique identifier of the instrument
            data: Dictionary containing updated instrument data
            
        Returns:
            The updated Instrument instance if successful, otherwise None
        """
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

    def delete_instrument(self, identifier: str) -> bool:
        """Delete an instrument by its identifier."""
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
            if instrument:
                session.delete(instrument)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to delete instrument: {str(e)}")
            raise
        finally:
            session.close()

    def get_or_create_instrument(self, identifier: str, instrument_type: str = "equity") -> Optional[Instrument]:
        """Get existing instrument or create from FIRDS data."""
        with get_session() as session:
            try:
                # Check if instrument exists
                instrument = (
                    session.query(Instrument)
                    .filter(Instrument.isin == identifier)
                    .first()
                )
                if instrument:
                    return instrument

                # If not found, get FIRDS data and create
                instrument_data = self._get_firds_data(identifier, instrument_type)
                if not instrument_data:
                    return None

                instrument = self.create_instrument(instrument_data, instrument_type)
                return instrument

            except Exception as e:
                self.logger.error(f"Failed to get/create instrument {identifier}: {str(e)}")
                raise InstrumentServiceError(f"Failed to get/create instrument: {str(e)}")

    def _get_firds_data(self, identifier: str, instrument_type: str) -> Optional[Dict[str, Any]]:
        """Helper method to fetch FIRDS data."""
        try:
            list_files = self.esma_loader.load_mifid_file_list(['firds'])
            file_type = 'FULINS_E' if instrument_type == 'equity' else 'FULINS_D'
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

    def enrich_instrument(self, instrument: Instrument) -> tuple[Session, Instrument]:
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

    def _enrich_figi(self, session: Session, instrument: Instrument) -> None:
        """Helper method to handle FIGI enrichment"""
        self.logger.debug(f"Starting FIGI enrichment for {instrument.isin}")
        figi_data = search_openfigi(instrument.isin, instrument.type)
        if figi_data:
            self.logger.debug(f"Received FIGI data: {figi_data}")
            figi_mapping = map_figi_data(figi_data, instrument.isin)
            if figi_mapping:
                self.logger.info(f"Created FIGI mapping for {instrument.isin}")
                instrument.figi_mapping = figi_mapping
                session.add(figi_mapping)
                self.logger.debug(f"FIGI mapping added to session")

    def _enrich_legal_entity(self, session: Session, instrument: Instrument) -> None:
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
