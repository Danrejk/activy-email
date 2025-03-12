import os
from src.gpx.generator.utils.generate_route import generate_route
from src.gpx.generator.utils.generate_gpx import generate_gpx

key_file_path = 'ORS_API.key'
if not os.path.exists(key_file_path):
    raise FileNotFoundError(f"API key file not found: {key_file_path}")

with open(key_file_path, 'r') as file:
    ORS_API_KEY = file.read().strip()

start_lat, start_lon = 54.3520, 18.6466  # Gdansk
end_lat, end_lon = 50.0647, 19.9450  # Krakow

route_coords = generate_route(start_lat, start_lon, end_lat, end_lon, ORS_API_KEY)

generate_gpx(route_coords, 'example.gpx')