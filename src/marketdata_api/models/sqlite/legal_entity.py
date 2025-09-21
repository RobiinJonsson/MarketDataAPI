import uuid
from datetime import UTC, datetime

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

from .base_model import Base


class LegalEntity(Base):
    __tablename__ = "legal_entities"
    __table_args__ = (
        Index("idx_lei_status", "lei", "status"),
        CheckConstraint('status IN ("ACTIVE", "INACTIVE", "PENDING")', name="ck_status_values"),
        {"extend_existing": True},  # Allow table redefinition
    )

    lei = Column(String(20), primary_key=True, nullable=False)  # LEI is always 20 characters
    name = Column(String(255), nullable=False)
    jurisdiction = Column(String(5), nullable=False)  # Country codes are typically 2-5 chars
    legal_form = Column(String(255), nullable=False)
    registered_as = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False)
    bic = Column(String(11))  # BIC codes are 8-11 characters
    next_renewal_date = Column(DateTime)
    registration_status = Column(String(20), nullable=False)
    managing_lou = Column(String(20), nullable=False)
    creation_date = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))

    # Relationships - using lambda for forward references
    addresses = relationship(
        lambda: EntityAddress, back_populates="entity", cascade="all, delete-orphan"
    )
    registration = relationship(
        lambda: EntityRegistration,
        back_populates="entity",
        uselist=False,
        cascade="all, delete-orphan",
    )
    instruments = relationship(
        "marketdata_api.models.sqlite.instrument.Instrument",
        back_populates="legal_entity",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="select",
    )
    # Parent-Child relationships - using lambda for forward references
    direct_parent_relation = relationship(
        lambda: EntityRelationship,
        foreign_keys="EntityRelationship.child_lei",
        primaryjoin="and_(LegalEntity.lei==EntityRelationship.child_lei, EntityRelationship.relationship_type=='DIRECT')",
        back_populates="child",
        uselist=False,
    )

    ultimate_parent_relation = relationship(
        lambda: EntityRelationship,
        foreign_keys="EntityRelationship.child_lei",
        primaryjoin="and_(LegalEntity.lei==EntityRelationship.child_lei, EntityRelationship.relationship_type=='ULTIMATE')",
        back_populates="child",
        uselist=False,
        overlaps="direct_parent_relation",
    )

    direct_children_relations = relationship(
        lambda: EntityRelationship,
        foreign_keys="EntityRelationship.parent_lei",
        primaryjoin="and_(LegalEntity.lei==EntityRelationship.parent_lei, EntityRelationship.relationship_type=='DIRECT')",
        back_populates="parent",
    )

    ultimate_children_relations = relationship(
        lambda: EntityRelationship,
        foreign_keys="EntityRelationship.parent_lei",
        primaryjoin="and_(LegalEntity.lei==EntityRelationship.parent_lei, EntityRelationship.relationship_type=='ULTIMATE')",
        back_populates="parent",
        overlaps="direct_children_relations",
    )

    # Parent exception reporting
    parent_exceptions = relationship(
        lambda: EntityRelationshipException, back_populates="entity", cascade="all, delete-orphan"
    )

    def to_api_response(
        self, include_relationships=True, include_addresses=True, include_registration=True
    ):
        """Build comprehensive API response for Legal Entity"""
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
        if include_addresses and self.addresses:
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
        if include_registration and self.registration:
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
        if include_relationships:
            relationships = {
                "direct_parent": None,
                "ultimate_parent": None,
                "direct_children": [],
                "ultimate_children": [],
                "parent_exceptions": [],
            }

            # Direct parent
            if self.direct_parent_relation and self.direct_parent_relation.parent:
                parent = self.direct_parent_relation.parent
                relationships["direct_parent"] = {
                    "lei": parent.lei,
                    "name": parent.name,
                    "jurisdiction": parent.jurisdiction,
                    "status": parent.status,
                    "relationship_status": self.direct_parent_relation.relationship_status,
                    "relationship_period_start": (
                        self.direct_parent_relation.relationship_period_start.isoformat()
                        if self.direct_parent_relation.relationship_period_start
                        else None
                    ),
                    "relationship_period_end": (
                        self.direct_parent_relation.relationship_period_end.isoformat()
                        if self.direct_parent_relation.relationship_period_end
                        else None
                    ),
                }

            # Ultimate parent
            if self.ultimate_parent_relation and self.ultimate_parent_relation.parent:
                parent = self.ultimate_parent_relation.parent
                relationships["ultimate_parent"] = {
                    "lei": parent.lei,
                    "name": parent.name,
                    "jurisdiction": parent.jurisdiction,
                    "status": parent.status,
                    "relationship_status": self.ultimate_parent_relation.relationship_status,
                    "relationship_period_start": (
                        self.ultimate_parent_relation.relationship_period_start.isoformat()
                        if self.ultimate_parent_relation.relationship_period_start
                        else None
                    ),
                    "relationship_period_end": (
                        self.ultimate_parent_relation.relationship_period_end.isoformat()
                        if self.ultimate_parent_relation.relationship_period_end
                        else None
                    ),
                }

            # Direct children
            for relation in self.direct_children_relations:
                if relation.child:
                    child = relation.child
                    relationships["direct_children"].append(
                        {
                            "lei": child.lei,
                            "name": child.name,
                            "jurisdiction": child.jurisdiction,
                            "status": child.status,
                            "relationship_status": relation.relationship_status,
                            "relationship_period_start": (
                                relation.relationship_period_start.isoformat()
                                if relation.relationship_period_start
                                else None
                            ),
                            "relationship_period_end": (
                                relation.relationship_period_end.isoformat()
                                if relation.relationship_period_end
                                else None
                            ),
                        }
                    )

            # Ultimate children
            for relation in self.ultimate_children_relations:
                if relation.child:
                    child = relation.child
                    relationships["ultimate_children"].append(
                        {
                            "lei": child.lei,
                            "name": child.name,
                            "jurisdiction": child.jurisdiction,
                            "status": child.status,
                            "relationship_status": relation.relationship_status,
                            "relationship_period_start": (
                                relation.relationship_period_start.isoformat()
                                if relation.relationship_period_start
                                else None
                            ),
                            "relationship_period_end": (
                                relation.relationship_period_end.isoformat()
                                if relation.relationship_period_end
                                else None
                            ),
                        }
                    )

            # Parent exceptions
            for exception in self.parent_exceptions:
                relationships["parent_exceptions"].append(
                    {
                        "exception_type": exception.exception_type,
                        "exception_reason": exception.exception_reason,
                        "exception_category": exception.exception_category,
                        "provided_parent_lei": exception.provided_parent_lei,
                        "provided_parent_name": exception.provided_parent_name,
                        "last_updated": (
                            exception.last_updated.isoformat() if exception.last_updated else None
                        ),
                    }
                )

            response["relationships"] = relationships

        return response


