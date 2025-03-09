import requests

def fetch_property(api_url):
    """Fetch properties from API, rank them, and return sorted list."""
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch API data: {response.status_code}")

    properties = response.json()

    return properties