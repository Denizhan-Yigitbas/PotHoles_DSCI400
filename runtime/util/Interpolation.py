import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from scipy.spatial import Delaunay

from dataloader import WeatherData

class Interpolator():
    def __init__(self):
        self.weather = WeatherData()
        self.weather_df = self.weather.all_weather_in_range(2010, 2019)
        self.stations = pd.read_csv("../data/output/all_houston_stations.csv", dtype = str)

        #relevant columns
        self.stations = self.stations[['station_id', 'lat', 'lon']]

        #convert coordinate columns to numeric value

        self.stations['lat'] = pd.to_numeric(self.stations['lat'])
        self.stations['lon'] = pd.to_numeric(self.stations['lon'])


    def interpolate_point(self, lat, lon, date):
        """
        Interpolates a given coordinate and date
        :param lat: latitude
        :param lon: longitiude
        :param date: date
        :return: np.array
        """
        date = pd.to_datetime(date, format = "%Y%m%d")
        coord = np.array([(lat, lon)])
        delta = timedelta(days = 365)
        entries = np.zeros((365, 3))
        weather = self.weather_df.loc[(self.weather_df.date < date) & (self.weather_df.date >= date - delta)]
        freeze_flag = False
        freeze_counter = 0
        freeze_days = 0      #freezing days in the previous three weeks 
        prcp_freeze = 0      #freezing days less than 5 days after heavy rainfall
        variation = 0        #days with 13 degree C temperature variation
        tmax_c = 0           #sum tmax
        tmin_c = 0           #sum tmin
        for i, day in enumerate(range(365, 0, -1)):
            delta = timedelta(days = day)
            weather_on_day = weather.loc[weather.date == (date - delta)]
            tmin_on_day = weather_on_day.loc[weather_on_day.reading_type == 'TMIN']
            tmax_on_day = weather_on_day.loc[weather_on_day.reading_type == 'TMAX']
            prcp_on_day = weather_on_day.loc[weather_on_day.reading_type == 'PRCP']

            tmin = float(tmin_on_day.loc[tmin_on_day.station_id == self.__nearest_stat(tmin_on_day.station_id.unique())]['value'])
            tmax = float(tmax_on_day.loc[tmax_on_day.station_id == self.__nearest_stat(tmax_on_day.station_id.unique())]['value'])

            tmax_c += tmax
            tmin_c += tmin

            tri_stats, b_coords = self.__triangulate(prcp_on_day.station_id.unique(), coord)
            #print(len(prcp_on_day.index))
            #print(tri_stats, b_coords)
            #print(prcp_on_day.loc[(weather_on_day.station_id == tri_stats[0]) & (weather_on_day.reading_type == 'PRCP')]['value'] * b_coords[0])
            #print(prcp_on_day.loc[(weather_on_day.station_id == tri_stats[1]) & (weather_on_day.reading_type == 'PRCP')]['value'] * b_coords[1])
            #print(prcp_on_day.loc[(weather_on_day.station_id == tri_stats[2]) & (weather_on_day.reading_type == 'PRCP')]['value'] * b_coords[2])

            prcp_val =  (float(prcp_on_day.loc[(weather_on_day.station_id == tri_stats[0]) & (weather_on_day.reading_type == 'PRCP')]['value']) * b_coords[0]) + (float(prcp_on_day.loc[(weather_on_day.station_id == tri_stats[1]) & (weather_on_day.reading_type == 'PRCP')]['value']) * b_coords[1]) + (float(prcp_on_day.loc[(weather_on_day.station_id == tri_stats[2]) & (weather_on_day.reading_type == 'PRCP')]['value']) * b_coords[2])
            print(prcp_val)

            #days with high variation
            if tmax - tmin > 130.0:
                variation += 1
            #freeze tracking
            if tmin < 0.0:
                if day < 22:
                    freeze_days += 1
                if freeze_flag:
                    prcp_freeze += 1
            if prcp_val > 300:
                freeze_flag = True
                freeze_counter = 5
            if freeze_counter < 0:
                freeze_flag = False
            freeze_counter -= 1

        return np.array([tmax_c / i, tmin_c / i, freeze_days, prcp_freeze, variation, lat, lon, date.month])

    def __nearest_stat(self, ava_stats):
        ava_stations = self.stations.loc[self.stations.station_id.isin(ava_stats)]
    
        stats_ = ava_stations[['station_id', 'lat','lon']].to_numpy()
        stat_ids = stats_[:,0]
        stats_ = stats_[:,1:]
        pairs = []
        for i in range(stats_.shape[1]):
            dist = (stats_[i][0] ** 2 + stats_[i][1] ** 2) ** .5
            pairs.append((i, dist))
        pairs.sort(key = lambda x: x[1])

        return stat_ids[pairs[0][0]]

    def __triangulate(self, ava_stats, coord):
        """
        Private method to triangulate the data
        :param ava_stats: ava statistics
        :param coord: location coordinate
        :return:
        """
        ava_stations = self.stations.loc[self.stations.station_id.isin(ava_stats)]

        points = ava_stations[['station_id', 'lat', 'lon']].to_numpy()
        station_ids = points[:,0]
        points = points[:,1:].astype(float)
        samples = coord

        dim    = len(points[0])               # determine the dimension of the samples
        simp   = Delaunay(points)             # create simplexes for the defined points
        s      = simp.find_simplex(samples)   # for each sample, find corresponding simplex for each sample
        b0      = np.zeros((len(samples),dim)) # reserve space for each barycentric coordinate
        for ii in range(len(samples)):
            b0[ii,:] = simp.transform[s[ii],:dim].dot((samples[ii] - simp.transform[s[ii],dim]).transpose())
        bary_coords = np.c_[b0, 1 - b0.sum(axis=1)]

        #print(station_ids[simp.simplices])
        #print(points[simp.simplices][s[0]])
        return station_ids[simp.simplices][s[0]], bary_coords[0]