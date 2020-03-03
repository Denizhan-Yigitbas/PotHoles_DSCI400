
import pandas as pd
import os
from datetime import datetime
import calendar


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

    def all_weather_in_range(self, year1, year2, df=None):

        if df is None:
            df = self.weather_df

        return df.loc[
            (df.date >= datetime(day=1, month=1, year=year1)) &
            (df.date < datetime(day=1, month=1, year=year2 + 1))
        ]

    def station_df(self, stat_id):
        stat_df = self.weather_df.loc[self.weather_df.reading_type.isin(['TMAX', 'TMIN','PRCP'])]
        return stat_df.loc[stat_df.station_id == stat_id]

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

    def avg_daily_temp_df(self):
        temp_df = self.temp_df
        return temp_df.groupby(['station_id', 'date']).value.agg('mean')
        
    def avg_station_precipitation_per_month(self, year1, year2, station_id):
        # get all the precipiation data
        prcp_df = self.all_weather_in_range(year1, year2, df=self.precipitation_df)
        
        # change the index
        prcp_df.set_index("date", inplace=True)
        
        # filter out only precipitation data for the specific station
        prcp_df = prcp_df[prcp_df["station_id"] == station_id]
        
        # group by average percipitation per month
        prcp_df = prcp_df.resample('M').mean()
        
        # structure the df for export
        prcp_df["date"] = list(prcp_df.index)
        prcp_df["month-year"] = prcp_df["date"] \
            .apply(lambda x: x.strftime('%b %Y'))
        prcp_df.set_index('month-year', inplace=True)
        
        return prcp_df["value"]

    def avg_station_temp_per_month(self, year1, year2, station_id):
        # get all the precipiation data
        avg_temp_df = self.avg_daily_temp_df()
        avg_temp_df= avg_temp_df.to_frame()
        avg_temp_df = avg_temp_df.reset_index()
        avg_temp_df = self.all_weather_in_range(year1, year2, df=avg_temp_df)
        
        #
        # # change the index
        avg_temp_df.set_index("date", inplace=True)

        # filter out only precipitation data for the specific station
        avg_temp_df = avg_temp_df[avg_temp_df["station_id"] == station_id]
        
        # # group by average percipitation per month
        avg_temp_df = avg_temp_df.resample('M').mean()

        # # structure the df for export
        avg_temp_df["date"] = list(avg_temp_df.index)
        avg_temp_df["month-year"] = avg_temp_df["date"] \
            .apply(lambda x: x.strftime('%b %Y'))
        avg_temp_df.set_index('month-year', inplace=True)
        
        return avg_temp_df["value"]
    
if __name__ == "__main__":
    x = WeatherData().avg_station_temp_per_month(2015, 2019, "USW00012918")
    