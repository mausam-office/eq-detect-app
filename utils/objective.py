import numpy as np
from utils.distance import haversine

def objective_function(source, sensor_positions, arrival_times, wave_speed):
    estimated_times = [
        haversine(source, pos)/ wave_speed for pos in sensor_positions
    ]
    time_diffs = np.array(arrival_times) - np.array(estimated_times)
    return np.sum(time_diffs**2)