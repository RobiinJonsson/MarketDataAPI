"""Instrument interface defining the contract for all instrument implementations."""

from typing import Dict, Any, Optional, List
from datetime import datetime, date
from .base_model_interface import BaseModelInterface


class InstrumentInterface(BaseModelInterface):
    """Interface for instrument models across different database implementations."""
    
    # Core identification fields
    @property
    def isin(self) -> Optional[str]:
        """ISIN identifier."""
        raise NotImplementedError("Subclasses must implement isin property")
    
    @property
    def full_name(self) -> Optional[str]:
        """Full name of the instrument."""
        raise NotImplementedError("Subclasses must implement full_name property")
    
    @property
    def short_name(self) -> Optional[str]:
        """Short name of the instrument."""
        raise NotImplementedError("Subclasses must implement short_name property")
    
    @property
    def symbol(self) -> Optional[str]:
        """Trading symbol."""
        raise NotImplementedError("Subclasses must implement symbol property")
    
    @property
    def figi(self) -> Optional[str]:
        """FIGI identifier."""
        raise NotImplementedError("Subclasses must implement figi property")
    
    @property
    def instrument_type(self) -> str:
        """Type of instrument (equity, debt, future, etc.)."""
        raise NotImplementedError("Subclasses must implement instrument_type property")
    
    # Common FIRDS fields
    @property
    def cfi_code(self) -> Optional[str]:
        """CFI code."""
        raise NotImplementedError("Subclasses must implement cfi_code property")
    
    @property
    def currency(self) -> Optional[str]:
        """Currency code."""
        raise NotImplementedError("Subclasses must implement currency property")
    
    @property
    def trading_venue(self) -> Optional[str]:
        """Trading venue."""
        raise NotImplementedError("Subclasses must implement trading_venue property")
    
    @property
    def lei_id(self) -> Optional[str]:
        """Legal Entity Identifier."""
        raise NotImplementedError("Subclasses must implement lei_id property")
    
    # Instrument type-specific methods
    def get_equity_fields(self) -> Dict[str, Any]:
        """Get equity-specific fields if this is an equity instrument."""
        raise NotImplementedError("Subclasses must implement get_equity_fields method")
    
    def get_debt_fields(self) -> Dict[str, Any]:
        """Get debt-specific fields if this is a debt instrument."""
        raise NotImplementedError("Subclasses must implement get_debt_fields method")
    
    def get_future_fields(self) -> Dict[str, Any]:
        """Get future-specific fields if this is a future instrument."""
        raise NotImplementedError("Subclasses must implement get_future_fields method")
    
    def set_equity_fields(self, data: Dict[str, Any]) -> None:
        """Set equity-specific fields."""
        raise NotImplementedError("Subclasses must implement set_equity_fields method")
    
    def set_debt_fields(self, data: Dict[str, Any]) -> None:
        """Set debt-specific fields."""
        raise NotImplementedError("Subclasses must implement set_debt_fields method")
    
    def set_future_fields(self, data: Dict[str, Any]) -> None:
        """Set future-specific fields."""
        raise NotImplementedError("Subclasses must implement set_future_fields method")
