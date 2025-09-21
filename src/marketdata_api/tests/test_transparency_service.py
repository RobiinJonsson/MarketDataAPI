"""
Test script for TransparencyService.get_or_create_transparency_calculation

This script tests the transparency service with specific ISINs and their instrument types.
It directly calls the service method to create or retrieve transparency calculations.
"""

import logging
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Test ISINs with their instrument types
TEST_INSTRUMENTS = [
    {
        "isin": "SE0000242455",
        "type": "equity",
        "calculation_type": "EQUITY",
        "description": "Swedish equity instrument",
    },
]


def test_transparency_service():
    """Test the transparency service with predefined ISINs"""
    try:
        from marketdata_api.services.sqlite.transparency_service import TransparencyService

        # Initialize the service
        service = TransparencyService()
        logger.info("Transparency service initialized successfully")

        results = []

        for test_instrument in TEST_INSTRUMENTS:
            isin = test_instrument["isin"]
            calculation_type = test_instrument["calculation_type"]
            instrument_type = test_instrument["type"]
            description = test_instrument["description"]

            logger.info(f"\n{'='*80}")
            logger.info(f"Testing ISIN: {isin}")
            logger.info(f"Type: {instrument_type} ({calculation_type})")
            logger.info(f"Description: {description}")
            logger.info(f"{'='*80}")

            try:
                # Test with ensure_instrument=True first
                logger.info(f"Step 1: Testing with ensure_instrument=True")
                calculations = service.get_or_create_transparency_calculation(
                    isin=isin, calculation_type=calculation_type, ensure_instrument=True
                )

                if calculations:
                    logger.info(
                        f"✅ SUCCESS: Found/created {len(calculations)} transparency calculation(s)"
                    )
                    for i, calc in enumerate(calculations, 1):
                        logger.info(f"   Calculation {i}:")
                        logger.info(f"     - ID: {calc.id}")
                        logger.info(f"     - ISIN: {calc.isin}")
                        logger.info(f"     - Type: {calc.calculation_type}")
                        logger.info(f"     - Tech Record ID: {calc.tech_record_id}")
                        logger.info(f"     - Liquidity: {calc.liquidity}")
                        logger.info(
                            f"     - Total Transactions: {calc.total_transactions_executed}"
                        )
                        logger.info(f"     - Total Volume: {calc.total_volume_executed}")

                        # Check for specific transparency details
                        if calculation_type == "EQUITY":
                            if hasattr(calc, "equity_transparency") and calc.equity_transparency:
                                logger.info(f"     - Equity Details: Available")
                                logger.info(
                                    f"       * Methodology: {calc.equity_transparency.methodology}"
                                )
                                logger.info(
                                    f"       * Average Daily Turnover: {calc.equity_transparency.average_daily_turnover}"
                                )
                            else:
                                logger.info(f"     - Equity Details: Not available")
                        else:
                            details_found = False
                            if hasattr(calc, "debt_transparency") and calc.debt_transparency:
                                logger.info(f"     - Debt Details: Available")
                                logger.info(
                                    f"       * Bond Type: {calc.debt_transparency.bond_type}"
                                )
                                logger.info(
                                    f"       * Is Liquid: {calc.debt_transparency.is_liquid}"
                                )
                                details_found = True
                            elif (
                                hasattr(calc, "futures_transparency") and calc.futures_transparency
                            ):
                                logger.info(f"     - Futures Details: Available")
                                logger.info(
                                    f"       * Underlying ISIN: {calc.futures_transparency.underlying_isin}"
                                )
                                logger.info(
                                    f"       * Is Stock Dividend Future: {calc.futures_transparency.is_stock_dividend_future}"
                                )
                                details_found = True
                            elif (
                                hasattr(calc, "non_equity_transparency")
                                and calc.non_equity_transparency
                            ):
                                logger.info(f"     - Non-Equity Details: Available")
                                logger.info(
                                    f"       * Description: {calc.non_equity_transparency.description}"
                                )
                                logger.info(
                                    f"       * Criterion Name: {calc.non_equity_transparency.criterion_name}"
                                )
                                details_found = True

                            if not details_found:
                                logger.info(f"     - Specific Details: Not available")

                    results.append(
                        {
                            "isin": isin,
                            "type": instrument_type,
                            "calculation_type": calculation_type,
                            "status": "success",
                            "count": len(calculations),
                            "calculations": calculations,
                        }
                    )
                else:
                    logger.warning(f"⚠️  No transparency calculations found/created for {isin}")

                    # Try without ensure_instrument
                    logger.info(f"Step 2: Retrying with ensure_instrument=False")
                    calculations_retry = service.get_or_create_transparency_calculation(
                        isin=isin, calculation_type=calculation_type, ensure_instrument=False
                    )

                    if calculations_retry:
                        logger.info(
                            f"✅ SUCCESS (retry): Found/created {len(calculations_retry)} transparency calculation(s)"
                        )
                        results.append(
                            {
                                "isin": isin,
                                "type": instrument_type,
                                "calculation_type": calculation_type,
                                "status": "success_retry",
                                "count": len(calculations_retry),
                                "calculations": calculations_retry,
                            }
                        )
                    else:
                        logger.error(f"❌ FAILED: No transparency data available for {isin}")
                        results.append(
                            {
                                "isin": isin,
                                "type": instrument_type,
                                "calculation_type": calculation_type,
                                "status": "failed",
                                "count": 0,
                                "error": "No transparency data found",
                            }
                        )

            except Exception as e:
                logger.error(f"❌ ERROR testing {isin}: {str(e)}")
                results.append(
                    {
                        "isin": isin,
                        "type": instrument_type,
                        "calculation_type": calculation_type,
                        "status": "error",
                        "count": 0,
                        "error": str(e),
                    }
                )
                continue

        # Summary report
        logger.info(f"\n{'='*80}")
        logger.info("SUMMARY REPORT")
        logger.info(f"{'='*80}")

        successful = [r for r in results if r["status"].startswith("success")]
        failed = [r for r in results if r["status"] == "failed"]
        errors = [r for r in results if r["status"] == "error"]

        logger.info(f"Total instruments tested: {len(TEST_INSTRUMENTS)}")
        logger.info(f"Successful: {len(successful)}")
        logger.info(f"Failed: {len(failed)}")
        logger.info(f"Errors: {len(errors)}")

        if successful:
            logger.info(f"\n✅ SUCCESSFUL INSTRUMENTS:")
            for result in successful:
                logger.info(
                    f"  - {result['isin']} ({result['type']}): {result['count']} calculation(s)"
                )

        if failed:
            logger.info(f"\n⚠️  FAILED INSTRUMENTS:")
            for result in failed:
                logger.info(f"  - {result['isin']} ({result['type']}): {result['error']}")

        if errors:
            logger.info(f"\n❌ ERROR INSTRUMENTS:")
            for result in errors:
                logger.info(f"  - {result['isin']} ({result['type']}): {result['error']}")

        return results

    except Exception as e:
        logger.error(f"Failed to initialize transparency service: {str(e)}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        return []


def test_database_content():
    """Test what transparency data already exists in the database"""
    try:
        from marketdata_api.database.session import SessionLocal  # Use SessionLocal instead
        from marketdata_api.models.sqlite.transparency import TransparencyCalculation

        logger.info(f"\n{'='*80}")
        logger.info("CHECKING EXISTING DATABASE CONTENT")
        logger.info(f"{'='*80}")

        session = SessionLocal()  # Use SessionLocal() instead of get_session()

        try:
            # Count total transparency calculations
            total_count = session.query(TransparencyCalculation).count()
            logger.info(f"Total transparency calculations in database: {total_count}")

            # Count by calculation type
            equity_count = (
                session.query(TransparencyCalculation)
                .filter(TransparencyCalculation.calculation_type == "EQUITY")
                .count()
            )
            non_equity_count = (
                session.query(TransparencyCalculation)
                .filter(TransparencyCalculation.calculation_type == "NON_EQUITY")
                .count()
            )

            logger.info(f"EQUITY calculations: {equity_count}")
            logger.info(f"NON_EQUITY calculations: {non_equity_count}")

            # Check for our specific test ISINs
            logger.info(f"\nChecking for test ISINs:")
            for test_instrument in TEST_INSTRUMENTS:
                isin = test_instrument["isin"]
                existing = (
                    session.query(TransparencyCalculation)
                    .filter(TransparencyCalculation.isin == isin)
                    .all()
                )

                if existing:
                    logger.info(f"  ✅ {isin}: {len(existing)} calculation(s) found")
                    for calc in existing:
                        logger.info(
                            f"     - ID: {calc.id}, Type: {calc.calculation_type}, Tech ID: {calc.tech_record_id}"
                        )
                else:
                    logger.info(f"  ❌ {isin}: No calculations found")

        finally:
            session.close()

    except Exception as e:
        logger.error(f"Error checking database content: {str(e)}")


def main():
    """Main test function"""
    logger.info("Starting Transparency Service Test")
    logger.info(f"Project root: {project_root}")

    # First check what's already in the database
    test_database_content()

    # Then test the service
    results = test_transparency_service()

    logger.info(f"\n🏁 Test completed!")
    logger.info("Check the logs above for detailed results.")

    return results


if __name__ == "__main__":
    main()
