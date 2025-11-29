import logging
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session, joinedload

from ...constants import RetryConfig
from ..utils.gleif import flatten_address, map_lei_record
from ...database.session import SessionLocal, get_session
from ...config import DatabaseConfig
from ..utils.gleif import fetch_lei_info  # Re-enabled for enrichment
from ..interfaces.legal_entity_service_interface import LegalEntityServiceInterface


class LegalEntityServiceError(Exception):
    """Base exception for legal entity service errors."""

    pass


class LegalEntityService(LegalEntityServiceInterface):
    _batch_operation_in_progress = False
    
    def __init__(self):
        self.database_type = DatabaseConfig.get_database_type()
        self.logger = logging.getLogger(__name__)
        
        # Dynamic model imports based on database type
        if self.database_type == 'sqlite':
            from ...models.sqlite.legal_entity import (
                EntityAddress,
                EntityRegistration,
                EntityRelationship,
                LegalEntity,
            )
            from ...models.sqlite.instrument import Instrument
        elif self.database_type in ['azure_sql', 'sqlserver', 'sql_server', 'mssql']:
            from ...models.sqlserver.legal_entity import (
                SqlServerEntityAddress as EntityAddress,
                SqlServerEntityRegistration as EntityRegistration,
                SqlServerEntityRelationship as EntityRelationship,
                SqlServerLegalEntity as LegalEntity,
            )
            from ...models.sqlserver.instrument import SqlServerInstrument as Instrument
        else:
            raise ValueError(f"Unsupported database type: {self.database_type}")
        
        self.LegalEntity = LegalEntity
        self.EntityAddress = EntityAddress
        self.EntityRegistration = EntityRegistration
        self.EntityRelationship = EntityRelationship
        self.Instrument = Instrument

    def create_basic_entity(self, lei: str) -> Tuple[Session, Optional[object]]:
        """Create basic legal entity without relationships (for instrument creation)."""
        from ..utils.gleif import fetch_lei_info
        
        gleif_data = fetch_lei_info(lei)
        if not gleif_data:
            self.logger.warning(f"No GLEIF data found for LEI: {lei}")
            return None, None
            
        session = SessionLocal()
        try:
            from ..utils.gleif import map_lei_record
            mapped_data = map_lei_record(gleif_data)
            entity_data = mapped_data["lei_record"]
            
            # Check if entity already exists
            existing_entity = session.query(self.LegalEntity).filter(self.LegalEntity.lei == lei).first()
            if existing_entity:
                self.logger.info(f"Legal entity {lei} already exists")
                return session, existing_entity
                
            # Create basic entity without relationships
            entity = self.LegalEntity(**entity_data)
            session.add(entity)
            session.commit()
            session.refresh(entity)
            
            self.logger.info(f"Created basic legal entity for LEI: {lei}")
            return session, entity
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to create basic entity {lei}: {str(e)}")
            raise LegalEntityServiceError(f"Failed to create basic entity: {str(e)}")

    def get_entity(self, lei: str) -> Tuple[Session, Optional[object]]:
        """Get legal entity by LEI with all relationships eagerly loaded."""
        session = SessionLocal()
        try:
            entity = (
                session.query(self.LegalEntity)
                .options(
                    # Eager load addresses
                    joinedload(self.LegalEntity.addresses),
                    # Eager load registration
                    joinedload(self.LegalEntity.registration),
                    # Eager load direct parent relationship and the parent entity
                    joinedload(self.LegalEntity.direct_parent_relation).joinedload(
                        self.EntityRelationship.parent
                    ),
                    # Eager load ultimate parent relationship and the parent entity
                    joinedload(self.LegalEntity.ultimate_parent_relation).joinedload(
                        self.EntityRelationship.parent
                    ),
                    # Eager load direct children relationships and the child entities
                    joinedload(self.LegalEntity.direct_children_relations).joinedload(
                        self.EntityRelationship.child
                    ),
                    # Eager load ultimate children relationships and the child entities
                    joinedload(self.LegalEntity.ultimate_children_relations).joinedload(
                        self.EntityRelationship.child
                    ),
                    # Eager load parent exceptions
                    joinedload(self.LegalEntity.parent_exceptions),
                )
                .filter(self.LegalEntity.lei == lei)
                .first()
            )

            if entity:
                # Ensure all relationships are loaded
                session.refresh(entity)
                self.logger.debug(
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
            query = session.query(self.LegalEntity)

            # Apply filters if provided
            if filters:
                filter_conditions = []
                if "status" in filters and filters["status"]:
                    filter_conditions.append(self.LegalEntity.status == filters["status"])
                if "jurisdiction" in filters and filters["jurisdiction"]:
                    filter_conditions.append(self.LegalEntity.jurisdiction == filters["jurisdiction"])

                if filter_conditions:
                    query = query.filter(and_(*filter_conditions))

            # Apply pagination with ORDER BY for SQL Server compatibility
            query = query.order_by(self.LegalEntity.lei)
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
        from ..utils.gleif import fetch_lei_info, sync_entity_relationships

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

        entity = session.query(self.LegalEntity).filter(self.LegalEntity.lei == lei).first()
        if not entity:
            entity = self.LegalEntity(**entity_data)
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
            address = self.EntityAddress(**addr_data)
            entity.addresses.append(address)

    def _update_entity_registration(
        self, entity: object, registration_data: Dict[str, Any]
    ) -> None:
        """Helper to update entity registration."""
        if entity.registration:
            for key, value in registration_data.items():
                setattr(entity.registration, key, value)
        else:
            entity.registration = self.EntityRegistration(**registration_data)

    def batch_fill_entity_data(self, batch_size: int = 100) -> Dict[str, Any]:
        """
        Fill missing entity data for instruments with LEI information from GLEIF.
        
        Robust implementation with duplicate prevention, proper error handling,
        and database lock management.
        
        Args:
            batch_size: Maximum number of instruments to process in one batch
            
        Returns:
            Dict with statistics: {"scanned": int, "updated": int, "failed": int, "skipped": int}
        """
        from ...models.sqlite.instrument import Instrument
        from ..utils.gleif import fetch_lei_info
        import time
        from sqlalchemy.exc import OperationalError
        
        # Prevent concurrent batch operations
        if LegalEntityService._batch_operation_in_progress:
            self.logger.warning("Batch entity fill already in progress, skipping request")
            return {
                "scanned": 0,
                "updated": 0,
                "failed": 1,
                "skipped": 0,
                "error": "Another batch operation is already in progress"
            }
        
        LegalEntityService._batch_operation_in_progress = True
        
        scanned = 0
        updated = 0  
        failed = 0
        skipped = 0
        
        session = SessionLocal()
        try:
            # Find instruments that have lei_id but no corresponding legal entity record
            instruments_query = session.query(self.Instrument).filter(
                self.Instrument.lei_id.isnot(None),
                ~session.query(self.LegalEntity).filter(
                    self.LegalEntity.lei == self.Instrument.lei_id
                ).exists()
            ).limit(batch_size)
            
            instruments = instruments_query.all()
            self.logger.info(f"Found {len(instruments)} instruments to process for entity data")
            
            # Process in smaller sub-batches to reduce lock contention
            processed_leis = set()  # Track processed LEIs to avoid duplicates
            
            for instrument in instruments:
                scanned += 1
                try:
                    # Get LEI from instrument (now populated during creation)
                    lei_code = instrument.lei_id
                    
                    if not lei_code or len(lei_code) != 20:
                        self.logger.debug(f"Invalid LEI for instrument {instrument.isin}: '{lei_code}'")
                        skipped += 1
                        continue
                    
                    # Skip if we've already processed this LEI in this batch
                    if lei_code in processed_leis:
                        self.logger.debug(f"LEI {lei_code} already processed in this batch, skipping")
                        skipped += 1
                        continue
                    
                    # Double-check if entity already exists (fresh query to avoid stale data)
                    existing_entity = session.query(self.LegalEntity).filter(
                        self.LegalEntity.lei == lei_code
                    ).first()
                    
                    if existing_entity:
                        self.logger.debug(f"Entity already exists for LEI {lei_code}, skipping")
                        processed_leis.add(lei_code)
                        skipped += 1
                        continue
                    
                    # Fetch entity data from GLEIF API and create entity
                    self.logger.debug(f"Fetching entity data for LEI: {lei_code}")
                    gleif_response = fetch_lei_info(lei_code)
                    
                    if isinstance(gleif_response, dict) and gleif_response.get('error'):
                        self.logger.warning(f"Failed to fetch LEI {lei_code}: {gleif_response['error']}")
                        failed += 1
                        continue
                    
                    # Create entity from GLEIF data with retry logic
                    max_retries = RetryConfig.DEFAULT_MAX_RETRIES
                    for attempt in range(max_retries):
                        try:
                            mapped_data = map_lei_record(gleif_response)
                            existing_entity = self._update_entity_from_data(session, mapped_data)
                            
                            # Commit immediately to reduce lock time
                            session.commit()
                            
                            processed_leis.add(lei_code)
                            updated += 1
                            self.logger.info(f"Created new entity for LEI: {lei_code}")
                            break
                            
                        except OperationalError as e:
                            if "database is locked" in str(e) and attempt < max_retries - 1:
                                self.logger.warning(f"Database locked, retrying in {0.5 * (attempt + 1)}s (attempt {attempt + 1}/{max_retries})")
                                session.rollback()
                                time.sleep(0.5 * (attempt + 1))  # Exponential backoff
                                continue
                            else:
                                self.logger.error(f"Failed to create entity for LEI {lei_code} after {max_retries} attempts: {str(e)}")
                                session.rollback()
                                failed += 1
                                break
                        except Exception as e:
                            self.logger.error(f"Failed to create entity for LEI {lei_code}: {str(e)}")
                            session.rollback()
                            failed += 1
                            break
                    
                except Exception as e:
                    self.logger.error(f"Error processing instrument {instrument.isin}: {str(e)}")
                    try:
                        session.rollback()
                    except:
                        pass
                    failed += 1
                    continue
            
            # Final commit for any remaining changes
            try:
                session.commit()
            except Exception as e:
                self.logger.warning(f"Final commit failed, but individual commits may have succeeded: {str(e)}")
                session.rollback()
            
            self.logger.info(f"Batch entity fill completed: {scanned} scanned, {updated} updated, {failed} failed, {skipped} skipped")
            
            return {
                "scanned": scanned,
                "updated": updated,
                "failed": failed,
                "skipped": skipped
            }
            
        except Exception as e:
            try:
                session.rollback()
            except:
                pass
            self.logger.error(f"Critical error in batch entity fill: {str(e)}")
            # Return partial results instead of raising exception
            return {
                "scanned": scanned,
                "updated": updated,
                "failed": failed + 1,  # Count this critical error
                "skipped": skipped,
                "error": str(e)
            }
        finally:
            LegalEntityService._batch_operation_in_progress = False
            session.close()

    def delete_entity(self, lei: str) -> bool:
        """Delete a legal entity and its relationships."""
        session = SessionLocal()
        try:
            entity = session.query(self.LegalEntity).filter(self.LegalEntity.lei == lei).first()
            if entity:
                # First, delete any relationships where this entity is a parent or child

                # Delete relationships where this entity is a parent
                session.query(self.EntityRelationship).filter(
                    self.EntityRelationship.parent_lei == lei
                ).delete(synchronize_session=False)

                # Delete relationships where this entity is a child
                session.query(self.EntityRelationship).filter(
                    self.EntityRelationship.child_lei == lei
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
