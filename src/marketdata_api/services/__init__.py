"""MarketDataAPI Services Package

Organized service modules:
- core/: Database-agnostic business logic services
- interfaces/: Service interface definitions  
- utils/: Utility services and helper functions

Backward compatibility:
- sqlite/: Compatibility aliases for legacy tests
"""

# Import core services
from .core import InstrumentService, LegalEntityService, TransparencyService, VenueService

# Import utility services  
from .utils import EsmaDataLoader, MICDataLoader

# Create backward compatibility namespace
class SqliteCompatModule:
    """Compatibility module for old sqlite-specific imports"""
    def __init__(self):
        # Import the services from their new locations
        from .core.instrument_service import InstrumentService as CoreInstrumentService
        from .core.legal_entity_service import LegalEntityService as CoreLegalEntityService
        from ..database.session import get_session
        
        # Create compatibility classes
        self.instrument_service = type('instrument_service', (), {
            'InstrumentService': CoreInstrumentService,
            'get_session': get_session
        })()
        
        self.legal_entity_service = type('legal_entity_service', (), {
            'LegalEntityService': CoreLegalEntityService,
            'get_session': get_session
        })()

# Create the sqlite compatibility namespace
import sys
sqlite_compat = SqliteCompatModule()
sys.modules[__name__ + '.sqlite'] = sqlite_compat
sys.modules[__name__ + '.sqlite.instrument_service'] = sqlite_compat.instrument_service
sys.modules[__name__ + '.sqlite.legal_entity_service'] = sqlite_compat.legal_entity_service

__all__ = [
    # Core services
    "InstrumentService",
    "LegalEntityService", 
    "TransparencyService",
    "VenueService",
    
    # Utility services
    "EsmaDataLoader",
    "MICDataLoader",
    
    # Compatibility
    "sqlite",
]