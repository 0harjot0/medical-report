from typing import List, Dict, Optional
import requests

def search_drugs(term: str) -> Optional[Dict]:
    """
    Performs a search for drugs using the OpenFDA API.

    Args:
        term: str - The search term or drug name

    Returns:
        Optional[Dict]: Dictionary containing drug information if successful, else None
    """
    base_url = "https://api.fda.gov/drug/label.json"
    params = {
        "search": f"openfda.brand_name:{term}",
        "limit": 5  # Limit to top 5 results
    }

    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        print(f"Search request failed with status code {response.status_code}")
        return None
    
    try:
        data = response.json()
        results = data.get("results", [])
        return results.items
    except ValueError as e:
        print(f"JSON parsing error: {str(e)}")
        return None

