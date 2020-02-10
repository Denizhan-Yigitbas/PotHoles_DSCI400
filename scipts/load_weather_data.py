import pandas as pd
import os
import gzip
from io import StringIO
import requests
import urllib.request

base_url = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/"

station_path = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt"

# Set these to non-null to save results to a csv file
data_output_path = None
stations_output_path = None

station_data = []

# Retrieve the file containing station data from the url above,
# and parse it into distinct fields
with urllib.request.urlopen(station_path) as fn:
    for sb in fn.readlines():
        row = []
        s = sb.decode('utf-8')

        row.append(s[:11].strip())
        row.append(float(s[12:20].strip()))
        row.append(float(s[22:30].strip()))
        row.append(float(s[31:37].strip()))
        row.append(s[38:40].strip())
        row.append(s[41:71].strip())
        row.append(s[72:75].strip())
        row.append(s[76:79].strip())
        row.append(s[80:].strip())
        station_data.append(row)

# Construct a dataframe containing the data for all stations
stations = pd.DataFrame(
    station_data,
    columns=['station_id', 'lat', 'lon', 'elev', 'state', 'name', 'gsn_flag', 'hcn/crn_flag', 'wmo_id']
)

tx_stations = stations.loc[stations['state'] == 'TX']


column_headers = ['station_id', 'date', 'reading_type', 'value', 'm_flag', 'q_flag', 's_flag', 'time']

# Retrieve all weather data from start_year to end_year, inclusive
start_year = 1950
end_year = 2020

years = list(range(start_year, end_year + 1))

frames = []
tx_ids = tx_stations.station_id.values

# For each year, download the file for that year to a local file,
# decompress it using gzip, and create a dataframe with all the Texas data.
# Deletes the downloaded file after completion.
for year in years:
    fname = f"{year}.csv.gz"

    # Download the compressed data
    with open(fname, "wb") as fn:
        r = requests.get(base_url + fname)
        fn.write(r.content)

    # Read the compressed data into a file-like object
    f = gzip.open(fname, 'rb')
    data = StringIO(f.read().decode('utf-8'))
    f.close()

    # Create a dataframe containing only data from Texas stations
    df = pd.read_csv(data, header=None, names=column_headers)
    df = df.loc[df.station_id.isin(tx_ids)]
    frames.append(df)

    os.remove(fname)

    print(f"Data loaded for {year}")

# Join each years data together into a single dataframe
all_df = pd.concat(frames)

# If a local path is provided, the data and station dataframes are saved to a local file
if data_output_path is not None:
    all_df.to_csv(data_output_path, index=False)
if stations_output_path is not None:
    tx_stations.to_csv(stations_output_path, index=False)