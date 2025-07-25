#!/usr/bin/env python3
"""
Simple test script for download-by-criteria endpoint.
Tests downloading FIRDS FULINS_F file for 2025-07-12.
"""

import requests
import json

def test_firds_fulins():
    """Test downloading FIRDS FULINS_D file for specific date."""
    
    url = "http://localhost:5000/api/v1/files/download-by-criteria"
    
    payload = {
        "file_type": "firds",
        "dataset": "FULINS_F", 
        "date": "2025-07-12"
    }
    
    print("Testing Download by Criteria Endpoint")
    print("=" * 50)
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print()
    
    try:
        print("Sending request...")
        response = requests.post(url, json=payload, timeout=300)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Message: {result.get('message', 'No message')}")
            print(f"Files processed: {result.get('files_processed', 0)}")
            print(f"Files downloaded: {len(result.get('files_downloaded', []))}")
            print(f"Files skipped: {len(result.get('files_skipped', []))}")
            print(f"Files failed: {len(result.get('files_failed', []))}")
            
            if result.get('files_downloaded'):
                print("\nDownloaded files:")
                for file_name in result['files_downloaded']:
                    print(f"  - {file_name}")
            
            if result.get('files_skipped'):
                print("\nSkipped files:")
                for file_name in result['files_skipped']:
                    print(f"  - {file_name}")
            
            # Show full response for debugging
            print("\nFull Response:")
            print(json.dumps(result, indent=2))
            
        else:
            print("❌ ERROR!")
            try:
                error_data = response.json()
                print(f"Error: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"Response: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error!")
        print("Make sure the Flask app is running on http://localhost:5000")
    except requests.exceptions.Timeout:
        print("⏰ Request Timeout!")
        print("The download took longer than 5 minutes.")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    test_firds_fulins()