class EntityAddress(Base):
    __tablename__ = "entity_addresses"
    __table_args__ = {"extend_existing": True}  # Allow table redefinition

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # UUID length
    lei = Column(String(20), ForeignKey("legal_entities.lei", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False)
    address_lines = Column(String(500))
    country = Column(String(5))
    city = Column(String(100))
    region = Column(String(100))
    postal_code = Column(String(20), nullable=False)

    entity = relationship(lambda: LegalEntity, back_populates="addresses")


class EntityRegistration(Base):
    __tablename__ = "entity_registrations"
    __table_args__ = {"extend_existing": True}  # Allow table redefinition

    lei = Column(String(20), ForeignKey("legal_entities.lei", ondelete="CASCADE"), primary_key=True)
    initial_date = Column(DateTime)  # Changed from registration_date
    last_update = Column(DateTime)  # Changed from last_updated
    status = Column(String(20))  # Changed from registration_status
    next_renewal = Column(DateTime)
    managing_lou = Column(String(20))
    validation_sources = Column(String(255))  # Added

    entity = relationship(lambda: LegalEntity, back_populates="registration")


class EntityRelationship(Base):
    """Represents parent-child relationships between legal entities."""

    __tablename__ = "entity_relationships"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    parent_lei = Column(
        String(20), ForeignKey("legal_entities.lei", ondelete="NO ACTION"), nullable=False
    )
    child_lei = Column(
        String(20), ForeignKey("legal_entities.lei", ondelete="NO ACTION"), nullable=False
    )
    relationship_type = Column(String(20), nullable=False)  # 'DIRECT' or 'ULTIMATE'
    relationship_status = Column(String(20), nullable=False)
    relationship_period_start = Column(DateTime, nullable=False)
    relationship_period_end = Column(DateTime)
    percentage_of_ownership = Column(Integer)  # Optional field if ownership percentage is known
    qualification_method = Column(String(100))  # How the relationship was determined
    last_updated = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))

    # Relationships
    parent = relationship(
        lambda: LegalEntity,
        foreign_keys=[parent_lei],
        primaryjoin="EntityRelationship.parent_lei==LegalEntity.lei",
        back_populates="direct_children_relations",  # This will be overridden by specific relationship types
    )

    child = relationship(
        lambda: LegalEntity,
        foreign_keys=[child_lei],
        primaryjoin="EntityRelationship.child_lei==LegalEntity.lei",
        back_populates="direct_parent_relation",  # This will be overridden by specific relationship types
    )

    __table_args__ = (
        Index("idx_parent_child", "parent_lei", "child_lei", "relationship_type", unique=True),
        CheckConstraint(
            'relationship_type IN ("DIRECT", "ULTIMATE")', name="ck_relationship_type_values"
        ),
        {"extend_existing": True},  # Allow table redefinition
    )


class EntityRelationshipException(Base):
    """Represents exceptions to reporting parent-child relationships."""

    __tablename__ = "entity_relationship_exceptions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lei = Column(String(20), ForeignKey("legal_entities.lei", ondelete="NO ACTION"), nullable=False)
    exception_type = Column(String(30), nullable=False)  # 'DIRECT_PARENT' or 'ULTIMATE_PARENT'
    exception_reason = Column(String(500), nullable=False)
    exception_category = Column(
        String(50), nullable=False
    )  # E.g., 'NO_KNOWN_PERSON', 'NATURAL_PERSONS', 'NON_CONSOLIDATING', etc.
    provided_parent_lei = Column(String(20))  # Optional: if parent exists but doesn't have LEI
    provided_parent_name = Column(String(255))  # Optional: if parent exists but doesn't have LEI
    last_updated = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))

    # Relationship
    entity = relationship(lambda: LegalEntity, back_populates="parent_exceptions")

    __table_args__ = (
        Index("idx_lei_exception_type", "lei", "exception_type", unique=True),
        CheckConstraint(
            exception_type.in_(["DIRECT_PARENT", "ULTIMATE_PARENT"]),
            name="ck_exception_type_values",
        ),
        {"extend_existing": True},  # Allow table redefinition
    )
