import pytest
from ..services.sqlite.instrument_service import SqliteInstrumentService
from ..models.sqlite.instrument import Instrument, Equity  # Fix import path
from ..models.sqlite.figi import FigiMapping
from ..models.sqlite.legal_entity import LegalEntity
from ..database.session import get_session
from ..database.base import Base, engine
from datetime import datetime, UTC

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="module")
def test_service():
    return SqliteInstrumentService()

def test_figi_relationship(setup_database):
    with get_session() as session:
        # Create equity instrument instead of base instrument
        instrument = Equity(
            id="test-id",
            isin="TEST123",
            type="equity",
            exchange="NYSE"  # Add required equity field
        )
        
        # Create FIGI mapping
        figi = FigiMapping(
            isin="TEST123",
            figi="BBG000123",
            security_type="Common Stock"
        )
        
        instrument.figi_mappings = [figi]
        session.add(instrument)
        session.commit()
        
        # Test relationship
        loaded = session.get(Equity, "test-id")  # Use Equity instead of Instrument
        assert loaded.figi_mappings[0].figi == "BBG000123"

def test_legal_entity_relationship(setup_database):
    with get_session() as session:
        # Create legal entity
        entity = LegalEntity(
            lei="TEST_LEI",
            legal_name="Test Corp"
        )
        session.add(entity)
        
        # Create equity instrument with relationship
        instrument = Equity(  # Use Equity instead of Instrument
            id="test-id-2",
            isin="TEST456",
            type="equity",
            exchange="NYSE",  # Add required equity field
            lei_id="TEST_LEI"
        )
        session.add(instrument)
        session.commit()
        
        # Test relationships
        loaded_entity = session.get(LegalEntity, "TEST_LEI")
        assert len(loaded_entity.instruments) == 1
        assert loaded_entity.instruments[0].isin == "TEST456"
