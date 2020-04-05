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
        
    def model(self):
        Mod = Modeler.Modeler()
        Mod.train()

if __name__ == '__main__':
    fire.Fire(FireCLI)

# import fire
#
# class Calculator(object):
#   """A simple calculator class."""
#
#   def double(self, number):
#     return 2 * number
#
# if __name__ == '__main__':
#   fire.Fire(Calculator)