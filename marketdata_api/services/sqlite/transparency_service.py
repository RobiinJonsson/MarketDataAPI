"""
Unified Transparency Service

This service replaces the complex polymorphic inheritance transparency service
with a simplified approach using the unified transparency models.

Based on the successful FIRDS unification pattern.
"""

import uuid
import logging
import pandas as pd
import time
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
        """
        Validate required transparency data fields with improved handling for sparse data.
        
        Based on FITRS analysis, many fields have low fill rates:
        - Transaction data: ~25% fill rate
        - Threshold amounts: ~31% fill rate  
        - Dates: ~95% missing in some files
        """
        required_fields = ['TechRcrdId']
        missing = [f for f in required_fields if f not in data or data[f] is None]
        if missing:
            raise TransparencyValidationError(f"Missing required fields: {', '.join(missing)}")
        
        # Validate ISIN presence for non-equity data
        if 'ISIN' not in data and 'Id' not in data:
            raise TransparencyValidationError("Either ISIN or Id field must be present")
        
        # For debt instruments, check for basic classification
        if 'FinInstrmClssfctn' in data:
            classification = data.get('FinInstrmClssfctn', '').upper()
            if classification == 'BOND':
                # Debt-specific validation - be lenient with sparse data
                if not data.get('Desc') and not data.get('CritVal'):
                    self.logger.warning(f"Debt instrument missing description and criteria value")
        
        # Validate numeric fields when present
        numeric_fields = ['TtlNbOfTxsExctd', 'TtlVolOfTxsExctd', 'PreTradLrgInScaleThrshld_Amt', 
                         'PstTradLrgInScaleThrshld_Amt', 'PreTradInstrmSzSpcfcThrshld_Amt', 
                         'PstTradInstrmSzSpcfcThrshld_Amt']
        
        for field in numeric_fields:
            if field in data and data[field] is not None and data[field] != '':
                try:
                    float(data[field])
                except (ValueError, TypeError):
                    self.logger.warning(f"Invalid numeric value for {field}: {data[field]}")
                    data[field] = None  # Set to None rather than fail validation
    
    def determine_file_type(self, data: Dict[str, Any], source_filename: str = None) -> str:
        """
        Determine FITRS file type from data structure or filename.
        
        Based on FITRS analysis, we have these instrument types:
        - FULECR: C (ETFs/ETCs), E (Equities/Shares), R (Rights)  
        - FULNCR: C (Corporate/Certificates), D (Debt/Bonds), E (ETFs), F (Funds/Derivatives), 
                  H (Structured Products), I (Index-linked), J (Warrants), O (Options)
        
        Returns: Specific file type like 'FULECR_E', 'FULNCR_D', etc.
        """
        # Try filename first if available - this is the most reliable method
        if source_filename:
            import re
            
            # Match all the actual instrument types found in FITRS analysis
            instrument_patterns = {
                # FULECR patterns (equity files)
                'FULECR_C': r'FULECR.*_C_',  # ETFs/ETCs
                'FULECR_E': r'FULECR.*_E_',  # Equities/Shares
                'FULECR_R': r'FULECR.*_R_',  # Rights
                
                # FULNCR patterns (non-equity files)
                'FULNCR_C': r'FULNCR.*_C_',  # Corporate/Certificates
                'FULNCR_D': r'FULNCR.*_D_',  # Debt/Bonds  
                'FULNCR_E': r'FULNCR.*_E_',  # ETFs (non-equity)
                'FULNCR_F': r'FULNCR.*_F_',  # Funds/Derivatives
                'FULNCR_H': r'FULNCR.*_H_',  # Structured Products
                'FULNCR_I': r'FULNCR.*_I_',  # Index-linked
                'FULNCR_J': r'FULNCR.*_J_',  # Warrants
                'FULNCR_O': r'FULNCR.*_O_',  # Options
            }
            
            for file_type, pattern in instrument_patterns.items():
                if re.search(pattern, source_filename):
                    return file_type
        
        # Enhanced data structure analysis for when filename isn't available
        has_isin = 'ISIN' in data and data.get('ISIN')
        has_id_only = 'Id' in data and data.get('Id') and not has_isin
        has_desc = 'Desc' in data and data.get('Desc')
        has_methodology = 'Mthdlgy' in data and data.get('Mthdlgy')
        has_classification = 'FinInstrmClssfctn' in data and data.get('FinInstrmClssfctn')
        
        # Get key classification indicators
        classification = data.get('FinInstrmClssfctn', '').upper()
        description = data.get('Desc', '').lower()
        criteria_value = data.get('CritVal', '').upper()
        
        # Equity classification (FULECR files)
        if has_id_only and has_methodology and not has_desc:
            # This is equity data - determine specific type
            if 'equity' in description or 'EQTY' in classification:
                return 'FULECR_E'  # Shares/Equities
            elif 'etc' in description or 'etf' in description:
                return 'FULECR_C'  # ETFs/ETCs
            elif 'right' in description or 'RGHT' in classification:
                return 'FULECR_R'  # Rights
            else:
                return 'FULECR_E'  # Default to equities
        
        # Non-equity classification (FULNCR files) - be specific about instrument types
        elif has_isin and has_desc:
            # Debt instruments
            if classification == 'BOND' or 'bond' in description or 'BOND' in criteria_value:
                return 'FULNCR_D'  # Debt/Bonds
            
            # ETFs (non-equity)
            elif classification == 'ETFS' or 'etf' in description or 'ETC' in description:
                return 'FULNCR_E'  # ETFs (non-equity category)
                
            # Structured products  
            elif 'structured' in description or 'STRP' in classification:
                return 'FULNCR_H'  # Structured Products
                
            # Warrants
            elif 'warrant' in description or 'WRNT' in classification:
                return 'FULNCR_J'  # Warrants
                
            # Options
            elif 'option' in description or 'OPTN' in classification:
                return 'FULNCR_O'  # Options
                
            # Index-linked
            elif 'index' in description or 'INDX' in classification:
                return 'FULNCR_I'  # Index-linked
                
            # Funds and derivatives (complex instruments)
            elif any(f'CritNm_{i}' in data for i in range(3, 8)) or 'fund' in description:
                return 'FULNCR_F'  # Funds/Derivatives
                
            # Default corporate/certificates
            else:
                return 'FULNCR_C'  # Corporate/Certificates
        
        # Fallback
        self.logger.warning(f"Could not determine specific file type for data: {data.keys()}")
        return 'FULNCR_C'  # Conservative fallback
        
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
                liquidity=self._determine_liquidity(data, file_type),
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

    def create_transparency(self, isin: str, instrument_type: str = None) -> List[TransparencyCalculation]:
        """
        Create transparency calculations for an ISIN from FITRS data.
        
        This method requires the ISIN to exist in the instruments table (FIRDS reference data).
        If the ISIN doesn't exist in instruments, it raises an error.
        Searches FITRS files to create transparency data.
        
        Args:
            isin: The ISIN to create transparency data for
            instrument_type: The instrument type to determine which FITRS files to search
        """
        # 1. First check if ISIN exists in instruments table (FIRDS reference data)
        session = SessionLocal()
        try:
            instrument = session.query(Instrument).filter(
                Instrument.isin == isin
            ).first()
            
            if not instrument:
                raise TransparencyNotFoundError(f"ISIN {isin} does not exist in the database")
            
            # Use provided instrument_type or get from database
            final_instrument_type = instrument_type or instrument.instrument_type
            self.logger.info(f"Found instrument {isin} with type {final_instrument_type}")
            
        finally:
            session.close()
        
        # 2. Check if transparency calculations already exist
        existing_calculations = self.get_transparency_by_isin(isin)
        if existing_calculations:
            self.logger.info(f"Found {len(existing_calculations)} existing transparency calculations for {isin}")
            return existing_calculations
        
        # 3. Search FITRS files to create them
        self.logger.info(f"No transparency data found for {isin}, searching FITRS files...")
        
        # Search for ISIN in stored FITRS files
        created_calculations = self._search_and_create_from_fitrs_files(isin, final_instrument_type)
        
        if not created_calculations:
            self.logger.warning(f"No transparency data found in FITRS files for {isin}")
            return []
        
        self.logger.info(f"Created {len(created_calculations)} transparency calculations for {isin} from FITRS files")
        return created_calculations

    def get_all_transparency_calculations(self) -> List[TransparencyCalculation]:
        """Get all transparency calculations"""
        session = SessionLocal()
        try:
            calculations = session.query(TransparencyCalculation).all()
            # Detach from session to avoid issues
            for calc in calculations:
                session.expunge(calc)
            return calculations
        except Exception as e:
            self.logger.error(f"Failed to get all transparency calculations: {str(e)}")
            return []
        finally:
            session.close()

    def get_transparency_by_isin(self, isin: str) -> Optional[List[TransparencyCalculation]]:
        """Get all transparency calculations for an ISIN"""
        session = SessionLocal()
        try:
            calculations = session.query(TransparencyCalculation).filter(
                TransparencyCalculation.isin == isin
            ).all()
            # Detach from session to avoid issues
            for calc in calculations:
                session.expunge(calc)
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

    def _search_and_create_from_fitrs_files(self, isin: str, instrument_type: str) -> List[TransparencyCalculation]:
        """
        Search for ISIN in stored FITRS files and create transparency calculations.
        
        Uses CFI code-based file selection when possible for optimal performance:
        - C -> FULNCR_C/FULECR_C files (Collective investment vehicles)
        - D -> FULNCR_D files (Debt instruments)
        - E -> FULECR_E/FULNCR_E files (Equities)
        - F -> FULNCR_F files (Futures)
        - H -> FULNCR_H files (Structured products)
        - I -> FULNCR_I files (Index-linked)
        - J -> FULNCR_J files (Warrants)
        - O -> FULNCR_O files (Options)
        - R -> FULECR_R files (Rights)
        
        Falls back to instrument_type-based mapping when CFI code is not available.
        
        Args:
            isin: The ISIN to search for
            instrument_type: The instrument type (fallback for CFI detection)
            
        Returns:
            List of created TransparencyCalculation instances
        """
        import os
        import pandas as pd
        
        fitrs_directory = "c:/Users/robin/Projects/MarketDataAPI/downloads/fitrs"
        created_calculations = []
        
        if not os.path.exists(fitrs_directory):
            self.logger.warning(f"FITRS directory not found: {fitrs_directory}")
            return []
        
        # Get all FITRS CSV files
        all_fitrs_files = [f for f in os.listdir(fitrs_directory) if f.endswith('.csv')]
        
        # First try CFI-based file pattern detection for optimal accuracy
        cfi_based_patterns = self._get_cfi_based_file_patterns(isin)
        search_method = "CFI-based"
        
        # Check if CFI-based returned actual file patterns or fallback
        if cfi_based_patterns == ['FULNCR_', 'FULECR_']:  # General fallback patterns
            # Fall back to instrument type-based letter patterns
            target_letters = self._get_fitrs_file_patterns(instrument_type)
            search_method = "instrument-type-based"
        else:
            # CFI-based returned specific patterns, but we need to convert them to letters
            # Extract letters from instrument database lookup
            try:
                session = SessionLocal()
                try:
                    instrument = session.query(Instrument).filter(Instrument.isin == isin).first()
                    if instrument and instrument.cfi_code:
                        target_letters = [instrument.cfi_code[0].upper()]
                    else:
                        target_letters = self._get_fitrs_file_patterns(instrument_type)
                finally:
                    session.close()
            except:
                target_letters = self._get_fitrs_file_patterns(instrument_type)
        
        # Filter files using precise letter matching
        target_files = self._filter_fitrs_files_by_letter(all_fitrs_files, target_letters)
        
        self.logger.info(f"Using {search_method} search: {len(target_files)} FITRS files for ISIN {isin}")
        self.logger.debug(f"Target letters: {target_letters}")
        self.logger.debug(f"Target files: {target_files}")
        
        for filename in target_files:
            filepath = os.path.join(fitrs_directory, filename)
            self.logger.debug(f"Searching file {filename} for ISIN {isin}")
            
            try:
                # Read the CSV file with dtype specification to avoid warnings
                # Most FITRS columns are mixed text/numeric, so read as string first
                df = pd.read_csv(filepath, dtype=str, low_memory=False)
                
                # Search for the ISIN in both 'ISIN' and 'Id' columns (FULECR uses 'Id')
                # Fixed pandas alignment issue by using proper column checks
                matching_rows = pd.DataFrame()
                
                if 'ISIN' in df.columns:
                    isin_matches = df[df['ISIN'] == isin]
                    matching_rows = pd.concat([matching_rows, isin_matches], ignore_index=True)
                
                if 'Id' in df.columns:
                    id_matches = df[df['Id'] == isin]
                    matching_rows = pd.concat([matching_rows, id_matches], ignore_index=True)
                
                # Remove duplicates if any
                matching_rows = matching_rows.drop_duplicates()
                
                if not matching_rows.empty:
                    self.logger.info(f"Found {len(matching_rows)} records for {isin} in {filename}")
                    
                    # Create transparency calculations for each matching row
                    for index, row in matching_rows.iterrows():
                        try:
                            # Convert pandas Series to dict, handling NaN values
                            data = {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}
                            
                            calc = self.create_transparency_calculation(
                                data=data,
                                source_filename=filename
                            )
                            created_calculations.append(calc)
                            
                        except Exception as e:
                            self.logger.warning(f"Failed to create transparency calculation from row {index} in {filename}: {str(e)}")
                            continue
                            
            except Exception as e:
                self.logger.warning(f"Failed to read FITRS file {filename}: {str(e)}")
                continue
        
        self.logger.info(f"Created {len(created_calculations)} transparency calculations for {isin} from FITRS files")
        return created_calculations

    def _get_fitrs_file_patterns(self, instrument_type_or_cfi: str) -> List[str]:
        """
        Get FITRS file patterns using CFI manager for consistency.
        
        Returns specific letter patterns to match in FITRS filenames.
        FITRS format: FUL{ECR|NCR}_{date}_{letter}_{part}_fitrs_data.csv
        
        Args:
            instrument_type_or_cfi: Instrument type or CFI first letter
            
        Returns:
            List of single letters to match in FITRS filenames
        """
        from marketdata_api.models.utils.cfi_instrument_manager import CFIInstrumentTypeManager
        
        # If it's a single letter, treat as CFI category
        if len(instrument_type_or_cfi) == 1:
            letter = instrument_type_or_cfi.upper()
            self.logger.info(f"CFI-based mapping: '{instrument_type_or_cfi}' -> ['{letter}']")
            return [letter]
        
        # For longer strings, map to CFI letters
        legacy_to_cfi_mapping = {
            'equity': 'E',
            'share': 'E', 
            'stock': 'E',
            'debt': 'D',
            'bond': 'D',
            'note': 'D',
            'debenture': 'D',
            'collective_investment': 'C',
            'fund': 'C',
            'etf': 'C',
            'future': 'F',
            'futures': 'F',
            'structured': 'H',
            'structured_product': 'H',
            'index_linked': 'I',
            'warrant': 'J',
            'warrants': 'J',
            'option': 'O',
            'options': 'O',
            'rights': 'R'
        }
        
        # Map legacy type to CFI letter
        cfi_letter = legacy_to_cfi_mapping.get(instrument_type_or_cfi.lower(), 'C')
        
        self.logger.info(f"Legacy type '{instrument_type_or_cfi}' mapped to CFI letter '{cfi_letter}'")
        return [cfi_letter]
    
    def _filter_fitrs_files_by_letter(self, all_files: List[str], target_letters: List[str]) -> List[str]:
        """
        Filter FITRS files by letter using precise filename parsing.
        
        Args:
            all_files: List of all FITRS filenames
            target_letters: List of letters to match (e.g., ['E', 'D'])
            
        Returns:
            List of matching filenames
        """
        import re
        
        matching_files = []
        
        for filename in all_files:
            # Parse filename format: FUL{ECR|NCR}_{date}_{letter}_{part}_fitrs_data.csv
            match = re.match(r'^FUL(ECR|NCR)_\d{8}_([A-Z])_\d+of\d+_fitrs_data\.csv$', filename)
            if match:
                file_type = match.group(1)  # ECR or NCR
                file_letter = match.group(2)  # C, D, E, F, H, I, J, O, R, S
                
                # Check if this file letter matches our target
                if file_letter in target_letters:
                    matching_files.append(filename)
        
        return matching_files

    def _get_cfi_based_file_patterns(self, isin: str) -> List[str]:
        """
        Get FITRS file patterns based on the instrument's CFI code using CFI manager.
        
        This method uses the CFI model as the single source of truth for file pattern determination.
        
        Args:
            isin: The ISIN to look up
            
        Returns:
            List of FITRS filename patterns optimized for this instrument type
        """
        from marketdata_api.models.utils.cfi_instrument_manager import CFIInstrumentTypeManager
        
        try:
            # Get the instrument's CFI code from the database
            session = SessionLocal()
            try:
                instrument = session.query(Instrument).filter(
                    Instrument.isin == isin
                ).first()
                
                if instrument and instrument.cfi_code:
                    # Use CFI manager for consistent pattern determination
                    patterns = CFIInstrumentTypeManager.get_fitrs_patterns_from_cfi(instrument.cfi_code)
                    self.logger.info(f"CFI-based file pattern for ISIN {isin}: CFI {instrument.cfi_code} -> {patterns}")
                    return patterns
                else:
                    # Fallback to general search if no CFI code available
                    self.logger.info(f"No CFI code found for ISIN {isin}, using general pattern")
                    return ['FULNCR_', 'FULECR_']
            finally:
                session.close()
                
        except Exception as e:
            self.logger.warning(f"Error getting CFI-based patterns for {isin}: {str(e)}")
            return ['FULNCR_', 'FULECR_']  # Safe fallback

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

    def _determine_liquidity(self, data: Dict[str, Any], file_type: str) -> Optional[bool]:
        """
        Determine liquidity status with smart inference based on FITRS file analysis.
        
        Based on analysis:
        - FULECR_E files often have missing Lqdty but contain actual trading data
        - FULNCR files have explicit Lqdty values but no trading data
        - If trading volume/transactions exist, instrument should be considered liquid
        """
        # First check if explicit liquidity flag exists
        lqdty_value = data.get('Lqdty')
        if lqdty_value is not None and lqdty_value != '':
            return self._parse_boolean(lqdty_value)
        
        # For FULECR_E files (equity shares), infer liquidity from trading activity
        if file_type == 'FULECR_E':
            volume = data.get('TtlVolOfTxsExctd')
            transactions = data.get('TtlNbOfTxsExctd')
            
            # If there's actual trading activity, consider it liquid
            if volume and transactions:
                try:
                    volume_float = float(volume)
                    transactions_int = int(transactions)
                    if volume_float > 0 or transactions_int > 0:
                        return True
                except (ValueError, TypeError):
                    pass
        
        # For other file types without explicit liquidity flag, return None
        # This preserves the original behavior for non-equity instruments
        return None

    def create_transparency_bulk(self, 
                               limit: Optional[int] = None,
                               batch_size: int = 10,
                               skip_existing: bool = True) -> Dict[str, Any]:
        """
        Create transparency calculations in bulk for instruments that don't have them yet.
        
        Args:
            limit: Maximum number of instruments to process (None = no limit)
            batch_size: Number of instruments to process per batch (default: 10)
            skip_existing: Skip instruments that already have transparency data (default: True)
            
        Returns:
            Dict with creation results and statistics
        """
        start_time = time.time()
        results = {
            'total_instruments': 0,
            'total_processed': 0,
            'total_created_calculations': 0,
            'total_skipped': 0,
            'total_failed': 0,
            'failed_instruments': [],
            'successful_instruments': [],
            'batch_results': [],
            'elapsed_time': 0
        }
        
        try:
            self.logger.info(f"🚀 Starting bulk transparency creation")
            self.logger.info(f"   Limit: {limit or 'No limit'}")
            self.logger.info(f"   Skip existing: {skip_existing}")
            self.logger.info(f"   Batch size: {batch_size}")
            
            # Get instruments without transparency calculations
            instruments_to_process = self._get_instruments_without_transparency(limit, skip_existing)
            
            if not instruments_to_process:
                self.logger.warning(f"❌ No instruments found that need transparency calculations")
                return results
            
            results['total_instruments'] = len(instruments_to_process)
            self.logger.info(f"📊 Found {len(instruments_to_process)} instruments needing transparency calculations")
            
            # Process in batches
            total_batches = (len(instruments_to_process) + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                batch_start_idx = batch_idx * batch_size
                batch_end_idx = min(batch_start_idx + batch_size, len(instruments_to_process))
                batch_instruments = instruments_to_process[batch_start_idx:batch_end_idx]
                
                batch_start_time = time.time()
                self.logger.info(f"🔄 Processing batch {batch_idx + 1}/{total_batches} ({len(batch_instruments)} instruments)")
                
                batch_result = self._process_transparency_batch(batch_instruments)
                
                # Update overall results
                results['total_processed'] += batch_result['processed']
                results['total_created_calculations'] += batch_result['created_calculations']
                results['total_skipped'] += batch_result['skipped']
                results['total_failed'] += batch_result['failed']
                results['failed_instruments'].extend(batch_result['failed_instruments'])
                results['successful_instruments'].extend(batch_result['successful_instruments'])
                
                batch_elapsed = time.time() - batch_start_time
                batch_result['elapsed_time'] = batch_elapsed
                results['batch_results'].append(batch_result)
                
                self.logger.info(f"✅ Batch {batch_idx + 1} completed: {batch_result['created_calculations']} calculations created, {batch_result['failed']} failed ({batch_elapsed:.1f}s)")
                
                # Progress update
                progress_pct = (results['total_processed'] / len(instruments_to_process)) * 100
                self.logger.info(f"📈 Overall progress: {results['total_processed']}/{len(instruments_to_process)} ({progress_pct:.1f}%)")
            
            results['elapsed_time'] = time.time() - start_time
            
            # Final summary
            self.logger.info(f"🎉 Bulk transparency creation completed!")
            self.logger.info(f"   Total instruments: {results['total_instruments']}")
            self.logger.info(f"   Total processed: {results['total_processed']}")
            self.logger.info(f"   Total calculations created: {results['total_created_calculations']}")
            self.logger.info(f"   Total failed: {results['total_failed']}")
            self.logger.info(f"   Total time: {results['elapsed_time']:.1f}s")
            
            return results
            
        except Exception as e:
            results['elapsed_time'] = time.time() - start_time
            self.logger.error(f"💥 Bulk transparency creation failed: {str(e)}")
            raise TransparencyServiceError(f"Bulk transparency creation failed: {str(e)}") from e

    def _get_instruments_without_transparency(self, 
                                            limit: Optional[int] = None,
                                            skip_existing: bool = True) -> List[Dict[str, Any]]:
        """Get instruments that don't have transparency calculations yet."""
        session = SessionLocal()
        
        try:
            if skip_existing:
                # Find instruments that don't have any transparency calculations
                subquery = session.query(TransparencyCalculation.isin).distinct()
                query = session.query(Instrument).filter(
                    ~Instrument.isin.in_(subquery)
                )
            else:
                # Get all instruments
                query = session.query(Instrument)
            
            if limit:
                query = query.limit(limit)
            
            instruments = query.all()
            
            # Convert to dict format for processing
            instrument_data = []
            for instrument in instruments:
                instrument_data.append({
                    'isin': instrument.isin,
                    'instrument_type': instrument.instrument_type,
                    'name': instrument.full_name or instrument.short_name,
                    'cfi_code': instrument.cfi_code
                })
            
            self.logger.info(f"🔍 Found {len(instrument_data)} instruments without transparency calculations")
            return instrument_data
            
        finally:
            session.close()

    def _process_transparency_batch(self, instruments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process a batch of instruments for transparency creation."""
        batch_result = {
            'processed': 0,
            'created_calculations': 0,
            'skipped': 0,
            'failed': 0,
            'failed_instruments': [],
            'successful_instruments': []
        }
        
        for instrument_data in instruments:
            isin = instrument_data['isin']
            instrument_type = instrument_data['instrument_type']
            
            try:
                self.logger.debug(f"   🔨 Creating transparency for {isin}...")
                
                # Create transparency calculations for this instrument
                calculations = self.create_transparency(isin, instrument_type)
                
                batch_result['processed'] += 1
                
                if calculations:
                    calc_count = len(calculations)
                    batch_result['created_calculations'] += calc_count
                    batch_result['successful_instruments'].append({
                        'isin': isin,
                        'calculations_created': calc_count
                    })
                    self.logger.debug(f"   ✅ Created {calc_count} calculations for {isin}")
                else:
                    batch_result['skipped'] += 1
                    self.logger.debug(f"   ⚪ No transparency data found for {isin}")
                
            except Exception as e:
                batch_result['failed'] += 1
                batch_result['processed'] += 1
                error_msg = str(e)
                batch_result['failed_instruments'].append({
                    'isin': isin, 
                    'error': error_msg
                })
                self.logger.warning(f"   ❌ Failed to create transparency for {isin}: {error_msg}")
        
        return batch_result
