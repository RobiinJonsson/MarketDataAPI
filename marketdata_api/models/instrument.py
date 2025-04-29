from sqlalchemy import Column, String, JSON, DateTime
from ..database.db import Base

class Instrument(Base):
    __tablename__ = "instruments"

    id = Column(String, primary_key=True)
    symbol = Column(String, index=True)
    isin = Column(String, index=True)
    name = Column(String)
    additional_data = Column(JSON)
    last_updated = Column(DateTime)
