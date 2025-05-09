from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, UTC

class LegalEntity(Base):
    __tablename__ = "legal_entities"
    
    lei = Column(String, primary_key=True)
    name = Column(String)  # Changed from legal_name
    jurisdiction = Column(String)  # Changed from legal_jurisdiction
    legal_form = Column(String)  # Changed from legal_form_id
    registered_as = Column(String)  # Added
    status = Column(String)
    bic = Column(String)  # Added
    next_renewal_date = Column(DateTime)  # Added
    registration_status = Column(String)  # Added
    managing_lou = Column(String)  # Added
    creation_date = Column(DateTime, default=lambda: datetime.now(UTC))
    
    # Relationships
    addresses = relationship("EntityAddress", back_populates="entity", cascade="all, delete-orphan")
    registration = relationship("EntityRegistration", back_populates="entity", uselist=False, cascade="all, delete-orphan")
    instruments = relationship("Instrument", back_populates="legal_entity", passive_deletes=True, lazy='select')

class EntityAddress(Base):
    __tablename__ = "entity_addresses"
    
    id = Column(Integer, primary_key=True)
    lei = Column(String, ForeignKey('legal_entities.lei', ondelete='CASCADE'))
    type = Column(String)  # Changed from address_type
    address_lines = Column(String)  # Added
    country = Column(String)
    city = Column(String)
    region = Column(String)  # Added
    postal_code = Column(String)  # Added
    
    entity = relationship("LegalEntity", back_populates="addresses")

class EntityRegistration(Base):
    __tablename__ = "entity_registrations"
    
    lei = Column(String, ForeignKey('legal_entities.lei', ondelete='CASCADE'), primary_key=True)
    initial_date = Column(DateTime)  # Changed from registration_date
    last_update = Column(DateTime)  # Changed from last_updated
    status = Column(String)  # Changed from registration_status
    next_renewal = Column(DateTime)
    managing_lou = Column(String)
    validation_sources = Column(String)  # Added
    
    entity = relationship("LegalEntity", back_populates="registration")