import gpxpy
import gpxpy.gpx
import numpy as np
import random

from src.gpx.calculateDistance import calculateDistance

def applyUrbanDrift(lat, lon, drift_type, urbanFactor=0.00005):
    # Simulate drift in a random direction within a small radius
    drift_direction = random.uniform(0, 2 * np.pi)  # Random direction in radians

    # Adjust drift distance based on drift type (lowered the range of error)
    if drift_type == 'smooth':
        drift_distance = np.random.normal(0, urbanFactor / 10)  # Smaller drift
    elif drift_type == 'harsh':
        drift_distance = np.random.normal(0, urbanFactor)  # Moderate drift
    elif drift_type == 'precise':
        drift_distance = np.random.normal(0, urbanFactor / 20)  # Very small drift
    else:  # fucked_up
        drift_distance = np.random.normal(0, urbanFactor * 2)  # More exaggerated but not extreme

    # Apply drift
    drift_lat = drift_distance * np.cos(drift_direction)
    drift_lon = drift_distance * np.sin(drift_direction)

    return lat + drift_lat, lon + drift_lon


def removeRandomPoints(points):
    # Print the total number of points initially
    print(f"Total points before removal: {len(points)}")

    # Remove a random number (1 to 3) of points from the start
    num_to_remove_start = random.randint(1, 3)

    # Remove a random number (1 to 3) of points from the end
    num_to_remove_end = random.randint(1, 3)

    # Print the number of points to remove
    print(f"Points to remove from start: {num_to_remove_start}")
    print(f"Points to remove from end: {num_to_remove_end}")

    # Ensure we don't try to remove more points than exist
    num_to_remove_start = min(num_to_remove_start, len(points) - 1)
    num_to_remove_end = min(num_to_remove_end, len(points) - 1)

    # Print the adjusted number of points to remove
    print(f"Adjusted points to remove from start: {num_to_remove_start}")
    print(f"Adjusted points to remove from end: {num_to_remove_end}")

    # Perform the point removal
    if num_to_remove_end > 0:
        points = points[num_to_remove_start:-num_to_remove_end]
    else:
        points = points[num_to_remove_start:]

    # Print the total number of points after removal
    print(f"Total points after removal: {len(points)}")

    return points


def fixGpxFile(inputFile, outputFile, distanceBetweenPoints=10, gpsError=0.00001, urbanFactor=0.00005,
               baseSegmentLength=1000, maxVariation=200, preserveLastPoint=True):
    with open(inputFile, 'r') as gpxFile:
        gpx = gpxpy.parse(gpxFile)

    all_lats = [p.latitude for track in gpx.tracks for segment in track.segments for p in segment.points]
    all_lons = [p.longitude for track in gpx.tracks for segment in track.segments for p in segment.points]

    # Global corruption factor: random between 0.5 and 1.5 (scale the drift factor)
    corruption_factor = random.uniform(0.5, 1.5)

    # Drift types and segment length
    drift_types = ['smooth', 'harsh', 'precise', 'fucked_up']
    current_drift_type = random.choice(drift_types)
    drift_type_switch_counter = 0

    for track in gpx.tracks:
        for segment in track.segments:
            newRoute = []
            i = 0
            while i < len(segment.points) - 1:
                startPoint, endPoint = segment.points[i], segment.points[i + 1]
                distance = calculateDistance(startPoint.latitude, startPoint.longitude, endPoint.latitude,
                                             endPoint.longitude)
                extraPoints = int(distance // distanceBetweenPoints)
                newRoute.append(
                    gpxpy.gpx.GPXTrackPoint(startPoint.latitude, startPoint.longitude, elevation=startPoint.elevation,
                                            time=startPoint.time))

                # Determine a random segment length around 1km
                segment_length = random.uniform(baseSegmentLength - maxVariation, baseSegmentLength + maxVariation)
                segment_points = 0

                while segment_points < segment_length and i < len(segment.points) - 1:
                    i += 1
                    currentPoint = segment.points[i]
                    lat, lon = currentPoint.latitude, currentPoint.longitude
                    lat += np.random.normal(0, gpsError)
                    lon += np.random.normal(0, gpsError)
                    # Apply urban drift effect for this segment
                    lat, lon = applyUrbanDrift(lat, lon, current_drift_type, urbanFactor * corruption_factor)
                    newRoute.append(gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=(
                                                                                            startPoint.elevation + currentPoint.elevation) / 2 if startPoint.elevation and currentPoint.elevation else None,
                                                            time=startPoint.time))

                    segment_points += calculateDistance(currentPoint.latitude, currentPoint.longitude,
                                                        segment.points[i - 1].latitude, segment.points[i - 1].longitude)

                # Update drift type after segment length
                drift_type_switch_counter += 1
                if drift_type_switch_counter >= segment_length:
                    current_drift_type = random.choice(drift_types)  # Switch to a new drift type
                    drift_type_switch_counter = 0  # Reset counter

            # Now remove random starting and ending points after applying all noise and drift
            newRoute = removeRandomPoints(newRoute)

            # Optionally preserve the last point
            if preserveLastPoint:
                # Ensure the last point is included but still removed from the previous step
                newRoute.append(gpxpy.gpx.GPXTrackPoint(segment.points[-1].latitude, segment.points[-1].longitude,
                                                        elevation=segment.points[-1].elevation,
                                                        time=segment.points[-1].time))

            # Set the segment points with the newly modified route
            segment.points = newRoute

    with open(outputFile, 'w') as outputGpx:
        outputGpx.write(gpx.to_xml())


# Example usage
if __name__ == "__main__":
    fixGpxFile('input.gpx', 'output.gpx', preserveLastPoint=False)