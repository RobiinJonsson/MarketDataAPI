"""
MIC Data Loader Service

Service for loading and updating ISO 10383 Market Identification Codes from CSV files
or remote URLs. Handles data validation, transformation, and bulk updates.
Supports both local database storage and direct remote lookups.
"""

import csv
import io
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import requests
from sqlalchemy.orm import Session

from ..constants import ExternalAPIs, APITimeouts, ValidationLimits
from ..models.sqlite.market_identification_code import (
    MarketCategoryCode,
    MarketIdentificationCode,
    MICStatus,
    MICType,
)

logger = logging.getLogger(__name__)


class MICDataLoader:
    """Loader for ISO 10383 MIC data from CSV files."""

    # CSV column mapping to model fields
    CSV_COLUMN_MAPPING = {
        "MIC": "mic",
        "OPERATING MIC": "operating_mic",
        "OPRT/SGMT": "operation_type",
        "MARKET NAME-INSTITUTION DESCRIPTION": "market_name",
        "LEGAL ENTITY NAME": "legal_entity_name",
        "LEI": "lei",
        "MARKET CATEGORY CODE": "market_category_code",
        "ACRONYM": "acronym",
        "ISO COUNTRY CODE (ISO 3166)": "iso_country_code",
        "CITY": "city",
        "WEBSITE": "website",
        "STATUS": "status",
        "CREATION DATE": "creation_date",
        "LAST UPDATE DATE": "last_update_date",
        "LAST VALIDATION DATE": "last_validation_date",
        "EXPIRY DATE": "expiry_date",
        "COMMENTS": "comments",
    }

    def __init__(self, session: Session):
        self.session = session

    def load_from_csv(
        self, csv_source: Union[str, io.StringIO], data_version: Optional[str] = None
    ) -> Tuple[int, int, List[str]]:
        """
        Load MIC data from CSV file or StringIO object.

        Args:
            csv_source: Path to CSV file or StringIO object with CSV data
            data_version: Version identifier for tracking data source

        Returns:
            Tuple of (created_count, updated_count, errors)
        """
        if isinstance(csv_source, str):
            csv_path = Path(csv_source)
            if not csv_path.exists():
                raise FileNotFoundError(f"CSV file not found: {csv_source}")

        if data_version is None:
            source_name = "remote" if isinstance(csv_source, io.StringIO) else "local_file"
            data_version = f"{source_name}_import_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"

        logger.info(
            f"Loading MIC data from {'remote source' if isinstance(csv_source, io.StringIO) else csv_source}"
        )

        created_count = 0
        updated_count = 0
        errors = []

        try:
            if isinstance(csv_source, str):
                file_handle = open(csv_source, "r", encoding="utf-8")
            else:
                file_handle = csv_source

            try:
                # Use DictReader for easier column access
                reader = csv.DictReader(file_handle)

                for row_num, row in enumerate(reader, start=2):  # Start at 2 for header
                    try:
                        mic_data = self._transform_csv_row(row, data_version)
                        if mic_data:
                            existing_mic = (
                                self.session.query(MarketIdentificationCode)
                                .filter_by(mic=mic_data["mic"])
                                .first()
                            )

                            if existing_mic:
                                self._update_mic_record(existing_mic, mic_data)
                                updated_count += 1
                            else:
                                new_mic = MarketIdentificationCode(**mic_data)
                                self.session.add(new_mic)
                                created_count += 1

                    except Exception as e:
                        error_msg = f"Row {row_num}: {str(e)}"
                        errors.append(error_msg)
                        logger.warning(error_msg)
                        continue

                # Commit changes
                self.session.commit()
                logger.info(
                    f"MIC data loaded: {created_count} created, {updated_count} updated, {len(errors)} errors"
                )

            finally:
                if isinstance(csv_source, str):
                    file_handle.close()

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to load MIC data: {str(e)}")

        return created_count, updated_count, errors

    def load_from_remote_url(
        self, url: str = ExternalAPIs.ISO_MIC_CSV_URL, data_version: Optional[str] = None
    ) -> Tuple[int, int, List[str]]:
        """
        Load MIC data from remote CSV URL.

        Args:
            url: URL to CSV file (defaults to official ISO 20022 source)
            data_version: Version identifier for tracking data source

        Returns:
            Tuple of (created_count, updated_count, errors)
        """
        logger.info(f"Downloading MIC data from {url}")

        try:
            response = requests.get(url, timeout=APITimeouts.DEFAULT_SINGLE)
            response.raise_for_status()

            # Create StringIO object from response content
            csv_data = io.StringIO(response.text)

            if data_version is None:
                data_version = f"remote_official_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"

            return self.load_from_csv(csv_data, data_version)

        except requests.RequestException as e:
            raise Exception(f"Failed to download MIC data from {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to process remote MIC data: {str(e)}")

    def _transform_csv_row(
        self, row: Dict[str, str], data_version: str
    ) -> Optional[Dict[str, Any]]:
        """Transform CSV row to MIC model data."""
        # Skip rows with empty MIC codes
        mic_code = row.get("MIC", "").strip()
        if not mic_code:
            return None

        # Basic validation
        if len(mic_code) != 4:
            raise ValueError(f"Invalid MIC code length: {mic_code}")

        mic_data = {
            "mic": mic_code.upper(),
            "data_source_version": data_version,
            "updated_at": datetime.now(UTC),
        }

        # Transform each field
        for csv_col, model_field in self.CSV_COLUMN_MAPPING.items():
            if csv_col in row:
                value = row[csv_col].strip()

                if model_field == "operation_type":
                    mic_data[model_field] = self._parse_operation_type(value)
                elif model_field == "status":
                    mic_data[model_field] = self._parse_status(value)
                elif model_field == "market_category_code":
                    mic_data[model_field] = self._parse_market_category(value)
                elif model_field.endswith("_date"):
                    mic_data[model_field] = self._parse_date(value)
                elif model_field in ["lei", "iso_country_code"]:
                    mic_data[model_field] = value.upper() if value else None
                else:
                    mic_data[model_field] = value if value else None

        return mic_data

    def _parse_operation_type(self, value: str) -> Optional[MICType]:
        """Parse operation type from CSV."""
        if not value:
            return None
        try:
            return MICType(value.upper())
        except ValueError:
            logger.warning(f"Unknown operation type: {value}")
            return None

    def _parse_status(self, value: str) -> MICStatus:
        """Parse status from CSV."""
        if not value:
            return MICStatus.ACTIVE
        try:
            return MICStatus(value.upper())
        except ValueError:
            logger.warning(f"Unknown status: {value}, defaulting to ACTIVE")
            return MICStatus.ACTIVE

    def _parse_market_category(self, value: str) -> Optional[MarketCategoryCode]:
        """Parse market category code from CSV."""
        if not value:
            return None
        try:
            return MarketCategoryCode(value.upper())
        except ValueError:
            logger.warning(f"Unknown market category: {value}")
            return None

    def _parse_date(self, value: str) -> Optional[datetime]:
        """Parse date from CSV (YYYYMMDD format)."""
        if not value:
            return None

        try:
            # Try YYYYMMDD format first
            if len(value) == 8:
                return datetime.strptime(value, "%Y%m%d").replace(tzinfo=UTC)
            # Try other common formats
            for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]:
                try:
                    return datetime.strptime(value, fmt).replace(tzinfo=UTC)
                except ValueError:
                    continue
        except ValueError:
            logger.warning(f"Unable to parse date: {value}")

        return None

    def _update_mic_record(self, existing_mic: MarketIdentificationCode, new_data: Dict[str, Any]):
        """Update existing MIC record with new data."""
        for field, value in new_data.items():
            if field not in ["mic", "created_at"]:  # Don't update primary key or creation time
                setattr(existing_mic, field, value)

    def get_load_statistics(self) -> Dict[str, Any]:
        """Get statistics about loaded MIC data."""
        from sqlalchemy import func

        total_mics = self.session.query(MarketIdentificationCode).count()
        active_mics = (
            self.session.query(MarketIdentificationCode).filter_by(status=MICStatus.ACTIVE).count()
        )
        operating_mics = (
            self.session.query(MarketIdentificationCode)
            .filter_by(operation_type=MICType.OPRT, status=MICStatus.ACTIVE)
            .count()
        )
        segment_mics = (
            self.session.query(MarketIdentificationCode)
            .filter_by(operation_type=MICType.SGMT, status=MICStatus.ACTIVE)
            .count()
        )

        # Count by country using proper SQL aggregation
        country_stats = (
            self.session.query(
                MarketIdentificationCode.iso_country_code,
                func.count(MarketIdentificationCode.mic).label("count"),
            )
            .filter(MarketIdentificationCode.status == MICStatus.ACTIVE)
            .group_by(MarketIdentificationCode.iso_country_code)
            .all()
        )

        country_counts = {country_code: count for country_code, count in country_stats}

        return {
            "total_mics": total_mics,
            "active_mics": active_mics,
            "operating_mics": operating_mics,
            "segment_mics": segment_mics,
            "countries": len(country_counts),
            "top_countries": sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:10],
        }

    def validate_mic_relationships(self) -> List[str]:
        """Validate MIC data relationships and return any issues."""
        issues = []

        # Check for segment MICs without valid operating MIC
        orphaned_segments = (
            self.session.query(MarketIdentificationCode)
            .filter(
                MarketIdentificationCode.operation_type == MICType.SGMT,
                ~self.session.query(MarketIdentificationCode)
                .filter(
                    MarketIdentificationCode.mic == MarketIdentificationCode.operating_mic,
                    MarketIdentificationCode.operation_type == MICType.OPRT,
                )
                .exists(),
            )
            .all()
        )

        for segment in orphaned_segments:
            issues.append(
                f"Segment MIC {segment.mic} references non-existent operating MIC {segment.operating_mic}"
            )

        return issues


