import pandas as pd
import matplotlib.pyplot as plt
import calendar
import gmplot
import matplotlib.dates as mdates

from util.WeatherVSPothole import WeatherVSPotholes

from util.PotholeServiceRequests import PotholeServiceRequests

class DataViz():
    def __init__(self):
        self.sr = PotholeServiceRequests()
    
    """
    Produce a pothole count vs time bar graph for a specific year
    """
    def potholes_by_month_single_year_viz(self, potholes_df, year):
        counts_df = self.sr.potholes_by_month_single_year(potholes_df)
        # plot the visual
        counts_df.plot(kind="bar", legend=False)
        plt.title("Number of Potholes Per Month in " + str(year))
        plt.ylabel("Number of Pothole")
        plt.subplots_adjust(bottom=.2)
        plt.show()
        
    """
    Produce the average overdue time to repair a pothole vs time for a given year
    """
    def overdue_by_month_single_year_viz(self, potholes_df, year):
        avg_overdue_df = self.sr.overdue_by_month_single_year(potholes_df)
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
    Produce a count vs channel type bar graph for potholes.
    
    Channel Type is the method of reporting a potholes i.e. Web, Phone, etc.
    
    Input note: Year is only used for graph title purposes
    """
    def channel_type_count(self, potholes_df, year):
        # count the number of occurences for each Channel Type
        channel_count_df = self.sr.channel_type_count(potholes_df)
        
        # plot the visual
        channel_count_df.plot(kind="bar", legend=False)
        plt.axhline()
        plt.title("Various Ways of Reporting in " + str(year))
        plt.ylabel("Count")
        plt.subplots_adjust(bottom=.28)
        plt.show()

    """
    Produce a line graph of reported precipitation values over time for a single station
    """
    # TODO: Move this to Weather Class
    def single_station_percip(self):
        comparer = WeatherVSPotholes()
        df = comparer.create_2019_2020_df()
        single_df = comparer.single_station_explore(df, "US1TXBEL016")
        
        print(single_df)
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

if __name__ == "__main__":
    potholes_csv = {
        2019: "../../data/output/potholePiped2019.csv",
        2018: "../../data/output/potholePiped2018.csv",
        2017: "../../data/output/potholePiped2017.csv"
    }
    
    visualizer = DataViz()
    viz_year = 2019
    potholes_df = pd.read_csv(potholes_csv[viz_year])
    # visualizer.potholes_by_month_single_year_viz(potholes_df, viz_year)
    # visualizer.overdue_by_month_single_year_viz(potholes_df, viz_year)
    # visualizer.pothole_heat_map(potholes_df, 2019)\
    visualizer.channel_type_count(potholes_df, "2015-2019")
    # visualizer.single_station_percip()