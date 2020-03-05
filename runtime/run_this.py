import fire
import pandas as pd

from util.DataViz import DataViz

# For Fire CLI
class FireCLI:
    def __init__(self):
        self.visualize = DataViz()

    def potholes_by_month(self, year):
        # potholes_df = pd.read_csv("../data/output/"+str(piped_pothole_csv_filename))
        self.visualize.potholes_by_month_single_year_viz(year)

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