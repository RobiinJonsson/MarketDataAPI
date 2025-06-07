"""
Test script for the Transparency Service

This script tests the complete transparency functionality including:
- Transparency service CRUD operations
- Database models and relationships
- Data mapping and validation
- Different transparency types (equity, debt, futures)
"""

import os
import sys
import logging
from datetime import datetime, date
from typing import Dict, Any

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from marketdata_api.services.transparency_service import TransparencyService, TransparencyServiceError
from marketdata_api.database.session import get_session, SessionLocal
from marketdata_api.models.transparency import (
    TransparencyCalculation, EquityTransparency, 
    NonEquityTransparency, DebtTransparency, FuturesTransparency
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TransparencyServiceTest:
    def __init__(self):
        self.service = TransparencyService()
        self.test_results = []
        
    def log_test_result(self, test_name: str, success: bool, message: str = ""):
        """Log test results for summary"""
        result = "✓ PASS" if success else "✗ FAIL"
        logger.info(f"{result}: {test_name} - {message}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message
        })
    
    def create_sample_equity_data(self) -> Dict[str, Any]:
        """Create sample FULECR (equity transparency) data"""
        return {
            'TechRcrdId': 'TEST_EQUITY_001',
            'ISIN': 'NL0000235190',  # Airbus SE (European equity)
            'FrDt': '2024-05-01',
            'ToDt': '2024-05-31',
            'Lqdty': 'true',
            'TtlNbOfTxsExctd': '15420',
            'TtlVolOfTxsExctd': '25000000.50',
            'Sttstcs': 'CALCULATED',
            'FinInstrmClssfctn': 'SHARE',
            'Mthdlgy': 'AVERAGE_DAILY_TURNOVER',
            'AvrgDalyTrnvr': '12500000.25',
            'LrgInScale': '5000000.00',
            'AvrgDalyNbOfTxs': '485.75',
            'Id_2': 'SECONDARY_ID_001',
            'AvrgDalyNbOfTxs_2': '125.50',
            'AvrgTxVal': '25750.80',
            'StdMktSz': '2500.00'
        }
    
    def create_sample_debt_data(self) -> Dict[str, Any]:
        """Create sample FULNCR (debt transparency) data"""
        return {
            'TechRcrdId': 'TEST_DEBT_001',
            'ISIN': 'DE0001102309',  # German Federal Bond (European debt)
            'FrDt': '2024-05-01',
            'ToDt': '2024-05-31',
            'Lqdty': 'false',
            'TtlNbOfTxsExctd': '245',
            'TtlVolOfTxsExctd': '15000000.00',
            'Desc': 'Corporate bond',
            'CritNm': 'CFI',
            'CritVal': 'DBFTFR',
            'FinInstrmClssfctn': 'BOND',
            'PreTradLrgInScaleThrshld_Amt': '15000000.00',
            'PstTradLrgInScaleThrshld_Amt': '15000000.00',
            'PreTradInstrmSzSpcfcThrshld_Amt': '100000.00',
            'PstTradInstrmSzSpcfcThrshld_Amt': '100000.00',
            'CritNm_2': 'ISSUER_SIZE',
            'CritVal_2': 'LARGE'
        }
    
    def create_sample_futures_data(self) -> Dict[str, Any]:
        """Create sample futures transparency data"""
        return {
            'TechRcrdId': 'TEST_FUTURES_001',
            'ISIN': 'SE0021060217',  # Sample futures ISIN
            'FrDt': '2024-05-01',
            'ToDt': '2024-05-31',
            'Lqdty': 'true',
            'TtlNbOfTxsExctd': '1250',
            'TtlVolOfTxsExctd': '50000000.00',
            'Desc': 'Stock dividend future',
            'CritNm': 'CFI',
            'CritVal': 'FFIXSX',
            'FinInstrmClssfctn': 'DERV',
            'PreTradLrgInScaleThrshld_Amt': '5000000.00',
            'PstTradLrgInScaleThrshld_Amt': '5000000.00',
            'PreTradInstrmSzSpcfcThrshld_Amt': '50000.00',
            'PstTradInstrmSzSpcfcThrshld_Amt': '50000.00',
            'CritNm_2': 'UINS',
            'CritVal_2': 'US0378331005',  # Underlying ISIN
            'CritNm_3': 'MATURITY',
            'CritVal_3': '2024-12-31',
            'CritNm_4': 'STRIKE',
            'CritVal_4': '150.00',
            'PreTradLrgInScaleThrshld_Nb': '1000',
            'PstTradLrgInScaleThrshld_Nb': '1000',
            'PreTradInstrmSzSpcfcThrshld_Nb': '100',
            'PstTradInstrmSzSpcfcThrshld_Nb': '100'
        }
    
    def create_sample_sdrv_data(self) -> Dict[str, Any]:
        """Create sample securitised derivative data"""
        return {
            'TechRcrdId': 'TEST_SDRV_001',
            'ISIN': 'DE000A1X3TV7',  # European securitised derivative
            'FrDt': '2024-05-01',
            'ToDt': '2024-05-31',
            'Lqdty': 'false',
            'TtlNbOfTxsExctd': '85',
            'TtlVolOfTxsExctd': '2500000.00',
            'Desc': 'Securitised derivative',
            'CritNm': 'CFI',
            'CritVal': 'SDRV',
            'FinInstrmClssfctn': 'SDRV',
            'PreTradLrgInScaleThrshld_Amt': '500000.00',
            'PstTradLrgInScaleThrshld_Amt': '500000.00',
            'PreTradInstrmSzSpcfcThrshld_Amt': '25000.00',
            'PstTradInstrmSzSpcfcThrshld_Amt': '25000.00'
        }
    
    def test_equity_transparency_creation(self):
        """Test creating equity transparency calculations"""
        try:
            data = self.create_sample_equity_data()
            calculation = self.service.create_transparency_calculation(data, "EQUITY")
            
            if calculation and calculation.id:
                # Verify the calculation was created
                session, retrieved = self.service.get_transparency_by_id(calculation.id)
                session.close()
                
                if retrieved:
                    self.log_test_result(
                        "Equity Transparency Creation", 
                        True, 
                        f"Created calculation with ID: {calculation.id}"
                    )
                    return calculation.id
                else:
                    self.log_test_result("Equity Transparency Creation", False, "Failed to retrieve created calculation")
            else:
                self.log_test_result("Equity Transparency Creation", False, "Failed to create calculation")
                
        except Exception as e:
            self.log_test_result("Equity Transparency Creation", False, f"Exception: {str(e)}")
        
        return None
    
    def test_debt_transparency_creation(self):
        """Test creating debt transparency calculations"""
        try:
            data = self.create_sample_debt_data()
            calculation = self.service.create_transparency_calculation(data, "NON_EQUITY")
            
            if calculation and calculation.id:
                self.log_test_result(
                    "Debt Transparency Creation", 
                    True, 
                    f"Created calculation with ID: {calculation.id}"
                )
                return calculation.id
            else:
                self.log_test_result("Debt Transparency Creation", False, "Failed to create calculation")
                
        except Exception as e:
            self.log_test_result("Debt Transparency Creation", False, f"Exception: {str(e)}")
        
        return None
    
    def test_futures_transparency_creation(self):
        """Test creating futures transparency calculations"""
        try:
            data = self.create_sample_futures_data()
            calculation = self.service.create_transparency_calculation(data, "NON_EQUITY")
            
            if calculation and calculation.id:
                self.log_test_result(
                    "Futures Transparency Creation", 
                    True, 
                    f"Created calculation with ID: {calculation.id}"
                )
                return calculation.id
            else:
                self.log_test_result("Futures Transparency Creation", False, "Failed to create calculation")
                
        except Exception as e:
            self.log_test_result("Futures Transparency Creation", False, f"Exception: {str(e)}")
        
        return None
    
    def test_sdrv_transparency_creation(self):
        """Test creating securitised derivative transparency calculations"""
        try:
            data = self.create_sample_sdrv_data()
            calculation = self.service.create_transparency_calculation(data, "NON_EQUITY")
            
            if calculation and calculation.id:
                self.log_test_result(
                    "SDRV Transparency Creation", 
                    True, 
                    f"Created calculation with ID: {calculation.id}"
                )
                return calculation.id
            else:
                self.log_test_result("SDRV Transparency Creation", False, "Failed to create calculation")
                
        except Exception as e:
            self.log_test_result("SDRV Transparency Creation", False, f"Exception: {str(e)}")
        
        return None
    
    def test_transparency_retrieval_by_isin(self):
        """Test retrieving transparency calculations by ISIN"""
        try:
            # Use the equity ISIN from our test data
            isin = "NL0000235190"  # European equity ISIN
            session, calculations = self.service.get_transparency_by_isin(isin)
            
            if calculations:
                self.log_test_result(
                    "Transparency Retrieval by ISIN", 
                    True, 
                    f"Found {len(calculations)} calculations for ISIN {isin}"
                )
                session.close()
                return True
            else:
                self.log_test_result("Transparency Retrieval by ISIN", False, f"No calculations found for ISIN {isin}")
                session.close()
                
        except Exception as e:
            self.log_test_result("Transparency Retrieval by ISIN", False, f"Exception: {str(e)}")
        
        return False
    
    def test_transparency_update(self, calculation_id: str):
        """Test updating transparency calculations"""
        if not calculation_id:
            self.log_test_result("Transparency Update", False, "No calculation ID provided")
            return False
            
        try:
            # Update with new data
            update_data = self.create_sample_equity_data()
            update_data['TtlNbOfTxsExctd'] = '20000'  # Change transaction count
            update_data['TtlVolOfTxsExctd'] = '35000000.75'  # Change volume
            
            updated_calculation = self.service.update_transparency_calculation(calculation_id, update_data)
            
            if updated_calculation:
                self.log_test_result(
                    "Transparency Update", 
                    True, 
                    f"Updated calculation {calculation_id}"
                )
                return True
            else:
                self.log_test_result("Transparency Update", False, f"Failed to update calculation {calculation_id}")
                
        except Exception as e:
            self.log_test_result("Transparency Update", False, f"Exception: {str(e)}")
        
        return False
    
    def test_batch_creation(self):
        """Test batch creation of transparency calculations"""
        try:
            batch_data = [
                self.create_sample_equity_data(),
                self.create_sample_debt_data(),
                self.create_sample_futures_data()
            ]
            
            # Generate unique ISINs to avoid duplicates with random suffix
            import random
            suffix = random.randint(1000, 9999)
            
            batch_data[0]['ISIN'] = f'NL000023519{suffix}'  # Unique European equity ISIN
            batch_data[1]['ISIN'] = f'DE000110230{suffix}'  # Unique European bond ISIN
            batch_data[2]['ISIN'] = f'SE002106021{suffix}'  # Unique futures ISIN
            
            # Also modify tech record IDs to ensure uniqueness
            batch_data[0]['TechRcrdId'] = f'TEST_BATCH_EQUITY_{suffix}'
            batch_data[1]['TechRcrdId'] = f'TEST_BATCH_DEBT_{suffix}'
            batch_data[2]['TechRcrdId'] = f'TEST_BATCH_FUTURES_{suffix}'
            
            created_count = self.service.batch_create_transparency_data(batch_data)
            
            if created_count > 0:
                self.log_test_result(
                    "Batch Creation", 
                    True, 
                    f"Created {created_count} transparency calculations"
                )
                return True
            else:
                self.log_test_result("Batch Creation", False, "No calculations created in batch")
                
        except Exception as e:
            self.log_test_result("Batch Creation", False, f"Exception: {str(e)}")
        
        return False
    
    def test_transparency_deletion(self, calculation_id: str):
        """Test deleting transparency calculations"""
        if not calculation_id:
            self.log_test_result("Transparency Deletion", False, "No calculation ID provided")
            return False
            
        try:
            result = self.service.delete_transparency_calculation(calculation_id)
            
            if result:
                self.log_test_result(
                    "Transparency Deletion", 
                    True, 
                    f"Deleted calculation {calculation_id}"
                )
                return True
            else:
                self.log_test_result("Transparency Deletion", False, f"Failed to delete calculation {calculation_id}")
                
        except Exception as e:
            self.log_test_result("Transparency Deletion", False, f"Exception: {str(e)}")
        
        return False
    
    def test_data_validation(self):
        """Test data validation"""
        try:
            # Test with missing required fields
            invalid_data = {'ISIN': 'NL0000235190'}  # Missing TechRcrdId - European ISIN
            
            try:
                self.service.create_transparency_calculation(invalid_data, "EQUITY")
                self.log_test_result("Data Validation", False, "Should have failed with missing required fields")
            except TransparencyServiceError:
                self.log_test_result("Data Validation", True, "Correctly caught missing required fields")
                return True
                
        except Exception as e:
            self.log_test_result("Data Validation", False, f"Unexpected exception: {str(e)}")
        
        return False
    
    def test_database_relationships(self):
        """Test database model relationships"""
        try:
            session = SessionLocal()
            
            # Query for some transparency calculations
            calculations = session.query(TransparencyCalculation).limit(5).all()
            
            if calculations:
                relationships_verified = 0
                
                for calc in calculations:
                    logger.info(f"Calculation ID: {calc.id}, Type: {calc.calculation_type}, ISIN: {calc.isin}")
                    
                    # Test relationships based on calculation type
                    if calc.calculation_type == "EQUITY":
                        equity_details = session.query(EquityTransparency).filter_by(id=calc.id).first()
                        if equity_details:
                            logger.info(f"  - Equity details found: methodology={equity_details.methodology}")
                            relationships_verified += 1
                    else:
                        # For non-equity, first check what specific subtype exists
                        debt_details = session.query(DebtTransparency).filter_by(id=calc.id).first()
                        futures_details = session.query(FuturesTransparency).filter_by(id=calc.id).first()
                        non_equity_details = session.query(NonEquityTransparency).filter_by(id=calc.id).first()
                        
                        if non_equity_details:
                            logger.info(f"  - Non-equity details found: description={non_equity_details.description}")
                            relationships_verified += 1
                            
                            if debt_details:
                                logger.info(f"  - Debt subtype found: bond_type={debt_details.bond_type}")
                                relationships_verified += 1
                            elif futures_details:
                                logger.info(f"  - Futures subtype found: underlying_isin={futures_details.underlying_isin}")
                                relationships_verified += 1
                            else:
                                logger.info(f"  - Generic non-equity transparency record")
                                relationships_verified += 1
                
                session.close()
                
                if relationships_verified > 0:
                    self.log_test_result("Database Relationships", True, f"Verified {relationships_verified} relationships for {len(calculations)} calculations")
                    return True
                else:
                    self.log_test_result("Database Relationships", False, "No relationships could be verified")
                    return False
            else:
                session.close()
                self.log_test_result("Database Relationships", False, "No calculations found to test relationships")
                
        except Exception as e:
            session.close()
            self.log_test_result("Database Relationships", False, f"Exception: {str(e)}")
        
        return False
    
    def test_external_data_sourcing(self):
        """Test sourcing transparency data from external FITRS files"""
        try:
            # Test equity transparency sourcing with European ISIN
            equity_calcs = self.service.get_or_create_transparency_calculation("NL0000235190", "EQUITY", ensure_instrument=False)
            
            if equity_calcs and len(equity_calcs) > 0:
                self.log_test_result(
                    "External Equity Data Sourcing", 
                    True, 
                    f"Successfully sourced {len(equity_calcs)} equity transparency calculations for ISIN NL0000235190"
                )
            else:
                self.log_test_result(
                    "External Equity Data Sourcing", 
                    False, 
                    "No equity transparency data found for NL0000235190"
                )
            
            # Test non-equity transparency sourcing with European ISIN
            non_equity_calcs = self.service.get_or_create_transparency_calculation("DE000A1X3TV7", "NON_EQUITY", ensure_instrument=False)
            
            if non_equity_calcs and len(non_equity_calcs) > 0:
                self.log_test_result(
                    "External Non-Equity Data Sourcing", 
                    True, 
                    f"Successfully sourced {len(non_equity_calcs)} non-equity transparency calculations for ISIN DE000A1X3TV7"
                )
            else:
                self.log_test_result(
                    "External Non-Equity Data Sourcing", 
                    False, 
                    "No non-equity transparency data found for DE000A1X3TV7"
                )

            # Test with instrument creation enabled using Swedish equity ISIN that should exist in database
            equity_calc_with_instrument = self.service.get_or_create_transparency_calculation_single("SE0000242455", "EQUITY", ensure_instrument=True)
            
            if equity_calc_with_instrument:
                self.log_test_result(
                    "Transparency with Instrument Creation", 
                    True, 
                    f"Successfully created transparency with instrument for ISIN SE0000242455"
                )
            else:
                self.log_test_result(
                    "Transparency with Instrument Creation", 
                    False, 
                    "Failed to create transparency with instrument for SE0000242455"
                )
                
        except Exception as e:
            self.log_test_result("External Data Sourcing", False, f"Exception: {str(e)}")

    def test_batch_sourcing(self):
        """Test batch sourcing of transparency data from FITRS"""
        try:
            # Test batch sourcing with CFI type filter for more targeted results
            created_calculations = self.service.batch_source_transparency_data(
                calculation_type="NON_EQUITY",
                isin_prefix="NL",  # Netherlands instruments
                limit=5,  # Small limit for testing
                cfi_type="D"  # Debt instruments only
            )
            
            if created_calculations and len(created_calculations) > 0:
                self.log_test_result(
                    "Batch Sourcing from FITRS", 
                    True, 
                    f"Successfully created {len(created_calculations)} transparency calculations from FITRS data"
                )
                return True
            else:
                # Try without CFI filter as fallback
                created_calculations = self.service.batch_source_transparency_data(
                    calculation_type="EQUITY",
                    isin_prefix="NL",  # Netherlands instruments
                    limit=3  # Small limit for testing
                )
                
                if created_calculations and len(created_calculations) > 0:
                    self.log_test_result(
                        "Batch Sourcing from FITRS", 
                        True, 
                        f"Successfully created {len(created_calculations)} equity transparency calculations from FITRS data"
                    )
                    return True
                else:
                    self.log_test_result(
                        "Batch Sourcing from FITRS", 
                        False, 
                        "No transparency calculations created from FITRS data"
                    )
                
        except Exception as e:
            self.log_test_result("Batch Sourcing from FITRS", False, f"Exception: {str(e)}")
        
        return False

    def run_all_tests(self):
        """Run all tests in sequence"""
        logger.info("=" * 80)
        logger.info("STARTING TRANSPARENCY SERVICE TESTS")
        logger.info("=" * 80)
        
        # Store calculation IDs for later tests
        equity_calc_id = None
        debt_calc_id = None
        futures_calc_id = None
        sdrv_calc_id = None
        
        # Test creation methods with sample data
        equity_calc_id = self.test_equity_transparency_creation()
        debt_calc_id = self.test_debt_transparency_creation()
        futures_calc_id = self.test_futures_transparency_creation()
        sdrv_calc_id = self.test_sdrv_transparency_creation()
        
        # Test external data sourcing
        self.test_external_data_sourcing()
        
        # Test batch sourcing from external data
        self.test_batch_sourcing()
        
        # Test retrieval and relationships
        self.test_transparency_retrieval_by_isin()
        self.test_database_relationships()
        
        # Test update functionality
        if equity_calc_id:
            self.test_transparency_update(equity_calc_id)
        
        # Test batch operations with sample data
        self.test_batch_creation()
        
        # Test validation
        self.test_data_validation()
        
        # Test deletion (do this last)
        if debt_calc_id:
            self.test_transparency_deletion(debt_calc_id)
        
        # Print summary
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print a summary of all test results"""
        logger.info("=" * 80)
        logger.info("TEST SUMMARY")
        logger.info("=" * 80)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        logger.info(f"Total Tests: {total}")
        logger.info(f"Passed: {passed}")
        logger.info(f"Failed: {total - passed}")
        logger.info(f"Success Rate: {(passed/total)*100:.1f}%")
        
        logger.info("\nDetailed Results:")
        for result in self.test_results:
            status = "✓ PASS" if result['success'] else "✗ FAIL"
            logger.info(f"{status}: {result['test']} - {result['message']}")
        
        logger.info("=" * 80)

def main():
    """Main test execution"""
    try:
        test_runner = TransparencyServiceTest()
        test_runner.run_all_tests()
        
    except Exception as e:
        logger.error(f"Test execution failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
