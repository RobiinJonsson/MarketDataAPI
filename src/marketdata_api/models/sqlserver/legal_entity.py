"""SQL Server legal entity models - EXACT copy of SQLite schema."""

import uuid
from datetime import UTC, datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import relationship

from .base_model import SqlServerBaseModel, SqlServerBase


class SqlServerLegalEntity(SqlServerBase):
    """SQL Server legal entity model - exact database schema match."""
    
    __tablename__ = "legal_entities"
    __table_args__ = (
        Index("idx_lei_status", "lei", "status"),
        CheckConstraint('status IN (\'ACTIVE\', \'INACTIVE\', \'PENDING\')', name="ck_status_values"),
    )

    # EXACT column match to database schema
    lei = Column(String(20), primary_key=True, nullable=False)  # LEI is always 20 characters
    name = Column(String(255), nullable=False)
    jurisdiction = Column(String(5), nullable=False)  # Country codes are typically 2-5 chars
    legal_form = Column(String(255), nullable=False)
    registered_as = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False)
    bic = Column(String(1000))  # Multiple BIC codes separated by commas - increased size
    next_renewal_date = Column(DateTime)
    registration_status = Column(String(20), nullable=False)
    managing_lou = Column(String(20), nullable=False)
    creation_date = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    # Base model columns that exist in database
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))

    # Relationships (SQL Server version)
    addresses = relationship(
        lambda: SqlServerEntityAddress, back_populates="entity", cascade="all, delete-orphan"
    )
    registration = relationship(
        lambda: SqlServerEntityRegistration,
        back_populates="entity", 
        uselist=False,
        cascade="all, delete-orphan",
    )
    instruments = relationship(
        "SqlServerInstrument", 
        back_populates="legal_entity",
        primaryjoin="SqlServerLegalEntity.lei == SqlServerInstrument.lei_id",
        foreign_keys="[SqlServerInstrument.lei_id]",
        lazy="select"
    )

    # Parent-Child relationships - using lambda for forward references
    direct_parent_relation = relationship(
        lambda: SqlServerEntityRelationship,
        foreign_keys="SqlServerEntityRelationship.child_lei",
        primaryjoin="and_(SqlServerLegalEntity.lei==SqlServerEntityRelationship.child_lei, SqlServerEntityRelationship.relationship_type=='DIRECT')",
        back_populates="child",
        uselist=False,
    )

    ultimate_parent_relation = relationship(
        lambda: SqlServerEntityRelationship,
        foreign_keys="SqlServerEntityRelationship.child_lei",
        primaryjoin="and_(SqlServerLegalEntity.lei==SqlServerEntityRelationship.child_lei, SqlServerEntityRelationship.relationship_type=='ULTIMATE')",
        back_populates="child",
        uselist=False,
        overlaps="direct_parent_relation",
    )

    direct_children_relations = relationship(
        lambda: SqlServerEntityRelationship,
        foreign_keys="SqlServerEntityRelationship.parent_lei", 
        primaryjoin="and_(SqlServerLegalEntity.lei==SqlServerEntityRelationship.parent_lei, SqlServerEntityRelationship.relationship_type=='DIRECT')",
        back_populates="parent",
        overlaps="ultimate_parent_relation,direct_parent_relation",
    )

    ultimate_children_relations = relationship(
        lambda: SqlServerEntityRelationship,
        foreign_keys="SqlServerEntityRelationship.parent_lei",
        primaryjoin="and_(SqlServerLegalEntity.lei==SqlServerEntityRelationship.parent_lei, SqlServerEntityRelationship.relationship_type=='ULTIMATE')",
        back_populates="parent",
        overlaps="direct_children_relations,ultimate_parent_relation,direct_parent_relation",
    )

    # Parent exception reporting
    parent_exceptions = relationship(
        lambda: SqlServerEntityRelationshipException, back_populates="entity", cascade="all, delete-orphan"
    )

    # Methods from SQLite model (copied exactly)
    def to_api_response(
        self, include_relationships=True, include_addresses=True, include_registration=True
    ):
        """Build comprehensive API response for Legal Entity - SQL Server version"""
        response = {
            "lei": self.lei,
            "name": self.name,
            "jurisdiction": self.jurisdiction,
            "legal_form": self.legal_form,
            "registered_as": self.registered_as,
            "status": self.status,
            "bic": self.bic,
            "next_renewal_date": (
                self.next_renewal_date.isoformat() if self.next_renewal_date else None
            ),
            "registration_status": self.registration_status,
            "managing_lou": self.managing_lou,
            "creation_date": self.creation_date.isoformat() if self.creation_date else None,
        }

        # Include addresses if requested and available
        if include_addresses and hasattr(self, 'addresses') and self.addresses:
            response["addresses"] = []
            for address in self.addresses:
                response["addresses"].append(
                    {
                        "id": address.id,
                        "type": address.type,
                        "address_lines": address.address_lines,
                        "country": address.country,
                        "city": address.city,
                        "region": address.region,
                        "postal_code": address.postal_code,
                    }
                )

        # Include registration details if requested and available
        if include_registration and hasattr(self, 'registration') and self.registration:
            registration = self.registration
            response["registration"] = {
                "initial_date": (
                    registration.initial_date.isoformat() if registration.initial_date else None
                ),
                "last_update": (
                    registration.last_update.isoformat() if registration.last_update else None
                ),
                "status": registration.status,
                "next_renewal": (
                    registration.next_renewal.isoformat() if registration.next_renewal else None
                ),
                "managing_lou": registration.managing_lou,
                "validation_sources": registration.validation_sources,
            }

        # Include parent-child relationships if requested
        # Note: SQL Server model may have different relationship attribute names
        # For now, provide empty relationships structure to maintain API compatibility
        if include_relationships:
            relationships = {
                "direct_parent": None,
                "ultimate_parent": None,
                "direct_children": [],
                "ultimate_children": [],
                "parent_exceptions": [],
            }
            
            # TODO: Implement relationship loading for SQL Server model when relationship
            # attributes are properly mapped (direct_parent_relation, etc.)
            response["relationships"] = relationships

        return response
    
    # Relationships (EXACT match to SQLite model)
    registration = relationship(
        "SqlServerEntityRegistration",
        uselist=False,
        back_populates="entity",
        cascade="all, delete-orphan"
    )
    addresses = relationship("SqlServerEntityAddress", back_populates="entity", cascade="all, delete-orphan")


