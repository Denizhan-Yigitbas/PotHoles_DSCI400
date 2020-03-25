import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath("../../runtime/"))
from dataloader import WeatherData, PotholeData

p = PotholeData()

p.pothole_df['date'] = p.pothole_df['SR CREATE DATE'].dt.date

nbrhoods = p.pothole_df['NEIGHBORHOOD'].unique()
nbrhood_counts = p.pothole_df.groupby('NEIGHBORHOOD').date.agg('count')

sorted_nbrhood_counts = nbrhood_counts.sort_values(ascending=False)

sorted_nbrhood_counts.plot.hist()
