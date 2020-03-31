import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath("../../runtime/"))
from dataloader import WeatherData, PotholeData

p = PotholeData()

p.pothole_df['date'] = p.pothole_df['SR CREATE DATE'].dt.date

nbrhood_counts = p.pothole_df.groupby('NEIGHBORHOOD').date.agg('count')

sorted_nbrhood_counts = nbrhood_counts.sort_values(ascending=False)
nbrhoods = sorted_nbrhood_counts.unique()
print(sorted_nbrhood_counts)
count_plot = sorted_nbrhood_counts.plot(kind='bar')
ax1 = plt.axes()
x_axis = ax1.axes.get_xaxis()
x_axis.set_visible(False)
plt.title("Number of Service Request Counts By Neighbood")
plt.ylabel("Number of Pothole Service Requests")
plt.xlabel("Neighborhoods")
plt.show()