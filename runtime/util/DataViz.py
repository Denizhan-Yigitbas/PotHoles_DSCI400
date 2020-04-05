import matplotlib.pyplot as plt
import gmplot

from dataloader.Houston311Data import PotholeData, FloodingData
from util.WeatherVSPothole import WeatherVSPotholes

class DataViz(object):
    def __init__(self):
        self.pothole = PotholeData()
        self.flooding = FloodingData()
        self.weatherVSpothole = WeatherVSPotholes()
        
    def potholes_by_month_single_year_viz(self, year):
        """
        Produce a pothole count vs time bar graph for a specific year
        
        :param year: year to viz
        :return: bar graph plot
        """
        counts_df = self.pothole.potholes_by_month_single_year(year)
        # plot the visual
        counts_df.plot(kind="bar", legend=False)
        plt.title("Number of Potholes Per Month in " + str(year))
        plt.ylabel("Number of Pothole")
        plt.subplots_adjust(bottom=.2)
        plt.show()

    def floodings_by_month_single_year_viz(self, year):
        """
        Produce a pothole count vs time bar graph for a specific year

        :param year: year to viz
        :return: bar graph plot
        """
        counts_df = self.flooding.flooding_by_month_single_year(year)
        # plot the visual
        counts_df.plot(kind="bar", legend=False)
        plt.title("Number of Floods Per Month in " + str(year))
        plt.ylabel("Number of Floods")
        plt.subplots_adjust(bottom=.2)
        plt.show()
        
    def potholes_overdue_by_month_single_year_viz(self, year):
        """
        Produce the average overdue time to repair a pothole vs time for a given year
        
        :param year: Year to visualize
        :return: Bar plot
        """
        avg_overdue_df = self.pothole.overdue_by_month_single_year(year)
        # plot the visual
        avg_overdue_df.plot(kind="bar", legend=False)
        plt.axhline()
        plt.title("Average Number of Days Overdue Per Month in " + str(year))
        plt.ylabel("Days")
        plt.subplots_adjust(bottom=.2)
        plt.show()
        
    def pothole_heat_map(self, year, all_years=False):
        """
        Produce a heat map of the amount of pothole service reports for a given year

        :param year: Year to visualize
        :return: html heatmap
        """
        # extract latitudes data - clean Nan and Unknown entries - convert to floats
        potholes_df = self.pothole.all_data_in_year_list([year])

        if all_years:
            potholes_df = self.pothole.pothole_df

        latitudes = potholes_df["LATITUDE"]

        # extract longitude data - clean Nan and Unknown entries - convert to floats
        longitudes = potholes_df["LONGITUDE"]

        # Creating the location we would like to initialize the focus on.
        # Parameters: Lattitude, Longitude, Zoom
        gmap = gmplot.GoogleMapPlotter(29.7604, -95.3698, 10)

        # create the map
        gmap.heatmap(latitudes, longitudes)
        gmap.draw("../../data/output/pothole_heatmap_" + str(year) + ".html")

    def flooding_heat_map(self, year, all_years=False):
        """
        Produce a heat map of the amount of flooding service reports for a given year

        :param year: Year to visualize
        :return: html heatmap
        """
        # extract latitudes data - clean Nan and Unknown entries - convert to floats
        floodings_df = self.flooding.all_data_in_year_list([year])

        if all_years:
            floodings_df = self.flooding.flooding_df

        latitudes = floodings_df["LATITUDE"]

        # extract longitude data - clean Nan and Unknown entries - convert to floats
        longitudes = floodings_df["LONGITUDE"]

        # Creating the location we would like to initialize the focus on.
        # Parameters: Latitude, Longitude, Zoom
        gmap = gmplot.GoogleMapPlotter(29.7604, -95.3698, 10)

        # create the map
        gmap.heatmap(latitudes, longitudes)
        
        if all_years:
            gmap.draw("../../data/output/flooding_heatmap_ALLYEARS.html")
        else:
            gmap.draw("../../data/output/flooding_heatmap_" + str(year) + ".html")
        
    def pothole_channel_type_count(self):
        """
        Produce a count vs channel type bar graph for potholes.
    
        Channel Type is the method of reporting a potholes i.e. Web, Phone, etc.
        
        :return: Bar Plot
        """
        # count the number of occurences for each Channel Type
        channel_count_df = self.pothole.channel_type_count()
        
        # plot the visual
        channel_count_df.plot(kind="bar", legend=False)
        plt.axhline()
        plt.title("Various Ways of Reporting Potholes")
        plt.ylabel("Count")
        plt.subplots_adjust(bottom=.28)
        plt.show()

    def single_station_pothole_vs_weather(self):
        self.weatherVSpothole.temp_precip_potholes(2015, 2019, "USW00012918", 0.05)
    

if __name__ == "__main__":
    visualizer = DataViz()
    viz_year = 2019
    
    # visualizer.potholes_by_month_single_year_viz(viz_year)
    # visualizer.floodings_by_month_single_year_viz(viz_year)
    # visualizer.potholes_overdue_by_month_single_year_viz(viz_year)
    # visualizer.pothole_heat_map(2019, all_years=True)
    # visualizer.flooding_heat_map(2019, all_years=True)
    # visualizer.pothole_channel_type_count()
    # visualizer.single_station_pothole_vs_weather()