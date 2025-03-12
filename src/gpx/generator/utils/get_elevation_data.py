import requests

def get_elevation_data(coords):
    url = 'https://api.open-elevation.com/api/v1/lookup'
    locations = [{'latitude': lat, 'longitude': lon} for lat, lon in coords]
    response = requests.post(url, json={'locations': locations})
    response.raise_for_status()
    elevation_data = response.json()['results']
    return [point['elevation'] for point in elevation_data]