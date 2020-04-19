from shapely.geometry import Point, Polygon
from datetime import datetime
import matplotlib.pyplot as plt
import calendar
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import pandas as pd
import scipy.stats as stats

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


        # -----------PLOTTING------------------#
        
        plt.figure(figsize=[15.5, 6])
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
        y = station_precip / 10
        p1, = ax_prcp.plot(list(range(len(x))), y, color='r', linewidth=3, label="Precipitation (mm)")
        
        station_temp = WeatherData().avg_station_temp_per_month(2015, 2019, station_id)
        x = station_temp.index
        y = station_temp / 10
        p2, = ax_temp.plot(list(range(len(x))), y, color='g', linewidth=3, label="Temperature  $^\circ$ C")

        ax_prcp.axis["right"].label.set_color(p1.get_color())
        ax_temp.axis["right"].label.set_color(p2.get_color())


        plt.draw()
        plt.show()

    def pothole_precipitation_correlation(self, r_window_size = 45):
        """
        Calculates overall correlation (pearson r) between aggregate potholes and average daily precipitation in Houston.
        Then plots a rolling correlation between potholes and precipitation, as two time series.
        :param r_window_size: rolling window for rolling correlation plot, in days
        :return:
        """
        w = self.weatherDat
        p = self.potholeDat
        avg_prcp = w.precipitation_df.groupby('date').value.agg('mean') / 10

        p.pothole_df['date'] = p.pothole_df['SR CREATE DATE'].dt.date
        date_counts = p.pothole_df.groupby('date').date.agg('count')

        dates = date_counts.index

        # # calculate time lagged correlation
        # for timedelta in range(0, 361, 30):
        #
        #     prcp_avg = avg_prcp.loc[[d - pd.Timedelta(days=timedelta) for d in dates]] /10
        #
        #     plt.figure()
        #     plt.scatter(prcp_avg.values, date_counts.values)
        #     plt.xlabel('Average Precipitation (mm)')
        #     plt.ylabel('Number of Potholes (Daily)')
        #     plt.title(f"Time delayed by {timedelta} days")

        # find pearson r between two time series representation
        # plt.show()

        # remove time stamp
        avg_prcp.index = avg_prcp.index.date

        merged_df = pd.merge(avg_prcp, date_counts, right_index=True, left_index=True)
        merged_df.columns = ['prcp', 'potholes']

        # average multiple readings from one day
        merged_df = merged_df.groupby(level=0).agg('mean')

        # save 1+ years of data
        merged_df.truncate(after=pd.to_datetime('2018-12-31'))

        overall_pearson_r = merged_df.corr().iloc[0, 1]
        print(f"Pandas computed Pearson r: {overall_pearson_r}")
        # Pandas computed Pearson r: -0.05044392292864415

        r, p = stats.pearsonr(merged_df['prcp'], merged_df['potholes'])
        print(f"Scipy computed Pearson r: {r} and p-value: {p}")
        # Scipy computed Pearson r: -0.050443922928643734 and p-value: 0.03178041654318355

        # plot rolling pearson R in a subplot with the time series on top
        # Compute rolling window synchrony
        rolling_r = merged_df['potholes'].rolling(window=r_window_size, center=True).corr(merged_df['prcp'])
        f, ax = plt.subplots(2, 1, figsize=(14, 6), sharex=True)
        # merged_df.rolling(window=1,center=True).median().plot(ax=ax[0])

        # plot both time series
        merged_df['prcp'].plot(ax=ax[0])
        ax[0].set(xlabel='Year', ylabel='Avg Precip. (mm)')

        ax1 = ax[0].twinx()
        merged_df['potholes'].plot(ax=ax1, color='orange')
        ax1.set(ylabel='# potholes')
        ax1.yaxis.label.set_color('orange')
        ax1.tick_params(axis='y', colors='orange')

        # rolling pearson r
        rolling_r.plot(ax=ax[1])
        ax[1].set(xlabel='Year', ylabel='Pearson r')
        plt.suptitle(f"Pothole and Weather data with rolling {r_window_size}-day window correlation")

        plt.show()
        
    
if __name__ == "__main__":
    pass
    # weatherDat = WeatherData()
    # potholeDat = PotholeData()
    #
    comparer = WeatherVSPotholes()
    comparer.pothole_precipitation_correlation()

    # comparer.temp_precip_potholes(2015, 2019, "USW00012918", 0.05)