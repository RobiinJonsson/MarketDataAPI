#!/usr/bin/env python3

import requests
import json

def test_server_health():
    """Test if the Flask server is running and responsive"""
    try:
        # Test the health endpoint first
        print("Testing server health...")
        response = requests.get("http://localhost:5000/health", timeout=10)
        print(f"Health check: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Server is running")
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectRefused:
        print("❌ Connection refused - server not running")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_simple_api():
    """Test a simple API endpoint"""
    try:
        print("Testing simple API endpoint...")
        response = requests.get("http://localhost:5000/api/v1/instruments?limit=1", timeout=10)
        print(f"API test: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API is responsive")
            return True
        else:
            print(f"❌ API test failed: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ API Error: {e}")
        return False

if __name__ == "__main__":
    print("Quick server connectivity test...")
    print("=" * 50)
    
    if test_server_health():
        test_simple_api()
    else:
        print("Server is not responding - check if Flask is running")
