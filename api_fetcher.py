import requests

def fetch_user_bar(username):
    url = f"http://services.baxus.co/api/bar/user/{username}"
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        bar_data = response.json()

        if isinstance(bar_data, dict) and 'bottles' in bar_data:
            bottles_list = bar_data['bottles']
        elif isinstance(bar_data, list):
            bottles_list = bar_data
        else:
            raise Exception("Unexpected API response format.")

        bottles = []
        for bottle in bottles_list:
            bottles.append({
                'name': bottle.get('name', ''),
                'region': bottle.get('region', ''),
                'price': bottle.get('price', 0),
                'age': bottle.get('age', None),
                'style': bottle.get('style', '')
            })
        return bottles
    else:
        raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")