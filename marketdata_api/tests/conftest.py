import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..database.base import Base
from datetime import datetime
from ..schema.schema_mapper import SchemaMapper

# Add the project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

@pytest.fixture(scope="session")
def test_engine():
    """Create test engine with in-memory SQLite database"""
    return create_engine("sqlite:///:memory:", echo=False)

@pytest.fixture(scope="session")
def TestingSessionLocal(test_engine):
    """Create session factory for tests"""
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
        expire_on_commit=False
    )

@pytest.fixture
def test_session(TestingSessionLocal):
    """Get test session for each test function"""
    session: Session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def setup_database(test_engine, test_session):
    """Create all tables before test and drop after"""
    Base.metadata.create_all(bind=test_engine)
    yield test_session
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def schema_mapper():
    return SchemaMapper()

@pytest.fixture
def sample_equity():
    # Lazy import to avoid model conflicts during regular app startup
    from ..database.factory.database_factory import DatabaseFactory
    db = DatabaseFactory.create_database()
    models = db.get_models()
    Equity = models.get('Equity')
    
    return Equity(
        isin="SE0000108656",
        full_name="Test Equity",
        short_name="TEST",
        symbol="TEST",
        currency="USD",
        market_cap=1000000.00,
        sector="Technology",
        price_multiplier=1.0
    )

@pytest.fixture
def sample_debt():
    # Lazy import to avoid model conflicts during regular app startup
    from ..database.factory.database_factory import DatabaseFactory
    db = DatabaseFactory.create_database()
    models = db.get_models()
    Debt = models.get('Debt')
    
    return Debt(
        isin="XS2332219612",
        full_name="Test Bond",
        short_name="TBOND",
        currency="EUR",
        maturity_date=datetime(2025, 1, 1).date(),
        fixed_interest_rate=0.05,
        total_issued_nominal=1000000.00
    )

@pytest.fixture
def sample_firds_data():
    return {
        'Id': 'SE0000108656',
        'FullNm': 'Test Equity',
        'ShrtNm': 'TEST',
        'NtnlCcy': 'USD',
        'ClssfctnTp': 'ESVUFR',
        'CmmdtyDerivInd': 'false',
        'PricMltplr': '1.0'
    }
