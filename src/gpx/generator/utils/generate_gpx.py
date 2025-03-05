import gpxpy
import gpxpy.gpx

def generate_gpx(route_coords, output_file):
    gpx = gpxpy.gpx.GPX()

    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    for lat, lon in route_coords:
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon))

    with open(output_file, 'w') as f:
        f.write(gpx.to_xml())