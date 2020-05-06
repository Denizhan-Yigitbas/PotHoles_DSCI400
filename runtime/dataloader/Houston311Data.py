import os

import pandas as pd
from datetime import datetime
import calendar

class Houston311Data():
    """
    Container class for loading flooding data.
    """
    
    # This operation ensures the path to the data is correct,
    # regardless of what directory it is called from.
    root_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(
        root_path,
        '../../data/output/'
    )
    
    def __init__(self, data_type_string):
        """
        Loads dataframe and merge in the station data for each reading.

        :param data_type_string:
        """
        
        self.data_dictionary = {
            year: pd.read_csv(self.data_path + data_type_string + f"Piped{year}.csv")
            for year in range(2012, 2020)
        }
        
        self.data_df = pd.concat(list(self.data_dictionary.values()))
        
        self.data_df = self.clean_correct_data(self.data_df)
    
    def clean_correct_data(self, data_df):
        """
        Clean original df to have usable objects

        :param data_df:
        :return: cleaned DataFrame
        """
        # convert create dates to date times
        data_df["SR CREATE DATE"] = data_df["SR CREATE DATE"] \
            .apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        
        # clean lat/lng
        data_df = data_df[data_df['LATITUDE'].notna()]
        data_df = data_df[~data_df.LATITUDE.str.contains("Unknown")]
        data_df["LATITUDE"] = data_df["LATITUDE"].apply(lambda x: float(x))
        
        data_df = data_df[data_df['LONGITUDE'].notna()]
        data_df = data_df[~data_df.LONGITUDE.str.contains("Unknown")]
        data_df["LONGITUDE"] = data_df["LONGITUDE"].apply(lambda x: float(x))
        
        return data_df
    
    def all_data_in_year_list(self, years_list):
        """
        Outputs a DataFrame that will only contain inputed years

        :param years_list: list of years in the form yyyy (i.e. 2019)
        :return: DataFrame containing only desired years
        """
        
        # extract the desired years from the dictionary and concatenate them
        selected_data_df_list = []
        for year in years_list:
            selected_data_df_list.append(self.data_dictionary[year])
        new_data_df = pd.concat(selected_data_df_list)
        
        return self.clean_correct_data(new_data_df)

class PotholeData(Houston311Data):
    def __init__(self):
        super().__init__("pothole")
        self.pothole_df = self.data_df

    def potholes_by_month_single_year(self, year):
        """
        Month -> number of potholes dataframe
        :param year: year to calculate
        :return:
        """
        # convert the the dates into datetime objects
        # potholes_df["SR CREATE DATE"] = pd.to_datetime(potholes_df["SR CREATE DATE"])
    
        pothole_df = self.all_data_in_year_list([year])
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
        pothole_df = self.all_data_in_year_list([year])
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

class FloodingData(Houston311Data):
    def __init__(self):
        super().__init__("flooding")
        self.flooding_df = self.data_df

    def flooding_by_month_single_year(self, year):
        """
        Month -> number of potholes dataframe
        :param year: year to calculate
        :return:
        """
        # convert the the dates into datetime objects
        # potholes_df["SR CREATE DATE"] = pd.to_datetime(potholes_df["SR CREATE DATE"])
    
        flooding_df = self.all_data_in_year_list([year])
        # group the dates by month and count the total number of occurences
        counts_series = flooding_df["SR CREATE DATE"] \
            .groupby([flooding_df["SR CREATE DATE"].dt.month]) \
            .count()
    
        # change the month numbers to names
        counts_df = counts_series.to_frame()
        counts_df["Month"] = list(counts_series.index)
        counts_df["Month"] = counts_df["Month"].apply(lambda x: calendar.month_abbr[x])
        counts_df.set_index("Month", inplace=True)
        counts_df.rename(columns={"SR CREATE DATE": "Number of Floods"}, inplace=True)
    
        return counts_df



if __name__ == "__main__":
    PotholeData()
    FloodingData()