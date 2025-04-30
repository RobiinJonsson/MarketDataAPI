from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DB_PATH = "sqlite:///market_data.db"
engine = create_engine(DB_PATH)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
