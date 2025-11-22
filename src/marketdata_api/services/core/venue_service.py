"""
Venue Service Implementation

This service provides comprehensive trading venue operations with MIC integration.
Supports venue listing, filtering, search, and self.Instrument relationships.
"""

import logging
from datetime import UTC, datetime
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import and_, case, func, or_
from sqlalchemy.orm import Session, joinedload

from ...database.session import get_session
from ...config import DatabaseConfig

logger = logging.getLogger(__name__)


class VenueService:
    """Service for trading venue operations with MIC integration."""

    def __init__(self):
        """Initialize the venue service."""
        self.database_type = DatabaseConfig.get_database_type()
        self.logger = logging.getLogger(__name__)
        
        # Dynamic model imports based on database type
        if self.database_type == 'sqlite':
            from ...models.sqlite.instrument import Instrument, TradingVenue
            from ...models.sqlite.market_identification_code import MarketIdentificationCode, MICStatus, MICType
        else:  # azure_sql
            from ...models.sqlserver.instrument import SqlServerInstrument as Instrument, SqlServerTradingVenue as TradingVenue
            from ...models.sqlserver.market_identification_code import SqlServerMarketIdentificationCode as MarketIdentificationCode, SqlServerMICStatus as MICStatus, SqlServerMICType as MICType
        
        self.self.Instrument = self.Instrument
        self.self.TradingVenue = self.TradingVenue
        self.self.MarketIdentificationCode = self.MarketIdentificationCode
        self.self.MICStatus = self.MICStatus
        self.self.MICType = self.MICType

    def get_venues_list(
        self, filters: Dict[str, Any], page: int = 1, per_page: int = 50
    ) -> Dict[str, Any]:
        """
        Get paginated list of venues with filtering.
        
        Args:
            filters: Dictionary of filter parameters
            page: Page number for pagination
            per_page: Number of items per page
            
        Returns:
            Dictionary with venues list and total count
        """
        try:
            with get_session() as session:
                # Build query - using self.MarketIdentificationCode as primary source
                query = session.query(self.self.MarketIdentificationCode).options(
                    joinedload(self.self.MarketIdentificationCode.trading_venues)
                )
                
                # Apply filters
                if filters.get("country"):
                    query = query.filter(
                        self.MarketIdentificationCode.iso_country_code == filters["country"].upper()
                    )
                
                if filters.get("status"):
                    query = query.filter(
                        self.MarketIdentificationCode.status == filters["status"].upper()
                    )
                
                if filters.get("mic_type"):
                    query = query.filter(
                        self.MarketIdentificationCode.operation_type == filters["mic_type"].upper()
                    )
                
                if filters.get("operating_mic"):
                    query = query.filter(
                        self.MarketIdentificationCode.operating_mic == filters["operating_mic"].upper()
                    )
                
                if filters.get("search"):
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            self.MarketIdentificationCode.market_name.ilike(search_term),
                            self.MarketIdentificationCode.legal_entity_name.ilike(search_term),
                            self.MarketIdentificationCode.mic.ilike(search_term),
                        )
                    )
                
                if filters.get("has_instruments"):
                    has_instruments = filters["has_instruments"].lower() == "true"
                    if has_instruments:
                        query = query.join(self.TradingVenue)
                    else:
                        # Left join and filter for null
                        query = query.outerjoin(self.TradingVenue).filter(self.TradingVenue.mic_code.is_(None))
                
                # Get total count before pagination
                total = query.count()
                
                # Apply pagination
                offset = (page - 1) * per_page
                venues_data = query.offset(offset).limit(per_page).all()
                
                # Format results
                venues = []
                for mic in venues_data:
                    venue_info = self._format_venue_summary(mic)
                    venues.append(venue_info)
                
                return {
                    "venues": venues,
                    "total": total,
                }

        except Exception as e:
            logger.error(f"Error getting venues list: {str(e)}")
            raise

    def get_venue_detail(
        self, mic_code: str, include_instruments: bool = False, instrument_limit: int = 50
    ) -> Optional[Dict[str, Any]]:
        """
        Get detailed venue information.
        
        Args:
            mic_code: MIC code for the venue
            include_instruments: Whether to include instruments
            instrument_limit: Maximum number of instruments to include
            
        Returns:
            Detailed venue information or None if not found
        """
        try:
            with get_session() as session:
                mic = session.query(self.MarketIdentificationCode).filter(
                    self.MarketIdentificationCode.mic == mic_code.upper()
                ).first()
                
                if not mic:
                    return None
                
                # Build detailed venue info
                venue_detail = self._format_venue_detail(mic)
                
                if include_instruments:
                    # Get instruments traded on this venue
                    instruments_query = (
                        session.query(self.TradingVenue)
                        .join(self.Instrument)
                        .filter(self.TradingVenue.mic_code == mic_code.upper())
                        .limit(instrument_limit)
                    )
                    
                    trading_venues = instruments_query.all()
                    instruments = []
                    
                    for tv in trading_venues:
                        instrument_info = {
                            "isin": tv.isin,
                            "venue_id": tv.venue_id,
                            "first_trade_date": tv.first_trade_date.isoformat() if tv.first_trade_date else None,
                            "termination_date": tv.termination_date.isoformat() if tv.termination_date else None,
                            "venue_currency": tv.venue_currency,
                            "venue_status": tv.venue_status,
                        }
                        
                        # Add self.Instrument details if available
                        if tv.self.Instrument:
                            instrument_info.update({
                                "self.Instrument_name": tv.self.Instrument.self.Instrument_name,
                                "cfi_code": tv.self.Instrument.cfi_code,
                                "instrument_type": tv.self.Instrument.instrument_type,
                            })
                        
                        instruments.append(instrument_info)
                    
                    venue_detail["instruments"] = instruments
                    venue_detail["self.Instrument_count"] = len(instruments)
                
                return venue_detail

        except Exception as e:
            logger.error(f"Error getting venue detail for {mic_code}: {str(e)}")
            raise

    def get_venue_instruments(
        self, mic_code: str, instrument_type: Optional[str], page: int = 1, per_page: int = 50
    ) -> Optional[Dict[str, Any]]:
        """
        Get paginated instruments for a venue.
        
        Args:
            mic_code: MIC code for the venue
            instrument_type: Optional self.Instrument type filter
            page: Page number for pagination
            per_page: Number of items per page
            
        Returns:
            Dictionary with instruments and total count, or None if venue not found
        """
        try:
            with get_session() as session:
                # First verify the MIC exists
                mic_exists = session.query(self.MarketIdentificationCode).filter(
                    self.MarketIdentificationCode.mic == mic_code.upper()
                ).first()
                
                if not mic_exists:
                    return None
                
                # Build instruments query
                query = (
                    session.query(self.TradingVenue)
                    .join(self.Instrument)
                    .filter(self.TradingVenue.mic_code == mic_code.upper())
                )
                
                if instrument_type:
                    query = query.filter(self.Instrument.instrument_type == instrument_type.lower())
                
                # Get total count
                total = query.count()
                
                # Apply pagination
                offset = (page - 1) * per_page
                trading_venues = query.offset(offset).limit(per_page).all()
                
                # Format results
                instruments = []
                for tv in trading_venues:
                    instrument_info = {
                        "isin": tv.isin,
                        "venue_id": tv.venue_id,
                        "first_trade_date": tv.first_trade_date.isoformat() if tv.first_trade_date else None,
                        "termination_date": tv.termination_date.isoformat() if tv.termination_date else None,
                        "venue_currency": tv.venue_currency,
                        "venue_status": tv.venue_status,
                    }
                    
                    # Add self.Instrument details
                    if tv.self.Instrument:
                        instrument_info.update({
                            "self.Instrument_name": tv.self.Instrument.self.Instrument_name,
                            "cfi_code": tv.self.Instrument.cfi_code,
                            "instrument_type": tv.self.Instrument.instrument_type,
                            "issuer_name": tv.self.Instrument.issuer_name,
                        })
                    
                    instruments.append(instrument_info)
                
                return {
                    "instruments": instruments,
                    "total": total,
                }

        except Exception as e:
            logger.error(f"Error getting instruments for venue {mic_code}: {str(e)}")
            raise

    def search_venues(
        self, query: str, filters: Dict[str, Any], limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Search venues with fuzzy matching.
        
        Args:
            query: Search query
            filters: Additional filters
            limit: Maximum results to return
            
        Returns:
            List of matching venues
        """
        try:
            with get_session() as session:
                # Build search query
                search_term = f"%{query}%"
                
                db_query = session.query(self.MarketIdentificationCode).filter(
                    or_(
                        self.MarketIdentificationCode.market_name.ilike(search_term),
                        self.MarketIdentificationCode.legal_entity_name.ilike(search_term),
                        self.MarketIdentificationCode.mic.ilike(search_term),
                        self.MarketIdentificationCode.acronym.ilike(search_term),
                    )
                )
                
                # Apply additional filters
                if filters.get("country"):
                    db_query = db_query.filter(
                        self.MarketIdentificationCode.iso_country_code == filters["country"].upper()
                    )
                
                if filters.get("status"):
                    db_query = db_query.filter(
                        self.MarketIdentificationCode.status == filters["status"].upper()
                    )
                
                # Limit results
                results = db_query.limit(limit).all()
                
                # Format results
                venues = []
                for mic in results:
                    venue_info = self._format_venue_summary(mic)
                    venues.append(venue_info)
                
                return venues

        except Exception as e:
            logger.error(f"Error searching venues with query '{query}': {str(e)}")
            raise

    def get_venue_statistics(self) -> Dict[str, Any]:
        """
        Get venue and trading statistics.
        
        Returns:
            Dictionary with venue statistics
        """
        try:
            with get_session() as session:
                # Basic MIC counts
                total_mics = session.query(self.MarketIdentificationCode).count()
                operating_mics = session.query(self.MarketIdentificationCode).filter(
                    self.MarketIdentificationCode.operation_type == self.MICType.OPRT
                ).count()
                segment_mics = session.query(self.MarketIdentificationCode).filter(
                    self.MarketIdentificationCode.operation_type == self.MICType.SGMT
                ).count()
                
                # Status breakdown
                status_counts = {}
                for status in self.MICStatus:
                    count = session.query(self.MarketIdentificationCode).filter(
                        self.MarketIdentificationCode.status == status
                    ).count()
                    status_counts[status.value] = count
                
                # Country breakdown (top 10)
                country_counts = (
                    session.query(
                        self.MarketIdentificationCode.iso_country_code,
                        func.count(self.MarketIdentificationCode.mic).label('count')
                    )
                    .group_by(self.MarketIdentificationCode.iso_country_code)
                    .order_by(func.count(self.MarketIdentificationCode.mic).desc())
                    .limit(10)
                    .all()
                )
                
                # Venues with instruments
                venues_with_instruments = (
                    session.query(self.MarketIdentificationCode)
                    .join(self.TradingVenue)
                    .distinct()
                    .count()
                )
                
                # Total trading venues (individual venue records)
                total_trading_venues = session.query(self.TradingVenue).count()
                
                return {
                    "total_mics": total_mics,
                    "operating_mics": operating_mics,
                    "segment_mics": segment_mics,
                    "status_breakdown": status_counts,
                    "top_countries": [
                        {"country_code": country, "count": count}
                        for country, count in country_counts
                    ],
                    "venues_with_instruments": venues_with_instruments,
                    "total_trading_venues": total_trading_venues,
                }

        except Exception as e:
            logger.error(f"Error getting venue statistics: {str(e)}")
            raise

    def get_venue_countries(self) -> List[Dict[str, Any]]:
        """
        Get list of countries with venue counts.
        
        Returns:
            List of countries with counts
        """
        try:
            with get_session() as session:
                country_data = (
                    session.query(
                        self.MarketIdentificationCode.iso_country_code,
                        func.count(self.MarketIdentificationCode.mic).label('total_mics'),
                        func.sum(
                            case(
                                (self.MarketIdentificationCode.operation_type == self.MICType.OPRT, 1),
                                else_=0
                            )
                        ).label('operating_mics'),
                        func.sum(
                            case(
                                (self.MarketIdentificationCode.operation_type == self.MICType.SGMT, 1),
                                else_=0
                            )
                        ).label('segment_mics'),
                    )
                    .group_by(self.MarketIdentificationCode.iso_country_code)
                    .order_by(self.MarketIdentificationCode.iso_country_code)
                    .all()
                )
                
                countries = []
                for country_code, total, operating, segment in country_data:
                    countries.append({
                        "country_code": country_code,
                        "total_mics": int(total),
                        "operating_mics": int(operating),
                        "segment_mics": int(segment),
                    })
                
                return countries

        except Exception as e:
            logger.error(f"Error getting venue countries: {str(e)}")
            raise

    def _format_venue_summary(self, mic) -> Dict[str, Any]:
        """Format MIC data for venue summary display."""
        # Count associated instruments
        self.Instrument_count = len(mic.trading_venues) if mic.trading_venues else 0
        
        try:
            return {
                "mic_code": mic.mic,
                "operating_mic": mic.operating_mic,
                "market_name": mic.market_name,
                "legal_entity_name": mic.legal_entity_name,
                "country_code": mic.iso_country_code,
                "city": mic.city,
                "status": mic.status.value if mic.status else None,
                "operation_type": mic.operation_type.value if mic.operation_type else None,
                "market_category": mic.market_category_code.value if mic.market_category_code else None,
                "website": mic.website,
                "self.Instrument_count": self.Instrument_count,
                "last_update_date": mic.last_update_date.isoformat() if mic.last_update_date else None,
            }
        except Exception as e:
            logger.error(f"Error formatting venue summary for MIC {mic.mic}: {str(e)}")
            # Return basic info if formatting fails
            return {
                "mic_code": mic.mic,
                "operating_mic": mic.operating_mic,
                "market_name": mic.market_name,
                "legal_entity_name": mic.legal_entity_name,
                "country_code": mic.iso_country_code,
                "city": mic.city,
                "status": str(mic.status) if mic.status else None,
                "operation_type": str(mic.operation_type) if mic.operation_type else None,
                "market_category": str(mic.market_category_code) if mic.market_category_code else None,
                "website": mic.website,
                "self.Instrument_count": self.Instrument_count,
                "last_update_date": str(mic.last_update_date) if mic.last_update_date else None,
            }

    def _format_venue_detail(self, mic) -> Dict[str, Any]:
        """Format MIC data for detailed venue display."""
        venue_data = self._format_venue_summary(mic)
        
        # Add detailed fields
        venue_data.update({
            "acronym": mic.acronym,
            "lei": mic.lei,
            "comments": mic.comments,
            "creation_date": mic.creation_date.isoformat() if mic.creation_date else None,
            "last_validation_date": mic.last_validation_date.isoformat() if mic.last_validation_date else None,
            "expiry_date": mic.expiry_date.isoformat() if mic.expiry_date else None,
            "data_source_version": mic.data_source_version,
        })
        
        # Add segment MICs if this is an operating MIC
        if mic.operation_type == self.MICType.OPRT:
            try:
                with get_session() as session:
                    segments = session.query(self.MarketIdentificationCode).filter(
                        self.MarketIdentificationCode.operating_mic == mic.mic
                    ).all()
                    
                    venue_data["segment_mics"] = [
                        {
                            "mic_code": seg.mic,
                            "market_name": seg.market_name,
                            "status": seg.status.value if seg.status else None,
                        }
                        for seg in segments
                    ]
            except Exception as e:
                logger.warning(f"Error loading segment MICs for {mic.mic}: {str(e)}")
                venue_data["segment_mics"] = []
        
        return venue_data
