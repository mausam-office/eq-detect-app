import folium

from utils.constants import (
    MAX_ZOOM, INITIAL_ZOOM, MAP_TYPE, INITIAL_POINT, MARKER_MAP_C
    )

def get_map(token):
    map_tile = folium.Map(
        title="Nepal",
        max_zoom = MAX_ZOOM,
        zoom_start=INITIAL_ZOOM,
        location=MARKER_MAP_C,
        tiles=f"https://api.mapbox.com/styles/v1/mapbox/{MAP_TYPE}streets-v11/tiles/{{z}}/{{x}}/{{y}}?access_token={token}",
        attr="Mapbox attribution"
    )
    return map_tile


def plot_location(map, loc, icon_path, label):
    for lat, lon in loc:
        folium.Marker(
            location=(lat, lon),
            tooltip=label,
            icon=folium.CustomIcon(icon_path, icon_size=(20, 20)),
        ).add_to(map)
    
    return map


def plot_line(map, point1, point2):
    coordinates = [point1, point2]
    line = folium.PolyLine(coordinates, popup='Bias', color='blue', weight=5, opacity=0.8)

    line.add_to(map)

    return map
    