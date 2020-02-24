
from collections import deque
import math
from shapely.geometry import Point, Polygon
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import calendar
import pandas as pd
import numpy as np

from dataloader import WeatherData, PotholeData

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class WeatherVSPotholes():
    def __init__(self):
        self.weatherDat = WeatherData()
        self.potholeDat = PotholeData()

    # TODO: remove inputes by replaceing with variables form init?
    def precip_vs_potholes_near_station(self, year1, year2, station_id, radius):
        # create the desired DataFrames
        weather_df = weatherDat.all_weather_in_range(year1, year2)
        potholes_df = potholeDat.all_potholes_in_year_list(range(year1, year2+1, 1))
        
        # locate the input station coordinates
        station = weather_df[weather_df["station_id"] == station_id]
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
        
        # combine lat and lng to create Point objects
        potholes_df["coord"] = list(zip(potholes_df.LATITUDE, potholes_df.LONGITUDE))
        potholes_df["coord"] =  potholes_df["coord"].apply(lambda x: Point(x))
        
        # keep only potholes that are contained within the created Polygon
        potholes_df["contains"] = potholes_df["coord"].apply(lambda x: poly.contains(x))
        potholes_df = potholes_df[potholes_df.contains]

        # group the dates by month and year and count the total number of occurences
        counts_series = potholes_df["SR CREATE DATE"] \
            .groupby([(potholes_df["SR CREATE DATE"].dt.year),(potholes_df["SR CREATE DATE"].dt.month) ]) \
            .count()

        counts_df = counts_series.to_frame()
        counts_df["month-year"] = list(counts_df.index)
        counts_df["month-year"] = counts_df["month-year"]\
            .apply(lambda x: datetime.strptime(str(calendar.month_abbr[x[1]]) + " " + str(x[0]), '%b %Y'))
        counts_df["month-year"] = counts_df["month-year"] \
            .apply(lambda x: x.strftime('%b %Y'))
        counts_df.set_index("month-year", inplace=True)
        
        # visualize the data
        fig, ax = plt.subplots()
        x = counts_df.index
        y = counts_df["SR CREATE DATE"]
        ax.bar(x, y, width=0.7, label="Potholes")
        ax.set_title("Pothole formation around station " + station_id)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b %Y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        ax.tick_params(axis='x', rotation=45)
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Pothole")
        ax.legend(loc="upper left")
    
        ax2 = ax.twinx()
        station_precip = WeatherData().avg_station_precipitation_per_month(2015, 2019, station_id)
        x = station_precip.index
        y = station_precip
        ax2.plot(x, y, color='r', linewidth=3, label="Precipitation")
        ax2.set_ylabel("Precipitation (tenths of mm)")
        ax2.legend(loc=0)
        # ax2.set_title("Precipitation recorded for station " + station_id)
        plt.subplots_adjust(bottom=.2, left=0.11, right= 0.87)
        plt.show()

    def temp_vs_potholes_near_station(self, year1, year2, station_id, radius):
        # create the desired DataFrames
        weather_df = weatherDat.all_weather_in_range(year1, year2)
        potholes_df = potholeDat.all_potholes_in_year_list(range(year1, year2 + 1, 1))
    
        # locate the input station coordinates
        station = weather_df[weather_df["station_id"] == station_id]
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
    
        # combine lat and lng to create Point objects
        potholes_df["coord"] = list(zip(potholes_df.LATITUDE, potholes_df.LONGITUDE))
        potholes_df["coord"] = potholes_df["coord"].apply(lambda x: Point(x))
    
        # keep only potholes that are contained within the created Polygon
        potholes_df["contains"] = potholes_df["coord"].apply(lambda x: poly.contains(x))
        potholes_df = potholes_df[potholes_df.contains]
    
        # group the dates by month and year and count the total number of occurences
        counts_series = potholes_df["SR CREATE DATE"] \
            .groupby([(potholes_df["SR CREATE DATE"].dt.year), (potholes_df["SR CREATE DATE"].dt.month)]) \
            .count()
    
        counts_df = counts_series.to_frame()
        counts_df["month-year"] = list(counts_df.index)
        counts_df["month-year"] = counts_df["month-year"] \
            .apply(lambda x: datetime.strptime(str(calendar.month_abbr[x[1]]) + " " + str(x[0]), '%b %Y'))
        counts_df["month-year"] = counts_df["month-year"] \
            .apply(lambda x: x.strftime('%b %Y'))
        counts_df.set_index("month-year", inplace=True)
    
        # visualize the data
        fig, ax = plt.subplots()
        x = counts_df.index
        y = counts_df["SR CREATE DATE"]
        ax.bar(x, y, width=0.7, label="Potholes")
        ax.set_title("Pothole formation around station " + station_id)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b %Y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        ax.tick_params(axis='x', rotation=45)
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Pothole")
        ax.legend(loc="upper right")
    
        ax2 = ax.twinx()
        station_temp = WeatherData().avg_station_temp_per_month(2015, 2019, station_id)
        x = station_temp.index
        y = station_temp
        ax2.plot(x, y, color='r', linewidth=3, label="Temperature")
        ax2.legend(loc=0)
        ax2.set_ylabel("Temperature (tenths of degree Celcius)")
        # ax2.set_title("Precipitation recorded for station " + station_id)
        plt.subplots_adjust(bottom=.2, left=0.11, right=0.87)
        plt.show()

    def temp_precip_potholes(self, year1, year2, station_id, radius):
        # create the desired DataFrames
        weather_df = weatherDat.all_weather_in_range(year1, year2)
        potholes_df = potholeDat.all_potholes_in_year_list(range(year1, year2 + 1, 1))
    
        # locate the input station coordinates
        station = weather_df[weather_df["station_id"] == station_id]
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
    
        # combine lat and lng to create Point objects
        potholes_df["coord"] = list(zip(potholes_df.LATITUDE, potholes_df.LONGITUDE))
        potholes_df["coord"] = potholes_df["coord"].apply(lambda x: Point(x))
    
        # keep only potholes that are contained within the created Polygon
        potholes_df["contains"] = potholes_df["coord"].apply(lambda x: poly.contains(x))
        potholes_df = potholes_df[potholes_df.contains]
    
        # group the dates by month and year and count the total number of occurences
        counts_series = potholes_df["SR CREATE DATE"] \
            .groupby([(potholes_df["SR CREATE DATE"].dt.year), (potholes_df["SR CREATE DATE"].dt.month)]) \
            .count()
    
        counts_df = counts_series.to_frame()
        counts_df["month-year"] = list(counts_df.index)
        counts_df["month-year"] = counts_df["month-year"] \
            .apply(lambda x: datetime.strptime(str(calendar.month_abbr[x[1]]) + " " + str(x[0]), '%b %Y'))
        counts_df["month-year"] = counts_df["month-year"] \
            .apply(lambda x: x.strftime('%b %Y'))
        counts_df.set_index("month-year", inplace=True)
    
        # visualize the data
        fig, ax = plt.subplots()
        x = counts_df.index
        y = counts_df["SR CREATE DATE"]
        ax.bar(x, y, width=0.7, label="Potholes")
        ax.set_title("Pothole formation around station " + station_id)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b %Y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        ax.tick_params(axis='x', rotation=45)
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Pothole")
        ax.legend(loc=0)
    
        ax2 = ax.twinx()
        station_precip = WeatherData().avg_station_precipitation_per_month(2015, 2019, station_id)
        x = station_precip.index
        y = station_precip
        ax2.plot(x, y, color='r', linewidth=3, label="Precipitation")
        ax2.set_ylabel("Precipitation (tenths of mm)")
        # ax2.legend(loc=0)
        # ax2.set_title("Precipitation recorded for station " + station_id)
        
        station_temp = WeatherData().avg_station_temp_per_month(2015, 2019, station_id)
        x = station_temp.index
        y = station_temp
        ax2.plot(x, y, color='g', linewidth=3, label="Temperature")
        ax2.legend(loc = 1)
        ax2.set_ylabel("Temperature (tenths of degree Celcius)")
        # ax2.set_title("Precipitation recorded for station " + station_id)
        
        
        plt.subplots_adjust(bottom=.2, left=0.11, right=0.87)
        plt.show()
        
    
if __name__ == "__main__":
    
    weatherDat = WeatherData()
    potholeDat = PotholeData()
    
    comparer = WeatherVSPotholes()

    
    # comparer.precip_vs_potholes_near_station(2015, 2019, "USW00012918", 0.05)
    # comparer.temp_vs_potholes_near_station(2015, 2019, "USW00012918", 0.05)
    comparer.temp_precip_potholes(2015, 2019, "USW00012918", 0.05)