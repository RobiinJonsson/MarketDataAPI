import uuid
import logging
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from ..database.session import get_session, SessionLocal
from ..database.model_mapper import map_transparency_data
from ..models.transparency import TransparencyCalculation, EquityTransparency, NonEquityTransparency, DebtTransparency, FuturesTransparency
from ..models.instrument import Instrument
from datetime import datetime, UTC
from .esma_data_loader import EsmaDataLoader
from ..config import esmaConfig


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

class TransparencyService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.esma_loader = EsmaDataLoader(esmaConfig.start_date, esmaConfig.end_date)

    def validate_transparency_data(self, data: Dict[str, Any]) -> None:
        """Validate required transparency data fields"""
        required_fields = ['ISIN', 'TechRcrdId']
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise TransparencyValidationError(f"Missing required fields: {', '.join(missing)}")

    def create_transparency_calculation(self, data: Dict[str, Any], calculation_type: str = "NON_EQUITY") -> TransparencyCalculation:
        """
        Create a new transparency calculation in the database.
        
        Args:
            data: Dictionary containing transparency data
            calculation_type: Type of calculation ('EQUITY' or 'NON_EQUITY')
            
        Returns:
            Created TransparencyCalculation instance
        """
        self.validate_transparency_data(data)
        session = SessionLocal()
        
        try:
            # Determine instrument type from data or CFI code
            instrument_type = self._determine_instrument_type(data)
            
            # Map data to transparency models
            transparency_data = map_transparency_data(data, calculation_type, instrument_type)
            
            # Create base transparency calculation
            base_calc = TransparencyCalculation(
                id=str(uuid.uuid4()),
                **transparency_data['base']
            )
            
            session.add(base_calc)
            session.flush()  # Get the ID
            
            # Create specific transparency type based on instrument
            if calculation_type == "EQUITY":
                specific_calc = EquityTransparency(
                    id=base_calc.id,
                    **transparency_data['specific']
                )
            else:
                # Non-equity - determine if debt or futures
                if instrument_type == "debt":
                    specific_calc = DebtTransparency(
                        id=base_calc.id,
                        **transparency_data['specific']
                    )
                elif instrument_type == "futures":
                    specific_calc = FuturesTransparency(
                        id=base_calc.id,
                        **transparency_data['specific']
                    )
                else:
                    # Generic non-equity
                    specific_calc = NonEquityTransparency(
                        id=base_calc.id,
                        **transparency_data['specific']
                    )
            
            session.add(specific_calc)
            session.commit()
            session.refresh(base_calc)
            
            self.logger.info(f"Created transparency calculation with ID: {base_calc.id}")
            return base_calc
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to create transparency calculation: {str(e)}")
            raise TransparencyServiceError(f"Failed to create transparency calculation: {str(e)}") from e
        finally:
            session.close()

    def get_transparency_by_isin(self, isin: str, calculation_type: str = None) -> Tuple[Session, List[TransparencyCalculation]]:
        """Get transparency calculations for a specific ISIN"""
        session = SessionLocal()  # Use SessionLocal() instead of get_session()
        
        try:
            query = session.query(TransparencyCalculation).filter(
                TransparencyCalculation.isin == isin
            )
            
            if calculation_type:
                query = query.filter(TransparencyCalculation.calculation_type == calculation_type)
            
            # Add eager loading for related entities
            if calculation_type == "EQUITY":
                query = query.options(joinedload(TransparencyCalculation.equity_transparency))
            elif calculation_type == "NON_EQUITY":
                query = query.options(
                    joinedload(TransparencyCalculation.non_equity_transparency),
                    joinedload(TransparencyCalculation.debt_transparency),
                    joinedload(TransparencyCalculation.futures_transparency)
                )
            
            calculations = query.all()
            
            logger.info(f"Found {len(calculations)} transparency calculations for ISIN {isin} with type {calculation_type}")
            
            return session, calculations
            
        except Exception as e:
            logger.error(f"Error getting transparency by ISIN {isin}: {str(e)}")
            session.close()
            raise

    def get_transparency_by_id(self, transparency_id: str) -> Tuple[Session, Optional[TransparencyCalculation]]:
        """
        Retrieve a transparency calculation by ID.
        
        Args:
            transparency_id: The unique identifier of the transparency calculation
            
        Returns:
            Tuple of (Session, TransparencyCalculation)
        """
        session = SessionLocal()
        try:
            calculation = session.get(TransparencyCalculation, transparency_id)
            return session, calculation
        except:
            session.close()
            raise

    def update_transparency_calculation(self, transparency_id: str, data: Dict[str, Any]) -> Optional[TransparencyCalculation]:
        """
        Update an existing transparency calculation.
        
        Args:
            transparency_id: The unique identifier of the transparency calculation
            data: Dictionary containing updated transparency data
            
        Returns:
            The updated TransparencyCalculation instance if successful
        """
        session = SessionLocal()
        try:
            calculation = session.get(TransparencyCalculation, transparency_id)
            if not calculation:
                self.logger.warning(f"Transparency calculation with ID {transparency_id} not found")
                return None
            
            # Determine calculation type and instrument type
            calculation_type = calculation.calculation_type
            instrument_type = self._determine_instrument_type(data)
            
            # Map updated data
            transparency_data = map_transparency_data(data, calculation_type, instrument_type)
            
            # Update base calculation
            for key, value in transparency_data['base'].items():
                if hasattr(calculation, key):
                    setattr(calculation, key, value)
            
            # Update specific calculation if it exists
            if calculation_type == "EQUITY" and hasattr(calculation, 'equity_transparency'):
                for key, value in transparency_data['specific'].items():
                    if hasattr(calculation.equity_transparency, key):
                        setattr(calculation.equity_transparency, key, value)
            elif calculation_type == "NON_EQUITY":
                # Handle different non-equity types
                if instrument_type == "debt" and hasattr(calculation, 'debt_transparency'):
                    for key, value in transparency_data['specific'].items():
                        if hasattr(calculation.debt_transparency, key):
                            setattr(calculation.debt_transparency, key, value)
                elif instrument_type == "futures" and hasattr(calculation, 'futures_transparency'):
                    for key, value in transparency_data['specific'].items():
                        if hasattr(calculation.futures_transparency, key):
                            setattr(calculation.futures_transparency, key, value)
                elif hasattr(calculation, 'non_equity_transparency'):
                    for key, value in transparency_data['specific'].items():
                        if hasattr(calculation.non_equity_transparency, key):
                            setattr(calculation.non_equity_transparency, key, value)
            
            session.commit()
            session.refresh(calculation)
            self.logger.info(f"Updated transparency calculation with ID: {transparency_id}")
            return calculation
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to update transparency calculation: {str(e)}")
            raise TransparencyServiceError(f"Failed to update transparency calculation: {str(e)}") from e
        finally:
            session.close()

    def delete_transparency_calculation(self, transparency_id: str) -> bool:
        """Delete a transparency calculation by its identifier."""
        session = SessionLocal()
        try:
            calculation = session.get(TransparencyCalculation, transparency_id)
            if calculation:
                session.delete(calculation)
                session.commit()
                self.logger.info(f"Deleted transparency calculation with ID: {transparency_id}")
                return True
            return False
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to delete transparency calculation: {str(e)}")
            raise TransparencyServiceError(f"Failed to delete transparency calculation: {str(e)}") from e
        finally:
            session.close()

    def get_transparency_by_instrument_type(self, instrument_type: str, limit: int = 100) -> Tuple[Session, List[TransparencyCalculation]]:
        """
        Get transparency calculations by instrument type.
        
        Args:
            instrument_type: Type of instrument ('equity', 'debt', 'futures')
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (Session, List[TransparencyCalculation])
        """
        session = SessionLocal()
        try:
            query = session.query(TransparencyCalculation)
            
            if instrument_type == "equity":
                query = query.filter(TransparencyCalculation.calculation_type == "EQUITY")
            else:
                query = query.filter(TransparencyCalculation.calculation_type == "NON_EQUITY")
                
                # Further filter by specific instrument type if needed
                if instrument_type in ["debt", "futures"]:
                    # This would require joining with specific tables
                    pass
            
            calculations = query.limit(limit).all()
            return session, calculations
        except:
            session.close()
            raise

    def batch_create_transparency_data(self, transparency_records: List[Dict[str, Any]]) -> int:
        """
        Batch create transparency calculations.
        
        Args:
            transparency_records: List of transparency data dictionaries
            
        Returns:
            Number of successfully created records
        """
        created_count = 0
        session = SessionLocal()
        
        try:
            for record in transparency_records:
                try:
                    # Determine calculation type from data
                    calculation_type = "EQUITY" if record.get('calculation_type') == "EQUITY" else "NON_EQUITY"
                    instrument_type = self._determine_instrument_type(record)
                    
                    # Check for existing record
                    existing = session.query(TransparencyCalculation).filter(
                        TransparencyCalculation.isin == record.get('ISIN'),
                        TransparencyCalculation.tech_record_id == record.get('TechRcrdId')
                    ).first()
                    
                    if existing:
                        self.logger.info(f"Transparency calculation for ISIN {record.get('ISIN')} already exists. Skipping.")
                        continue
                    
                    # Map and create transparency data
                    transparency_data = map_transparency_data(record, calculation_type, instrument_type)
                    
                    # Create base calculation
                    base_calc = TransparencyCalculation(
                        id=str(uuid.uuid4()),
                        **transparency_data['base']
                    )
                    session.add(base_calc)
                    session.flush()
                    
                    # Create specific calculation
                    if calculation_type == "EQUITY":
                        specific_calc = EquityTransparency(
                            id=base_calc.id,
                            **transparency_data['specific']
                        )
                    else:
                        if instrument_type == "debt":
                            specific_calc = DebtTransparency(
                                id=base_calc.id,
                                **transparency_data['specific']
                            )
                        elif instrument_type == "futures":
                            specific_calc = FuturesTransparency(
                                id=base_calc.id,
                                **transparency_data['specific']
                            )
                        else:
                            specific_calc = NonEquityTransparency(
                                id=base_calc.id,
                                **transparency_data['specific']
                            )
                    
                    session.add(specific_calc)
                    created_count += 1
                    
                    # Commit in batches
                    if created_count % 100 == 0:
                        session.commit()
                        self.logger.info(f"Committed {created_count} transparency records...")
                        
                except Exception as e:
                    self.logger.error(f"Error creating transparency record: {str(e)}")
                    session.rollback()
                    continue
            
            # Final commit
            session.commit()
            self.logger.info(f"Successfully created {created_count} transparency calculations")
            return created_count
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Batch creation failed: {str(e)}")
            raise TransparencyServiceError(f"Batch creation failed: {str(e)}") from e
        finally:
            session.close()

    def _determine_instrument_type(self, data: Dict[str, Any]) -> str:
        """Determine instrument type from transparency data"""
        # Check for specific indicators in the data
        desc = data.get('Desc', '').lower()
        cfi_val = data.get('CritVal', '')
        fin_class = data.get('FinInstrmClssfctn', '')
        
        # Futures indicators
        if 'future' in desc or 'forward' in desc or fin_class == 'DERV':
            return "futures"
        
        # Debt indicators
        if 'bond' in desc or 'debt' in desc or cfi_val.startswith('BOND') or fin_class == 'BOND':
            return "debt"
        
        # Check for securitised derivatives (often debt-like)
        if cfi_val == 'SDRV' or 'securitised' in desc:
            return "debt"
        
        # Default to generic non-equity
        return "non_equity"

    def get_or_create_transparency_calculation(self, isin: str, calculation_type: str, ensure_instrument: bool = True) -> List[TransparencyCalculation]:
        """
        Get existing transparency calculations or create from FITRS data.
        
        Args:
            isin: The ISIN to search for
            calculation_type: 'EQUITY' or 'NON_EQUITY'
            ensure_instrument: Whether to ensure instrument exists before creating transparency data
            
        Returns:
            List of TransparencyCalculation instances (multiple venues possible)
        """
        try:
            # Check if transparency calculations exist first
            session, existing_calculations = self.get_transparency_by_isin(isin)
            try:
                type_calculations = [calc for calc in existing_calculations if calc.calculation_type == calculation_type]
                if type_calculations:
                    for calc in type_calculations:
                        session.refresh(calc)
                    self.logger.info(f"Found {len(type_calculations)} existing transparency calculations for ISIN {isin}")
                    return type_calculations
            finally:
                session.close()

            # If ensure_instrument is True, check/create instrument first
            if ensure_instrument:
                try:
                    from .instrument_service import InstrumentService
                    instrument_service = InstrumentService()
                    
                    # Try to get or create the instrument first
                    instrument = instrument_service.get_or_create_instrument(isin, calculation_type.lower())
                    if not instrument:
                        self.logger.warning(f"Could not create/find instrument for ISIN {isin}, proceeding without instrument context")
                except Exception as e:
                    self.logger.warning(f"Error handling instrument for ISIN {isin}: {str(e)}, proceeding without instrument context")

            # If not found, get FITRS data and create
            transparency_records = self._get_fitrs_data(isin, calculation_type)
            if not transparency_records:
                self.logger.warning(f"No FITRS data found for ISIN {isin} with type {calculation_type}")
                return []

            # Create transparency calculations for each record (multiple venues)
            created_calculations = []
            for i, transparency_data in enumerate(transparency_records):
                try:
                    # Check if this specific record already exists (by tech_record_id)
                    tech_record_id = transparency_data.get('TechRcrdId')
                    if tech_record_id:
                        session, existing = self.get_transparency_by_tech_record_id(tech_record_id)
                        session.close()
                        if existing:
                            self.logger.info(f"Transparency calculation for tech record {tech_record_id} already exists. Skipping.")
                            continue
                    
                    calculation = self.create_transparency_calculation(transparency_data, calculation_type)
                    if calculation:
                        created_calculations.append(calculation)
                        self.logger.info(f"Created transparency calculation {i+1}/{len(transparency_records)}: {calculation.id}")
                        
                except Exception as e:
                    self.logger.error(f"Failed to create transparency calculation for record {i+1}: {str(e)}")
                    continue

            self.logger.info(f"Created {len(created_calculations)} transparency calculations for ISIN {isin}")
            return created_calculations

        except Exception as e:
            self.logger.error(f"Failed to get/create transparency calculations for {isin}: {str(e)}")
            raise TransparencyServiceError(f"Failed to get/create transparency calculations: {str(e)}")

    def get_or_create_transparency_calculation_single(self, isin: str, calculation_type: str, ensure_instrument: bool = True) -> Optional[TransparencyCalculation]:
        """
        Get existing transparency calculation or create from FITRS data (returns first/most recent).
        
        Args:
            isin: The ISIN to search for
            calculation_type: 'EQUITY' or 'NON_EQUITY'
            ensure_instrument: Whether to ensure instrument exists before creating transparency data
            
        Returns:
            TransparencyCalculation instance if found/created, None otherwise
        """
        calculations = self.get_or_create_transparency_calculation(isin, calculation_type, ensure_instrument)
        if calculations:
            # Return the most recent one (assuming they're ordered by creation)
            return calculations[-1]
        return None

    def _get_instrument_cfi_from_isin(self, isin: str) -> Optional[str]:
        """
        Helper method to get CFI code from existing instrument data.
        
        Args:
            isin: The ISIN to look up
            
        Returns:
            CFI code if found, None otherwise
        """
        try:
            session = SessionLocal()
            try:
                instrument = session.query(Instrument).filter(Instrument.isin == isin).first()
                if instrument and instrument.cfi_code:
                    return instrument.cfi_code
                return None
            finally:
                session.close()
        except Exception as e:
            self.logger.error(f"Error getting CFI code for ISIN {isin}: {str(e)}")
            return None

    def get_transparency_by_tech_record_id(self, tech_record_id: str) -> Tuple[Session, Optional[TransparencyCalculation]]:
        """
        Get transparency calculation by technical record ID.
        
        Args:
            tech_record_id: The technical record ID to search for
            
        Returns:
            Tuple of (Session, TransparencyCalculation) if found
        """
        session = SessionLocal()
        try:
            calculation = session.query(TransparencyCalculation).filter(
                TransparencyCalculation.tech_record_id == tech_record_id
            ).first()
            
            if calculation:
                session.refresh(calculation)
            
            return session, calculation
        except:
            session.close()
            raise

    def _get_fitrs_data(self, isin: str, calculation_type: str) -> Optional[List[Dict[str, Any]]]:
        """
        Helper method to fetch FITRS transparency data from ESMA.
        
        Args:
            isin: The ISIN to search for
            calculation_type: 'EQUITY' or 'NON_EQUITY'
            
        Returns:
            List of dictionaries containing FITRS data if found (multiple venues possible), None otherwise
        """
        try:
            self.logger.info(f"Fetching FITRS data for ISIN {isin}, type {calculation_type}")
            
            # Load FITRS file list
            list_files = self.esma_loader.load_mifid_file_list(['fitrs'])
            
            # Determine file type based on calculation type
            if calculation_type == 'EQUITY':
                # For EQUITY, ONLY look for FULECR_E files (equity transparency with CFI "E")
                fitrs_files = list_files[list_files['download_link'].str.contains('FULECR_E', na=False)]
                self.logger.info(f"Found {len(fitrs_files)} FULECR_E files for equity calculations")
            else:
                # For NON_EQUITY, ONLY search target FULNCR file types: D, F, E
                target_types = ['D', 'F', 'E']  # Debt, Futures, ETFs only
                fitrs_files = pd.DataFrame()
                
                # Strategy 1: Try to get CFI from existing instrument data for targeted search
                instrument_cfi = self._get_instrument_cfi_from_isin(isin)
                if instrument_cfi:
                    cfi_type = instrument_cfi[0].upper()  # First character of CFI
                    # Only proceed if it's one of our target types
                    if cfi_type in target_types:
                        specific_pattern = f'FULNCR_{cfi_type}'
                        specific_files = list_files[list_files['download_link'].str.contains(specific_pattern, na=False)]
                        if not specific_files.empty:
                            fitrs_files = specific_files
                            self.logger.info(f"Found {len(fitrs_files)} {specific_pattern} files for CFI type {cfi_type}")
                        else:
                            self.logger.info(f"No specific {specific_pattern} files found for CFI {cfi_type}")
                    else:
                        self.logger.info(f"CFI type {cfi_type} not in target types (D, F, E), will search only target types")
                
                # Strategy 2: If no instrument CFI or not in target types, search ALL target types
                if fitrs_files.empty:
                    for cfi_type in target_types:
                        pattern = f'FULNCR_{cfi_type}'
                        type_files = list_files[list_files['download_link'].str.contains(pattern, na=False)]
                        if not type_files.empty:
                            if fitrs_files.empty:
                                fitrs_files = type_files
                            else:
                                fitrs_files = pd.concat([fitrs_files, type_files])
                    
                    if instrument_cfi is None:
                        self.logger.info(f"No instrument found for ISIN {isin}, searching target FULNCR file types (D, F, E)")
                    else:
                        self.logger.info(f"Instrument CFI {instrument_cfi} not in target types, searching all target FULNCR file types (D, F, E)")
                
                self.logger.info(f"Found {len(fitrs_files)} target FULNCR files total")
            
            if fitrs_files.empty:
                self.logger.warning(f"No FITRS files found for calculation type {calculation_type}")
                return None

            # Search through files for the ISIN - collect ALL matching records
            all_isin_data = []
            for _, file_info in fitrs_files.iterrows():
                try:
                    # Double-check file URL contains only our target patterns
                    file_url = file_info['download_link']
                    if calculation_type == 'EQUITY':
                        # Ensure this file is actually FULECR_E
                        if 'FULECR_E' not in file_url:
                            self.logger.warning(f"Skipping non-FULECR_E file: {file_url}")
                            continue
                    elif calculation_type == 'NON_EQUITY':
                        # Ensure this file is actually one of our target types
                        if not any(f'FULNCR_{target}' in file_url for target in ['D', 'F', 'E']):
                            self.logger.warning(f"Skipping non-target file: {file_url}")
                            continue
                    
                    self.logger.info(f"Searching in file: {file_url}")
                    df = self.esma_loader.download_file(file_url)
                    
                    if df.empty:
                        self.logger.warning(f"Empty dataframe from file: {file_url}")
                        continue

                    # Search for ISIN in the dataframe - check multiple possible column names
                    isin_data = None
                    possible_isin_columns = ['ISIN', 'Id', 'Isin', 'isin']
                    
                    for col_name in possible_isin_columns:
                        if col_name in df.columns:
                            matching_data = df[df[col_name] == isin]
                            if not matching_data.empty:
                                isin_data = matching_data
                                self.logger.info(f"Found ISIN using column '{col_name}'")
                                break
                    
                    if isin_data is not None and not isin_data.empty:
                        self.logger.info(f"Found {len(isin_data)} FITRS records for ISIN {isin} in file: {file_url}")
                        # Convert each row to dict and add to our collection
                        for _, row in isin_data.iterrows():
                            record_dict = row.to_dict()
                            # Normalize ISIN field name to 'ISIN' for consistency
                            if 'ISIN' not in record_dict:
                                for col_name in possible_isin_columns:
                                    if col_name in record_dict:
                                        record_dict['ISIN'] = record_dict[col_name]
                                        break
                            all_isin_data.append(record_dict)
                        
                except Exception as e:
                    self.logger.error(f"Error processing FITRS file {file_info['download_link']}: {str(e)}")
                    continue

            if all_isin_data:
                self.logger.info(f"Found total of {len(all_isin_data)} FITRS records for ISIN {isin}")
                return all_isin_data
            else:
                self.logger.warning(f"No FITRS data found for ISIN {isin}")
                return None

        except Exception as e:
            self.logger.error(f"Error fetching FITRS data: {str(e)}")
            return None

    def batch_source_transparency_data(
        self,
        calculation_type: str,
        isin_prefix: Optional[str] = None,
        limit: Optional[int] = None,
        cfi_type: Optional[str] = None
    ) -> List[TransparencyCalculation]:
        """
        Batch source transparency calculations from FITRS data.

        Args:
            calculation_type: 'EQUITY' or 'NON_EQUITY'
            isin_prefix: Optional ISIN prefix to filter (e.g., 'NL' for Netherlands instruments)
            limit: Optional maximum number of calculations to create
            cfi_type: Optional CFI type to filter specific FULNCR files (e.g., 'D' for debt)

        Returns:
            List of created TransparencyCalculation instances
        """
        created_calculations = []
        try:
            self.logger.info(f"Starting batch sourcing for calculation type: {calculation_type}")
            
            # Load FITRS file list
            list_files = self.esma_loader.load_mifid_file_list(['fitrs'])
            
            # Filter files based on calculation type and optional CFI type
            if calculation_type == 'EQUITY':
                # For EQUITY, ONLY use FULECR_E files
                fitrs_files = list_files[list_files['download_link'].str.contains('FULECR_E', na=False)]
                self.logger.info(f"Found {len(fitrs_files)} FULECR_E files for equity calculations")
            else:
                # For NON_EQUITY, ONLY use target FULNCR file types: D, F, E
                target_types = ['D', 'F', 'E']  # Debt, Futures, ETFs only
                
                if cfi_type and cfi_type.upper() in target_types:
                    # Filter by specific FULNCR type (only target types)
                    pattern = f'FULNCR_{cfi_type.upper()}'
                    fitrs_files = list_files[list_files['download_link'].str.contains(pattern, na=False)]
                    self.logger.info(f"Filtering for {pattern} files")
                else:
                    # Get only target FULNCR files (D, F, E)
                    fitrs_files = pd.DataFrame()
                    
                    for target_type in target_types:
                        pattern = f'FULNCR_{target_type}'
                        pattern_files = list_files[list_files['download_link'].str.contains(pattern, na=False)]
                        if not pattern_files.empty:
                            if fitrs_files.empty:
                                fitrs_files = pattern_files
                            else:
                                fitrs_files = pd.concat([fitrs_files, pattern_files])
                    
                    self.logger.info(f"Using target FULNCR file types (D, F, E)")
            
            if fitrs_files.empty:
                self.logger.warning(f"No FITRS files found for calculation type {calculation_type}")
                return []

            count = 0
            for _, file_info in fitrs_files.iterrows():
                try:
                    file_url = file_info['download_link']
                    
                    # Double-check file URL contains only our target patterns
                    if calculation_type == 'EQUITY':
                        if 'FULECR_E' not in file_url:
                            self.logger.warning(f"Skipping non-FULECR_E file: {file_url}")
                            continue
                    elif calculation_type == 'NON_EQUITY':
                        if not any(f'FULNCR_{target}' in file_url for target in ['D', 'F', 'E']):
                            self.logger.warning(f"Skipping non-target file: {file_url}")
                            continue
                    
                    self.logger.info(f"Processing file: {file_url}")
                    df = self.esma_loader.download_file(file_url)
                    
                    if df.empty:
                        continue

                    # Apply ISIN prefix filter if specified
                    # Check multiple possible ISIN column names
                    isin_column = None
                    for possible_col in ['ISIN', 'Id', 'Isin', 'isin']:
                        if possible_col in df.columns:
                            isin_column = possible_col
                            break
                    
                    if not isin_column:
                        self.logger.warning(f"No ISIN column found in file {file_url}")
                        continue
                    
                    if isin_prefix:
                        df = df[df[isin_column].str.startswith(isin_prefix)]

                    # Process each record
                    for _, row in df.iterrows():
                        if limit is not None and count >= limit:
                            self.logger.info(f"Reached limit of {limit} calculations")
                            return created_calculations
                        
                        try:
                            data = row.to_dict()
                            
                            # Normalize ISIN field name
                            if 'ISIN' not in data and isin_column in data:
                                data['ISIN'] = data[isin_column]
                            
                            # Check if calculation already exists
                            isin = data.get('ISIN')
                            tech_record_id = data.get('TechRcrdId')
                            
                            if not isin or not tech_record_id:
                                self.logger.warning("Missing ISIN or TechRcrdId, skipping record")
                                continue
                            
                            # Check for existing calculation
                            session, existing = self.get_transparency_by_tech_record_id(tech_record_id)
                            session.close()
                            
                            if existing:
                                self.logger.info(f"Transparency calculation for tech record {tech_record_id} already exists. Skipping.")
                                continue
                            
                            # Create new calculation
                            calculation = self.create_transparency_calculation(data, calculation_type)
                            if calculation:
                                created_calculations.append(calculation)
                                count += 1
                                self.logger.info(f"Created transparency calculation {count}: {calculation.id}")
                            
                        except Exception as e:
                            self.logger.error(f"Failed to create transparency calculation: {str(e)}")
                            continue
                    
                    if limit is not None and count >= limit:
                        break
                        
                except Exception as e:
                    self.logger.error(f"Error processing FITRS file {file_info['download_link']}: {str(e)}")
                    continue

            self.logger.info(f"Batch sourcing completed. Created {len(created_calculations)} transparency calculations")
            return created_calculations

        except Exception as e:
            self.logger.error(f"Batch sourcing failed: {str(e)}")
            return []

    def get_all_calculations(self, calculation_type=None, instrument_type=None, isin=None, page=1, per_page=20):
        """Get all transparency calculations with optional filtering"""
        session = SessionLocal()  # Use SessionLocal() instead of get_session()
        
        try:
            logger.info(f"Service called with: calculation_type={calculation_type}, instrument_type={instrument_type}, isin={isin}")
            
            query = session.query(TransparencyCalculation)
            
            # Apply filters
            if calculation_type:
                query = query.filter(TransparencyCalculation.calculation_type == calculation_type)
                logger.info(f"Applied calculation_type filter: {calculation_type}")
            
            if isin:
                query = query.filter(TransparencyCalculation.isin == isin)
                logger.info(f"Applied isin filter: {isin}")
            
            # Note: instrument_type filtering would need to join with instruments table
            # For now, we'll skip this filter or implement it later
            
            # Add pagination
            offset = (page - 1) * per_page
            query = query.offset(offset).limit(per_page)
            
            calculations = query.all()
            logger.info(f"Query returned {len(calculations)} calculations")
            
            return session, calculations
            
        except Exception as e:
            logger.error(f"Error in get_all_calculations: {str(e)}")
            session.close()
            raise

    