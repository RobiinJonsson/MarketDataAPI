import uuid
from typing import Dict, Any, Optional
from ..database.session import get_session, SessionLocal
from ..database.model_mapper import map_to_model
from ..models.instrument import Instrument, Equity, Debt
from datetime import datetime, UTC

class InstrumentService:
    def create_instrument(self, data: Dict[str, Any], instrument_type: str = "equity") -> Instrument:
        session = SessionLocal()
        try:
            model_data = map_to_model(data, instrument_type)
            model_data['id'] = str(uuid.uuid4())
            model_data['type'] = instrument_type
            
            if instrument_type == "equity":
                instrument = Equity(**model_data)
            elif instrument_type == "debt":
                instrument = Debt(**model_data)
            else:
                instrument = Instrument(**model_data)
            
            instrument.last_updated = datetime.now(UTC)
            
            unmapped = {k: v for k, v in data.items() if k not in model_data}
            if unmapped:
                instrument.additional_data = unmapped
            
            session.add(instrument)
            session.flush()
            session.refresh(instrument)
            session.commit()
            
            return session.get(Instrument, instrument.id)
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_instrument(self, identifier: str) -> Optional[Instrument]:
        with get_session() as session:
            return (
                session.query(Instrument)
                .filter(
                    (Instrument.id == identifier) |
                    (Instrument.isin == identifier) |
                    (Instrument.symbol == identifier)
                )
                .first()
            )

    def update_instrument(self, identifier: str, data: Dict[str, Any]) -> Optional[Instrument]:
        with get_session() as session:
            instrument = self.get_instrument(identifier)
            if not instrument:
                return None
                
            mapped_data = map_to_model(data, instrument.type)
            for key, value in mapped_data.items():
                setattr(instrument, key, value)
            
            instrument.last_updated = datetime.now(UTC)
            session.commit()
            return instrument
