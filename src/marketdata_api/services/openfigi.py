"""
Simplified OpenFIGI Service

This service implements a clean two-stage search strategy:
1. ISIN + MIC code (venue-specific search)
2. ISIN only (broad search if venue-specific fails)

The MIC code is always provided externally from FIRDS data, never generated internally.
All FIGI results are stored and linked to the ISIN for later exchange code handling.
"""

import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests

logger = logging.getLogger(__name__)


@dataclass
class OpenFIGISearchResult:
    """Structured result from OpenFIGI search"""

    figi: str
    name: Optional[str] = None
    ticker: Optional[str] = None
    exch_code: Optional[str] = None
    security_type: Optional[str] = None
    market_sector: Optional[str] = None
    composite_figi: Optional[str] = None
    share_class_figi: Optional[str] = None
    currency: Optional[str] = None
    security_description: Optional[str] = None
    search_strategy: str = None  # 'mic_specific' or 'broad_search'


class OpenFIGIService:
    """Simplified OpenFIGI service with two-stage search strategy"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENFIGI_API_KEY")
        self.base_url = "https://api.openfigi.com/v3/mapping"

    def search_figi(self, isin: str, mic_code: str) -> Tuple[List[OpenFIGISearchResult], str]:
        """
        Search OpenFIGI with two-stage approach:
        1. ISIN + MIC code (venue-specific)
        2. ISIN only (broad search) if venue-specific fails

        Args:
            isin: ISIN to search for
            mic_code: MIC code from FIRDS (always provided externally)

        Returns:
            Tuple of (results_list, search_strategy_used)
        """

        logger.info(f"Starting OpenFIGI search for ISIN {isin} with MIC {mic_code}")

        # Stage 1: Try ISIN + MIC code (venue-specific search)
        results = self._search_with_mic(isin, mic_code)
        if results:
            logger.info(f"✅ Success with venue-specific search (MIC: {mic_code})")
            for result in results:
                result.search_strategy = "mic_specific"
            return results, "mic_specific"

        # Stage 2: Try ISIN only (broad search)
        logger.info(f"🔄 Venue-specific search failed, trying broad search for ISIN {isin}")
        results = self._search_broad(isin)
        if results:
            logger.info(f"✅ Success with broad search")
            for result in results:
                result.search_strategy = "broad_search"
            return results, "broad_search"

        logger.warning(f"❌ Both search strategies failed for ISIN {isin}")
        return [], "no_results"

    def _search_with_mic(self, isin: str, mic_code: str) -> List[OpenFIGISearchResult]:
        """Search using ISIN + MIC code"""
        payload = [{"idType": "ID_ISIN", "idValue": isin, "micCode": mic_code}]

        logger.debug(f"OpenFIGI MIC-specific request: ISIN={isin}, MIC={mic_code}")
        return self._execute_search(payload)

    def _search_broad(self, isin: str) -> List[OpenFIGISearchResult]:
        """Search using ISIN only (no venue restrictions)"""
        payload = [{"idType": "ID_ISIN", "idValue": isin}]

        logger.debug(f"OpenFIGI broad request: ISIN={isin}")
        return self._execute_search(payload)

    def _execute_search(self, payload: List[Dict]) -> List[OpenFIGISearchResult]:
        """Execute the actual API request"""
        try:
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["X-OPENFIGI-APIKEY"] = self.api_key

            response = requests.post(self.base_url, json=payload, headers=headers, timeout=30)

            if response.status_code == 200:
                data = response.json()
                logger.debug(f"OpenFIGI response: {data}")

                if data and len(data) > 0:
                    # Check for successful response with data
                    if "data" in data[0] and data[0]["data"]:
                        # Return ALL results (multiple FIGIs for the same ISIN)
                        return [self._parse_figi_result(item) for item in data[0]["data"]]
                    elif "error" in data[0]:
                        logger.debug(f"OpenFIGI error response: {data[0]['error']}")
                    elif "warning" in data[0]:
                        logger.debug(f"OpenFIGI warning: {data[0]['warning']}")
            else:
                logger.warning(f"OpenFIGI HTTP error: {response.status_code} - {response.text}")

        except Exception as e:
            logger.error(f"OpenFIGI request failed: {str(e)}")

        return []

    def _parse_figi_result(self, figi_data: Dict) -> OpenFIGISearchResult:
        """Parse FIGI API response into structured result"""
        return OpenFIGISearchResult(
            figi=figi_data.get("figi"),
            name=figi_data.get("name"),
            ticker=figi_data.get("ticker"),
            exch_code=figi_data.get("exchCode"),  # This comes from the API response
            security_type=figi_data.get("securityType"),
            market_sector=figi_data.get("marketSector"),
            composite_figi=figi_data.get("compositeFIGI"),
            share_class_figi=figi_data.get("shareClassFIGI"),
            currency=figi_data.get("currency"),
            security_description=figi_data.get("securityDescription"),
        )

    def batch_search(
        self, search_requests: List[Tuple[str, str]], rate_limit_delay: float = 2.5
    ) -> List[Tuple[str, str, List[OpenFIGISearchResult], str]]:
        """
        Batch search for multiple ISIN + MIC combinations

        Args:
            search_requests: List of (isin, mic_code) tuples
            rate_limit_delay: Delay between requests in seconds

        Returns:
            List of tuples: (isin, mic_code, results, search_strategy)
        """
        import time

        results = []

        for i, (isin, mic_code) in enumerate(search_requests):
            logger.info(f"Processing batch item {i+1}/{len(search_requests)}: {isin}")

            figi_results, strategy = self.search_figi(isin, mic_code)
            results.append((isin, mic_code, figi_results, strategy))

            # Rate limiting (except for the last request)
            if i < len(search_requests) - 1:
                time.sleep(rate_limit_delay)

        return results


# Convenience function for easy integration with existing code
def search_openfigi_simplified(isin: str, mic_code: str) -> Dict[str, Any]:
    """
    Simplified OpenFIGI search function for easy integration.

    Args:
        isin: ISIN to search for
        mic_code: MIC code from FIRDS data (mandatory)

    Returns:
        Dict with 'success', 'results', 'strategy', 'error' keys
    """
    try:
        service = OpenFIGIService()
        results, strategy = service.search_figi(isin, mic_code)

        # Convert to dictionary format for easier handling
        results_dict = []
        for result in results:
            results_dict.append(
                {
                    "figi": result.figi,
                    "name": result.name,
                    "ticker": result.ticker,
                    "exchCode": result.exch_code,
                    "securityType": result.security_type,
                    "marketSector": result.market_sector,
                    "compositeFIGI": result.composite_figi,
                    "shareClassFIGI": result.share_class_figi,
                    "currency": result.currency,
                    "securityDescription": result.security_description,
                    "searchStrategy": result.search_strategy,
                }
            )

        return {
            "success": len(results) > 0,
            "results": results_dict,
            "strategy": strategy,
            "total_results": len(results),
            "error": None,
        }

    except Exception as e:
        logger.error(f"Error in OpenFIGI search for {isin}: {str(e)}")
        return {
            "success": False,
            "results": [],
            "strategy": "error",
            "total_results": 0,
            "error": str(e),
        }


# Legacy compatibility for existing code (if needed)
def search_openfigi_enhanced(
    isin: str, instrument_type: str, venue_id: str = None, **kwargs
) -> list:
    """
    Legacy compatibility function.

    Note: instrument_type and other parameters are ignored in the simplified approach.
    Only ISIN and venue_id (as MIC code) are used.
    """
    if not venue_id:
        logger.warning(f"No venue_id provided for ISIN {isin}, this will likely fail")
        return []

    result = search_openfigi_simplified(isin, venue_id)

    if result["success"]:
        return result["results"]
    else:
        return []


def map_figi_data(data: list, isin: str):
    """Maps OpenFIGI API response to list of FigiMapping models for multiple FIGIs per ISIN"""
    if not data or len(data) == 0:
        return []

    # Get the FigiMapping model directly
    from ..models.sqlite.figi import FigiMapping

    figi_mappings = []

    try:
        # Handle the list of FIGI results (can be multiple per ISIN)
        for item in data:
            figi_data = item

            # Check if item is a dataclass (OpenFIGISearchResult) or dict
            if hasattr(item, 'figi'):  # It's a dataclass
                figi_mapping = FigiMapping(
                    isin=isin,
                    figi=item.figi,
                    composite_figi=item.composite_figi,
                    share_class_figi=item.share_class_figi,
                    ticker=item.ticker,
                    security_type=item.security_type,
                    market_sector=item.market_sector,
                    security_description=item.security_description,
                )
                figi_mappings.append(figi_mapping)
            elif isinstance(item, dict):
                # Handle nested data structure from OpenFIGI (old format)
                if "data" in item:
                    # If there are multiple FIGIs in the data array, create a mapping for each
                    for figi_item in item["data"]:
                        if "warning" not in figi_item:  # Skip items with warnings
                            figi_mapping = FigiMapping(
                                isin=isin,
                                figi=figi_item.get("figi"),
                                composite_figi=figi_item.get("compositeFIGI"),
                                share_class_figi=figi_item.get("shareClassFIGI"),
                                ticker=figi_item.get("ticker"),
                                security_type=figi_item.get("securityType"),
                                market_sector=figi_item.get("marketSector"),
                                security_description=figi_item.get("securityDescription"),
                            )
                            figi_mappings.append(figi_mapping)
                else:
                    # Fallback to old structure - single FIGI (dict format)
                    if "warning" not in figi_data:
                        figi_mapping = FigiMapping(
                            isin=isin,
                            figi=figi_data.get("figi"),
                            composite_figi=figi_data.get("compositeFIGI"),
                            share_class_figi=figi_data.get("shareClassFIGI"),
                            ticker=figi_data.get("ticker"),
                            security_type=figi_data.get("securityType"),
                            market_sector=figi_data.get("marketSector"),
                            security_description=figi_data.get("securityDescription"),
                        )
                        figi_mappings.append(figi_mapping)

        return figi_mappings

    except (KeyError, IndexError, TypeError) as e:
        logger.error(f"Error mapping FIGI data: {e}")
        return []
