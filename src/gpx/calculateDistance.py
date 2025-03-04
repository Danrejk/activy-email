import numpy as np

def calculateDistance(startLatitude, startLongitude, endLatitude, endLongitude):
    earthRadius = 6371.0  # radius of the earth in kilometers
    startLatitude, startLongitude, endLatitude, endLongitude = np.radians([startLatitude, startLongitude, endLatitude, endLongitude])
    dlat, dlon = endLatitude - startLatitude, endLongitude - startLongitude
    a = np.sin(dlat / 2) ** 2 + np.cos(startLatitude) * np.cos(endLatitude) * np.sin(dlon / 2) ** 2
    return earthRadius * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)) * 1000  # convert to meters
