"""Base instrument service interface."""

from typing import Any, Dict, List, Optional

from ...models.interfaces.instrument_interface import InstrumentInterface


class InstrumentServiceInterface:
    """Interface for instrument services across different database implementations."""

    def create_instrument(
        self, data: Dict[str, Any], instrument_type: str = "equity"
    ) -> InstrumentInterface:
        """Create a new instrument."""
        raise NotImplementedError("Subclasses must implement this method")

    def get_instruments(
        self, limit: int = 100, offset: int = 0, instrument_type: Optional[str] = None
    ) -> List[InstrumentInterface]:
        """Get a list of instruments with pagination."""
        raise NotImplementedError("Subclasses must implement this method")

    def update_instrument(
        self, instrument_id: str, data: Dict[str, Any]
    ) -> Optional[InstrumentInterface]:
        """Update an existing instrument."""
        raise NotImplementedError("Subclasses must implement this method")

    def delete_instrument(self, identifier: str, cascade: bool = False) -> bool:
        """Delete an instrument by ISIN or ID, optionally with cascade deletion of related data."""
        raise NotImplementedError("Subclasses must implement this method")

    def search_instruments(self, query: str, limit: int = 100) -> List[InstrumentInterface]:
        """Search instruments by name, symbol, or ISIN."""
        raise NotImplementedError("Subclasses must implement this method")

    def validate_instrument_data(self, data: Dict[str, Any]) -> None:
        """Validate instrument data."""
        raise NotImplementedError("Subclasses must implement this method")

    def enrich_with_figi(self, instrument: InstrumentInterface) -> InstrumentInterface:
        """Enrich instrument with FIGI data."""
        raise NotImplementedError("Subclasses must implement this method")

    def enrich_with_lei(self, instrument: InstrumentInterface) -> InstrumentInterface:
        """Enrich instrument with LEI data."""
        raise NotImplementedError("Subclasses must implement this method")

    def get_instrument(self, identifier: str):
        """Get instrument returning session and instrument (legacy compatibility)."""
        raise NotImplementedError("Subclasses must implement this method")

    def get_or_create_instrument(
        self, identifier: str, instrument_type: str
    ) -> InstrumentInterface:
        """Get existing instrument or create from FIRDS data."""
        raise NotImplementedError("Subclasses must implement this method")

    def enrich_instrument(self, instrument: InstrumentInterface):
        """Enrich instrument with external data (legacy compatibility)."""
        raise NotImplementedError("Subclasses must implement this method")
