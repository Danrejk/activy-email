import openrouteservice

with open('ORS_API.key', 'r') as file:
    ORS_API_KEY = file.read().strip()

def generate_route(start_lat, start_lon, end_lat, end_lon):
    client = openrouteservice.Client(key=ORS_API_KEY)
    coords = ((start_lon, start_lat), (end_lon, end_lat))
    route = client.directions(coords, profile='cycling-regular', format='geojson')

    route_coords = [(point[1], point[0]) for point in route['features'][0]['geometry']['coordinates']]
    return route_coords

