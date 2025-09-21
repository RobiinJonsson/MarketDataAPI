import logging
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session, joinedload

from ...database.model_mapper import flatten_address, map_lei_record
from ...database.session import SessionLocal, get_session

# Direct model imports at module level - importing only what this service needs
from ...models.sqlite.legal_entity import (
    EntityAddress,
    EntityRegistration,
    EntityRelationship,
    LegalEntity,
)
from ..gleif import fetch_lei_info  # Re-enabled for enrichment
from ..interfaces.legal_entity_service_interface import LegalEntityServiceInterface


class LegalEntityServiceError(Exception):
    """Base exception for legal entity service errors."""

    pass


class LegalEntityService(LegalEntityServiceInterface):
    def __init__(self):
        self.database_type = "sqlite"
        self.logger = logging.getLogger(__name__)

    def get_entity(self, lei: str) -> Tuple[Session, Optional[object]]:
        """Get legal entity by LEI with all relationships eagerly loaded."""
        session = SessionLocal()
        try:
            entity = (
                session.query(LegalEntity)
                .options(
                    # Eager load addresses
                    joinedload(LegalEntity.addresses),
                    # Eager load registration
                    joinedload(LegalEntity.registration),
                    # Eager load direct parent relationship and the parent entity
                    joinedload(LegalEntity.direct_parent_relation).joinedload(
                        EntityRelationship.parent
                    ),
                    # Eager load ultimate parent relationship and the parent entity
                    joinedload(LegalEntity.ultimate_parent_relation).joinedload(
                        EntityRelationship.parent
                    ),
                    # Eager load direct children relationships and the child entities
                    joinedload(LegalEntity.direct_children_relations).joinedload(
                        EntityRelationship.child
                    ),
                    # Eager load ultimate children relationships and the child entities
                    joinedload(LegalEntity.ultimate_children_relations).joinedload(
                        EntityRelationship.child
                    ),
                    # Eager load parent exceptions
                    joinedload(LegalEntity.parent_exceptions),
                )
                .filter(LegalEntity.lei == lei)
                .first()
            )

            if entity:
                # Ensure all relationships are loaded
                session.refresh(entity)
                self.logger.info(
                    f"Loaded entity {lei} with relationships: "
                    f"addresses={len(entity.addresses) if entity.addresses else 0}, "
                    f"direct_parent={entity.direct_parent_relation is not None}, "
                    f"ultimate_parent={entity.ultimate_parent_relation is not None}, "
                    f"direct_children={len(entity.direct_children_relations) if entity.direct_children_relations else 0}, "
                    f"ultimate_children={len(entity.ultimate_children_relations) if entity.ultimate_children_relations else 0}"
                )

            return session, entity
        except Exception as e:
            self.logger.error(f"Error loading entity {lei}: {str(e)}")
            session.close()
            raise

    def get_all_entities(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Session, List[object]]:
        """
        Get all legal entities with optional pagination and filtering.

        Args:
            limit (int, optional): Maximum number of results to return
            offset (int, optional): Number of results to skip (for pagination)
            filters (dict, optional): Dictionary of filters to apply (e.g. {'status': 'ACTIVE'})

        Returns:
            tuple: (session, list of entities)
        """
        session = SessionLocal()
        try:
            query = session.query(LegalEntity)

            # Apply filters if provided
            if filters:
                filter_conditions = []
                if "status" in filters and filters["status"]:
                    filter_conditions.append(LegalEntity.status == filters["status"])
                if "jurisdiction" in filters and filters["jurisdiction"]:
                    filter_conditions.append(LegalEntity.jurisdiction == filters["jurisdiction"])

                if filter_conditions:
                    query = query.filter(and_(*filter_conditions))

            # Apply pagination
            if offset is not None:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)

            entities = query.all()
            return session, entities
        except:
            session.close()
            raise

    def create_or_update_entity(self, lei: str) -> Tuple[Session, Optional[object]]:
        """Create or update legal entity from GLEIF data."""
        # Lazy import to avoid conflicts
        from ..gleif import fetch_lei_info, sync_entity_relationships

        gleif_data = fetch_lei_info(lei)
        if not gleif_data:
            self.logger.warning(f"No GLEIF data found for LEI: {lei}")
            return None, None

        session = SessionLocal()
        try:
            mapped_data = map_lei_record(gleif_data)
            entity = self._update_entity_from_data(session, mapped_data)

            # Sync entity relationships after creating/updating the basic entity data
            self.logger.info(f"Syncing relationships for LEI: {lei}")
            relationship_results = sync_entity_relationships(session, lei)
            self.logger.debug(f"Relationship sync results for {lei}: {relationship_results}")

            session.commit()
            session.refresh(entity)  # Ensure entity is bound to session
            return session, entity
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to create/update entity {lei}: {str(e)}")
            raise LegalEntityServiceError(f"Failed to create/update entity: {str(e)}")

    def _update_entity_from_data(self, session: Session, mapped_data: Dict[str, Any]) -> object:
        """Helper to update entity from mapped data."""
        entity_data = mapped_data["lei_record"]
        lei = entity_data["lei"]

        entity = session.query(LegalEntity).filter(LegalEntity.lei == lei).first()
        if not entity:
            entity = LegalEntity(**entity_data)
            session.add(entity)
        else:
            for key, value in entity_data.items():
                setattr(entity, key, value)

        # Update relationships
        self._update_entity_addresses(entity, mapped_data["addresses"])
        self._update_entity_registration(entity, mapped_data["registration"])

        return entity

    def _update_entity_addresses(
        self, entity: object, addresses_data: List[Dict[str, Any]]
    ) -> None:
        """Helper to update entity addresses."""
        entity.addresses = []
        for addr_data in addresses_data:
            address = EntityAddress(**addr_data)
            entity.addresses.append(address)

    def _update_entity_registration(
        self, entity: object, registration_data: Dict[str, Any]
    ) -> None:
        """Helper to update entity registration."""
        if entity.registration:
            for key, value in registration_data.items():
                setattr(entity.registration, key, value)
        else:
            entity.registration = EntityRegistration(**registration_data)

    def delete_entity(self, lei: str) -> bool:
        """Delete a legal entity and its relationships."""
        session = SessionLocal()
        try:
            entity = session.query(LegalEntity).filter(LegalEntity.lei == lei).first()
            if entity:
                # First, delete any relationships where this entity is a parent or child

                # Delete relationships where this entity is a parent
                session.query(EntityRelationship).filter(
                    EntityRelationship.parent_lei == lei
                ).delete(synchronize_session=False)

                # Delete relationships where this entity is a child
                session.query(EntityRelationship).filter(
                    EntityRelationship.child_lei == lei
                ).delete(synchronize_session=False)

                # Now delete the entity itself
                session.delete(entity)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to delete entity {lei}: {str(e)}")
            raise
        finally:
            session.close()
