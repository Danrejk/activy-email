def calculate_speed(avg_speed, elevation_change):
    if elevation_change > 0:
        # Uphill: slower speed
        speed = avg_speed * (1 - min(elevation_change * 10 / 100, 0.85))
    else:
        # Downhill: faster speed
        speed = avg_speed * (1 + min(abs(elevation_change) * 10 / 100, 1.15))
    return speed
