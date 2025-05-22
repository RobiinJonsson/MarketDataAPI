from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, UTC
import uuid

class LegalEntity(Base):
    __tablename__ = "legal_entities"
    
    lei = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    jurisdiction = Column(String, nullable=False)
    legal_form = Column(String, nullable=False)
    registered_as = Column(String, nullable=False)
    status = Column(String, nullable=False)
    bic = Column(String)
    next_renewal_date = Column(DateTime)
    registration_status = Column(String, nullable=False)
    managing_lou = Column(String, nullable=False)
    creation_date = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))

    __table_args__ = (
        Index('idx_lei_status', 'lei', 'status'),
        CheckConstraint(status.in_(['ACTIVE', 'INACTIVE', 'PENDING']), name='ck_status_values')
    )
    
    # Relationships
    addresses = relationship("EntityAddress", back_populates="entity", cascade="all, delete-orphan")
    registration = relationship("EntityRegistration", back_populates="entity", uselist=False, cascade="all, delete-orphan")
    instruments = relationship(
        "Instrument",
        back_populates="legal_entity",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy='select'
    )

class EntityAddress(Base):
    __tablename__ = "entity_addresses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lei = Column(String, ForeignKey('legal_entities.lei', ondelete='CASCADE'), nullable=False)
    type = Column(String, nullable=False)
    address_lines = Column(String)
    country = Column(String)
    city = Column(String)
    region = Column(String)
    postal_code = Column(String, nullable=False)
    
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