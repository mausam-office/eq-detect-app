from datetime import datetime
from utils.distance import haversine

def calculate_duration(pos, epicenter, v):
    """
    t = dist / v
    """
    durations = []
    for p in pos:
        duration = haversine(epicenter, p) / v
        durations.append(duration)
    return durations


def convert_to_seconds_relative(timestamp, reference_time):
    fmt = "%Y-%m-%d %H:%M:%S.%f"
    dt = datetime.strptime(timestamp, fmt)
    # Convert datetime to seconds since the reference_time
    return (dt - reference_time).total_seconds()
