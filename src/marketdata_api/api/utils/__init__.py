"""
API utilities package.

This package contains common utilities and helpers for Flask-RESTX API resources,
including consolidated utility functions for instruments, MIC codes, and response building.
"""

# Import consolidated utilities for easier access
from .instrument_utils import (
    build_instrument_response,
    validate_instrument_data,
    format_instrument_list_response
)

from .mic_utils import (
    get_mic_segments_data,
    get_countries_data,
    search_mics_data,
    get_mic_statistics_data,
    load_mic_data_logic,
    get_mic_enums
)

from .response_builders import (
    build_success_response,
    build_error_response,
    build_paginated_response
)

__all__ = [
    # Instrument utilities
    'build_instrument_response',
    'validate_instrument_data', 
    'format_instrument_list_response',
    
    # MIC utilities
    'get_mic_segments_data',
    'get_countries_data',
    'search_mics_data', 
    'get_mic_statistics_data',
    'load_mic_data_logic',
    'get_mic_enums',
    
    # Response builders
    'build_success_response',
    'build_error_response', 
    'build_paginated_response'
]