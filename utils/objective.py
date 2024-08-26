import numpy as np

from datetime import timedelta
from utils.distance import haversine



def objective_function(source, sensor_positions, arrival_times, wave_speed):
    estimated_times = [
        haversine(source, pos)/ wave_speed for pos in sensor_positions
    ]
    time_diffs = np.array(arrival_times) - np.array(estimated_times)
    return np.sum(time_diffs**2)

# Objective function to minimize
def objective_function2(params, sensor_positions, arrival_times):
    source_location = params[:2]  # First two parameters are the source location
    wave_speed = params[2]        # Third parameter is the wave speed

    n = len(sensor_positions)
    errors = []
    
    # Use the first sensor as the reference
    ref_distance = haversine(source_location, sensor_positions[0])
    ref_arrival_time = arrival_times[0]
    
    for i in range(1, n):
        distance_i = haversine(source_location, sensor_positions[i])
        estimated_time = ref_arrival_time + timedelta(seconds=(distance_i - ref_distance) / wave_speed)
        
        # Calculate the observed time difference in seconds
        observed_time = arrival_times[i]
        error = (observed_time - estimated_time).total_seconds() ** 2
        errors.append(error)
    return np.sum(errors)