class SqlServerEntityAddress(SqlServerBaseModel):
    """SQL Server entity address model - EXACT match to SQLite EntityAddress."""
    
    __tablename__ = "entity_addresses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lei = Column(String(20), ForeignKey("legal_entities.lei", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False)  # EXACT match to SQLite model
    address_lines = Column(String(500))
    country = Column(String(5))
    city = Column(String(100))
    region = Column(String(100))
    postal_code = Column(String(20), nullable=True)
    
    # Relationship
    entity = relationship("SqlServerLegalEntity", back_populates="addresses")


class SqlServerEntityRegistration(SqlServerBaseModel):
    """SQL Server entity registration model."""
    
    __tablename__ = "entity_registrations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lei = Column(String(20), ForeignKey("legal_entities.lei", ondelete="CASCADE"), nullable=False)
    
    # Registration details (EXACT match to SQLite EntityRegistration)
    initial_date = Column(DateTime, nullable=True)
    last_update = Column(DateTime, nullable=True)  
    status = Column(String(20), nullable=True)
    next_renewal = Column(DateTime, nullable=True)
    
    # Authority information
    managing_lou = Column(String(20), nullable=True)
    validation_sources = Column(String(255), nullable=True)  # EXACT match to SQLite
    
    # Relationship
    entity = relationship("SqlServerLegalEntity", back_populates="registration")


class SqlServerEntityRelationship(SqlServerBaseModel):
    """SQL Server entity relationship model - EXACT match to SQLite EntityRelationship."""
    
    __tablename__ = "entity_relationships"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    parent_lei = Column(String(20), nullable=False)  # Removed FK constraint
    child_lei = Column(String(20), nullable=False)   # Removed FK constraint
    relationship_type = Column(String(20), nullable=False)  # 'DIRECT' or 'ULTIMATE'
    relationship_status = Column(String(20), nullable=False)
    relationship_period_start = Column(DateTime, nullable=False)
    relationship_period_end = Column(DateTime, nullable=True)
    percentage_of_ownership = Column(Integer, nullable=True)  # Optional field if ownership percentage is known
    qualification_method = Column(String(100), nullable=True)  # How the relationship was determined
    last_updated = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    
    # Relationships - match SQLite EntityRelationship exactly
    parent = relationship(
        lambda: SqlServerLegalEntity,
        foreign_keys=[parent_lei],
        primaryjoin="SqlServerEntityRelationship.parent_lei==SqlServerLegalEntity.lei",
        back_populates="direct_children_relations",  # This will be overridden by specific relationship types
    )

    child = relationship(
        lambda: SqlServerLegalEntity,
        foreign_keys=[child_lei],
        primaryjoin="SqlServerEntityRelationship.child_lei==SqlServerLegalEntity.lei",
        back_populates="direct_parent_relation",  # This will be overridden by specific relationship types
    )
    
    __table_args__ = (
        Index("idx_parent_child", "parent_lei", "child_lei", "relationship_type", unique=True),
        CheckConstraint(
            'relationship_type IN ("DIRECT", "ULTIMATE")', name="ck_relationship_type_values"
        ),
    )


class SqlServerEntityRelationshipException(SqlServerBase):
    """SQL Server entity relationship exception model - exact database schema match."""
    
    __tablename__ = "entity_relationship_exceptions"
    
    # All columns must match the actual database schema exactly
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lei = Column(String(20), ForeignKey("legal_entities.lei", ondelete="NO ACTION"), nullable=False)
    exception_type = Column(String(30), nullable=False)  # 'DIRECT_PARENT' or 'ULTIMATE_PARENT'
    exception_category = Column(String(100), nullable=True)
    exception_reason = Column(String(200), nullable=True)
    provided_parent_lei = Column(String(20), nullable=True)  # Optional: if parent exists but doesn't have LEI
    provided_parent_name = Column(String(255), nullable=True)  # Optional: if parent exists but doesn't have LEI
    last_updated = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    # Base model columns that exist in database
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    
    # Relationship to legal entity
    entity = relationship(lambda: SqlServerLegalEntity, back_populates="parent_exceptions")
    
    __table_args__ = (
        Index("idx_lei_exception_type", "lei", "exception_type", unique=True),
        CheckConstraint(
            exception_type.in_(["DIRECT_PARENT", "ULTIMATE_PARENT"]),
            name="ck_exception_type_values",
        ),
    )