from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, UTC

class LegalEntity(Base):
    __tablename__ = 'legal_entities'

    lei = Column(String, primary_key=True)
    legal_name = Column(String)
    legal_jurisdiction = Column(String)
    creation_date = Column(DateTime, default=lambda: datetime.now(UTC))
    status = Column(String)
    
    # Relationship with instruments
    instruments = relationship(
        "Instrument",
        back_populates="legal_entity",
        passive_deletes=True,
        lazy='select'
    )