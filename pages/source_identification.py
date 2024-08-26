import copy
import random
import pandas as pd
import streamlit as st

from datetime import datetime, timedelta
from scipy.optimize import minimize, differential_evolution
from streamlit_folium import folium_static

from utils.base import base
from utils.constants import WAVE_VELOCITY, LAT, LON, SOURCE_MARKER_PATH, SENSOR_MARKER_PATH, CONFIG_FP
from utils.distance import haversine
from utils.map import get_map, plot_location, plot_line
from utils.objective import objective_function, objective_function2
from utils.time import calculate_duration

base()

try:
    with open(CONFIG_FP) as cfg:
        st.session_state['token'] = cfg.read()
except Exception as e:
    st.exception(Exception("Token can't be loaded."))
    st.stop()

if 'wave_velocity' not in st.session_state:
    st.session_state['wave_velocity'] = WAVE_VELOCITY

if 'lat_lon' not in st.session_state:
    st.session_state['lat_lon'] = f"{LAT},{LON}"

if 'map' not in st.session_state:
    try:
        st.session_state['map'] = get_map(st.session_state['token'])
    except Exception as e:
        st.exception(e)
        st.stop()



def plot():
    if 'df' not in st.session_state:
        return
    
    df = st.session_state['df']

    latitudes = df['latitude'].to_list()
    longitudes = df['longitude'].to_list()

    sensor_positions = list(zip(latitudes, longitudes))

    lat, lon = st.session_state['lat_lon'].split(',')[:2]
    epicenter = [float(lat), float(lon)]
    
    arrival_times = calculate_duration(
        sensor_positions, 
        epicenter, 
        st.session_state['wave_velocity']
    )

    ref_timestamp = str(datetime.now())
    # Convert timestamps to datetime objects
    arrival_timestamp = [datetime.strptime(ref_timestamp, "%Y-%m-%d %H:%M:%S.%f") + timedelta(seconds=ts) for ts in arrival_times]

    result = differential_evolution(
        objective_function2,
        bounds=[(23.0, 32.0), (77.0, 91.0), (4800, 7200)],  # Latitude, longitude and speed bounds
        args=(sensor_positions, arrival_timestamp),
    )

    # estimated_location = result.x.tolist()
    estimated_location = result.x[:2]
    estimated_wave_speed = result.x[2]

    print(f"{estimated_wave_speed=}")

    bias = haversine(epicenter, estimated_location)    # in meters
    
    map = plot_location(copy.deepcopy(st.session_state['map']), sensor_positions, SENSOR_MARKER_PATH, 'Sensor')
    map = plot_location(map, [estimated_location], SOURCE_MARKER_PATH, 'Epicenter')
    map = plot_line(map, epicenter, estimated_location)

    folium_static(map, height=850, width=1625)


def column_validation():
    try:
        cols = st.session_state['df'].columns

        assert ('lat' in cols or 'latitude' in cols) and ('lon' in cols or 'longitude' in cols)

        new_names = {}
        if 'lat' in cols:
            new_names['lat'] = 'latitude'
        if 'lon' in cols:
            new_names['lon'] = 'longitude'

        st.session_state['df'] = st.session_state['df'].rename(new_names)
    except Exception as e:
        st.exception(e)
        st.stop()



with st.sidebar as s_bar:
    st.session_state['wave_velocity'] = st.slider(
        "Enter P-Wave Velocity:",
        min_value=5000,
        max_value=7000,
        value=WAVE_VELOCITY,
    )
    
    st.session_state['lat_lon'] = st.text_input(
        "Enter Testing Epicenter: (lat, lon) [Optional]",
        value=str(LAT) + ',' + str(LON),
    )

    file = st.file_uploader("Select file with stations list:")
    if file and file.name.endswith(('.csv', '.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
        st.session_state['df'] = pd.read_csv(file)

        column_validation()

        disabled = False
    else:
        disabled = True
    
    st.button("Submit", disabled=disabled, on_click=plot)
    


