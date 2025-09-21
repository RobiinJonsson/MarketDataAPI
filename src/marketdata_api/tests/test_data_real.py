"""
Real test data provider for MarketDataAPI tests.

Provides real data samples from the database and hardcoded known-good data
that works with actual services and external APIs.
"""

from typing import Any, Dict, List, Optional

# REAL DATA SAMPLES FROM DATABASE
# These are actual instruments in your database that can be used for testing

KNOWN_INSTRUMENTS = {
    "SE0000120784": {
        "isin": "SE0000120784",
        "full_name": "Skandinaviska Enskilda Banken AB",
        "short_name": "SEB/SH C",
        "instrument_type": "equity",
        "currency": "SEK",
        "country_of_incorporation": "SE",
        "venue_mic": "XSTO",
        "cfi_code": "ESVUFR",
        "lei_id": "213800WAVVOPS85N2205",
    },
    "CH0012221716": {
        "isin": "CH0012221716",
        "full_name": "ABB Ltd",
        "short_name": "ABB",
        "instrument_type": "equity",
        "currency": "CHF",
        "country_of_incorporation": "CH",
        "venue_mic": "XSWX",
        "cfi_code": "ESVUFR",
        "lei_id": "CH0244767585X6ZG5O6858",
    },
    "SE0007100581": {
        "isin": "SE0007100581",
        "full_name": "Assa Abloy AB",
        "short_name": "ASSA B",
        "instrument_type": "equity",
        "currency": "SEK",
        "country_of_incorporation": "SE",
        "venue_mic": "XSTO",
    },
    "GB0009895292": {
        "isin": "GB0009895292",
        "full_name": "AstraZeneca PLC",
        "short_name": "AZN",
        "instrument_type": "equity",
        "currency": "USD",
        "country_of_incorporation": "GB",
        "venue_mic": "XLON",
    },
    "XS2908107019": {
        "isin": "XS2908107019",
        "full_name": "ING Bank N.V. EO-M.-T. Mortg.Cov.Bds 24(29)",
        "short_name": "ING 24/29",
        "instrument_type": "debt",
        "currency": "EUR",
        "country_of_incorporation": "NL",
    },
}

KNOWN_LEGAL_ENTITIES = {
    "213800WAVVOPS85N2205": {
        "lei": "213800WAVVOPS85N2205",
        "name": "Skandinaviska Enskilda Banken AB",
        "jurisdiction": "SE",
        "legal_form": "Aktiebolag",
        "status": "ACTIVE",
    },
    "CH0244767585X6ZG5O6858": {
        "lei": "CH0244767585X6ZG5O6858",
        "name": "ABB Ltd",
        "jurisdiction": "CH",
        "legal_form": "Corporation",
        "status": "ACTIVE",
    },
}

KNOWN_MIC_CODES = {
    "XSTO": {
        "mic": "XSTO",
        "operating_mic_name": "NASDAQ STOCKHOLM AB",
        "country_code": "SE",
        "city": "STOCKHOLM",
        "website": "WWW.NASDAQOMXNORDIC.COM",
    },
    "XSWX": {
        "mic": "XSWX",
        "operating_mic_name": "SIX SWISS EXCHANGE AG",
        "country_code": "CH",
        "city": "ZURICH",
        "website": "WWW.SIX-SWISS-EXCHANGE.COM",
    },
    "XLON": {
        "mic": "XLON",
        "operating_mic_name": "LONDON STOCK EXCHANGE PLC",
        "country_code": "GB",
        "city": "LONDON",
        "website": "WWW.LONDONSTOCKEXCHANGE.COM",
    },
}


class RealTestDataProvider:
    """Provider for real test data that can be used across different test scenarios."""

    @staticmethod
    def get_instruments(limit: int = None) -> List[Dict[str, Any]]:
        """Get list of known instruments."""
        instruments = list(KNOWN_INSTRUMENTS.values())
        return instruments[:limit] if limit else instruments

    @staticmethod
    def get_legal_entities(limit: int = None) -> List[Dict[str, Any]]:
        """Get list of known legal entities."""
        entities = list(KNOWN_LEGAL_ENTITIES.values())
        return entities[:limit] if limit else entities

    @staticmethod
    def get_mic_codes(limit: int = None) -> List[Dict[str, Any]]:
        """Get list of known MIC codes."""
        mics = list(KNOWN_MIC_CODES.values())
        return mics[:limit] if limit else mics


def get_test_instrument(isin: str = None) -> Dict[str, Any]:
    """Get a test instrument by ISIN or return the first available one."""
    if isin and isin in KNOWN_INSTRUMENTS:
        return KNOWN_INSTRUMENTS[isin]
    return list(KNOWN_INSTRUMENTS.values())[0]


def get_test_isin(index: int = 0) -> str:
    """Get a test ISIN by index."""
    isins = list(KNOWN_INSTRUMENTS.keys())
    return isins[index] if index < len(isins) else isins[0]


def get_test_lei(index: int = 0) -> str:
    """Get a test LEI by index."""
    leis = list(KNOWN_LEGAL_ENTITIES.keys())
    return leis[index] if index < len(leis) else leis[0]


def get_test_mic(index: int = 0) -> str:
    """Get a test MIC by index."""
    mics = list(KNOWN_MIC_CODES.keys())
    return mics[index] if index < len(mics) else mics[0]


def get_test_mic_code(index: int = 0) -> str:
    """Get a test MIC code by index (alias for get_test_mic)."""
    return get_test_mic(index)


# Commonly used test values
TEST_ISIN = "SE0000120784"
TEST_LEI = "213800WAVVOPS85N2205"
TEST_MIC = "XSTO"

# Test data for specific scenarios
EQUITY_INSTRUMENTS = {
    k: v for k, v in KNOWN_INSTRUMENTS.items() if v["instrument_type"] == "equity"
}
DEBT_INSTRUMENTS = {k: v for k, v in KNOWN_INSTRUMENTS.items() if v["instrument_type"] == "debt"}
NORDIC_INSTRUMENTS = {
    k: v
    for k, v in KNOWN_INSTRUMENTS.items()
    if v.get("country_of_incorporation") in ["SE", "NO", "DK", "FI"]
}
