#!/usr/bin/env python3

import requests
import json

def test_simple_creation():
    """Simple test of instrument creation endpoint"""
    
    # Test with a known European equity ISIN that exists in our local files
    payload = {
        'Id': 'NL00150001S5',  # Kingfish Co NV (confirmed to exist in FULINS_E files)
        'type': 'equity'       # This should be found in local files
    }
    
    url = 'http://localhost:5000/api/v1/instruments'
    
    print(f"Testing instrument creation:")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)  # 30 second timeout
        print(f"\nResponse status: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            result = response.json()
            print(f"Response body: {json.dumps(result, indent=2)}")
        else:
            print(f"Response body (non-JSON): {response.text}")
            
        return response.status_code in [200, 201]
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_simple_creation()
    print(f"\nTest result: {'SUCCESS' if success else 'FAILED'}")
