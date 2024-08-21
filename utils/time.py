from datetime import datetime
from utils.distance import haversine

def calculate_duration(pos, p1, v=6000):
    """
    t = dist / v
    """
    durations = []
    # p1  = (27.587364, 85.513386) # panauti
    # p1  = (26.730892, 86.466027) # lahan
    # p1  = (27.485745, 85.137086) 
    # p1  = (26.566788, 84.210440) 
    # p1  = pos[0]
    for p in pos:
        duration = haversine(p1, p) / v
        durations.append(duration)
    return durations


def convert_to_seconds_relative(timestamp, reference_time):
    fmt = "%Y-%m-%d %H:%M:%S.%f"
    dt = datetime.strptime(timestamp, fmt)
    # Convert datetime to seconds since the reference_time
    return (dt - reference_time).total_seconds()
