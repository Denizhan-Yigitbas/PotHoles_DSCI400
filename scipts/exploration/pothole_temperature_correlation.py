
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath("../../runtime/"))
from dataloader import WeatherData, PotholeData


w = WeatherData()
p = PotholeData()

avg_temp = w.temp_df.groupby('date').value.agg('mean')

p.pothole_df['date'] = p.pothole_df['SR CREATE DATE'].dt.date
date_counts = p.pothole_df.groupby('date').date.agg('count')

dates = date_counts.index


for timedelta in range(0, 361, 30):

    tavg = avg_temp.loc[[d - pd.Timedelta(days=timedelta) for d in date_counts.index]]


    plt.scatter(tavg.values, date_counts.values)
    plt.xlabel('Average Temperature')
    plt.ylabel('Number of Potholes (Daily)')

    plt.title(f"Time delayed by {timedelta} days")

    plt.show()







