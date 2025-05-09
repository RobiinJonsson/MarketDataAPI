import requests

GLEIF_BASE_URL = "https://api.gleif.org/api/v1/lei-records"

def fetch_lei_info(lei_code):
    """Fetches issuer info for a given LEI code from the GLEIF API."""
    url = f"{GLEIF_BASE_URL}/{lei_code}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from GLEIF API: {e}")
        return {"error": "Failed to retrieve LEI information"}

