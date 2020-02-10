import pandas as pd
import matplotlib.pyplot as plt
import calendar

class dataViz():
    def __init__(self):
        pass
    
    def potholes_2019_date_viz(self, potholes_df):
        # convert the the dates into datetime objects
        potholes_df["SR CREATE DATE"] = pd.to_datetime(potholes_df["SR CREATE DATE"])
        
        # group the dates by month and count the total number of occurences
        counts_series = potholes_df["SR CREATE DATE"]\
            .groupby([potholes_df["SR CREATE DATE"].dt.month])\
            .count()
        
        # change the month nubers to names
        counts_df = counts_series.to_frame()
        counts_df["Month"] = list(counts_series.index)
        counts_df["Month"] = counts_df["Month"].apply(lambda x: calendar.month_abbr[x])
        counts_df.set_index("Month", inplace=True)
        counts_df.rename(columns={"SR CREATE DATE":"Number of Potholes"}, inplace=True)
        
        # plot the visual
        counts_df.plot(kind="bar", legend=False)
        plt.title("Number of Potholes Per Month in 2019")
        plt.ylabel("Number of Pothole")
        plt.subplots_adjust(bottom=.2)
        plt.show()
        
pothole_data = "../../data/output/potholePiped2019.csv"
potholes_df = pd.read_csv(pothole_data)

dataViz().potholes_2019_date_viz(potholes_df)