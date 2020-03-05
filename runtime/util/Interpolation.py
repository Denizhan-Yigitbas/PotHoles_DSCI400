import pandas as pd

from potholes.runtime.dataloader import WeatherData


class Interpolator(object):

    def __init__(self):
        self.weather = WeatherData()
        self.stations = pd.read_csv("../data/output/all_houston_stations.csv", dtype = str)

        #relevant columns
        self.stations = self.stations[['station_id', 'lat', 'lon']]

        #convert coordinate columns to numeric value

        self.stations['lat'] = pd.to_numeric(self.stations['lat'])
        self.stations['lon'] = pd.to_numeric(self.stations['lon'])

    def __interpolate_stations(self, df_potholes):
        """
        Private method to find the three nearest stations for each pothole request, and
        calculate the three interpolation weights
        """
        for index, row in df_potholes.iterrows():
            print(index)
            stations = []
            for ind, r in self.stations.iterrows():
                dist = ( (r['lat'] - row['LATITUDE']) ** 2 + (r['lon'] - row['LONGITUDE']) ** 2 ) ** .5
                stations.append( (self.stations.at[ind, 'station_id'] , dist) )
            stations.sort(key = lambda x: x[1])
            stations = stations[:3]

            tot = sum(i[1] for i in stations)

            df_potholes.at[index, 'Station1'] = stations[0][0]
            df_potholes.at[index, 'Station2'] = stations[1][0]
            df_potholes.at[index, 'Station3'] = stations[2][0]

            df_potholes.at[index, 'inter1'] = stations[2][1] / tot
            df_potholes.at[index, 'inter2'] = stations[1][1] / tot
            df_potholes.at[index, 'inter3'] = stations[0][1] / tot
        return df_potholes

    def nearest_stations(self, year = -1):
        """
        Public method that exports a csv of pothole service requests with the three nearest weather stations
        along with each weather stations weight in interpolation
        """
        #select the relevent pothole requests file to open
        if year == -1:
            df = pd.read_csv("../data/output/potholePiped2015-2019.csv")
            out = "../data/output/interpolations2015-2019.csv"
        else:
            df = pd.read_csv("../data/output/potholePiped" + str(year) + ".csv")
            out = "../data/output/interpolations" + str(year) + ".csv"

        #select relevant columns from service requests
        pot_df = df[['SR CREATE DATE', 'LATITUDE', 'LONGITUDE']]

        #drop the invalid rows
        pot_df = pot_df[pot_df['LATITUDE'].notna()]
        pot_df = pot_df.loc[pot_df['LATITUDE'] != 'Unknown']

        #convert the numeric columns
        pot_df['LATITUDE'] = pd.to_numeric(pot_df['LATITUDE'])
        pot_df['LONGITUDE'] = pd.to_numeric(pot_df['LONGITUDE'])

        #add columns for the nearest weather stations and interpolation weights
        pot_df = pot_df.reindex(columns = ['SR CREATE DATE', 'LATITUDE', 'LONGITUDE', 'Station1', 'Station2', 'Station3', 'inter1', 'inter2', 'inter3'])

        #cast weather station columns as string
        pot_df['Station1'] = pot_df['Station1'].astype(str)
        pot_df['Station2'] = pot_df['Station2'].astype(str)
        pot_df['Station3'] = pot_df['Station3'].astype(str)

        #find the nearest weather stations and calculate interpolation weights
        final_df = self.__interpolate_stations(pot_df)

        #output the result
        final_df.to_csv(out)
