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


stations = pd.DataFrame(
    station_data,
    columns=['station_id', 'lat', 'lon', 'elev', 'state', 'name', 'gsn_flag', 'hcn/crn_flag', 'wmo_id']
)

tx_stations = stations.loc[stations['state'] == 'TX']


column_headers = ['station_id', 'date', 'reading_type', 'value', 'm_flag', 'q_flag', 's_flag', 'time']

start_year = 1950
end_year = 2020

years = list(range(start_year, end_year + 1))

frames = []
tx_ids = tx_stations.station_id.values

for year in years:
    fname = f"{year}.csv.gz"

    with open(fname, "wb") as fn:
        r = requests.get(base_url + fname)
        fn.write(r.content)

    f = gzip.open(fname, 'rb')
    data = StringIO(f.read().decode('utf-8'))
    f.close()

    df = pd.read_csv(data, header=None, names=column_headers)
    df = df.loc[df.station_id.isin(tx_ids)]
    frames.append(df)

    os.remove(fname)

    print(f"Data loaded for {year}")

all_df = pd.concat(frames)


if data_output_path is not None:
    all_df.to_csv(data_output_path, index=False)
if stations_output_path is not None:
    tx_stations.to_csv(stations_output_path, index=False)