from datetime import datetime, timedelta

import gpxpy
import gpxpy.gpx

from src.gpx.calculateDistance import calculateDistance
from src.gpx.generator.utils.get_elevation_data import get_elevation_data


def generate_timestamps_gpx(route_coords, avg_speed):
    gpx = gpxpy.gpx.GPX()

    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    elevations = get_elevation_data(route_coords)

    # Start time
    current_time = datetime.now()

    for i, ((lat, lon), ele) in enumerate(zip(route_coords, elevations)):
        gpx_point = gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=ele, time=current_time)
        gpx_segment.points.append(gpx_point)

        if i < len(route_coords) - 1:
            next_lat, next_lon = route_coords[i + 1]
            distance = calculateDistance(lat, lon, next_lat, next_lon) / 1000  # convert back
            time_diff = timedelta(hours=distance / avg_speed)
            current_time += time_diff

    return gpx.to_xml()
