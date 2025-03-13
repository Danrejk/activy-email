def calculate_speed(avg_speed, elevation_change):
    if elevation_change > 0:
        # Uphill: slower speed
        speed = avg_speed * (1 - min(elevation_change / 100, 0.5))  # reduce speed by up to 50%
    else:
        # Downhill: faster speed
        speed = avg_speed * (1 + min(abs(elevation_change) / 100, 0.3))  # increase speed by up to 30%
    return speed
