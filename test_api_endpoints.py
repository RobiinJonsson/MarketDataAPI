#!/usr/bin/env python3
"""
API Endpoint Test Script

Test all consolidated API endpoints to verify functionality and display outputs.
"""
import json
import requests
from datetime import datetime


def test_endpoint(url, method="GET", data=None):
    """Test an API endpoint and return the response"""
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=5)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=5)
        
        print(f"\n{'='*80}")
        print(f"ENDPOINT: {method} {url}")
        print(f"STATUS CODE: {response.status_code}")
        print(f"HEADERS: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                response_json = response.json()
                print(f"RESPONSE TYPE: {type(response_json)}")
                if isinstance(response_json, dict):
                    print(f"RESPONSE KEYS: {list(response_json.keys())}")
                    if 'data' in response_json and isinstance(response_json['data'], list) and len(response_json['data']) > 0:
                        print(f"FIRST DATA ITEM KEYS: {list(response_json['data'][0].keys())}")
                        print(f"SAMPLE DATA ITEM:")
                        print(json.dumps(response_json['data'][0], indent=2, default=str))
                print(f"FULL RESPONSE:")
                print(json.dumps(response_json, indent=2, default=str))
            except json.JSONDecodeError:
                print(f"RAW RESPONSE TEXT: {response.text[:500]}...")
        else:
            print(f"ERROR RESPONSE: {response.text}")
        
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"\n{'='*80}")
        print(f"ENDPOINT: {method} {url}")
        print(f"ERROR: {e}")
        return None


def main():
    """Test all API endpoints"""
    base_url = "http://localhost:5000/api/v1"
    
    print(f"Testing API endpoints at {base_url}")
    print(f"Test started at: {datetime.now()}")
    
    # Test all endpoints
    endpoints = [
        # Instruments
        (f"{base_url}/instruments?limit=2", "GET"),
        (f"{base_url}/instruments/types", "GET"),
        
        # MIC codes
        (f"{base_url}/mic?limit=2", "GET"),
        (f"{base_url}/mic/countries", "GET"),
        
        # Legal entities (rich responses)
        (f"{base_url}/legal-entities?limit=2", "GET"),
        (f"{base_url}/legal-entities/M312WZV08Y7LYUC71685", "GET"),
        
        # Transparency (rich responses)
        (f"{base_url}/transparency?limit=1", "GET"),
        (f"{base_url}/transparency/isin/US8793601050", "GET"),
        
        # Files (if available)
        (f"{base_url}/files?limit=1", "GET"),
    ]
    
    successful_tests = 0
    total_tests = len(endpoints)
    
    for url, method in endpoints:
        response = test_endpoint(url, method)
        if response and response.status_code == 200:
            successful_tests += 1
    
    print(f"\n{'='*80}")
    print(f"SUMMARY: {successful_tests}/{total_tests} endpoints successful")
    print(f"Test completed at: {datetime.now()}")


if __name__ == "__main__":
    main()