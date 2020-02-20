
from collections import deque
import math
from shapely.geometry import Point, Polygon
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import calendar
import pandas as pd
import numpy as np

from dataloader import WeatherData

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class WeatherVSPotholes():
    def __init__(self):
        pass

    @staticmethod
    def __create_last_n_rows_df(n):
        """
        Private method that extracts the last n rows of the all_tx_weather.csv file in order to access the
         most recent recordings
        """
        with open(weather_data, 'r') as f:
            q = deque(f, n)  # replace 2 with n (lines read at the end)
        column_names = ['station_id', 'date', 'reading_type', 'value', 'm_flag', 'q_flag', 's_flag', 'time',
                        'lat', 'lon', 'elev', 'state', 'name', 'gsn_flag', 'hcn/crn_flag', 'wmo_id']
        df = pd.read_csv(StringIO(''.join(q)), header=None)
        df.columns = column_names
        return df

    def create_2019_2020_df(self):
        """
        Creates a DataFrame that contains the weather recording between Feb 2019 and Feb 2020
        """
        df = self.__create_last_n_rows_df(2000000)
        one_year_row = df.loc[df["date"] == 20190208].index.values[0]
        one_year_df = df.loc[one_year_row:]
        return one_year_df

    def create_2015_2019_df(self):
        df = self.__create_last_n_rows_df(10000000)
        row_2015 = df.loc[df["date"] == 20150101].index.values[0]
        row_2019 = df.loc[df["date"] == 20191231].index.values[0]
        final_df = df.loc[row_2015:row_2019]
        return final_df

    @staticmethod
    def __extract_precip_data(weather_df):
        """
        Private method that extracts only the precipation recordings from the weather stations
        """
        precip_df = weather_df[weather_df["reading_type"] == "PRCP"]
        return precip_df


    # TODO: are these static
    def __extract_max_temp_data(self, weather_df):
        """
        Private method that extracts only the precipation recordings from the weather stations
        """
        tmax_df = weather_df[weather_df["reading_type"] == "TMAX"]
        return tmax_df
    
    
    # TODO: are these static
    def __extract_min_temp_data(self, weather_df):
        """
        Private method that extracts only the precipation recordings from the weather stations
        """
        tmax_df = weather_df[weather_df["reading_type"] == "TMIN"]
        return tmax_df
    
    
    def single_station_explore(self, weather_df, station_id):
        """
        Initial exploration method for a single station
        """
        p_df = self.__extract_precip_data(weather_df)
        single = p_df[p_df["station_id"] == station_id]
        single["date"] = pd.to_datetime(single["date"], format='%Y%m%d')
        return single

    def create_tx_stations_df(self, filepath):
        df = pd.read_csv(filepath)
        return df

    def potholes_near_station(self, potholes_df, weather_df, station_id, radius):
        station = weather_df[weather_df["station_id"] == station_id]
        print(station)
        station_lat = station["lat"].values[0]
        station_lng = station["lon"].values[0]
        

        # get coordinates that create a square centered about the station's coordinates
        bot_left = (station_lat - radius, station_lng - radius)
        bot_right = (station_lat - radius, station_lng + radius)
        top_left = (station_lat + radius, station_lng - radius)
        top_right = (station_lat + radius, station_lng + radius)
    
        # create a square polygon
        coords = [bot_left, bot_right, top_right, top_left]
        poly = Polygon(coords)
        
        # clean the potholes lat/lng data
        pothole_locations = potholes_df[["SR CREATE DATE", "LATITUDE", "LONGITUDE"]].dropna()
        pothole_locations = pothole_locations[~pothole_locations.LATITUDE.str.contains("Unknown")]
        pothole_locations["LATITUDE"] = pothole_locations["LATITUDE"].apply(lambda x: float(x))

        pothole_locations = pothole_locations[~pothole_locations.LONGITUDE.str.contains("Unknown")]
        pothole_locations["LONGITUDE"] = pothole_locations["LONGITUDE"].apply(lambda x: float(x))

        # combine lat and lng to create Point objects
        pothole_locations["coord"] = list(zip(pothole_locations.LATITUDE, pothole_locations.LONGITUDE))
        pothole_locations["coord"] =  pothole_locations["coord"].apply(lambda x: Point(x))

        # keep only potholes that are contained within the created Polygon
        pothole_locations["contains"] = pothole_locations["coord"].apply(lambda x: poly.contains(x))
        pothole_locations = pothole_locations[pothole_locations.contains]

        # convert string dates to datetime
        pothole_locations["SR CREATE DATE"] = pothole_locations["SR CREATE DATE"]\
            .apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

        # group the dates by month and year and count the total number of occurences
        counts_series = pothole_locations["SR CREATE DATE"] \
            .groupby([(pothole_locations["SR CREATE DATE"].dt.year),(pothole_locations["SR CREATE DATE"].dt.month) ]) \
            .count()

        counts_df = counts_series.to_frame()
        counts_df["month-year"] = list(counts_df.index)
        counts_df["month-year"] = counts_df["month-year"]\
            .apply(lambda x: datetime.strptime(str(calendar.month_abbr[x[1]]) + " " + str(x[0]), '%b %Y'))
        counts_df.set_index("month-year", inplace=True)

        # counts_df.plot(kind="bar", legend=False)
 

        # plt.plot_date(x,y,'b-')
        # plt.title("Pothole formation around station " + station_id)
        # plt.xlabel("Time")
        fig, ax = plt.subplots()
        x = counts_df.index
        y = counts_df["SR CREATE DATE"]
        b1 = ax.bar(x, y, width=15, label="Potholes")
        ax.set_title("Pothole formation around station " + station_id)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b %Y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
        ax.tick_params(axis='x', rotation=45)
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Pothole")
        ax.legend(loc=0)
        # plt.ylabel("Number of Pothole")
    
        
        
        # fig, ax = plt.subplots()
        ax2 = ax.twinx()
        station_precip = self.__extract_precip_data(weather_df)
        station_precip["date"] = pd.to_datetime(station_precip["date"], format='%Y%m%d')
        x = station_precip.date
        y = station_precip.value
        ax2.bar(x, y, width=15, color='g', label="Precipitation")
        ax2.set_ylabel("Precipitation (tenths of mm)")
        ax2.legend(loc=0)
        # ax2.set_title("Precipitation recorded for station " + station_id)

        plt.subplots_adjust(bottom=.2)
        plt.show()

    def distance(slef, origin, destination):
        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = 6371  # km
    
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c
    
        return d
    

if __name__ == "__main__":
    
    weather_data = "../../data/output/houston_weather_joined.csv"
    
    comparer = WeatherVSPotholes()

    potholes_csv = {
        2019: "../../data/output/potholePiped2019.csv",
        2018: "../../data/output/potholePiped2018.csv",
        2017: "../../data/output/potholePiped2017.csv",
        2222: "../../data/output/potholePiped2015-2019.csv"
    }

    potholes_df = pd.read_csv(potholes_csv[2222])

    weather_df = comparer.create_2015_2019_df()
    
    comparer.potholes_near_station(potholes_df, weather_df, "USW00012918", 0.05)