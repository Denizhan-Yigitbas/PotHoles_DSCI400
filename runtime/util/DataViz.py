import pandas as pd
import matplotlib.pyplot as plt
import calendar
import gmplot
import matplotlib.dates as mdates

from util.WeatherVSPothole import WeatherVSPotholes


class DataViz():
    def __init__(self):
        pass
    
    """
    Produce a pothole count vs time bar graph for a specific year
    """
    def potholes_by_month_viz(self, potholes_df, year):
        # convert the the dates into datetime objects
        potholes_df["SR CREATE DATE"] = pd.to_datetime(potholes_df["SR CREATE DATE"])
        
        # group the dates by month and count the total number of occurences
        counts_series = potholes_df["SR CREATE DATE"]\
            .groupby([potholes_df["SR CREATE DATE"].dt.month])\
            .count()
        
        # change the month numbers to names
        counts_df = counts_series.to_frame()
        counts_df["Month"] = list(counts_series.index)
        counts_df["Month"] = counts_df["Month"].apply(lambda x: calendar.month_abbr[x])
        counts_df.set_index("Month", inplace=True)
        counts_df.rename(columns={"SR CREATE DATE":"Number of Potholes"}, inplace=True)
        
        # plot the visual
        counts_df.plot(kind="bar", legend=False)
        plt.title("Number of Potholes Per Month in " + str(year))
        plt.ylabel("Number of Pothole")
        plt.subplots_adjust(bottom=.2)
        plt.show()
        
    """
    Produce the average overdue time to repair a pothole vs time for a given year
    """
    def overdue_by_month_viz(self, potholes_df, year):
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

        # plot the visual
        avg_overdue_df.plot(kind="bar", legend=False)
        plt.axhline()
        plt.title("Average Number of Days Overdue Per Month in " + str(year))
        plt.ylabel("Days")
        plt.subplots_adjust(bottom=.2)
        plt.show()
        
    """
    Produce a heat map of the amount of pothole service reports for a given year
    """
    def pothole_heat_map(self, potholes_df, year):
        # extract latitudes data - clean Nan and Unknown entries - convert to floats
        latitudes = potholes_df["LATITUDE"].dropna()
        latitudes = latitudes[~latitudes.str.contains("Unknown")]
        latitudes = latitudes.apply(lambda x: float(x))

        # extract longitude data - clean Nan and Unknown entries - convert to floats
        longitudes = potholes_df["LONGITUDE"].dropna()
        longitudes = longitudes[~longitudes.str.contains("Unknown")]
        longitudes = longitudes.apply(lambda x: float(x))
        
        # Creating the location we would like to initialize the focus on.
        # Parameters: Lattitude, Longitude, Zoom
        gmap = gmplot.GoogleMapPlotter(29.7604, -95.3698, 10)

        # create the map
        gmap.heatmap(latitudes, longitudes)
        gmap.draw("../../data/output/pothole_heatmap_" + str(year) + ".html")
        
    """
    Produce a count vs channel type bar graph for potholes in a given year.
    
    Channel Type is the method of reporting a potholes i.e. Web, Phone, etc.
    """
    def channel_type_count(self, potholes_df, year):
        # count the number of occurences for each Channel Type
        channel_count = potholes_df["Channel Type"].groupby(potholes_df["Channel Type"]).count()
        
        # plot the visual
        channel_count.plot(kind="bar", legend=False)
        plt.axhline()
        plt.title("Various Ways of Reporting in " + str(year))
        plt.ylabel("Count")
        plt.subplots_adjust(bottom=.28)
        plt.show()

    """
    Produce a line graph of reported precipitation values over time for a single station
    """
    def single_station_percip(self):
        comparer = WeatherVSPotholes()
        df = comparer.create_2019_2020_df()
        single_df = comparer.single_station_explore(df, "US1TXBEL016")
        x = list(single_df.date)
        y = list(single_df.value)

        fig, ax = plt.subplots()
        ax.plot_date(x,y,xdate=True, fmt="r-")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b-%Y"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b-%Y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=.28)
        plt.title("Precipitation Values for US1TXBEL016 in the Past Year")
        plt.show()
        
        

potholes_csv = {
    2019: "../../data/output/potholePiped2019.csv",
    2018: "../../data/output/potholePiped2018.csv",
    2017: "../../data/output/potholePiped2017.csv"
}

if __name__ == "__main__":
    visualizer = DataViz()
    viz_year = 2019
    potholes_df = pd.read_csv(potholes_csv[viz_year])
    # visualizer.potholes_by_month_viz(potholes_df, viz_year)
    # visualizer.overdue_by_month_viz(potholes_df, viz_year)
    # visualizer.pothole_heat_map(potholes_df, 2019)\
    # visualizer.channel_type_count(potholes_df, 2019)
    visualizer.single_station_percip()