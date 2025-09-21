"""
Test runner for MarketDataAPI test suite.

This script provides convenient ways to run different test categories
and generates comprehensive test reports for version upgrades.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and return the result."""
    print(f"\n{'='*60}")
    if description:
        print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    return result


def run_unit_tests():
    """Run unit tests."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-m",
        "unit",
        "-v",
        "--tb=short",
        "--cov=marketdata_api",
        "--cov-report=term-missing",
    ]
    return run_command(cmd, "Unit Tests")


def run_integration_tests():
    """Run integration tests."""
    cmd = [sys.executable, "-m", "pytest", "-m", "integration", "-v", "--tb=short"]
    return run_command(cmd, "Integration Tests")


def run_cli_tests():
    """Run CLI tests."""
    cmd = [sys.executable, "-m", "pytest", "-m", "cli", "-v", "--tb=short"]
    return run_command(cmd, "CLI Tests")


def run_upgrade_tests():
    """Run version upgrade tests."""
    cmd = [sys.executable, "-m", "pytest", "-m", "upgrade", "-v", "--tb=short"]
    return run_command(cmd, "Version Upgrade Tests")


def run_slow_tests():
    """Run slow/performance tests."""
    cmd = [sys.executable, "-m", "pytest", "-m", "slow", "-v", "--tb=short"]
    return run_command(cmd, "Performance Tests")


def run_all_tests():
    """Run the complete test suite."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-v",
        "--tb=short",
        "--cov=marketdata_api",
        "--cov-report=html",
        "--cov-report=term",
    ]
    return run_command(cmd, "Complete Test Suite")


def run_quick_tests():
    """Run quick tests (unit + CLI, no slow tests)."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-m",
        "unit or cli",
        "-v",
        "--tb=line",
        "-x",  # Stop on first failure for quick feedback
    ]
    return run_command(cmd, "Quick Test Suite")


def check_test_collection():
    """Check that tests can be collected without errors."""
    cmd = [sys.executable, "-m", "pytest", "--collect-only", "-q"]
    return run_command(cmd, "Test Collection Check")


def generate_upgrade_report():
    """Generate a comprehensive upgrade test report."""
    print(f"\n{'='*80}")
    print("MARKETDATAAPI VERSION UPGRADE TEST REPORT")
    print(f"Generated: {datetime.now().isoformat()}")
    print(f"{'='*80}")

    report = {"timestamp": datetime.now().isoformat(), "test_results": {}, "summary": {}}

    # Run different test categories
    test_categories = [
        ("collection", check_test_collection),
        ("unit", run_unit_tests),
        ("integration", run_integration_tests),
        ("cli", run_cli_tests),
        ("upgrade", run_upgrade_tests),
    ]

    total_passed = 0
    total_failed = 0

    for category, test_func in test_categories:
        print(f"\n{'-'*60}")
        print(f"Running {category.upper()} tests...")
        print(f"{'-'*60}")

        result = test_func()

        report["test_results"][category] = {
            "exit_code": result.returncode,
            "passed": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

        if result.returncode == 0:
            total_passed += 1
            print(f"✅ {category.upper()} tests PASSED")
        else:
            total_failed += 1
            print(f"❌ {category.upper()} tests FAILED")

    # Generate summary
    report["summary"] = {
        "total_categories": len(test_categories),
        "passed_categories": total_passed,
        "failed_categories": total_failed,
        "overall_success": total_failed == 0,
    }

    # Print summary
    print(f"\n{'='*80}")
    print("UPGRADE TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Total test categories: {len(test_categories)}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"Overall result: {'✅ PASS' if total_failed == 0 else '❌ FAIL'}")

    if total_failed > 0:
        print(f"\n❌ Failed categories:")
        for category, result in report["test_results"].items():
            if not result["passed"]:
                print(f"   - {category}")

    # Save report to file
    report_file = Path("test_report.json")
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nDetailed report saved to: {report_file}")
    return report


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description="MarketDataAPI Test Runner")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--cli", action="store_true", help="Run CLI tests")
    parser.add_argument("--upgrade", action="store_true", help="Run upgrade tests")
    parser.add_argument("--slow", action="store_true", help="Run slow/performance tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--quick", action="store_true", help="Run quick tests (unit + CLI)")
    parser.add_argument("--check", action="store_true", help="Check test collection")
    parser.add_argument(
        "--upgrade-report", action="store_true", help="Generate comprehensive upgrade test report"
    )

    args = parser.parse_args()

    # Change to project directory
    project_root = Path(__file__).parent.parent.parent.parent
    import os

    os.chdir(project_root)

    if args.unit:
        run_unit_tests()
    elif args.integration:
        run_integration_tests()
    elif args.cli:
        run_cli_tests()
    elif args.upgrade:
        run_upgrade_tests()
    elif args.slow:
        run_slow_tests()
    elif args.all:
        run_all_tests()
    elif args.quick:
        run_quick_tests()
    elif args.check:
        check_test_collection()
    elif args.upgrade_report:
        generate_upgrade_report()
    else:
        # Default: run quick tests
        print("No specific test category specified. Running quick tests...")
        run_quick_tests()


if __name__ == "__main__":
    main()
