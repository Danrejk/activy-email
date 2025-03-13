import gpxpy
import gpxpy.gpx

from src.gpx.generator.utils.create_gpx_structure import create_gpx_structure
from src.gpx.generator.utils.get_elevation_data import get_elevation_data


def generate_gpx(route_coords):
    gpx, gpx_segment = create_gpx_structure()
    elevations = get_elevation_data(route_coords)

    for (lat, lon), ele in zip(route_coords, elevations):
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=ele))

    return gpx.to_xml()
