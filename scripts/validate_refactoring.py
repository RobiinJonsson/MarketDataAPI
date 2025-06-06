#!/usr/bin/env python
"""
Validation script for the refactored routes.
This script tests all routes to ensure they work properly after refactoring.

Run this script directly from the command line:
python scripts/validate_refactoring.py [--base-url http://localhost:5000]

Or, if the server isn't already running, use the --start-server flag:
python scripts/validate_refactoring.py --start-server
"""

import sys
import os
import time
import requests
import argparse
import subprocess
from urllib.parse import urljoin

# Try to import tabulate, but provide fallback if not available
try:
    from tabulate import tabulate
except ImportError:
    def tabulate(data, **kwargs):
        result = []
        headers = kwargs.get('headers', [])
        if headers:
            result.append(' | '.join(headers))
            result.append('-' * 80)
        for row in data:
            result.append(' | '.join(str(item) for item in row))
        return '\n'.join(result)

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

def test_endpoint(base_url, endpoint, method='GET', expected_status=200, description=None):
    """Test an API endpoint and return the result"""
    url = urljoin(base_url, endpoint)
    try:
        # Prepare different payloads for different endpoints
        payload = {}
        
        if method in ['POST', 'PUT']:
            if 'instruments' in endpoint:
                # Basic instrument data with required fields (using 'Id' as expected by service)
                payload = {
                    "Id": "SE0000242455",  # Use 'Id' field as expected by InstrumentService
                    "FinInstrmGnlAttrbts_FullNm": "Test Instrument",
                    "type": "equity",  # Required field
                    "currency": "USD"
                }           
            elif 'entities' in endpoint:
                # Basic entity data with LEI - using Apple Inc's real LEI
                payload = {
                    "lei": "HWUPKR0MPOU8FGXBT394",  # Apple Inc's real LEI from GLEIF
                    "name": "Test Entity",
                    "status": "ACTIVE"
                }
        
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=payload)        
        elif method == 'PUT':
            response = requests.put(url, json=payload)
        elif method == 'DELETE':
            response = requests.delete(url)
        else:
            return False, f"Unsupported method: {method}", None
        
        success = response.status_code == expected_status
        status = f"{response.status_code} ({'PASS' if success else 'FAIL'})"
        json_data = None
        try:
            json_data = response.json()
        except Exception:
            pass
        
        return success, status, json_data
    except Exception as e:
        return False, f"Error: {str(e)}", None

