"""SQL Server legal entity models."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base_model import SqlServerBaseModel


class SqlServerLegalEntity(SqlServerBaseModel):
    """SQL Server legal entity model."""
    
    __tablename__ = "legal_entities"
    
    # Primary identification
    lei = Column(String(20), primary_key=True)
    legal_name = Column(String(500), nullable=True)
    legal_form = Column(String(100), nullable=True)
    
    # Status information
    entity_status = Column(String(20), nullable=True)
    entity_expiration_date = Column(DateTime, nullable=True)
    entity_expiration_reason = Column(String(100), nullable=True)
    
    # Registration information
    registration_status = Column(String(20), nullable=True)
    next_renewal_date = Column(DateTime, nullable=True)
    managing_lou = Column(String(20), nullable=True)
    
    # Validation information
    validation_sources = Column(String(20), nullable=True)
    validation_authority_id = Column(String(100), nullable=True)
    validation_authority_entity_id = Column(String(100), nullable=True)
    
    # Additional data
    other_entity_names = Column(Text, nullable=True)
    transliterated_other_entity_names = Column(Text, nullable=True)
    
    # Relationships
    addresses = relationship("SqlServerEntityAddress", back_populates="entity", cascade="all, delete-orphan")
    instruments = relationship("SqlServerInstrument", back_populates="legal_entity")


class SqlServerEntityAddress(SqlServerBaseModel):
    """SQL Server entity address model."""
    
    __tablename__ = "entity_addresses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lei = Column(String(20), ForeignKey("legal_entities.lei", ondelete="CASCADE"), nullable=False)
    address_type = Column(String(50), nullable=True)  # LEGAL_ADDRESS, HEADQUARTERS_ADDRESS
    
    # Address components
    first_address_line = Column(String(300), nullable=True)
    additional_address_line = Column(String(300), nullable=True)
    city = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    country = Column(String(2), nullable=True)
    postal_code = Column(String(20), nullable=True)  # Made nullable
    
    # Relationship
    entity = relationship("SqlServerLegalEntity", back_populates="addresses")


class SqlServerEntityRegistration(SqlServerBaseModel):
    """SQL Server entity registration model."""
    
    __tablename__ = "entity_registrations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lei = Column(String(20), ForeignKey("legal_entities.lei", ondelete="CASCADE"), nullable=False)
    
    # Registration details
    initial_registration_date = Column(DateTime, nullable=True)
    last_update_date = Column(DateTime, nullable=True)
    registration_status = Column(String(20), nullable=True)
    next_renewal_date = Column(DateTime, nullable=True)
    
    # Authority information
    managing_lou = Column(String(20), nullable=True)
    validation_sources = Column(String(20), nullable=True)


class SqlServerEntityRelationship(SqlServerBaseModel):
    """SQL Server entity relationship model."""
    
    __tablename__ = "entity_relationships"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    start_node_lei = Column(String(20), nullable=False)
    end_node_lei = Column(String(20), nullable=False)
    relationship_type = Column(String(50), nullable=True)
    relationship_status = Column(String(20), nullable=True)


class SqlServerEntityRelationshipException(SqlServerBaseModel):
    """SQL Server entity relationship exception model."""
    
    __tablename__ = "entity_relationship_exceptions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lei = Column(String(20), nullable=False)
    exception_category = Column(String(100), nullable=True)
    exception_reason = Column(String(200), nullable=True)