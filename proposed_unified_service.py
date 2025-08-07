"""
Proposed Unified Service Implementation

This shows how the service layer would work with the new document-based approach.
Much simpler, cleaner, and addresses all your concerns.
"""

import logging
import uuid
from typing import Dict, Any, Optional, List, Tuple
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, UTC

logger = logging.getLogger(__name__)


class UnifiedInstrumentService:
    """Simplified instrument service using document-based approach."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_instrument(self, identifier: str, instrument_type: str = "equity") -> 'Instrument':
        """
        Create instrument and store ALL venue records in database.
        
        NEW BEHAVIOR:
        1. Gets ALL FIRDS records for the ISIN
        2. Creates single instrument with primary data
        3. Creates separate venue records for EACH venue
        4. No raw FIRDS data in responses
        """
        session = SessionLocal()
        
        try:
            # Get ALL FIRDS data for this ISIN
            all_venue_records = self._get_firds_data_from_storage(identifier, instrument_type)
            if not all_venue_records:
                raise InstrumentNotFoundError(f"No FIRDS data found for {identifier}")
            
            self.logger.info(f"Found {len(all_venue_records)} venue records for {identifier}")
            
            # Use first record for primary instrument data
            primary_record = all_venue_records[0]
            
            # Create instrument with core fields
            instrument_data = self._extract_core_fields(primary_record)
            instrument_data.update({
                'id': str(uuid.uuid4()),
                'isin': identifier,
                'instrument_type': instrument_type,
                'firds_data': primary_record,  # Keep original for reference
                'processed_attributes': self._process_type_specific_attributes(primary_record, instrument_type)
            })
            
            # Check for existing and delete if present
            existing = session.query(Instrument).filter(Instrument.isin == identifier).first()
            if existing:
                self.logger.info(f"Deleting existing instrument {identifier}")
                session.delete(existing)
                session.flush()
            
            # Create new instrument
            instrument = Instrument(**instrument_data)
            session.add(instrument)
            session.flush()
            
            # Create venue records for ALL venues
            venue_records = []
            for venue_data in all_venue_records:
                venue_record = self._create_venue_record(instrument.id, venue_data)
                venue_records.append(venue_record)
                session.add(venue_record)
            
            session.commit()
            
            self.logger.info(f"Created instrument {identifier} with {len(venue_records)} venue records")
            
            # Try enrichment
            try:
                enriched_session, enriched_instrument = self.enrich_instrument(instrument)
                enriched_session.close()
                
                # Return fresh copy
                return session.get(Instrument, instrument.id)
            except Exception as e:
                self.logger.warning(f"Enrichment failed: {e}")
                return instrument
                
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_instrument_venues(self, identifier: str) -> List[Dict[str, Any]]:
        """
        Get ALL venue records from DATABASE (not files).
        
        NEW BEHAVIOR:
        1. Queries database trading_venues table
        2. Returns clean structured data
        3. No raw FIRDS data included
        4. Much faster than file access
        """
        session = SessionLocal()
        
        try:
            # Find instrument
            instrument = session.query(Instrument).filter(
                (Instrument.id == identifier) |
                (Instrument.isin == identifier)
            ).first()
            
            if not instrument:
                return None
            
            # Get all venue records from database
            venue_records = session.query(TradingVenue).filter(
                TradingVenue.instrument_id == instrument.id
            ).all()
            
            if not venue_records:
                self.logger.warning(f"No venue records found in database for {identifier}")
                return []
            
            # Return clean structured data
            result = [venue.to_dict() for venue in venue_records]
            
            self.logger.info(f"Retrieved {len(result)} venue records for {identifier} from database")
            return result
            
        except Exception as e:
            self.logger.error(f"Error retrieving venues for {identifier}: {e}")
            return None
        finally:
            session.close()
    
    def _extract_core_fields(self, firds_record: Dict[str, Any]) -> Dict[str, Any]:
        """Extract core fields that go into main instrument table."""
        return {
            'full_name': firds_record.get('FinInstrmGnlAttrbts_FullNm'),
            'short_name': firds_record.get('FinInstrmGnlAttrbts_ShrtNm'),
            'currency': firds_record.get('FinInstrmGnlAttrbts_NtnlCcy'),
            'cfi_code': firds_record.get('FinInstrmGnlAttrbts_ClssfctnTp'),
            'lei_id': firds_record.get('Issr'),
        }
    
    def _process_type_specific_attributes(self, firds_record: Dict[str, Any], instrument_type: str) -> Dict[str, Any]:
        """Process type-specific attributes into clean JSON structure."""
        attributes = {}
        
        if instrument_type == "equity":
            # Extract equity-specific fields
            if firds_record.get('DerivInstrmAttrbts_PricMltplr'):
                attributes['price_multiplier'] = float(firds_record['DerivInstrmAttrbts_PricMltplr'])
            
            if firds_record.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
                attributes['underlying_isin'] = firds_record['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']
            
            # Asset class attributes
            asset_class = {}
            if firds_record.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct'):
                asset_class['oil_type'] = firds_record['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct']
            
            if asset_class:
                attributes['asset_class'] = asset_class
                
        elif instrument_type == "debt":
            # Extract debt-specific fields
            if firds_record.get('DebtInstrmAttrbts_MtrtyDt'):
                attributes['maturity_date'] = firds_record['DebtInstrmAttrbts_MtrtyDt']
            
            if firds_record.get('DebtInstrmAttrbts_TtlIssdNmnlAmt'):
                attributes['total_issued_nominal'] = float(firds_record['DebtInstrmAttrbts_TtlIssdNmnlAmt'])
                
        elif instrument_type == "future":
            # Extract future-specific fields
            if firds_record.get('DerivInstrmAttrbts_XpryDt'):
                attributes['expiration_date'] = firds_record['DerivInstrmAttrbts_XpryDt']
            
            if firds_record.get('DerivInstrmAttrbts_DlvryTp'):
                attributes['delivery_type'] = firds_record['DerivInstrmAttrbts_DlvryTp']
        
        return attributes
    
    def _create_venue_record(self, instrument_id: str, venue_data: Dict[str, Any]) -> 'TradingVenue':
        """Create a venue record from FIRDS data."""
        venue_record = TradingVenue(
            id=str(uuid.uuid4()),
            instrument_id=instrument_id,
            venue_id=venue_data.get('TradgVnRltdAttrbts_Id'),
            isin=venue_data.get('Id'),
            first_trade_date=self._parse_date(venue_data.get('TradgVnRltdAttrbts_FrstTradDt')),
            termination_date=self._parse_date(venue_data.get('TradgVnRltdAttrbts_TermntnDt')),
            admission_approval_date=self._parse_date(venue_data.get('TradgVnRltdAttrbts_AdmssnApprvlDtByIssr')),
            request_for_admission_date=self._parse_date(venue_data.get('TradgVnRltdAttrbts_ReqForAdmssnDt')),
            venue_full_name=venue_data.get('FinInstrmGnlAttrbts_FullNm'),
            venue_short_name=venue_data.get('FinInstrmGnlAttrbts_ShrtNm'),
            classification_type=venue_data.get('FinInstrmGnlAttrbts_ClssfctnTp'),
            venue_currency=venue_data.get('FinInstrmGnlAttrbts_NtnlCcy'),
            issuer_requested=venue_data.get('TradgVnRltdAttrbts_IssrReq'),
            competent_authority=venue_data.get('TechAttrbts_RlvntCmptntAuthrty'),
            relevant_trading_venue=venue_data.get('TechAttrbts_RlvntTradgVn'),
            publication_from_date=self._parse_date(venue_data.get('TechAttrbts_PblctnPrd_FrDt')),
        )
        
        # Store any additional venue-specific attributes
        venue_attributes = {}
        for key, value in venue_data.items():
            if key not in self._get_mapped_fields() and value:
                venue_attributes[key] = value
        
        if venue_attributes:
            venue_record.venue_attributes = venue_attributes
        
        return venue_record
    
    def _get_mapped_fields(self) -> set:
        """Get list of fields that are already mapped to specific columns."""
        return {
            'Id', 'TradgVnRltdAttrbts_Id', 'TradgVnRltdAttrbts_FrstTradDt',
            'TradgVnRltdAttrbts_TermntnDt', 'TradgVnRltdAttrbts_AdmssnApprvlDtByIssr',
            'TradgVnRltdAttrbts_ReqForAdmssnDt', 'FinInstrmGnlAttrbts_FullNm',
            'FinInstrmGnlAttrbts_ShrtNm', 'FinInstrmGnlAttrbts_ClssfctnTp',
            'FinInstrmGnlAttrbts_NtnlCcy', 'TradgVnRltdAttrbts_IssrReq',
            'TechAttrbts_RlvntCmptntAuthrty', 'TechAttrbts_RlvntTradgVn',
            'TechAttrbts_PblctnPrd_FrDt', 'Issr'
        }
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime object."""
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            return None


"""
COMPARISON: Current vs Proposed

CURRENT APPROACH:
- create_instrument(): Stores only 1 record, complex polymorphic inheritance
- get_instrument_venues(): Reads from files every time, returns raw FIRDS data
- Database: 5 tables, 120+ columns, many NULLs
- API: Raw FIRDS data exposed, complex responses

PROPOSED APPROACH:  
- create_instrument(): Stores ALL venue records in database
- get_instrument_venues(): Fast database query, clean structured data
- Database: 2 main tables, JSON for flexibility, no NULLs
- API: Clean structured responses, no raw data

BENEFITS:
1. ✅ ALL venue records stored in database
2. ✅ Fast venue queries (no file access)
3. ✅ Clean API responses (no raw FIRDS)
4. ✅ Handles variable FIRDS columns naturally
5. ✅ Much simpler codebase
6. ✅ Better performance
7. ✅ Easier to maintain

The "controversial" part is using JSON columns, but modern databases handle this very well,
and it's perfect for the variable structure of FIRDS data.
"""
