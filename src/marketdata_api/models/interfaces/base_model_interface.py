"""Base model interface defining common fields and behavior across all instruments."""

from datetime import datetime
from typing import Any, Dict, Optional


class BaseModelInterface:
    """Base class defining the interface for all database models."""

    @property
    def id(self) -> str:
        """Unique identifier for the model."""
        raise NotImplementedError("Subclasses must implement id property")

    @property
    def created_at(self) -> datetime:
        """Timestamp when the record was created."""
        raise NotImplementedError("Subclasses must implement created_at property")

    @property
    def updated_at(self) -> datetime:
        """Timestamp when the record was last updated."""
        raise NotImplementedError("Subclasses must implement updated_at property")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the model instance to a dictionary."""
        raise NotImplementedError("Subclasses must implement to_dict method")

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Update the model instance from a dictionary."""
        raise NotImplementedError("Subclasses must implement update_from_dict method")
