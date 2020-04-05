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

    #def __check_freeze():
    def __triangulate(self, ava_stats, coord):
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

    '''
    """
    Private method to find the three nearest stations for each pothole request, and
    calculate the three interpolation weights
    """
    def __interpolate_points(self):
        for per, lat in enumerate(np.linspace(self.lat[0], self.lat[1], 100)):
            print(str(per) + f'% done')
            for lon in np.linspace(self.lon[0], self.lon[1], 100):
                tstations = []
                pstations = []
                for ind, r in self.tstats.iterrows():
                    dist = ( (float(r['lat']) - lat) ** 2 + (float(r['lon']) - lon) ** 2 ) ** .5
                    tstations.append( (self.ts_encode[self.tstats.at[ind, 'station_id']] , dist) )
                tstations.sort(key = lambda x: x[1])
                tstations = tstations[:3]
                for ind, r in self.pstats.iterrows():
                    dist = ( (float(r['lat']) - lat) ** 2 + (float(r['lon']) - lon) ** 2 ) ** .5
                    pstations.append( (self.ps_encode[self.pstats.at[ind, 'station_id']] , dist) )
                pstations.sort(key = lambda x: x[1])
                pstations = pstations[:3]

                tot = sum(i[1] for i in tstations)
                tot2 = sum(i[1] for i in pstations)
                
                lat_i, lon_i = self.__get_indicies(lat, lon)
            
                self.grid[lat_i][lon_i] = np.array([tstations[0][0], tstations[1][0], tstations[2][0], 
                                                    tstations[2][1] / tot, tstations[1][1] / tot, tstations[0][1] / tot,
                                                    pstations[0][0], pstations[1][0], pstations[2][0],
                                                    pstations[2][1] / tot2, pstations[1][1] / tot2, pstations[0][1] / tot2,
                                                    ])
        

    def __build_grid(self, pot_df):
        #drop the invalid rows
        pot_df = pot_df[pot_df['LATITUDE'].notna()]
        pot_df = pot_df.loc[pot_df['LATITUDE'] != 'Unknown']

        #convert the numeric columns
        pot_df['LATITUDE'] = pd.to_numeric(pot_df['LATITUDE'])
        pot_df['LONGITUDE'] = pd.to_numeric(pot_df['LONGITUDE'])

        self.lat = [pot_df['LATITUDE'].min(), pot_df['LATITUDE'].max(), pot_df['LATITUDE'].max() - pot_df['LATITUDE'].min()]
        self.lon = [pot_df['LONGITUDE'].min(), pot_df['LONGITUDE'].max(), pot_df['LONGITUDE'].max() - pot_df['LONGITUDE'].min()]

        #(lat, lon) -> [TS, TS, TS, TI, TI, TI, PS, PS, PS, PI, PI, PI]
        self.grid = np.zeros((100,100,12))

    def __get_indicies(self, lati, longi):
        return int( (lati / self.lat[1]) * 100 ) - 1, int( (longi / self.lon[1]) * 100 ) - 1
    """
    Public method that exports a csv of pothole service requests with the three nearest weather stations
    along with each weather stations weight in interpolation
    """

    def inter_weather(self, lati, longi, date):
        latii, longii = self.__get_indicies(lati, longi)
        date = pd.to_datetime(date, format="%Y%m%d")
        delta = timedelta(days = 365)
        info = self.grid[latii][longii]
        weather = self.weather_df.loc[(self.weather_df.date < date) & (self.weather_df.date > date - delta)]

        t1 = weather.loc[(weather.station_id == self.ts_decode[info[0]]) & (weather.reading_type == 'TMIN')]
        t2 = weather.loc[(weather.station_id == self.ts_decode[info[1]]) & (weather.reading_type == 'TMIN')]
        t3 = weather.loc[(weather.station_id == self.ts_decode[info[2]]) & (weather.reading_type == 'TMIN')]

        empty_c = 0
        empty_val = 0.0
        starter = None
        if len(t1.index) != 364:
            empty_c+=1
            empty_val += info[3]
        else:
            starter = t1
        if len(t2.index) != 364:
            empty_c += 1
            empty_val +=info[4]
        else:
            starter = t2
        if len(t3.index) != 364:
            empty_c += 1
            empty_val += info[5]
        else:
            starter = t3
        
        print("Interpolating min temp from " + str(3- empty_c) + " stations")
        df_final = pd.DataFrame(columns = ['date', 'tm_value', 'prcp_value'])
        df_final['date'] = starter['date']
        df_final = df_final.fillna(0)
        df_final = df_final.reset_index(drop = True)
        
        if len(t1.index) == 364:
            df_final['tm_value'] += t1['value'].reset_index(drop = True) * (info[3] + empty_val / (3 - empty_c))
        if len(t2.index) == 364:
            df_final['tm_value'] += t2['value'].reset_index(drop = True) * (info[4] + empty_val / (3 - empty_c))
        if len(t3.index) == 364:
            df_final['tm_value'] += t3['value'].reset_index(drop = True) * (info[5] + empty_val / (3 - empty_c))

        p1 = weather.loc[(weather.station_id == self.ps_decode[info[6]]) & (weather.reading_type == 'PRCP')]
        p2 = weather.loc[(weather.station_id == self.ps_decode[info[7]]) & (weather.reading_type == 'PRCP')]
        p3 = weather.loc[(weather.station_id == self.ps_decode[info[8]]) & (weather.reading_type == 'PRCP')]
        print(p1,p2,p3)
        empty_c = 0
        empty_val = 0.0
        starter = None
        if len(p1.index) != 364:
            empty_c+=1
            empty_val += info[9]

        if len(p2.index) != 364:
            empty_c += 1
            empty_val +=info[10]

        if len(p3.index) != 364:
            empty_c += 1
            empty_val += info[11]

        print("Interpolating precipitation from " + str(3- empty_c) + " stations")
        
        
        print(df_final)
        if len(p1.index) == 364:
            print(p1['value'].reset_index(drop = True), info[9] + empty_val / (3 - empty_c))
            print(p1['value'].reset_index(drop = True) * (info[9] + empty_val / (3 - empty_c)))
            df_final['prcp_value'] += p1['value'].reset_index(drop = True) * (info[9] + empty_val / (3 - empty_c))
        if len(p2.index) == 364:
            print(p2['value'].reset_index(drop = True) * (info[10] + empty_val / (3 - empty_c)))
            df_final['prcp_value'] += p2['value'].reset_index(drop = True) * (info[10] + empty_val / (3 - empty_c))
        if len(p3.index) == 364:
            print(p3['value'].reset_index(drop = True) * (info[11] + empty_val / (3 - empty_c)))
            df_final['prcp_value'] += p3['value'].reset_index(drop = True) * (info[11] + empty_val / (3 - empty_c))
        return df_final


    def nearest_stations(self):
        #select the relevent pothole requests file to open
        df = pd.read_csv("../data/output/potholePiped2015-2019.csv")
        out = "../data/output/interpolations2015-2019.csv"
        

        #add columns for the nearest weather stations and interpolation weights
        pot_df = pot_df.reindex(columns = ['SR CREATE DATE', 'LATITUDE', 'LONGITUDE', 'TStation1', 'TStation2', 'TStation3', 'TInter1', 'TInter2', 'TInter3',
                                            'PStation1', 'PStation2', 'PStation3', 'PInter1', 'PInter2', 'PInter3'])


        #cast weather station columns as string
        pot_df['TStation1'] = pot_df['TStation1'].astype(str)
        pot_df['TStation2'] = pot_df['TStation2'].astype(str)
        pot_df['TStation3'] = pot_df['TStation3'].astype(str)

        pot_df['PStation1'] = pot_df['PStation1'].astype(str)
        pot_df['PStation2'] = pot_df['PStation2'].astype(str)
        pot_df['PStation3'] = pot_df['PStation3'].astype(str)

        #find the nearest weather stations and calculate interpolation weights
        final_df = self.__interpolate_stations(pot_df)

        #output the result
        final_df.to_csv(out)
    def find_temp_stations(self):
        out = '../data/output/temp_stats_2010-2019.csv'
        h_stats = set(list(self.stations.station_id.unique()))
        final_df = self.weather_df.loc[ (self.weather_df.reading_type.isin(['TMIN', 'TMAX'])) & (self.weather_df.station_id.isin(h_stats)) ]
        self.tstats = self.stations.loc[ self.stations.station_id.isin(final_df['station_id'].unique()) ]
        for stat in self.tstats.station_id.unique():
            find = final_df.loc[final_df.station_id == stat]
            if len(find.index) < 7200:
                self.tstats = self.tstats[self.tstats.station_id != stat]
        self.ts_encode = {}
        for i, station in enumerate(final_df['station_id'].unique()):
            self.ts_encode.update({station : i})
        self.ts_decode = {v: k for k, v in self.ts_encode.items()}
        final_df.to_csv(out, index = False)

    def find_precp_stations(self):
        out = '../data/output/prcp_stats_2010-2019.csv'
        h_stats = set(list(self.stations.station_id.unique()))
        final_df = self.weather_df.loc[ (self.weather_df.reading_type.isin(['PRCP'])) & (self.weather_df.station_id.isin(h_stats)) ]
        self.pstats = self.stations.loc[ self.stations.station_id.isin(final_df['station_id'].unique()) ]
        for stat in self.pstats.station_id.unique():
            find = final_df.loc[final_df.station_id == stat]
            if len(find.index) < 7200:
                self.pstats = self.pstats[self.pstats.station_id != stat]
        print(len(self.pstats.index))
        self.ps_encode = {}
        for i, station in enumerate(final_df['station_id'].unique()):
            self.ps_encode.update({station : i})
        self.ps_decode = {v: k for k, v in self.ps_encode.items()}
        final_df.to_csv(out, index = False)
    '''