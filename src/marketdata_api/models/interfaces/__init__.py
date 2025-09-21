"""Base models and interfaces for the MarketData API."""

from .base_model_interface import BaseModelInterface
from .instrument_interface import InstrumentInterface

__all__ = ["InstrumentInterface", "BaseModelInterface"]
