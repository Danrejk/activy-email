import gpxpy
import gpxpy.gpx

from src.gpx.generator.utils.get_elevation_data import get_elevation_data


def generate_gpx(route_coords):
    gpx = gpxpy.gpx.GPX()

    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    elevations = get_elevation_data(route_coords)

    for (lat, lon), ele in zip(route_coords, elevations):
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=ele))

    return gpx.to_xml()
