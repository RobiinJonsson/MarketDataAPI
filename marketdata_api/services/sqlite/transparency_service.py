"""
Unified Transparency Service

This service replaces the complex polymorphic inheritance transparency service
with a simplified approach using the unified transparency models.

Based on the successful FIRDS unification pattern.
"""

import uuid
import logging
import pandas as pd
from typing import Dict, Any, Optional, List, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ...database.session import get_session, SessionLocal
from ...models.sqlite.transparency import TransparencyCalculation, TransparencyThreshold
from ...models.sqlite.instrument import Instrument
from datetime import datetime, UTC, date
from ..esma_data_loader import EsmaDataLoader
from ...config import esmaConfig
from ..interfaces.transparency_service_interface import TransparencyServiceInterface


logger = logging.getLogger(__name__)


class TransparencyServiceError(Exception):
    """Base exception for transparency service errors"""
    pass


class TransparencyNotFoundError(TransparencyServiceError):
    """Raised when transparency data cannot be found"""
    pass


class TransparencyValidationError(TransparencyServiceError):
    """Raised when transparency data validation fails"""
    pass


class TransparencyService(TransparencyServiceInterface):
    """
    Unified transparency service using simplified JSON-based storage.
    
    Handles all FITRS file types (FULECR_E, FULNCR_C, FULNCR_D, FULNCR_F)
    with a single, flexible data structure.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.esma_loader = EsmaDataLoader(esmaConfig.start_date, esmaConfig.end_date)

    
    def validate_transparency_data(self, data: Dict[str, Any]) -> None:
        """Validate required transparency data fields"""
        required_fields = ['TechRcrdId']
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise TransparencyValidationError(f"Missing required fields: {', '.join(missing)}")
        
        # Validate ISIN presence for non-equity data
        if 'ISIN' not in data and 'Id' not in data:
            raise TransparencyValidationError("Either ISIN or Id field must be present")
    
    def determine_file_type(self, data: Dict[str, Any], source_filename: str = None) -> str:
        """
        Determine FITRS file type from data structure or filename.
        
        Returns: 'FULECR_E', 'FULNCR_C', 'FULNCR_D', or 'FULNCR_F'
        """
        # Try filename first if available
        if source_filename:
            if 'FULECR' in source_filename and '_E_' in source_filename:
                return 'FULECR_E'
            elif 'FULNCR' in source_filename:
                if '_C_' in source_filename:
                    return 'FULNCR_C'
                elif '_D_' in source_filename:
                    return 'FULNCR_D'
                elif '_F_' in source_filename:
                    return 'FULNCR_F'
        
        # Analyze data structure
        has_isin = 'ISIN' in data
        has_id_only = 'Id' in data and not has_isin
        has_desc = 'Desc' in data
        has_methodology = 'Mthdlgy' in data
        has_multiple_criteria = any(f'CritNm_{i}' in data for i in range(2, 8))
        
        if has_id_only and has_methodology and not has_desc:
            return 'FULECR_E'  # Equity - has Id, methodology, no description
        elif has_isin and has_desc and has_multiple_criteria:
            return 'FULNCR_F'  # Futures - has multiple criteria pairs
        elif has_isin and has_desc and 'bond' in data.get('Desc', '').lower():
            return 'FULNCR_D'  # Debt - has description mentioning bonds
        elif has_isin and has_desc:
            return 'FULNCR_C'  # Corporate - basic non-equity
        
        # Default fallback
        return 'FULNCR_C'

    def create_transparency_calculation(self, data: Dict[str, Any], calculation_type: str = None, source_filename: str = None) -> TransparencyCalculation:
        """
        Create a new transparency calculation with unified structure.
        
        Args:
            data: Dictionary containing FITRS transparency data
            calculation_type: Deprecated - file type is auto-determined
            source_filename: Original filename for type determination
            
        Returns:
            Created TransparencyCalculation instance
        """
        self.validate_transparency_data(data)
        
        # Determine file type
        file_type = self.determine_file_type(data, source_filename)
        
        session = SessionLocal()
        try:
            # Extract core fields
            transparency_calc = TransparencyCalculation(
                id=str(uuid.uuid4()),
                tech_record_id=data.get('TechRcrdId'),
                isin=data.get('ISIN') or data.get('Id'),  # FULECR_E uses 'Id' instead of 'ISIN'
                from_date=self._parse_date(data.get('FrDt')),
                to_date=self._parse_date(data.get('ToDt')),
                liquidity=self._parse_boolean(data.get('Lqdty')),
                total_transactions_executed=data.get('TtlNbOfTxsExctd'),
                total_volume_executed=data.get('TtlVolOfTxsExctd'),
                file_type=file_type,
                source_file=source_filename,
                raw_data=data.copy()  # Store all original data
            )
            
            session.add(transparency_calc)
            session.flush()  # Get the ID
            
            # Create threshold records
            thresholds = TransparencyThreshold.create_from_fitrs_data(
                transparency_calc.id, 
                data
            )
            
            for threshold in thresholds:
                session.add(threshold)
            
            session.commit()
            
            # Refresh and load the thresholds relationship
            session.refresh(transparency_calc)
            # Eager load the thresholds to avoid lazy loading issues
            _ = len(transparency_calc.thresholds)  # This loads the relationship and forces evaluation
            
            self.logger.info(f"Created transparency calculation {transparency_calc.id} for {file_type}")
            
            # Create a detached copy to return
            session.expunge(transparency_calc)
            return transparency_calc
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to create transparency calculation: {str(e)}")
            raise TransparencyServiceError(f"Failed to create transparency calculation: {str(e)}")
        finally:
            session.close()

    def get_transparency_by_isin(self, isin: str) -> Optional[List[TransparencyCalculation]]:
        """Get all transparency calculations for an ISIN"""
        session = SessionLocal()
        try:
            calculations = session.query(TransparencyCalculation).filter(
                TransparencyCalculation.isin == isin
            ).all()
            return calculations if calculations else None
        except Exception as e:
            self.logger.error(f"Failed to get transparency for ISIN {isin}: {str(e)}")
            raise TransparencyServiceError(f"Failed to get transparency: {str(e)}")
        finally:
            session.close()

    def delete_transparency_calculation(self, calc_id: str) -> bool:
        """Delete a transparency calculation and all associated thresholds"""
        session = SessionLocal()
        try:
            calc = session.query(TransparencyCalculation).filter(
                TransparencyCalculation.id == calc_id
            ).first()
            
            if calc:
                session.delete(calc)  # Cascades to thresholds automatically
                session.commit()
                self.logger.info(f"Deleted transparency calculation {calc_id}")
                return True
            return False
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to delete transparency calculation {calc_id}: {str(e)}")
            raise TransparencyServiceError(f"Failed to delete transparency calculation: {str(e)}")
        finally:
            session.close()

    def process_fitrs_file(self, file_data: pd.DataFrame, source_filename: str) -> List[TransparencyCalculation]:
        """Process an entire FITRS file and create transparency calculations"""
        results = []
        
        self.logger.info(f"Processing FITRS file {source_filename} with {len(file_data)} records")
        
        for index, row in file_data.iterrows():
            try:
                # Convert pandas Series to dict, handling NaN values
                data = {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}
                
                calc = self.create_transparency_calculation(
                    data=data,
                    source_filename=source_filename
                )
                results.append(calc)
                
            except Exception as e:
                self.logger.warning(f"Failed to process row {index} in {source_filename}: {str(e)}")
                continue
        
        self.logger.info(f"Successfully processed {len(results)} transparency calculations from {source_filename}")
        return results

    def _parse_date(self, date_str: Union[str, date, None]) -> Optional[date]:
        """Parse date string to date object"""
        if not date_str:
            return None
        
        if isinstance(date_str, date):
            return date_str
        
        if isinstance(date_str, str):
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                try:
                    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').date()
                except ValueError:
                    self.logger.warning(f"Could not parse date: {date_str}")
                    return None
        
        return None

    def _parse_boolean(self, value: Union[str, bool, None]) -> Optional[bool]:
        """Parse boolean value from various formats"""
        if value is None:
            return None
        
        if isinstance(value, bool):
            return value
        
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        
        return bool(value)
