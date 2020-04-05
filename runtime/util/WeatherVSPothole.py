from shapely.geometry import Point, Polygon
from datetime import datetime
import matplotlib.pyplot as plt
import calendar
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA

from dataloader.Houston311Data import PotholeData
from dataloader import WeatherData

class WeatherVSPotholes(object):
    def __init__(self):
        """
        Load both the weather data and pothole data
        """
        self.weatherDat = WeatherData()
        self.potholeDat = PotholeData()

    def temp_precip_potholes(self, year1, year2, station_id, radius):
        """
        Comparing temperature, precipitation, and pothole formation
        
        :param year1: start year
        :param year2: end year
        :param station_id: weather station id
        :param radius: radius size in degrees
        :return:
        """
        # create the desired DataFrames
        weather_df = self.weatherDat.all_weather_in_range(year1, year2)
        potholes_df = self.potholeDat.all_data_in_year_list(range(year1, year2 + 1, 1))
        
        # locate the input station coordinates
        station = weather_df[weather_df["station_id"] == station_id]
        station_lat = station["lat"].values[0]
        station_lng = station["lon"].values[0]
    
        # get coordinates that create a square centered about the station's coordinates
        bot_left = (station_lat - radius, station_lng - radius)
        bot_right = (station_lat - radius, station_lng + radius)
        top_left = (station_lat + radius, station_lng - radius)
        top_right = (station_lat + radius, station_lng + radius)
    
        # create a square polygon
        coords = [bot_left, bot_right, top_right, top_left]
        poly = Polygon(coords)
    
        # combine lat and lng to create Point objects
        potholes_df["coord"] = list(zip(potholes_df.LATITUDE, potholes_df.LONGITUDE))
        potholes_df["coord"] = potholes_df["coord"].apply(lambda x: Point(x))
    
        # keep only potholes that are contained within the created Polygon
        potholes_df["contains"] = potholes_df["coord"].apply(lambda x: poly.contains(x))
        potholes_df = potholes_df[potholes_df.contains]
    
        # group the dates by month and year and count the total number of occurences
        counts_series = potholes_df["SR CREATE DATE"] \
            .groupby([(potholes_df["SR CREATE DATE"].dt.year), (potholes_df["SR CREATE DATE"].dt.month)]) \
            .count()
    
        counts_df = counts_series.to_frame()
        counts_df["month-year"] = list(counts_df.index)
        counts_df["month-year"] = counts_df["month-year"] \
            .apply(lambda x: datetime.strptime(str(calendar.month_abbr[x[1]]) + " " + str(x[0]), '%b %Y'))
        counts_df["month-year"] = counts_df["month-year"] \
            .apply(lambda x: x.strftime('%b %Y'))
        counts_df.set_index("month-year", inplace=True)
    
        # visualize the data
        ax = host_subplot(111, axes_class=AA.Axes)
        plt.subplots_adjust(bottom=.2, left=0.11, right=0.87)

        
        x = counts_df.index
        y = counts_df["SR CREATE DATE"]

        ax.bar(x, y,  label="Potholes")
        ax.set_title("Pothole Formation Around Station " + station_id + " With Weather")
        ax.axis["bottom"].major_ticklabels.set_rotation(55)
        ax.axis["bottom"].major_ticklabels.set_pad(19)
        ax.axis["bottom"].label.set_pad(23)
        ax.axis["top"].toggle(all=False)

        ax_prcp = ax.twinx()
        ax_temp = ax.twinx()

        offset = 60
        new_fixed_axis = ax_temp.get_grid_helper().new_fixed_axis
        ax_temp.axis["right"] = new_fixed_axis(loc="right",
                                            axes=ax_temp,
                                            offset=(offset, 0))

        ax_temp.axis["right"].toggle(all=True)
        ax_prcp.axis["right"].toggle(all=True)

        ax.set_xlabel("Time")
        ax.set_ylabel("Potholes")
        ax_prcp.set_ylabel("Precipitation")
        ax_temp.set_ylabel("Temperature")
        
        station_precip = WeatherData().avg_station_precipitation_per_month(2015, 2019, station_id)
        x = station_precip.index
        y = station_precip
        p1, = ax_prcp.plot(list(range(len(x))), y, color='r', linewidth=3, label="Precipitation")
        
        station_temp = WeatherData().avg_station_temp_per_month(2015, 2019, station_id)
        x = station_temp.index
        y = station_temp
        p2, = ax_temp.plot(list(range(len(x))), y, color='g', linewidth=3, label="Temperature")

        ax_prcp.axis["right"].label.set_color(p1.get_color())
        ax_temp.axis["right"].label.set_color(p2.get_color())


        plt.draw()
        plt.show()

        
    
if __name__ == "__main__":
    pass
    # weatherDat = WeatherData()
    # potholeDat = PotholeData()
    #
    # comparer = WeatherVSPotholes()
    #
    # comparer.temp_precip_potholes(2015, 2019, "USW00012918", 0.05)