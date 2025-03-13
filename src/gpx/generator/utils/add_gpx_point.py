import gpxpy.gpx


def add_gpx_point(gpx_segment, lat, lon, ele, current_time):
    gpx_point = gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=ele, time=current_time)
    gpx_segment.points.append(gpx_point)