def load_mic_data_from_csv(
    session: Session, csv_source: Union[str, None] = None, data_version: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function to load MIC data from CSV file or remote source.

    Args:
        session: Database session
        csv_source: Path to CSV file or None for remote loading
        data_version: Optional version identifier

    Returns:
        Dictionary with load results and statistics
    """
    loader = MICDataLoader(session)

    try:
        if csv_source is None:
            # Load from official remote source
            created, updated, errors = loader.load_from_remote_url(data_version=data_version)
        else:
            # Load from local file
            created, updated, errors = loader.load_from_csv(csv_source, data_version)

        statistics = loader.get_load_statistics()
        validation_issues = loader.validate_mic_relationships()

        return {
            "success": True,
            "source": "remote_official" if csv_source is None else "local_file",
            "created_count": created,
            "updated_count": updated,
            "error_count": len(errors),
            "errors": errors,
            "statistics": statistics,
            "validation_issues": validation_issues,
        }

    except Exception as e:
        logger.error(f"Failed to load MIC data: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "source": "remote_official" if csv_source is None else "local_file",
            "created_count": 0,
            "updated_count": 0,
            "error_count": 0,
            "errors": [],
        }


class RemoteMICLookupService:
    """
    Service for direct MIC lookups from remote source without database dependency.
    Useful for real-time validation and occasional lookups.
    """

    def __init__(self, cache_duration_minutes: int = 60):
        self.cache_duration_minutes = cache_duration_minutes
        self._cache = {}
        self._cache_timestamp = None

    def _fetch_remote_data(self, url: str = ExternalAPIs.ISO_MIC_CSV_URL) -> Dict[str, Dict[str, Any]]:
        """Fetch and parse MIC data from remote URL."""
        logger.info(f"Fetching MIC data from remote source: {url}")

        try:
            response = requests.get(url, timeout=APITimeouts.DEFAULT_SINGLE)
            response.raise_for_status()

            # Parse CSV data
            csv_data = io.StringIO(response.text)
            reader = csv.DictReader(csv_data)

            mic_data = {}
            for row in reader:
                mic_code = row.get("MIC", "").strip().upper()
                if mic_code:
                    mic_data[mic_code] = {
                        "mic": mic_code,
                        "operating_mic": row.get("OPERATING MIC", "").strip(),
                        "operation_type": row.get("OPRT/SGMT", "").strip(),
                        "market_name": row.get("MARKET NAME-INSTITUTION DESCRIPTION", "").strip(),
                        "legal_entity_name": row.get("LEGAL ENTITY NAME", "").strip(),
                        "lei": row.get("LEI", "").strip(),
                        "market_category_code": row.get("MARKET CATEGORY CODE", "").strip(),
                        "acronym": row.get("ACRONYM", "").strip(),
                        "iso_country_code": row.get("ISO COUNTRY CODE (ISO 3166)", "").strip(),
                        "city": row.get("CITY", "").strip(),
                        "website": row.get("WEBSITE", "").strip(),
                        "status": row.get("STATUS", "").strip(),
                        "comments": row.get("COMMENTS", "").strip(),
                    }

            logger.info(f"Successfully fetched {len(mic_data)} MIC records from remote source")
            return mic_data

        except requests.RequestException as e:
            raise Exception(f"Failed to fetch MIC data from remote source: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to parse remote MIC data: {str(e)}")

    def _is_cache_valid(self) -> bool:
        """Check if cached data is still valid."""
        if self._cache_timestamp is None:
            return False

        cache_age = (datetime.now(UTC) - self._cache_timestamp).total_seconds() / 60
        return cache_age < self.cache_duration_minutes

    def _get_cached_data(self) -> Dict[str, Dict[str, Any]]:
        """Get cached MIC data, refreshing if necessary."""
        if not self._is_cache_valid():
            self._cache = self._fetch_remote_data()
            self._cache_timestamp = datetime.now(UTC)

        return self._cache

    def lookup_mic(self, mic_code: str) -> Optional[Dict[str, Any]]:
        """
        Look up a specific MIC code from remote source.

        Args:
            mic_code: 4-character MIC code to lookup

        Returns:
            Dictionary with MIC details or None if not found
        """
        mic_code = mic_code.upper().strip()
        if len(mic_code) != 4:
            raise ValueError(f"Invalid MIC code format: {mic_code}")

        try:
            data = self._get_cached_data()
            return data.get(mic_code)
        except Exception as e:
            logger.error(f"Failed to lookup MIC {mic_code}: {str(e)}")
            raise

    def search_mics(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search MICs by name or code from remote source.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching MIC records
        """
        query = query.lower().strip()
        if not query:
            return []

        try:
            data = self._get_cached_data()
            results = []

            for mic_code, mic_info in data.items():
                if (
                    query in mic_code.lower()
                    or query in mic_info.get("market_name", "").lower()
                    or query in mic_info.get("legal_entity_name", "").lower()
                    or query in mic_info.get("acronym", "").lower()
                ):

                    results.append(mic_info)

                    if len(results) >= limit:
                        break

            return results

        except Exception as e:
            logger.error(f"Failed to search MICs: {str(e)}")
            raise

    def get_country_mics(self, country_code: str) -> List[Dict[str, Any]]:
        """
        Get all MICs for a specific country from remote source.

        Args:
            country_code: ISO 3166 country code

        Returns:
            List of MIC records for the country
        """
        country_code = country_code.upper().strip()

        try:
            data = self._get_cached_data()
            results = []

            for mic_info in data.values():
                if mic_info.get("iso_country_code") == country_code:
                    results.append(mic_info)

            return results

        except Exception as e:
            logger.error(f"Failed to get MICs for country {country_code}: {str(e)}")
            raise

    def validate_mic(self, mic_code: str) -> Dict[str, Any]:
        """
        Validate a MIC code and return validation result.

        Args:
            mic_code: MIC code to validate

        Returns:
            Dictionary with validation result
        """
        try:
            mic_info = self.lookup_mic(mic_code)

            if mic_info is None:
                return {"valid": False, "error": f"MIC code {mic_code} not found in ISO registry"}

            status = mic_info.get("status", "").upper()
            if status not in ["ACTIVE", "UPDATED"]:
                return {
                    "valid": False,
                    "error": f"MIC code {mic_code} is not active (status: {status})",
                    "mic_info": mic_info,
                }

            return {"valid": True, "mic_info": mic_info}

        except Exception as e:
            return {"valid": False, "error": f"Failed to validate MIC {mic_code}: {str(e)}"}

    def clear_cache(self):
        """Clear the cached MIC data."""
        self._cache = {}
        self._cache_timestamp = None
        logger.info("MIC cache cleared")


# Global instance for remote lookups
remote_mic_service = RemoteMICLookupService()
