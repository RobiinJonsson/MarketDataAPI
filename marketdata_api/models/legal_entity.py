from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from ..database.base import Base

class LegalEntity(Base):
    __tablename__ = "legal_entities"

    lei = Column(String, primary_key=True)
    legal_name = Column(String)
    legal_jurisdiction = Column(String)
    legal_form_id = Column(String)
    registered_as = Column(String)
    category = Column(String)
    sub_category = Column(String, nullable=True)
    status = Column(String)
    bic = Column(String)
    mic = Column(String)
    ocid = Column(String)
    qcc = Column(String)
    conformity_flag = Column(String)
    spglobal = Column(String)
    associated_entity_lei = Column(String, nullable=True)
    associated_entity_name = Column(String, nullable=True)
    successor_entity_lei = Column(String, nullable=True)
    successor_entity_name = Column(String, nullable=True)
    creation_date = Column(DateTime)

    # Relationship with instruments
    instruments = relationship("Instrument", back_populates="legal_entity")