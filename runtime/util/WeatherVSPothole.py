from collections import deque

import math
from shapely.geometry import Point, Polygon
from datetime import datetime

import matplotlib.pyplot as plt

import pandas as pd
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

weather_data = "../../data/output/all_tx_weather.csv"

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
        column_names = ['station_id', 'date', 'reading_type', 'value', 'm_flag', 'q_flag', 's_flag', 'time']
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
        # extract the station's latitude and longitude
        stations_df = self.create_tx_stations_df(stations_data)
        station = stations_df[stations_df["station_id"] == station_id]
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
        
        print(poly.contains(bot_right))
        # print(poly)
        # poly.contains(coords[0])
        #
        # # clean the potholes lat/lng data
        # pothole_locations = potholes_df[["SR CREATE DATE", "LATITUDE", "LONGITUDE"]].dropna()
        # pothole_locations = pothole_locations[~pothole_locations.LATITUDE.str.contains("Unknown")]
        # pothole_locations["LATITUDE"] = pothole_locations["LATITUDE"].apply(lambda x: float(x))
        #
        # pothole_locations = pothole_locations[~pothole_locations.LONGITUDE.str.contains("Unknown")]
        # pothole_locations["LONGITUDE"] = pothole_locations["LONGITUDE"].apply(lambda x: float(x))
        #
        # # combine lat and lng to create Point objects
        # pothole_locations["coord"] = list(zip(pothole_locations.LATITUDE, pothole_locations.LONGITUDE))
        # pothole_locations["coord"] =  pothole_locations["coord"].apply(lambda x: Point(x))
        #
        # # keep only potholes that are contained within the created Polygon
        # pothole_locations["contains"] = pothole_locations["coord"].apply(lambda x: poly.contains(x))
        # pothole_locations = pothole_locations[pothole_locations.contains]
        #
        # # convert string dates to datetime
        # pothole_locations["SR CREATE DATE"] = pothole_locations["SR CREATE DATE"]\
        #     .apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        #
        # # group the dates by month and year and count the total number of occurences
        # counts_series = pothole_locations["SR CREATE DATE"] \
        #     .groupby([(pothole_locations["SR CREATE DATE"].dt.year),(pothole_locations["SR CREATE DATE"].dt.month) ]) \
        #     .count()
        #
        # counts_df = counts_series.to_frame()
        # counts_df["month-year"] = list(counts_df.index)
        # counts_df["month-year"] = counts_df["month-year"].apply(lambda x: str(calendar.month_abbr[x[1]]) + " " + str(x[0]))
        # counts_df.set_index("month-year", inplace=True)
        #
        # counts_df.plot(kind="bar", legend=False)
        #
        # plt.title("Pothole formation around station " + station_id)
        # plt.xlabel("Time")
        # plt.ylabel("Number of Pothole")
        # plt.subplots_adjust(bottom=.2)
        # plt.show()
        #
        # lst = weather_df["station_id"].unique()
        #
        # stations_df = stations_df[stations_df["station_id"].isin(lst)]
        # stations_df["latlng"] = list(zip(stations_df.lat, stations_df.lon))
        # stations_df["distance"] = stations_df["latlng"]\
        #     .apply(lambda x: self.distance(x[0], x[1], 29.7604, 95.3698))
        # print(stations_df[stations_df.distance == min(stations_df.distance)])





        # print(len(weather_df["station_id"].unique()))
        # station_weather = weather_df[weather_df["station_id"]==station_id]
        # print(station_weather)
        # d = counts_series.to_dict()
        # print(pd.DataFrame(d))
        # copy = pd.DataFrame(data=counts_series.to_dict(), columns=["year", "month", "count"])
        

        # counts_series.to_csv("../../data/output/test.csv")
        #
        # print(counts_series)

        # print(pothole_locations["SR CREATE DATE"].iloc[0])
        # g = pothole_locations["SR CREATE DATE"].groupby(pd.Grouper(freq="M"))
        # print(g)

        # # extract latitudes data - clean Nan and Unknown entries - convert to floats
        # potholes_df["LATITUDE"] = potholes_df["LATITUDE"].dropna()
        # # potholes_df = potholes_df.dropna()
        # print(potholes_df["LATITUDE"][potholes_df["LATITUDE"].str.contains("Unknown")])
        # # latitudes = latitudes[~latitudes.str.contains("Unknown")]
        # potholes_df["LATITUDE"] = potholes_df["LATITUDE"].apply(lambda x: float(x))
        # print(potholes_df["LATITUDE"])
        #
        # # extract longitude data - clean Nan and Unknown entries - convert to floats
        # longitudes = potholes_df["LONGITUDE"].dropna()
        # longitudes = longitudes[~longitudes.str.contains("Unknown")]
        # longitudes = longitudes.apply(lambda x: float(x))
        #
        # potholes_df["coord"] = list(zip(potholes_df.LATITUDE, potholes_df.LONGITUDE))
        # potholes_df["coord"] = potholes_df["coord"].apply(lambda x: Point(x))
        # print(potholes_df["coord"])
        #

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
    
    weather_data = "../../data/output/all_tx_weather.csv"
    stations_data = "../../data/output/all_tx_stations.csv"
    
    
    comparer = WeatherVSPotholes()
    # weather_df = comparer.create_2019_2020_df()
    # df2 = comparer.single_station_explore(df, "US1TXBEL016")

    potholes_csv = {
        2019: "../../data/output/potholePiped2019.csv",
        2018: "../../data/output/potholePiped2018.csv",
        2017: "../../data/output/potholePiped2017.csv",
        2222: "../../data/output/potholePiped2015-2019.csv"
    }
    
    potholes_df = pd.read_csv(potholes_csv[2222])

    weather_df = comparer.create_2015_2019_df()
    comparer.potholes_near_station(potholes_df, weather_df, "USC00414310", 0.05)