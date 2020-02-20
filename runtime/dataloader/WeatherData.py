
import pandas as pd



class WeatherData(object):
    """
    Container class for loading weather data.
    """

    data_path = './data/output/'


    def __init__(self):
        """
        Loads weather dataframe and merge in the station data for each reading.
        """
        self.stations_df = pd.read_csv('../.' + WeatherData.data_path + 'all_tx_stations.csv')
        self.weather_df = pd.read_csv('../.' + WeatherData.data_path + 'houston_weather.csv')\
            .merge(self.stations_df, on='station_id', how='inner')

        self.weather_df.to_csv("../../data/output/houston_weather.csv", index=False)
        # TODO: process data fields into proper types


if __name__ == "__main__":
    WeatherData()