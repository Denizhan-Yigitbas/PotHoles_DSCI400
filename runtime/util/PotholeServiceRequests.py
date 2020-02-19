import pandas as pd
import calendar

class PotholeServiceRequests:
    def __init__(self):
        pass
    
    # THIS SHOULD CONVERT THE DATA TYPES INTO APPROPRIATE ONES -- NOT STRINGS
    def __clean_pothole_df(self, pothole_df):
        pass

    def potholes_by_month_single_year(self, potholes_df):
        # convert the the dates into datetime objects
        potholes_df["SR CREATE DATE"] = pd.to_datetime(potholes_df["SR CREATE DATE"])
    
        # group the dates by month and count the total number of occurences
        counts_series = potholes_df["SR CREATE DATE"] \
            .groupby([potholes_df["SR CREATE DATE"].dt.month]) \
            .count()
    
        # change the month numbers to names
        counts_df = counts_series.to_frame()
        counts_df["Month"] = list(counts_series.index)
        counts_df["Month"] = counts_df["Month"].apply(lambda x: calendar.month_abbr[x])
        counts_df.set_index("Month", inplace=True)
        counts_df.rename(columns={"SR CREATE DATE": "Number of Potholes"}, inplace=True)

        return counts_df
    
    def overdue_by_month_single_year(self, potholes_df):
        # calculate the average number of overdue days for every month of the year
        potholes_df["SR CREATE DATE"] = pd.to_datetime(potholes_df["SR CREATE DATE"])
        avg_overdue = potholes_df["OVERDUE"].groupby([potholes_df["SR CREATE DATE"].dt.month])
        avg_overdue_series = avg_overdue.mean()

        # change the month numbers to names
        avg_overdue_df = avg_overdue_series.to_frame()
        avg_overdue_df["Month"] = list(avg_overdue_series.index)
        avg_overdue_df["Month"] = avg_overdue_df["Month"].apply(lambda x: calendar.month_abbr[x])
        avg_overdue_df.set_index("Month", inplace=True)
        avg_overdue_df.rename(columns={"SR CREATE DATE": "Average Overdue Days"}, inplace=True)
        
        return avg_overdue_df

    def channel_type_count(self, potholes_df):
        # count the number of occurences for each Channel Type
        channel_count_df = potholes_df["Channel Type"].groupby(potholes_df["Channel Type"]).count()
        
        return channel_count_df

