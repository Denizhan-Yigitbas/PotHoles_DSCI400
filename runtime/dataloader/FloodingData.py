import os

import pandas as pd
from datetime import datetime
import calendar


class FloodingData(object):
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

    def __init__(self):
        """
        Loads weather dataframe and merge in the station data for each reading.
        """
        self.data2015 = pd.read_csv(FloodingData.data_path + "floodingPiped2015.csv")
        self.data2016 = pd.read_csv(FloodingData.data_path + "floodingPiped2016.csv")
        self.data2017 = pd.read_csv(FloodingData.data_path + "floodingPiped2017.csv")
        self.data2018 = pd.read_csv(FloodingData.data_path + "floodingPiped2018.csv")
        self.data2019 = pd.read_csv(FloodingData.data_path + "floodingPiped2019.csv")

        flooding_df_list = [self.data2015, self.data2016, self.data2017, self.data2018, self.data2019]

        self.flooding_df = pd.concat(flooding_df_list)

        self.flooding_df = self.clean_correct_flooding_data(self.flooding_df)

    def clean_correct_flooding_data(self, flooding_df):
        """
        Clean original flooding df to have usable objects
        :param flooding_df:
        :return: cleaned DataFrame
        """
        # convert create dates to date times
        flooding_df["SR CREATE DATE"] = flooding_df["SR CREATE DATE"] \
            .apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

        # clean lat/lng
        flooding_df = flooding_df[flooding_df['LATITUDE'].notna()]
        flooding_df = flooding_df[~flooding_df.LATITUDE.str.contains("Unknown")]
        flooding_df["LATITUDE"] = flooding_df["LATITUDE"].apply(lambda x: float(x))

        flooding_df = flooding_df[flooding_df['LONGITUDE'].notna()]
        flooding_df = flooding_df[~flooding_df.LONGITUDE.str.contains("Unknown")]
        flooding_df["LONGITUDE"] = flooding_df["LONGITUDE"].apply(lambda x: float(x))

        return flooding_df

    def all_floodings_in_year_list(self, years_list):
        """
        Outputs a DataFrame that will only contain inputed years

        :param years_list: list of years in the form yyyy (i.e. 2019)
        :return: DataFrame containing only desired years
        """
        floodings_dictionary = {
            2015: self.data2015,
            2016: self.data2016,
            2017: self.data2017,
            2018: self.data2018,
            2019: self.data2019
        }

        # extract the desired years from the dictionary and concatenate them
        selected_flooding_df_list = []
        for year in years_list:
            selected_flooding_df_list.append(floodings_dictionary[year])
        new_flooding_df = pd.concat(selected_flooding_df_list)

        return self.clean_correct_flooding_data(new_flooding_df)

    def floodings_by_month_single_year(self, year):
        # convert the the dates into datetime objects
        # floodings_df["SR CREATE DATE"] = pd.to_datetime(floodings_df["SR CREATE DATE"])

        flooding_df = self.all_floodings_in_year_list([year])
        # group the dates by month and count the total number of occurences
        counts_series = flooding_df["SR CREATE DATE"] \
            .groupby([flooding_df["SR CREATE DATE"].dt.month]) \
            .count()

        # change the month numbers to names
        counts_df = counts_series.to_frame()
        counts_df["Month"] = list(counts_series.index)
        counts_df["Month"] = counts_df["Month"].apply(lambda x: calendar.month_abbr[x])
        counts_df.set_index("Month", inplace=True)
        counts_df.rename(columns={"SR CREATE DATE": "Number of Floodings"}, inplace=True)

        return counts_df

    def overdue_by_month_single_year(self, year):
        # calculate the average number of overdue days for every month of the year
        flooding_df = self.all_floodings_in_year_list([year])
        avg_overdue = flooding_df["OVERDUE"].groupby([flooding_df["SR CREATE DATE"].dt.month])
        avg_overdue_series = avg_overdue.mean()

        # change the month numbers to names
        avg_overdue_df = avg_overdue_series.to_frame()
        avg_overdue_df["Month"] = list(avg_overdue_series.index)
        avg_overdue_df["Month"] = avg_overdue_df["Month"].apply(lambda x: calendar.month_abbr[x])
        avg_overdue_df.set_index("Month", inplace=True)
        avg_overdue_df.rename(columns={"SR CREATE DATE": "Average Overdue Days"}, inplace=True)

        return avg_overdue_df

    def channel_type_count(self):
        # count the number of occurences for each Channel Type
        channel_count_df = self.flooding_df["Channel Type"].groupby(self.flooding_df["Channel Type"]).count()

        return channel_count_df


if __name__ == "__main__":
    pass