import uuid
import logging
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from ...database.session import get_session, SessionLocal
from ...database.model_mapper import map_transparency_data
from ...models.sqlite.transparency import TransparencyCalculation, EquityTransparency, NonEquityTransparency, DebtTransparency, FuturesTransparency
from ...models.sqlite.instrument import Instrument
from datetime import datetime, UTC
from ..esma_data_loader import EsmaDataLoader
from ...config import esmaConfig
from ..interfaces.transparency_service_interface import TransparencyServiceInterface


logger = logging.getLogger(__name__)

class TransparencyServiceError(Exception):
    """Base exception for transparency service errors"""
    pass

class TransparencyNotFoundError(TransparencyServiceError):
    """Raised when transparency data cannot be found"""
    pass

class TransparencyValidationError(TransparencyServiceError):
    """Raised when transparency data validation fails"""
    pass

class TransparencyService(TransparencyServiceInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.esma_loader = EsmaDataLoader(esmaConfig.start_date, esmaConfig.end_date)

    def validate_transparency_data(self, data: Dict[str, Any]) -> None:
        """Validate required transparency data fields"""
        required_fields = ['ISIN', 'TechRcrdId']
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise TransparencyValidationError(f"Missing required fields: {', '.join(missing)}")

    def create_transparency_calculation(self, data: Dict[str, Any], calculation_type: str = "NON_EQUITY") -> TransparencyCalculation:
        """
        Create a new transparency calculation in the database.
        
        Args:
            data: Dictionary containing transparency data
            calculation_type: Type of calculation ('EQUITY' or 'NON_EQUITY')
            
        Returns:
            Created TransparencyCalculation instance
        """
        self.validate_transparency_data(data)
        session = SessionLocal()
        
        try:
            # Determine instrument type from data or CFI code
            instrument_type = self._determine_instrument_type(data)
            
            # Map data to transparency models
            transparency_data = map_transparency_data(data, calculation_type, instrument_type)
            
            # Create base transparency calculation
            base_calc = TransparencyCalculation(
                id=str(uuid.uuid4()),
                **transparency_data['base']
            )
            
            session.add(base_calc)
            session.flush()  # Get the ID
            
            # Create specific transparency type based on instrument
            if calculation_type == "EQUITY":
                specific_calc = EquityTransparency(
                    id=base_calc.id,
                    **transparency_data['specific']
                )
            else:
                # Non-equity - determine if debt or futures
                if instrument_type == "debt":
                    specific_calc = DebtTransparency(
                        id=base_calc.id,
                        **transparency_data['specific']
                    )
                elif instrument_type == "futures":
                    specific_calc = FuturesTransparency(
                        id=base_calc.id,
                        **transparency_data['specific']
                    )
                else:
                    # Generic non-equity
                    specific_calc = NonEquityTransparency(
                        id=base_calc.id,
                        **transparency_data['specific']
                    )
            
            session.add(specific_calc)
            session.commit()
            session.refresh(base_calc)
            return base_calc
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to create transparency calculation: {str(e)}")
            raise TransparencyServiceError(f"Failed to create transparency calculation: {str(e)}")
        finally:
            session.close()

    def _determine_instrument_type(self, data: Dict[str, Any]) -> str:
        """Determine instrument type from data"""
        # Simple logic - can be enhanced based on actual requirements
        if 'Desc' in data:
            desc = data['Desc'].lower()
            if 'bond' in desc:
                return 'debt'
            elif 'future' in desc or 'forward' in desc:
                return 'futures'
        return 'non_equity'

    def get_transparency_by_isin(self, isin: str) -> Optional[List[TransparencyCalculation]]:
        """Get transparency calculations for an ISIN"""
        session = SessionLocal()
        try:
            calculations = session.query(TransparencyCalculation).filter(
                TransparencyCalculation.isin == isin
            ).all()
            return calculations
        except Exception as e:
            self.logger.error(f"Failed to get transparency for ISIN {isin}: {str(e)}")
            raise TransparencyServiceError(f"Failed to get transparency: {str(e)}")
        finally:
            session.close()

    def delete_transparency_calculation(self, calc_id: str) -> bool:
        """Delete a transparency calculation"""
        session = SessionLocal()
        try:
            calc = session.query(TransparencyCalculation).filter(
                TransparencyCalculation.id == calc_id
            ).first()
            if calc:
                session.delete(calc)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to delete transparency calculation {calc_id}: {str(e)}")
            raise TransparencyServiceError(f"Failed to delete transparency calculation: {str(e)}")
        finally:
            session.close()
