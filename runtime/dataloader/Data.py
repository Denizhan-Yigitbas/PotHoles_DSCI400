
import pandas as pd
import scipy.interpolate as interp


from .WeatherData import WeatherData
from .PotholeData import PotholeData
from .FloodingData import FloodingData



class Data(object):
    
    timestamp_scalar = 3600 * 24

    def __init__(self):

        self.weather = WeatherData()
        self.pothole = PotholeData()
        # self.flooding = FloodingData()

        self.weather.weather_df['timestamp'] = \
            (self.weather.weather_df.date - pd.Timestamp('1970-01-01')) / pd.Timedelta('1s')
        self.pothole.pothole_df['timestamp'] = \
            (self.pothole.pothole_df['SR CREATE DATE'] - pd.Timestamp('1970-01-01')) / pd.Timedelta('1s')


        min_year = self.pothole.pothole_df['SR CREATE DATE'].dt.year.min()

        prcp = self.weather.precipitation_df.loc[self.weather.precipitation_df.date.dt.year >= min_year]
        temp = self.weather.temp_df.loc[self.weather.temp_df.date.dt.year >= min_year]
        tmin = temp.loc[temp.reading_type == 'TMIN']
        tmax = temp.loc[temp.reading_type == 'TMAX']

        self.precipitation_interpolator = interp.LinearNDInterpolator(
            (prcp.lat.values, prcp.lon.values, prcp.timestamp.values / self.timestamp_scalar),
            prcp.value.values
        )

        self.tmin_interpolator = interp.LinearNDInterpolator(
            (tmin.lat.values, tmin.lon.values, tmin.timestamp.values / self.timestamp_scalar),
            tmin.value.values
        )
        self.tmax_interpolator = interp.LinearNDInterpolator(
            (tmax.lat.values, tmax.lon.values, tmax.timestamp.values / self.timestamp_scalar),
            tmax.value.values
        )


        self.data = self.pothole.pothole_df
        self.data['prcp'] = self.precipitation_interpolator(
            self.data.LATITUDE, self.data.LONGITUDE, self.data.timestamp / self.timestamp_scalar
        )
        self.data['tmin'] = self.tmin_interpolator(
            self.data.LATITUDE, self.data.LONGITUDE, self.data.timestamp / self.timestamp_scalar
        )
        self.data['tmax'] = self.tmax_interpolator(
            self.data.LATITUDE, self.data.LONGITUDE, self.data.timestamp / self.timestamp_scalar
        )