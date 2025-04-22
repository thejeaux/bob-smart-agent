# api_fetcher.py

import requests

def fetch_user_data(username):
    """
    Fetch a user's bar data from the BAXUS API.
    """
    url = f"http://services.baxus.co/api/bar/user/{username}"
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")

    bottles = response.json()

    # Check if bottles list is truly empty
    if bottles is None or len(bottles) == 0:
        raise Exception("No bottles found in user bar.")

    return bottles
