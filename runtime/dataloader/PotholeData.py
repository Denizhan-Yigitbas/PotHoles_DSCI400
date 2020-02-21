import os

import pandas as pd
from datetime import datetime


class PotholeData(object):
    """
    Container class for loading pothole data.
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
        self.data2015 = pd.read_csv(PotholeData.data_path + "potholePiped2015.csv")
        self.data2016 = pd.read_csv(PotholeData.data_path + "potholePiped2016.csv")
        self.data2017 = pd.read_csv(PotholeData.data_path + "potholePiped2017.csv")
        self.data2018 = pd.read_csv(PotholeData.data_path + "potholePiped2018.csv")
        self.data2019 = pd.read_csv(PotholeData.data_path + "potholePiped2019.csv")

        pothole_df_list = [self.data2015, self.data2016, self.data2017, self.data2018, self.data2019]

        self.pothole_df = pd.concat(pothole_df_list)
        
        self.pothole_df = self.clean_correct_pothole_data(self.pothole_df)

    
    def clean_correct_pothole_data(self, pothole_df):
        """
        Clean original pothole df to have usable objects
        :param pothole_df:
        :return: cleaned DataFrame
        """
        # convert create dates to date times
        pothole_df["SR CREATE DATE"] = pothole_df["SR CREATE DATE"] \
            .apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

        # clean lat/lng
        pothole_df = pothole_df[pothole_df['LATITUDE'].notna()]
        pothole_df = pothole_df[~pothole_df.LATITUDE.str.contains("Unknown")]
        pothole_df["LATITUDE"] = pothole_df["LATITUDE"].apply(lambda x: float(x))
        
        pothole_df = pothole_df[pothole_df['LONGITUDE'].notna()]
        pothole_df = pothole_df[~pothole_df.LONGITUDE.str.contains("Unknown")]
        pothole_df["LONGITUDE"] = pothole_df["LONGITUDE"].apply(lambda x: float(x))
        
        return pothole_df
        
    
        
    def all_potholes_in_year_list(self, years_list):
        """
        Outputs a DataFrame that will only contain inputed years
        
        :param years_list: list of years in the form yyyy (i.e. 2019)
        :return: DataFrame containing only desired years
        """
        potholes_dictioary = {
            2015: self.data2015,
            2016: self.data2016,
            2017: self.data2017,
            2018: self.data2018,
            2019: self.data2019
        }
        
        # extract the desired years from the dictionary and concatenate them
        selected_pothole_df_list = []
        for year in years_list:
            selected_pothole_df_list.append(potholes_dictioary[year])
        new_pothole_df = pd.concat(selected_pothole_df_list)
        
        return self.clean_correct_pothole_data(new_pothole_df)
        

if __name__ == "__main__":
    
    PotholeData()