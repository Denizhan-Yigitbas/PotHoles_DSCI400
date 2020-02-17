from collections import deque

import pandas as pd
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

weather_data = "../data/raw/all_tx_weather.csv"

class WeatherVSPotholes():
    def __init__(self):
        pass
    
    """
    Private method that extracts the last n rows of the all_tx_weather.csv file in order to access the
     most recent recordings
    """
    def __create_last_n_rows_df(self, n):
        with open(weather_data, 'r') as f:
            q = deque(f, n)  # replace 2 with n (lines read at the end)
        column_names = ['station_id', 'date', 'reading_type', 'value', 'm_flag', 'q_flag', 's_flag', 'time']
        df = pd.read_csv(StringIO(''.join(q)), header=None)
        df.columns = column_names
        return df
    
    """
    Creates a DataFrame that contains the weather recording between Feb 2019 and Feb 2020
    """
    def create_2019_2020_df(self):
        df = self.__create_last_n_rows_df(2000000)
        one_year_row = df.loc[df["date"] == 20190208].index.values[0]
        one_year_df = df.loc[one_year_row:]
        return one_year_df
    
    """
    Private method that extracts only the precipation recordings from the weather stations
    """
    def __extract_precip_data(self, weather_df):
        precip_df = weather_df[weather_df["reading_type"] == "PRCP"]
        return precip_df
    
    """
    Initial exploration method for a single station
    """
    def single_station_explore(self, weather_df, station_id):
        p_df = self.__extract_precip_data(weather_df)
        single = p_df[p_df["station_id"] == station_id]
        single["date"] = pd.to_datetime(single["date"], format='%Y%m%d')
        return single
    
if __name__ == "__main__":
    comparer = WeatherVSPotholes()
    df = comparer.create_2019_2020_df()
    df2 = comparer.single_station_explore(df, "US1TXBEL016")