import uuid
import logging
from typing import Dict, Any, Optional, NoReturn
from ..database.session import get_session, SessionLocal
from ..database.model_mapper import map_to_model
from ..models.instrument import Instrument, Equity, Debt
from datetime import datetime, UTC

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
    def validate_instrument_data(self, data: Dict[str, Any]) -> None:
        """Validate required instrument data fields"""
        required_fields = ['FinInstrmGnlAttrbts_Id']
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
            
            instrument.last_updated = datetime.now(UTC)
            
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
            
            instrument.last_updated = datetime.now(UTC)
            session.commit()
            session.refresh(instrument)
            logger.info(f"Updated instrument with ID: {identifier}")
            return instrument
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()
