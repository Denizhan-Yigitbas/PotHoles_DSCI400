
import pandas as pd



class WeatherData(object):
    """
    Container class for loading weather data.
    """

    data_path = './data/raw/'


    def __init__(self):
        """
        Loads weather dataframe and merge in the station data for each reading.
        """
        stations_df = pd.read_csv(WeatherData.data_path + 'all_tx_stations.csv')
        self.df = pd.read_csv(WeatherData.data_path + 'houston_weather.csv')\
            .merge(stations_df, on='station_id', how='inner')

        # TODO: process data fields into proper types

