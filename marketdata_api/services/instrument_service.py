import uuid
import logging
from typing import Dict, Any, Optional, NoReturn
from ..database.session import get_session, SessionLocal
from ..database.model_mapper import map_to_model  # Use this instead of map_firds_to_instrument
from ..models.instrument import Instrument, Equity, Debt
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

    def get_instrument(self, identifier: str) -> Optional[Instrument]:
        """
        Retrieve an instrument by its identifier.
        
        Args:
            identifier: The unique identifier of the instrument
            
        Returns:
            The Instrument instance if found, otherwise None
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
            return instrument
        finally:
            session.close()

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

    def get_or_create_instrument(self, identifier: str, instrument_type: str = "equity") -> Optional[Instrument]:
        """Get instrument from database or create it from external sources if not found."""
        instrument = self.get_instrument(identifier)
        if instrument:
            return instrument
            
        try:
            # 1. Get FIRDS data using EsmaDataLoader
            list_files = self.esma_loader.load_mifid_file_list(['firds'])
            file_type = 'FULINS_E' if instrument_type == 'equity' else 'FULINS_D'
            fulins_files = list_files[list_files['download_link'].str.contains(file_type, na=False)]
            
            if fulins_files.empty:
                self.logger.warning(f"No {file_type} files found")
                return None

            instrument_data = None
            for _, file_info in fulins_files.iterrows():
                link = file_info['download_link']
                self.logger.info(f"Processing file: {link}")
                
                df = self.esma_loader.download_file(link)
                if df.empty:
                    continue
                    
                isin_data = df[df['Id'] == identifier]
                if not isin_data.empty:
                    instrument_data = isin_data.iloc[0].to_dict()
                    break
            
            if not instrument_data:
                self.logger.warning(f"No FIRDS data found for {identifier}")
                return None

            # Use map_to_model instead of map_firds_to_instrument
            return self.create_instrument(instrument_data, instrument_type)
            
        except Exception as e:
            self.logger.error(f"Failed to fetch/create instrument {identifier}: {str(e)}")
            raise InstrumentServiceError(f"Failed to fetch/create instrument: {str(e)}")

    def enrich_instrument(self, instrument: Instrument) -> Instrument:
        """
        Enrich existing instrument with additional data from external sources.
        """
        try:
            # Enrich with FIGI if not present
            if not instrument.figi:
                figi_data = search_openfigi(instrument.isin)
                if figi_data:
                    self.update_instrument(instrument.id, figi_data)
                    
            # Enrich with LEI data if not in additional_data
            if instrument.lei_id and 'lei_data' not in (instrument.additional_data or {}):
                lei_data = fetch_lei_info(instrument.lei_id)
                if lei_data and 'error' not in lei_data:
                    self.update_instrument(instrument.id, {'lei_data': lei_data})
                    
            return instrument
            
        except Exception as e:
            self.logger.error(f"Failed to enrich instrument {instrument.id}: {str(e)}")
            return instrument
