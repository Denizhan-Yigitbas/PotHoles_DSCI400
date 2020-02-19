"""
Filter existing Texas weather DataFrame into smaller DataFrame of Houston readings.
"""

import pandas as pd


max_lat, min_lat = 30.13, 29.5
max_lon, min_lon = -95, -95.8


data = pd.read_csv("../data/raw/all_tx_weather.csv")
stations = pd.read_csv("../data/raw/all_tx_stations.csv")

houston_ids = stations.loc[
    (min_lat <= stations.lat) & (stations.lat <= max_lat) & (min_lon <= stations.lon) & (stations.lon <= max_lon)
].station_id.values

houston_data = data.loc[data.station_id.isin(houston_ids)]

houston_data.to_csv("../data/raw/houston_weather.csv", index=False)

