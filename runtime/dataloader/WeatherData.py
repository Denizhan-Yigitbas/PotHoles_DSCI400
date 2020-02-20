
import pandas as pd
import os
from datetime import datetime


class WeatherData(object):
    """
    Container class for loading weather data.
    """

    # This operation ensures the path to the data is correct,
    # regardless of what directory it is called from.
    root_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(
        root_path,
        '../../data/output/'
    )

    def __init__(self):
        """
        Loads weather dataframe and merge in the station data for each reading.
        """
        self.stations_df = pd.read_csv(WeatherData.data_path + 'all_tx_stations.csv')
        self.weather_df = pd.read_csv(WeatherData.data_path + 'houston_weather.csv')\
            .merge(self.stations_df, on='station_id', how='inner')

        # Convert date to datetime type
        # TODO: add time to date column
        self.weather_df.date = pd.to_datetime(self.weather_df.date, format="%Y%m%d")

    def weather_joined_to_csv(self):
        self.weather_df.to_csv(
            os.path.join(WeatherData.root_path, "../../data/output/houston_weather_joined.csv"),
            index=False
        )

    def all_weather_in_range(self, year1, year2):

        return self.weather_df.loc[
            (self.weather_df.date >= datetime(day=1, month=1, year=year1)) &
            (self.weather_df.date < datetime(day=1, month=1, year=year2 + 1))
        ]

    @property
    def temp_df(self):
        """
        Generate a dataframe containing only the temperature readings.
        """
        return self.weather_df.loc[
            self.weather_df.reading_type.isin(['TMAX', 'TMIN'])
        ]

    @property
    def precipitation_df(self):
        """
        Generate a dataframe containing only the precipitation readings.
        """
        return self.weather_df.loc[
            self.weather_df.reading_type == 'PRCP'
        ]

    


if __name__ == "__main__":
    WeatherData()