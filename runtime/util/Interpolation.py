import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

from dataloader import WeatherData
class Interpolator():
    def __init__(self, build_grid = True):
        self.weather = WeatherData()
        self.weather_df = self.weather.all_weather_in_range(2010, 2019)
        self.stations = pd.read_csv("../data/output/all_houston_stations.csv", dtype = str)

        #relevant columns
        self.stations = self.stations[['station_id', 'lat', 'lon']]

        #convert coordinate columns to numeric value

        self.stations['lat'] = pd.to_numeric(self.stations['lat'])
        self.stations['lon'] = pd.to_numeric(self.stations['lon'])

        self.tstats = None
        self.pstats = None


        #[min, max, range]
        self.lat = None
        self.lon = None

        self.find_temp_stations()
        self.find_precp_stations()

        self.__build_grid(pd.read_csv("../data/output/potholePiped2015-2019.csv"))
        if build_grid:
            self.__interpolate_points()
        else:
            self.grid = np.load('grid.npy')


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
        if t1.empty:
            empty_c+=1
            empty_val += info[3]
        else:
            starter = t1
        if t2.empty:
            empty_c += 1
            empty_val +=info[4]
        else:
            starter = t2
        if t3.empty:
            empty_c += 1
            empty_val += info[5]
        else:
            starter = t3
        print(info[3],info[4],info[5])
        df_final = pd.DataFrame(columns = ['date', 'reading_type', 'value'])
        df_final['date'] = starter['date']
        df_final['reading_type'] = starter['reading_type']
        df_final = df_final.fillna(0)
        df_final = df_final.reset_index(drop = True)
        print(df_final)
        if not t1.empty:
            print(t1['value'].reset_index(drop = True), info[3] + empty_val / (3 - empty_c))
            print(t1['value'].reset_index(drop = True) * (info[3] + empty_val / (3 - empty_c)))
            df_final['value'] += t1['value'].reset_index(drop = True) * (info[3] + empty_val / (3 - empty_c))
        if not t2.empty:
            print(t2['value'].reset_index(drop = True) * (info[4] + empty_val / (3 - empty_c)))
            df_final['value'] += t2['value'].reset_index(drop = True) * (info[4] + empty_val / (3 - empty_c))
        if not t3.empty:
            print(t3['value'].reset_index(drop = True) * (info[5] + empty_val / (3 - empty_c)))
            df_final['value'] += t3['value'].reset_index(drop = True) * (info[5] + empty_val / (3 - empty_c))

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
        self.pstats = self.stations.loc[ self.stations.station_id.isin(final_df['station_id'].unique()) ]
        self.ps_encode = {}
        for i, station in enumerate(final_df['station_id'].unique()):
            self.ps_encode.update({station : i})
        self.ps_decode = {v: k for k, v in self.ps_encode.items()}
        final_df.to_csv(out, index = False)