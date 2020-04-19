import fire

from util.DataViz import DataViz
from util import Modeler


# For Fire CLI
class FireCLI:
    def __init__(self):
        self.visualize = DataViz()

    def potholes_by_month(self, year):
        self.visualize.potholes_by_month_single_year_viz(year)
    
    def floods_by_month(self, year):
        self.visualize.floodings_by_month_single_year_viz(year)
        
    def pothole_vs_weather(self):
        self.visualize.single_station_pothole_vs_weather()

    def pothole_weather_correlation(self, rolling_r_window_size=45, weather_type='temp'):
        self.visualize.overall_pothole_weather_correlation(rolling_r_window_size, weather_type)

    def pothole_weather_timelag_correlation(self, days_back=365, weather_type='temp'):
        self.visualize.overall_pothole_weather_time_lagged_xcorr(days_back, weather_type)

    def scatter_pothole_weather_timelag(self, day_lag=30, weather_type='temp', log_plot=False, show_regression=True):
        self.visualize.scatter_timelagged_weather_pothole_correlation(day_lag, weather_type, log_plot, show_regression)

    def potholes_meanshift(self):
        self.visualize.mean_shift_3D()
        
    def model(self):
        Mod = Modeler()
        Mod.train()

if __name__ == '__main__':
    fire.Fire(FireCLI)