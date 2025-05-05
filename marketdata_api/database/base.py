import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = "marketdata.db"
DB_PATH = os.path.join(BASE_DIR, DB_FILE)
SQLITE_URL = f"sqlite:///{DB_PATH}"

# Create engine and session factory
engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

def init_db():
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(bind=engine)
