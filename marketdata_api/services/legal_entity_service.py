from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.legal_entity import LegalEntity, EntityAddress, EntityRegistration
from ..database.model_mapper import map_lei_record, flatten_address
from ..database.session import get_session, SessionLocal
from .gleif import fetch_lei_info

class LegalEntityService:
    def __init__(self):
        pass

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

    def get_all_entities(self) -> tuple[Session, List[LegalEntity]]:
        session = SessionLocal()
        try:
            entities = session.query(LegalEntity).all()
            return session, entities
        except:
            session.close()
            raise

    def create_or_update_entity(self, lei: str) -> tuple[Session, Optional[LegalEntity]]:
        gleif_data = fetch_lei_info(lei)
        if not gleif_data:
            return None, None

        session = SessionLocal()
        try:
            # Map the data to our models
            mapped_data = map_lei_record(gleif_data)
            entity_data = mapped_data["lei_record"]
            addresses_data = mapped_data["addresses"]
            registration_data = mapped_data["registration"]

            # Create or update the entity
            entity = session.query(LegalEntity).filter(LegalEntity.lei == lei).first()
            if not entity:
                entity = LegalEntity(**entity_data)
                session.add(entity)
            else:
                for key, value in entity_data.items():
                    setattr(entity, key, value)

            # Clear existing addresses and add new ones
            entity.addresses = []
            for addr_data in addresses_data:
                address = EntityAddress(**addr_data)
                entity.addresses.append(address)

            # Update registration
            if entity.registration:
                for key, value in registration_data.items():
                    setattr(entity.registration, key, value)
            else:
                entity.registration = EntityRegistration(**registration_data)

            session.commit()
            session.refresh(entity)
            return session, entity
        except:
            session.rollback()
            raise

    def delete_entity(self, lei: str) -> bool:
        with get_session() as session:
            entity = session.query(LegalEntity).filter(LegalEntity.lei == lei).first()
            if entity:
                session.delete(entity)
                session.flush()
                return True
            return False
