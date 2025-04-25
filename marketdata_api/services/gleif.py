import requests, json
from typing import Dict, Any, List

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
from typing import Dict, Any, List


def flatten_address(address: Dict[str, Any], address_type: str, lei: str) -> Dict[str, Any]:
    return {
        "lei": lei,
        "type": address_type,
        "language": address.get("language"),
        "addressLines": ", ".join(address.get("addressLines", [])),
        "city": address.get("city"),
        "region": address.get("region"),
        "country": address.get("country"),
        "postalCode": address.get("postalCode")
    }


def map_lei_record(response: Dict[str, Any]) -> Dict[str, Any]:
    data = response.get("data", {})
    attributes = data.get("attributes", {})
    entity = attributes.get("entity", {})
    registration = attributes.get("registration", {})

    return {
        "leiRecord": {
            "lei": attributes.get("lei"),
            "legalName": entity.get("legalName", {}).get("name"),
            "legalJurisdiction": entity.get("jurisdiction"),
            "legalFormId": entity.get("legalForm", {}).get("id"),
            "registeredAs": entity.get("registeredAs"),
            "category": entity.get("category"),
            "subCategory": entity.get("subCategory"),
            "status": entity.get("status"),
            "bic": attributes.get("bic"),
            "mic": attributes.get("mic"),
            "ocid": attributes.get("ocid"),
            "qcc": attributes.get("qcc"),
            "conformityFlag": attributes.get("conformityFlag"),
            "spglobal": ", ".join(attributes.get("spglobal", [])),
            "associatedEntityLei": entity.get("associatedEntity", {}).get("lei"),
            "associatedEntityName": entity.get("associatedEntity", {}).get("name"),
            "successorEntityLei": entity.get("successorEntity", {}).get("lei"),
            "successorEntityName": entity.get("successorEntity", {}).get("name"),
            "creationDate": entity.get("creationDate")
        },
        "addresses": [
            flatten_address(entity.get("legalAddress", {}), "legal", attributes.get("lei")),
            flatten_address(entity.get("headquartersAddress", {}), "headquarters", attributes.get("lei")),
        ],
        "registration": {
            "lei": attributes.get("lei"),
            "initialRegistrationDate": registration.get("initialRegistrationDate"),
            "lastUpdateDate": registration.get("lastUpdateDate"),
            "status": registration.get("status"),
            "nextRenewalDate": registration.get("nextRenewalDate"),
            "managingLou": registration.get("managingLou"),
            "corroborationLevel": registration.get("corroborationLevel"),
            "validatedAt": registration.get("validatedAt", {}).get("id"),
            "validatedAs": registration.get("validatedAs")
        },
        "metaInfo": {
            "lei": attributes.get("lei"),
            "publishDate": response.get("meta", {}).get("goldenCopy", {}).get("publishDate")
        }
    }

result = fetch_lei_info("5493001KJTIIGC8Y1R12")
if "error" in result:
    print(result["error"])
else:
    mapped_result = map_lei_record(result)
    print(json.dumps(mapped_result, indent=2))
