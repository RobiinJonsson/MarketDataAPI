"""
Core CLI utilities and shared functionality.
"""
from .utils import console, check_database_initialized, handle_database_error
from .config import CLIConfig

__all__ = ['console', 'check_database_initialized', 'handle_database_error', 'CLIConfig']