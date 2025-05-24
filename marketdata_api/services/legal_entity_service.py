import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from ..models.legal_entity import LegalEntity, EntityAddress, EntityRegistration
from ..database.model_mapper import map_lei_record, flatten_address
from ..database.session import get_session, SessionLocal
from .gleif import fetch_lei_info

class LegalEntityServiceError(Exception):
    """Base exception for legal entity service errors."""
    pass

class LegalEntityService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_entity(self, lei: str) -> tuple[Session, Optional[LegalEntity]]:
        session = SessionLocal()
        try:
            entity = session.query(LegalEntity).filter(LegalEntity.lei == lei).first()
            if entity:
                session.refresh(entity)
            return session, entity
        except:
            session.close()
            raise

    def get_all_entities(self, limit: Optional[int] = None, offset: Optional[int] = None, filters: Optional[Dict[str, Any]] = None) -> tuple[Session, List[LegalEntity]]:
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
                if 'status' in filters and filters['status']:
                    filter_conditions.append(LegalEntity.status == filters['status'])
                if 'jurisdiction' in filters and filters['jurisdiction']:
                    filter_conditions.append(LegalEntity.jurisdiction == filters['jurisdiction'])
                
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

    def create_or_update_entity(self, lei: str) -> tuple[Session, Optional[LegalEntity]]:
        """Create or update legal entity from GLEIF data."""
        gleif_data = fetch_lei_info(lei)
        if not gleif_data:
            self.logger.warning(f"No GLEIF data found for LEI: {lei}")
            return None, None

        with get_session() as session:
            try:
                mapped_data = map_lei_record(gleif_data)
                entity = self._update_entity_from_data(session, mapped_data)
                return session, entity
            except Exception as e:
                self.logger.error(f"Failed to create/update entity {lei}: {str(e)}")
                raise LegalEntityServiceError(f"Failed to create/update entity: {str(e)}")

    def _update_entity_from_data(self, session: Session, mapped_data: Dict[str, Any]) -> LegalEntity:
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

    def _update_entity_addresses(self, entity: LegalEntity, addresses_data: List[Dict[str, Any]]) -> None:
        """Helper to update entity addresses."""
        entity.addresses = []
        for addr_data in addresses_data:
            address = EntityAddress(**addr_data)
            entity.addresses.append(address)

    def _update_entity_registration(self, entity: LegalEntity, registration_data: Dict[str, Any]) -> None:
        """Helper to update entity registration."""
        if entity.registration:
            for key, value in registration_data.items():
                setattr(entity.registration, key, value)
        else:
            entity.registration = EntityRegistration(**registration_data)

    def delete_entity(self, lei: str) -> bool:
        with get_session() as session:
            entity = session.query(LegalEntity).filter(LegalEntity.lei == lei).first()
            if entity:
                session.delete(entity)
                session.flush()
                return True
            return False
