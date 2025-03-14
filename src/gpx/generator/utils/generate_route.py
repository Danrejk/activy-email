import openrouteservice

def generate_route(start_lat, start_lon, end_lat, end_lon, api_key):
    client = openrouteservice.Client(key=api_key)
    coords = ((start_lon, start_lat), (end_lon, end_lat))
    route = client.directions(coords, profile='cycling-regular', format='geojson')

    route_coords = [(point[1], point[0]) for point in route['features'][0]['geometry']['coordinates']]
    return route_coords