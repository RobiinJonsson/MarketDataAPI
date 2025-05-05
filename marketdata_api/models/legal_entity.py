from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, UTC

class LegalEntity(Base):
    __tablename__ = "legal_entities"
    
    lei = Column(String, primary_key=True)
    legal_name = Column(String)
    legal_jurisdiction = Column(String)
    legal_form_id = Column(String)
    status = Column(String)
    creation_date = Column(DateTime, default=lambda: datetime.now(UTC))
    
    # Relationships
    addresses = relationship("EntityAddress", back_populates="entity", cascade="all, delete-orphan")
    registration = relationship("EntityRegistration", back_populates="entity", uselist=False, cascade="all, delete-orphan")
    instruments = relationship("Instrument", back_populates="legal_entity", passive_deletes=True, lazy='select')

class EntityAddress(Base):
    __tablename__ = "entity_addresses"
    
    id = Column(Integer, primary_key=True)
    lei = Column(String, ForeignKey('legal_entities.lei', ondelete='CASCADE'))
    address_type = Column(String)
    country = Column(String)
    city = Column(String)
    
    entity = relationship("LegalEntity", back_populates="addresses")

class EntityRegistration(Base):
    __tablename__ = "entity_registrations"
    
    lei = Column(String, ForeignKey('legal_entities.lei', ondelete='CASCADE'), primary_key=True)
    registration_status = Column(String)
    registration_date = Column(DateTime)
    last_updated = Column(DateTime, default=lambda: datetime.now(UTC))
    
    entity = relationship("LegalEntity", back_populates="registration")