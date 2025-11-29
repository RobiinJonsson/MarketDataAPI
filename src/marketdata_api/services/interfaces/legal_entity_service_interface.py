"""Legal entity service interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session


class LegalEntityServiceInterface(ABC):
    """Interface for legal entity services."""

    @abstractmethod
    def get_entity(self, lei: str) -> Tuple[Session, Optional[object]]:
        """Get legal entity by LEI."""
        pass

    @abstractmethod
    def count_entities(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Get count of legal entities with optional filtering."""
        pass

    @abstractmethod
    def get_all_entities(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Session, List[object]]:
        """Get all legal entities with optional filtering."""
        pass

    @abstractmethod
    def create_or_update_entity(self, lei: str) -> Tuple[Session, Optional[object]]:
        """Create or update legal entity from GLEIF data."""
        pass

    @abstractmethod
    def delete_entity(self, lei: str) -> bool:
        """Delete a legal entity."""
        pass

    @abstractmethod
    def batch_fill_entity_data(self, batch_size: int = 100) -> Dict[str, Any]:
        """Fill missing entity data for instruments with LEI information from GLEIF."""
        pass
