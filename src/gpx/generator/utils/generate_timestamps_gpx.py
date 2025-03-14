from datetime import datetime, timedelta

from src.gpx.generator.utils.add_gpx_point import add_gpx_point
from src.gpx.generator.utils.calculate_speed import calculate_speed
from src.gpx.generator.utils.create_gpx_structure import create_gpx_structure

from src.gpx.calculateDistance import calculateDistance
from src.gpx.generator.utils.get_elevation_data import get_elevation_data


def generate_timestamps_gpx(route_coords, avg_speed):
    gpx, gpx_segment = create_gpx_structure()
    elevations = get_elevation_data(route_coords)
    current_time = datetime.now()

    for i, ((lat, lon), ele) in enumerate(zip(route_coords, elevations)):
        add_gpx_point(gpx_segment, lat, lon, ele, current_time)

        if i < len(route_coords) - 1:
            next_lat, next_lon = route_coords[i + 1]
            next_ele = elevations[i + 1]
            distance = calculateDistance(lat, lon, next_lat, next_lon) / 1000  # convert to kilometers
            elevation_change = next_ele - ele
            speed = calculate_speed(avg_speed, elevation_change)
            time_diff = timedelta(hours=distance / speed)
            current_time += time_diff

    return gpx.to_xml()
