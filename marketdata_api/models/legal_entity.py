from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, CheckConstraint, Index, Table, Boolean
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
      # Parent-Child relationships
    direct_parent_relation = relationship(
        "EntityRelationship",
        foreign_keys="EntityRelationship.child_lei",
        primaryjoin="and_(LegalEntity.lei==EntityRelationship.child_lei, EntityRelationship.relationship_type=='DIRECT')",
        back_populates="child",
        uselist=False
    )
    
    ultimate_parent_relation = relationship(
        "EntityRelationship",
        foreign_keys="EntityRelationship.child_lei",
        primaryjoin="and_(LegalEntity.lei==EntityRelationship.child_lei, EntityRelationship.relationship_type=='ULTIMATE')",
        back_populates="child",
        uselist=False,
        overlaps="direct_parent_relation"
    )
    
    direct_children_relations = relationship(
        "EntityRelationship",
        foreign_keys="EntityRelationship.parent_lei",
        primaryjoin="and_(LegalEntity.lei==EntityRelationship.parent_lei, EntityRelationship.relationship_type=='DIRECT')",
        back_populates="parent"
    )
    
    ultimate_children_relations = relationship(
        "EntityRelationship",
        foreign_keys="EntityRelationship.parent_lei",
        primaryjoin="and_(LegalEntity.lei==EntityRelationship.parent_lei, EntityRelationship.relationship_type=='ULTIMATE')",
        back_populates="parent",
        overlaps="direct_children_relations"
    )
    
    # Parent exception reporting
    parent_exceptions = relationship("EntityRelationshipException", back_populates="entity", cascade="all, delete-orphan")

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

class EntityRelationship(Base):
    """Represents parent-child relationships between legal entities."""
    __tablename__ = "entity_relationships"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    parent_lei = Column(String, ForeignKey('legal_entities.lei', ondelete='CASCADE'), nullable=False)
    child_lei = Column(String, ForeignKey('legal_entities.lei', ondelete='CASCADE'), nullable=False)
    relationship_type = Column(String, nullable=False)  # 'DIRECT' or 'ULTIMATE'
    relationship_status = Column(String, nullable=False)
    relationship_period_start = Column(DateTime, nullable=False)
    relationship_period_end = Column(DateTime)
    percentage_of_ownership = Column(Integer)  # Optional field if ownership percentage is known
    qualification_method = Column(String)  # How the relationship was determined
    last_updated = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    
    # Relationships
    parent = relationship(
        "LegalEntity", 
        foreign_keys=[parent_lei],
        primaryjoin="EntityRelationship.parent_lei==LegalEntity.lei",
        back_populates="direct_children_relations"  # This will be overridden by specific relationship types
    )
    
    child = relationship(
        "LegalEntity", 
        foreign_keys=[child_lei],
        primaryjoin="EntityRelationship.child_lei==LegalEntity.lei",
        back_populates="direct_parent_relation"  # This will be overridden by specific relationship types
    )
    
    __table_args__ = (
        Index('idx_parent_child', 'parent_lei', 'child_lei', 'relationship_type', unique=True),
        CheckConstraint(relationship_type.in_(['DIRECT', 'ULTIMATE']), name='ck_relationship_type_values')
    )

class EntityRelationshipException(Base):
    """Represents exceptions to reporting parent-child relationships."""
    __tablename__ = "entity_relationship_exceptions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lei = Column(String, ForeignKey('legal_entities.lei', ondelete='CASCADE'), nullable=False)
    exception_type = Column(String, nullable=False)  # 'DIRECT_PARENT' or 'ULTIMATE_PARENT'
    exception_reason = Column(String, nullable=False)
    exception_category = Column(String, nullable=False)  # E.g., 'NO_KNOWN_PERSON', 'NATURAL_PERSONS', 'NON_CONSOLIDATING', etc.
    provided_parent_lei = Column(String)  # Optional: if parent exists but doesn't have LEI
    provided_parent_name = Column(String)  # Optional: if parent exists but doesn't have LEI
    last_updated = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    
    # Relationship
    entity = relationship("LegalEntity", back_populates="parent_exceptions")
    
    __table_args__ = (
        Index('idx_lei_exception_type', 'lei', 'exception_type', unique=True),
        CheckConstraint(exception_type.in_(['DIRECT_PARENT', 'ULTIMATE_PARENT']), name='ck_exception_type_values')
    )