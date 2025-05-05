"""Service loader to prevent circular imports"""

def get_instrument_service():
    from ..services.instrument_service import InstrumentService
    return InstrumentService()
