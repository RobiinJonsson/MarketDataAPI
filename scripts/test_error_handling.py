"""
Test script to demonstrate the robust error handling in GLEIF API calls
"""
import sys
import os
import logging
import requests
from pathlib import Path
import time
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from marketdata_api.services.gleif import (
    fetch_lei_info, fetch_direct_parent, fetch_ultimate_parent,
    fetch_direct_children, fetch_ultimate_children
)
from marketdata_api.services.api_utils import ApiError, RetryExhaustedError, ApiTimeoutError

class MockRequestsSession:
    """Mock requests session to simulate API errors"""
    def __init__(self, failure_count=2, failure_type="timeout"):
        self.failure_count = failure_count
        self.current_failures = 0
        self.failure_type = failure_type
        self._original_get = requests.get
    
    def __enter__(self):
        # Replace requests.get with our mock version
        requests.get = self._mock_get
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore the original requests.get
        requests.get = self._original_get
    
    def _mock_get(self, url, **kwargs):
        if self.current_failures < self.failure_count:
            self.current_failures += 1
            if self.failure_type == "timeout":
                logger.info(f"Simulating timeout error ({self.current_failures}/{self.failure_count})")
                raise requests.exceptions.Timeout("Simulated timeout error")
            elif self.failure_type == "connection":
                logger.info(f"Simulating connection error ({self.current_failures}/{self.failure_count})")
                raise requests.exceptions.ConnectionError("Simulated connection error")
            elif self.failure_type == "server_error":
                logger.info(f"Simulating server error ({self.current_failures}/{self.failure_count})")
                resp = requests.Response()
                resp.status_code = 500
                resp._content = b'{"error": "Internal Server Error"}'
                resp.url = url
                return resp
            elif self.failure_type == "rate_limit":
                logger.info(f"Simulating rate limit error ({self.current_failures}/{self.failure_count})")
                resp = requests.Response()
                resp.status_code = 429
                resp._content = b'{"error": "Rate limit exceeded"}'
                resp.url = url
                return resp
            
        # After failure count is reached, call the real method
        logger.info("Returning real response after simulated failures")
        return self._original_get(url, **kwargs)

def test_retry_mechanism():
    """Test the retry mechanism with different error types"""
    test_lei = "HWUPKR0MPOU8FGXBT394"  # Apple Inc.
    
    error_types = [
        {"type": "timeout", "count": 2, "description": "Timeout errors"},
        {"type": "connection", "count": 2, "description": "Connection errors"},
        {"type": "server_error", "count": 2, "description": "Server errors"},
        {"type": "rate_limit", "count": 2, "description": "Rate limit errors"}
    ]
    
    results = []
    
    for error_config in error_types:
        result = {
            "error_type": error_config["description"],
            "success": False,
            "retry_count": error_config["count"],
            "time_taken": 0,
            "error": None
        }
        
        logger.info(f"\n\nTesting retry with {error_config['description']} ({error_config['count']} failures)")
        print(f"\n{'-'*70}")
        print(f" Testing retry mechanism with {error_config['description']}")
        print(f"{'-'*70}")
        
        start_time = time.time()
        
        try:
            with MockRequestsSession(failure_count=error_config["count"], failure_type=error_config["type"]):
                # Try to fetch LEI info with simulated errors
                response = fetch_lei_info(test_lei)
                
            result["time_taken"] = time.time() - start_time
            
            # Check if we got a valid response
            if isinstance(response, dict) and "error" not in response:
                result["success"] = True
                print(f"\nSuccess after {error_config['count']} retries!")
                print(f"Total time: {result['time_taken']:.2f} seconds")
            else:
                result["error"] = response.get("error") if isinstance(response, dict) else "Unknown error"
                print(f"\nFailed after retries: {result['error']}")
        
        except (ApiError, RetryExhaustedError, ApiTimeoutError) as e:
            result["time_taken"] = time.time() - start_time
            result["error"] = str(e)
            print(f"\nException caught: {e}")
        
        results.append(result)
        
        # Let the API breathe between tests
        time.sleep(1)
    
    # Print summary
    print("\n\n" + "="*70)
    print(" RETRY TEST RESULTS")
    print("="*70)
    for result in results:
        status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
        print(f"{status} - {result['error_type']} - Time: {result['time_taken']:.2f}s")
        if not result["success"]:
            print(f"  Error: {result['error']}")
    print("="*70)

def test_real_api_calls():
    """Test error handling with real API calls"""
    # Test with valid LEI
    valid_lei = "HWUPKR0MPOU8FGXBT394"  # Apple Inc.
    
    # Test with invalid LEI
    invalid_lei = "INVALID12345NOTVALID"
    
    print("\n\n" + "="*70)
    print(" REAL API CALL TESTS")
    print("="*70)
    
    print("\nTesting with valid LEI (Apple Inc.):")
    try:
        response = fetch_lei_info(valid_lei)
        if "error" not in response:
            print(f"✅ SUCCESS - Valid LEI info retrieved")
            legal_name = response.get("data", {}).get("attributes", {}).get("entity", {}).get("legalName", {}).get("name")
            if legal_name:
                print(f"  Legal Name: {legal_name}")
        else:
            print(f"❌ FAILED - Error: {response['error']}")
    except Exception as e:
        print(f"❌ EXCEPTION - {str(e)}")
    
    print("\nTesting with invalid LEI:")
    try:
        response = fetch_lei_info(invalid_lei)
        if "error" in response:
            print(f"✅ EXPECTED ERROR - {response['error']}")
        else:
            print(f"❓ UNEXPECTED SUCCESS - Valid response with invalid LEI")
    except Exception as e:
        print(f"❌ EXCEPTION - {str(e)}")
    
    # Test parent/child relationships for Apple
    print("\nTesting relationships for Apple Inc.:")
    
    try:
        print("\nTesting direct parent retrieval:")
        direct_parent = fetch_direct_parent(valid_lei)
        if "error" not in direct_parent:
            print(f"✅ SUCCESS - Direct parent retrieved")
        else:
            print(f"ℹ️ INFO - {direct_parent['error']}")
            
        print("\nTesting direct children retrieval:")
        direct_children = fetch_direct_children(valid_lei)
        if "error" not in direct_children and "data" in direct_children:
            count = len(direct_children["data"])
            print(f"✅ SUCCESS - {count} direct children retrieved")
        else:
            print(f"ℹ️ INFO - {direct_children.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ EXCEPTION - {str(e)}")
    
    print("="*70)

if __name__ == "__main__":
    print("\nStarting robust error handling tests for GLEIF API integration...")
    try:
        # First test with simulated errors to demonstrate retry mechanism
        test_retry_mechanism()
        
        # Then test with real API calls
        test_real_api_calls()
        
    except Exception as e:
        logger.error(f"Unhandled exception in test script: {e}", exc_info=True)
