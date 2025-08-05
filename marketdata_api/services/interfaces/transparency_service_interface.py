"""Transparency service interface."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class TransparencyServiceInterface(ABC):
    """Interface for transparency services."""
    
    @abstractmethod
    def validate_transparency_data(self, data: Dict[str, Any]) -> None:
        """Validate required transparency data fields."""
        pass
    
    @abstractmethod
    def create_transparency_calculation(self, data: Dict[str, Any], calculation_type: str = "NON_EQUITY") -> object:
        """Create a new transparency calculation."""
        pass
    
    @abstractmethod
    def get_transparency_by_isin(self, isin: str) -> Optional[List[object]]:
        """Get transparency calculations for an ISIN."""
        pass
    
    @abstractmethod
    def delete_transparency_calculation(self, calc_id: str) -> bool:
        """Delete a transparency calculation."""
        pass
