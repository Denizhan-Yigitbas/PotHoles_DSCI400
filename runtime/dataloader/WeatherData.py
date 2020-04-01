
import pandas as pd
import os


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
            .merge(self.stations_df, on='station_id', how='inner')\
            .fillna({'time': 0})

        # Convert date to datetime type
        self.weather_df.loc[self.weather_df.time == 2400, 'time'] = 2359
        self.weather_df['date'] = pd.to_datetime(
            self.weather_df.date.astype(str) + ' ' + self.weather_df.time.map(lambda x: f"{int(x):04d}"),
            format="%Y%m%d %H%M"
        )
        self.weather_df = self.weather_df.drop(columns='time')

        self.weather_df.value = pd.to_numeric(self.weather_df.value)

    def weather_joined_to_csv(self):
        """
        Export the weather dataframe to the data/output directory with name houston_weather_joined.csv
        :return:
        """
        self.weather_df.to_csv(
            os.path.join(WeatherData.root_path, "../../data/output/houston_weather_joined.csv"),
            index=False
        )

    def all_weather_in_range(self, year1, year2, df=None):
        """
        Extracts data between 2 years
        :param year1: start year
        :param year2: end year
        :param df: if a df is given, that specific dataframe will be filtered
        :return:
        """
        if df is None:
            df = self.weather_df

        return df.loc[(year1 <= df.date.dt.year) & (df.date.dt.year <= year2)]

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
        """
        Calculate the average daily temperature
        :return:
        """
        temp_df = self.temp_df
        return temp_df.groupby(['station_id', 'date']).value.agg('mean')
        
    def avg_station_precipitation_per_month(self, year1, year2, station_id):
        """
        Average precipitation per month recorded at a specific weather station between 2 years
        :param year1: start year
        :param year2: end year
        :param station_id: weather station id
        :return: Pandas Series indexed on month-year
        """
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
        """
        Average temperature per month recorded at a specific weather station between 2 years
        :param year1: start year
        :param year2: end year
        :param station_id: weather station id
        :return: Pandas Series indexed on month-year
        """
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
    