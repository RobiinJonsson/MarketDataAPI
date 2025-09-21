"""SQLite models - Import all models together to ensure relationship resolution."""

# Import all models in the correct order to ensure relationships are resolved
from .base_model import Base
from .legal_entity import LegalEntity, EntityAddress, EntityRegistration, EntityRelationship, EntityRelationshipException
from .figi import FigiMapping
from .transparency import TransparencyCalculation
from .market_identification_code import MarketIdentificationCode
from .instrument import Instrument, TradingVenue

# Export all models
__all__ = [
    'Base',
    'LegalEntity', 
    'EntityAddress', 
    'EntityRegistration', 
    'EntityRelationship',
    'EntityRelationshipException',
    'FigiMapping',
    'TransparencyCalculation',
    'MarketIdentificationCode',
    'Instrument',
    'TradingVenue'
]
