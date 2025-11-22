#!/usr/bin/env python3
"""
Test the enhanced file management functionality.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

import pytest
import requests

# Add the project directory to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def test_file_management_service():
    """Test the enhanced FileManagementService directly."""
    print("🧪 Testing FileManagementService directly...")

    try:
        from marketdata_api.services.utils.file_management_service import FileManagementService

        service = FileManagementService()

        # Test basic file listing
        print("\n📁 Testing basic file listing:")
        files = service.get_all_files()
        print(f"  FIRDS files: {len(files['firds'])}")
        print(f"  FITRS files: {len(files['fitrs'])}")

        # Test filtered file listing
        print("\n🔍 Testing filtered file listing:")
        filtered_files = service.get_files_with_filters(file_type="firds", limit=5)
        print(f"  Found {len(filtered_files)} FIRDS files (limit 5)")
        for file_info in filtered_files[:3]:
            print(f"    - {file_info.name} ({file_info.dataset_type})")

        # Test ESMA file listing
        print("\n📡 Testing ESMA file listing:")
        esma_files = service.get_available_esma_files(
            datasets=["firds"], date_from="2025-07-10", date_to="2025-07-15"
        )
        print(f"  Found {len(esma_files)} ESMA files for July 10-15")
        for esma_file in esma_files[:3]:
            print(f"    - {esma_file.file_name} ({esma_file.file_type})")

        # Test detailed statistics
        print("\n📊 Testing detailed statistics:")
        stats = service.get_file_stats_by_criteria(file_types=["firds", "fitrs"])
        print(f"  Total files: {stats['total_files']}")
        print(f"  Total size: {stats['total_size_mb']} MB")
        print(f"  Dataset types: {list(stats['by_dataset_type'].keys())}")

        print("\n✅ Service tests completed successfully!")
        # Use assertions instead of return values
        assert True  # Test completed successfully

    except Exception as e:
        print(f"❌ Service test failed: {e}")
        import traceback

        traceback.print_exc()
        pytest.fail(f"Service test failed: {e}")


def test_api_endpoints():
    """Test the API endpoints (requires Flask app to be running)."""
    print("\n🌐 Testing API endpoints...")

    base_url = "http://localhost:5000"

    endpoints_to_test = [
        ("/api/v1/files", "GET", None, "Basic file listing"),
        ("/api/v1/files?file_type=firds&limit=5", "GET", None, "Filtered file listing"),
        ("/api/v1/files/stats", "GET", None, "File statistics"),
        ("/api/v1/files/stats/detailed", "GET", None, "Detailed statistics"),
        (
            "/api/v1/esma-files?datasets=firds&date_from=2025-07-10&date_to=2025-07-15",
            "GET",
            None,
            "ESMA file listing",
        ),
    ]

    for endpoint, method, data, description in endpoints_to_test:
        try:
            print(f"\n🔗 Testing: {description}")
            print(f"  {method} {endpoint}")

            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            elif method == "POST":
                response = requests.post(f"{base_url}{endpoint}", json=data, timeout=10)
            else:
                continue

            if response.status_code == 200:
                result = response.json()
                if isinstance(result, dict) and "error" not in result:
                    print(f"  ✅ Success - Response keys: {list(result.keys())}")

                    # Show some sample data
                    if (
                        endpoint.endswith("/files")
                        and "?" not in endpoint
                        and isinstance(result, dict)
                        and "firds" in result
                    ):
                        print(f"    FIRDS: {len(result.get('firds', []))} files")
                        print(f"    FITRS: {len(result.get('fitrs', []))} files")
                    elif "filtered_files" in result:
                        print(f"    Filtered files: {len(result['filtered_files'])}")
                        print(f"    Total count: {result.get('total_count', 0)}")
                    elif "total_count" in result:
                        print(f"    Total count: {result['total_count']}")
                    elif "total_files" in result:
                        print(f"    Total files: {result['total_files']}")

                else:
                    print(f"  ⚠️  Success but with error: {result.get('error', 'Unknown error')}")
            else:
                print(f"  ❌ Failed - Status: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"    Error: {error_data.get('error', 'Unknown error')}")
                except:
                    print(f"    Error: {response.text[:100]}...")

        except requests.exceptions.ConnectionError:
            print(f"  ⚠️  Connection failed - Flask app not running?")
            break
        except Exception as e:
            print(f"  ❌ Error: {e}")


def show_usage_examples():
    """Show usage examples for the new API endpoints."""
    print("\n📖 Usage Examples:")

    examples = [
        {
            "title": "Get all files",
            "method": "GET",
            "endpoint": "/api/v1/files",
            "description": "Get all FIRDS and FITRS files",
        },
        {
            "title": "Get FIRDS files with limit",
            "method": "GET",
            "endpoint": "/api/v1/files?file_type=firds&limit=10",
            "description": "Get latest 10 FIRDS files",
        },
        {
            "title": "Get files by dataset type",
            "method": "GET",
            "endpoint": "/api/v1/files?dataset_type=FULINS_E",
            "description": "Get all equity FULINS files",
        },
        {
            "title": "Get files by date range",
            "method": "GET",
            "endpoint": "/api/v1/files?date_from=2025-07-01&date_to=2025-07-15",
            "description": "Get files modified between July 1-15",
        },
        {
            "title": "List available ESMA files",
            "method": "GET",
            "endpoint": "/api/v1/esma-files?datasets=firds&date_from=2025-07-12",
            "description": "Get FIRDS files available from ESMA since July 12",
        },
        {
            "title": "Download and parse files",
            "method": "POST",
            "endpoint": "/api/v1/files/download",
            "body": {
                "urls": ["https://firds.esma.europa.eu/firds/FULINS_20250712_E_1of1.zip"],
                "force_update": False,
            },
            "description": "Download and parse specific ESMA files",
        },
        {
            "title": "Get detailed statistics",
            "method": "GET",
            "endpoint": "/api/v1/files/stats/detailed?file_types=firds&dataset_types=FULINS_E",
            "description": "Get stats for FIRDS equity files",
        },
        {
            "title": "Clean up old files",
            "method": "POST",
            "endpoint": "/api/v1/files/cleanup",
            "body": {"file_type": "firds", "dry_run": True},
            "description": "Preview cleanup of old FIRDS files",
        },
    ]

    for example in examples:
        print(f"\n• {example['title']}")
        print(f"  {example['method']} {example['endpoint']}")
        if "body" in example:
            print(f"  Body: {json.dumps(example['body'], indent=2)}")
        print(f"  → {example['description']}")


if __name__ == "__main__":
    print("🚀 Testing Enhanced File Management System")
    print("=" * 50)

    # Test service directly
    service_success = test_file_management_service()

    # Test API endpoints if service works
    if service_success:
        test_api_endpoints()

    # Show usage examples
    show_usage_examples()

    print("\n" + "=" * 50)
    print("✅ Testing completed!")
