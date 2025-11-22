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
    instruments = relationship(
        "SqlServerInstrument", 
        back_populates="legal_entity",
        primaryjoin="SqlServerLegalEntity.lei == SqlServerInstrument.lei_id",
        foreign_keys="[SqlServerInstrument.lei_id]",
        lazy="select"
    )

    # Methods from SQLite model (if any exist, will be copied exactly)
    
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
    
    # Relationships - simplified for now, may need adjustment based on SQLite relationships
    # parent = relationship("SqlServerLegalEntity", foreign_keys=[parent_lei])
    # child = relationship("SqlServerLegalEntity", foreign_keys=[child_lei])
    
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
    lei = Column(String(20), nullable=False)
    exception_type = Column(String(30), nullable=False)  # 'DIRECT_PARENT' or 'ULTIMATE_PARENT'
    exception_category = Column(String(100), nullable=True)
    exception_reason = Column(String(200), nullable=True)
    provided_parent_lei = Column(String(20), nullable=True)  # Optional: if parent exists but doesn't have LEI
    provided_parent_name = Column(String(255), nullable=True)  # Optional: if parent exists but doesn't have LEI
    last_updated = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    # Base model columns that exist in database
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    
    __table_args__ = (
        Index("idx_lei_exception_type", "lei", "exception_type", unique=True),
        CheckConstraint(
            exception_type.in_(["DIRECT_PARENT", "ULTIMATE_PARENT"]),
            name="ck_exception_type_values",
        ),
    )