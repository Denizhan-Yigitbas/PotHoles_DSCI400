import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import scipy.stats as stats

sys.path.append(os.path.abspath("../../runtime/"))
from dataloader import WeatherData, PotholeData


w = WeatherData()
p = PotholeData()


# date_only = w.precipitation_df['date'].apply(lambda x:x.date().strftime('%y-%m-%d'))
avg_prcp = w.precipitation_df.groupby('date').value.agg('mean') /10


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

merged_df = pd.merge(avg_prcp, date_counts, right_index = True, left_index= True)
merged_df.columns = ['prcp', 'potholes']

# average multiple readings from one day
merged_df = merged_df.groupby(level=0).agg('mean')

# save 1+ years of data
merged_df.truncate(after= pd.to_datetime('2018-12-31'))


overall_pearson_r = merged_df.corr().iloc[0,1]
print(f"Pandas computed Pearson r: {overall_pearson_r}")
#Pandas computed Pearson r: -0.05044392292864415


r, p = stats.pearsonr(merged_df['prcp'],merged_df['potholes'])
print(f"Scipy computed Pearson r: {r} and p-value: {p}")
# Scipy computed Pearson r: -0.050443922928643734 and p-value: 0.03178041654318355



# plot rolling pearson R in a subplot with the time series on top
for r_window_size in range(5,65,5):
    # Compute rolling window synchrony
    rolling_r = merged_df['potholes'].rolling(window=r_window_size, center=True).corr(merged_df['prcp'])
    f,ax=plt.subplots(2,1,figsize=(14,6),sharex=True)
    # merged_df.rolling(window=1,center=True).median().plot(ax=ax[0])

    # plot both time series
    merged_df['prcp'].plot(ax=ax[0])
    ax[0].set(xlabel='Year',ylabel='Avg Precip. (mm)')

    ax1 = ax[0].twinx()
    merged_df['potholes'].plot(ax=ax1, color='orange')
    ax1.set(ylabel='# potholes')
    ax1.yaxis.label.set_color('orange')
    ax1.tick_params(axis='y', colors='orange')


    # rolling pearson r
    rolling_r.plot(ax=ax[1])
    ax[1].set(xlabel='Year',ylabel='Pearson r')
    plt.suptitle(f"Pothole and Weather data with rolling {r_window_size}-day window correlation")

plt.show()