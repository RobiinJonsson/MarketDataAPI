"""
Simple test script for GLEIF API
"""
import requests
import json

def test_simple_gleif():
    # Example LEI code - Swedbank AB
    lei_code = "M312WZV08Y7LYUC71685"
    
    # Test the basic LEI info endpoint
    url = f"https://api.gleif.org/api/v1/lei-records/{lei_code}"
    
    print(f"Making request to: {url}")
    try:
        response = requests.get(url)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Exception occurred: {e}")
    
    # Test direct parent exception endpoint
    exception_url = f"https://api.gleif.org/api/v1/lei-records/{lei_code}/direct-parent-reporting-exception"
    
    print(f"\nMaking request to: {exception_url}")
    try:
        response = requests.get(exception_url)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Exception occurred: {e}")
        
    # Test direct children endpoint
    children_url = f"https://api.gleif.org/api/v1/lei-records/{lei_code}/direct-children"
    
    print(f"\nMaking request to: {children_url}")
    try:
        response = requests.get(children_url)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error response: {response.text}")
            
            # If direct children not found, try the relationships
            if response.status_code == 404:
                rel_url = f"https://api.gleif.org/api/v1/lei-records/{lei_code}/direct-child-relationships"
                print(f"\nTrying relationships endpoint: {rel_url}")
                rel_response = requests.get(rel_url)
                print(f"Status code: {rel_response.status_code}")
                
                if rel_response.status_code == 200:
                    data = rel_response.json()
                    print("Response:")
                    print(json.dumps(data, indent=2))
                else:
                    print(f"Error response: {rel_response.text}")
    except Exception as e:
        print(f"Exception occurred: {e}")

if __name__ == "__main__":
    test_simple_gleif()
