"""
Test configuration and fixtures for MarketDataAPI tests.

Provides shared fixtures, test data, and configuration for the test suite.
"""

import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from marketdata_api.config import Config
from marketdata_api.database.session import get_session

# Import MarketDataAPI components
from marketdata_api.models.sqlite.base_model import Base
from marketdata_api.models.sqlite.instrument import Instrument, TradingVenue
from marketdata_api.models.sqlite.legal_entity import LegalEntity
from marketdata_api.models.sqlite.market_identification_code import MarketIdentificationCode
from marketdata_api.models.sqlite.transparency import TransparencyCalculation

from .test_data_real import (
    RealTestDataProvider,
    get_test_instrument,
    get_test_isin,
    get_test_lei,
    get_test_mic,
    get_test_mic_code,
)


@pytest.fixture(scope="session")
def test_database_url():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    yield f"sqlite:///{db_path}"

    # Cleanup
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture(scope="session")
def test_engine(test_database_url):
    """Create test database engine."""
    engine = create_engine(test_database_url, echo=False)

    # Create all tables
    Base.metadata.create_all(engine)

    yield engine

    # Cleanup
    engine.dispose()


@pytest.fixture
def test_session(test_engine):
    """Create a test database session with rollback after each test."""
    connection = test_engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def sample_instrument():
    """Create a sample instrument for testing using real data."""
    real_data = get_test_instrument()
    return Instrument(
        isin=real_data["isin"],
        instrument_type=real_data["instrument_type"],
        full_name=real_data["full_name"],
        short_name=real_data["short_name"],
        currency=real_data["currency"],
        cfi_code=real_data["cfi_code"],
        lei_id=real_data["lei_id"],
        competent_authority=real_data["country"],
        publication_from_date="2024-01-01",
        firds_data={
            "notional_currency": real_data["currency"],
            "classification_type": (
                "EQTYSHR" if real_data["instrument_type"] == "equity" else "DBFTXX"
            ),
            "underlying_instrument_type": (
                "STOCK" if real_data["instrument_type"] == "equity" else "BOND"
            ),
        },
    )


@pytest.fixture
def sample_legal_entity():
    """Create a sample legal entity for testing using real data."""
    return LegalEntity(
        lei=get_test_lei(),
        legal_name="NASDAQ STOCKHOLM AB",
        entity_status="ACTIVE",
        legal_address={"country": "SE", "region": "SE-AB", "city": "Stockholm"},
        headquarters_address={"country": "SE", "region": "SE-AB", "city": "Stockholm"},
    )


@pytest.fixture
def sample_mic_code():
    """Create a sample MIC code for testing using real data."""
    real_mic = get_test_mic()
    return MarketIdentificationCode(
        mic=real_mic["mic"],
        market_name=real_mic["market_name"],
        legal_entity=real_mic["market_name"],
        country=real_mic["country"],
        city=real_mic["city"],
        status=real_mic["status"],
        type=real_mic["type"],
        operating_mic=real_mic["mic"],
        lei=real_mic.get("lei", get_test_lei()),
    )


@pytest.fixture
def sample_transparency_calculation():
    """Create a sample transparency calculation for testing using real data."""
    test_isin = get_test_isin()
    return TransparencyCalculation(
        isin=test_isin,
        file_type="FULECR_E",
        source_file="FULECR_20250830_E_1of1_fitrs_data.csv",
        period_from="2024-01-01",
        period_to="2024-12-31",
        liquid="No",
        transactions=0,
        volume=0.00,
        tech_record_id=33961,
        equity_data={
            "primary_identifier": test_isin,
            "secondary_identifier": get_test_mic_code(),
            "methodology": "YEAR",
            "average_daily_turnover": 537499.90515,
            "large_in_scale": 100000,
        },
    )


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    with patch.object(Config, "DATABASE_PATH", "/tmp/test.db"):
        with patch.object(Config, "ROOT_PATH", "/tmp"):
            yield Config


@pytest.fixture
def temp_directory():
    """Create a temporary directory for testing file operations."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_external_services():
    """Mock external services like ESMA, GLEIF, OpenFIGI."""
    mocks = {"esma_response": Mock(), "gleif_response": Mock(), "openfigi_response": Mock()}

    # Configure mock responses
    mocks["esma_response"].json.return_value = {"status": "success", "data": []}
    mocks["gleif_response"].json.return_value = {"data": []}
    mocks["openfigi_response"].json.return_value = [{"figi": "BBG000B9XRY4"}]

    return mocks


# Test data constants - using real data from our database
from .test_data_real import KNOWN_INSTRUMENTS, KNOWN_LEGAL_ENTITIES, KNOWN_MIC_CODES

TEST_ISINS = list(KNOWN_INSTRUMENTS.keys())
TEST_CURRENCIES = list(set(instr["currency"] for instr in KNOWN_INSTRUMENTS.values()))
TEST_MIC_CODES = list(KNOWN_MIC_CODES.keys())

# Test datasets for different scenarios
MINIMAL_DATASET = {"instruments": 5, "entities": 3, "mic_codes": 4, "transparency_calcs": 10}

MEDIUM_DATASET = {"instruments": 50, "entities": 30, "mic_codes": 25, "transparency_calcs": 100}

LARGE_DATASET = {"instruments": 500, "entities": 300, "mic_codes": 200, "transparency_calcs": 1000}