def main():
    parser = argparse.ArgumentParser(description='Test API endpoints to validate refactoring.')
    parser.add_argument('--base-url', default='http://localhost:5000', help='Base URL of the API')
    parser.add_argument('--start-server', action='store_true', help='Start the Flask server for testing')
    parser.add_argument('--server-port', type=int, default=5000, help='Port for the Flask server if starting one')
    args = parser.parse_args()
    
    base_url = args.base_url
    
    server_process = None
    # Start a Flask server if requested
    if args.start_server:
        print("Starting Flask development server...")
        server_cmd = [sys.executable, "-m", "flask", "run", "--port", str(args.server_port)]
        server_process = subprocess.Popen(
            server_cmd, 
            env={**os.environ, "FLASK_APP": "marketdata_api"}, 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
          # Wait for server to start
        print("Waiting for server to start...")
        time.sleep(2)  # Give it a couple seconds to start
        
    # Define endpoints to test
    endpoints = [        # Common endpoints
        {'endpoint': '/api/v1/', 'method': 'GET', 'expected': 200, 'description': 'API Root'},
        {'endpoint': '/api/v1/info', 'method': 'GET', 'expected': 200, 'description': 'API Info'},
        {'endpoint': '/api/v1/health', 'method': 'GET', 'expected': 200, 'description': 'Health Check'},
          # Instrument endpoints
        {'endpoint': '/api/v1/instruments', 'method': 'GET', 'expected': 200, 'description': 'List Instruments'},
        {'endpoint': '/api/v1/instruments', 'method': 'POST', 'expected': 201, 'description': 'Create Instrument'},
        {'endpoint': '/api/v1/instruments/SE0000242455', 'method': 'GET', 'expected': 200, 'description': 'Get Instrument'},
        {'endpoint': '/api/v1/instruments/XXINVALID', 'method': 'GET', 'expected': 404, 'description': 'Get Invalid Instrument'},
        {'endpoint': '/api/v1/instruments/SE0000242455', 'method': 'PUT', 'expected': 200, 'description': 'Update Instrument'},
        {'endpoint': '/api/v1/instruments/XXINVALID', 'method': 'PUT', 'expected': 404, 'description': 'Update Invalid Instrument'},
        {'endpoint': '/api/v1/instruments/SE0000242455', 'method': 'DELETE', 'expected': 200, 'description': 'Delete Instrument'},
        {'endpoint': '/api/v1/instruments/XXINVALID', 'method': 'DELETE', 'expected': 404, 'description': 'Delete Invalid Instrument'},
          # Entity endpoints
        {'endpoint': '/api/v1/entities', 'method': 'GET', 'expected': 200, 'description': 'List Entities'},
        {'endpoint': '/api/v1/entities', 'method': 'POST', 'expected': 201, 'description': 'Create Entity'},
        {'endpoint': '/api/v1/entities/HWUPKR0MPOU8FGXBT394', 'method': 'GET', 'expected': 200, 'description': 'Get Entity'},
        {'endpoint': '/api/v1/entities/XXINVALID', 'method': 'GET', 'expected': 404, 'description': 'Get Invalid Entity'},
        {'endpoint': '/api/v1/entities/HWUPKR0MPOU8FGXBT394', 'method': 'PUT', 'expected': 200, 'description': 'Update Entity'},
        {'endpoint': '/api/v1/entities/XXINVALID', 'method': 'PUT', 'expected': 404, 'description': 'Update Invalid Entity'},
        {'endpoint': '/api/v1/entities/HWUPKR0MPOU8FGXBT394', 'method': 'DELETE', 'expected': 200, 'description': 'Delete Entity'},
        {'endpoint': '/api/v1/entities/XXINVALID', 'method': 'DELETE', 'expected': 404, 'description': 'Delete Invalid Entity'},
        
        # CFI endpoints
        {'endpoint': '/api/v1/cfi/ESVUFN', 'method': 'GET', 'expected': 200, 'description': 'Decode Valid CFI'},
        {'endpoint': '/api/v1/cfi/XXX', 'method': 'GET', 'expected': 400, 'description': 'Invalid CFI Length'},
        {'endpoint': '/api/v1/cfi/XXXXXX', 'method': 'GET', 'expected': 400, 'description': 'Invalid CFI Format'},
    ]
    
    print(f"Testing API endpoints at {base_url}...")
    
    # Test all endpoints
    results = []
    all_success = True
    
    for endpoint_info in endpoints:
        success, status, resp_data = test_endpoint(
            base_url, 
            endpoint_info['endpoint'], 
            endpoint_info['method'], 
            endpoint_info['expected'],
            endpoint_info.get('description', '')        )
        
        results.append([
            endpoint_info.get('description', ''),
            f"{endpoint_info['method']} {endpoint_info['endpoint']}",
            status,
            'Success' if success else 'Failed'
        ])
        
        if not success:
            all_success = False
    
    # Display results
    print("\nRefactoring Validation Results:")
    print(tabulate(results, headers=['Description', 'Endpoint', 'Status', 'Result'], tablefmt='grid'))
    if all_success:
        print("\n[SUCCESS] All tests passed! The refactored routes are working correctly.")
        exit_code = 0
    else:
        print("\n[FAILED] Some tests failed. Please check the issues before removing the legacy code.")
        exit_code = 1
        
    # Clean up the server process if we started one
    if server_process:
        print("Stopping Flask server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
    
    return exit_code

if __name__ == '__main__':
    sys.exit(main())
