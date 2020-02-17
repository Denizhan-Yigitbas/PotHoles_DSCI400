from collections import deque

import pandas as pd
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

weather_data = "../../data/raw/all_tx_weather.csv"

class WeatherVSPotholes():
    def __init__(self):
        pass
    
    def create_last_n_rows_df(self, n):
        with open(weather_data, 'r') as f:
            q = deque(f, n)  # replace 2 with n (lines read at the end)
        column_names = ['station_id', 'date', 'reading_type', 'value', 'm_flag', 'q_flag', 's_flag', 'time']
        df = pd.read_csv(StringIO(''.join(q)), header=None)
        df.columns = column_names
        return df
    
    def create_2019_2020_df(self):
        df = self.create_last_n_rows_df(2000000)
        one_year_row = df.loc[df["date"] == 20190208].index.values[0]
        one_year_df = df.loc[one_year_row:]
        return one_year_df
    
        
if __name__ == "__main__":
    comparer = WeatherVSPotholes()
    comparer.create_2019_2020_df()