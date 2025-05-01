import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..database.base import Base
from ..models import *  # This ensures all models are loaded

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
