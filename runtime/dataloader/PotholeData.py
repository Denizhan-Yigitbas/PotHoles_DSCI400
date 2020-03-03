import os

import pandas as pd
from datetime import datetime
import calendar

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
        self.potholes_dictionary = {
            year: pd.read_csv(PotholeData.data_path + f"potholePiped{year}.csv")
            for year in range(2015, 2020)
        }

        self.pothole_df = pd.concat(list(self.potholes_dictionary.values()))
        
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
        
        # extract the desired years from the dictionary and concatenate them
        selected_pothole_df_list = []
        for year in years_list:
            selected_pothole_df_list.append(self.potholes_dictionary[year])
        new_pothole_df = pd.concat(selected_pothole_df_list)
        
        return self.clean_correct_pothole_data(new_pothole_df)

    def potholes_by_month_single_year(self, year):
        """
        Month -> number of potholes dataframe
        :param year: year to calculate
        :return:
        """
        # convert the the dates into datetime objects
        # potholes_df["SR CREATE DATE"] = pd.to_datetime(potholes_df["SR CREATE DATE"])
    
        pothole_df = self.all_potholes_in_year_list([year])
        # group the dates by month and count the total number of occurences
        counts_series = pothole_df["SR CREATE DATE"] \
            .groupby([pothole_df["SR CREATE DATE"].dt.month]) \
            .count()
    
        # change the month numbers to names
        counts_df = counts_series.to_frame()
        counts_df["Month"] = list(counts_series.index)
        counts_df["Month"] = counts_df["Month"].apply(lambda x: calendar.month_abbr[x])
        counts_df.set_index("Month", inplace=True)
        counts_df.rename(columns={"SR CREATE DATE": "Number of Potholes"}, inplace=True)
    
        return counts_df

    def overdue_by_month_single_year(self, year):
        """
        Month -> Average overdue time
        :param year: year to calculate
        :return: DataFrame
        """
        # calculate the average number of overdue days for every month of the year
        pothole_df = self.all_potholes_in_year_list([year])
        avg_overdue = pothole_df["OVERDUE"].groupby([pothole_df["SR CREATE DATE"].dt.month])
        avg_overdue_series = avg_overdue.mean()
    
        # change the month numbers to names
        avg_overdue_df = avg_overdue_series.to_frame()
        avg_overdue_df["Month"] = list(avg_overdue_series.index)
        avg_overdue_df["Month"] = avg_overdue_df["Month"].apply(lambda x: calendar.month_abbr[x])
        avg_overdue_df.set_index("Month", inplace=True)
        avg_overdue_df.rename(columns={"SR CREATE DATE": "Average Overdue Days"}, inplace=True)
    
        return avg_overdue_df

    def channel_type_count(self):
        """
        DataFrame that counts channel type
        :return:
        """
        # count the number of occurences for each Channel Type
        channel_count_df = self.pothole_df["Channel Type"].groupby(self.pothole_df["Channel Type"]).count()
    
        return channel_count_df
    
    
if __name__ == "__main__":
    pass