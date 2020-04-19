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

avg_temp = w.temp_df.groupby('date').value.agg('mean') /10

p.pothole_df['date'] = p.pothole_df['SR CREATE DATE'].dt.date
date_counts = p.pothole_df.groupby('date').date.agg('count')

dates = date_counts.index


# ## Time lagged correlation
# for timedelta in range(0, 361, 30):
#
#     tavg = avg_temp.loc[[d - pd.Timedelta(days=timedelta) for d in date_counts.index]] /10
#
#     plt.figure()
#     plt.scatter(tavg.values, date_counts.values)
#     plt.xlabel('Average Temperature $^\circ$ C')
#     plt.ylabel('Number of Potholes (Daily)')
#
#     plt.title(f"Time delayed by {timedelta} days")

avg_temp.index = avg_temp.index.date

merged_df = pd.merge(avg_temp, date_counts, right_index = True, left_index= True)
merged_df.columns = ['temp', 'potholes']

# average multiple readings from one day
merged_df = merged_df.groupby(level=0).agg('mean')

# save 1+ years of data
merged_df.truncate(after= pd.to_datetime('2018-12-31'))


overall_pearson_r = merged_df.corr().iloc[0,1]
print(f"Pandas computed Pearson r: {overall_pearson_r}")
#Pandas computed Pearson r: -0.05044392292864415


r, p = stats.pearsonr(merged_df['temp'],merged_df['potholes'])
print(f"Scipy computed Pearson r: {r} and p-value: {p}")
# Scipy computed Pearson r: -0.050443922928643734 and p-value: 0.03178041654318355



# # plot rolling pearson R in a subplot with the time series on top
# for r_window_size in range(5,65,5):
#     # Compute rolling window synchrony
#     rolling_r = merged_df['potholes'].rolling(window=r_window_size, center=True).corr(merged_df['temp'])
#     f,ax=plt.subplots(2,1,figsize=(14,6),sharex=True)
#     # merged_df.rolling(window=1,center=True).median().plot(ax=ax[0])
#
#     # plot both time series
#     merged_df['temp'].plot(ax=ax[0])
#     ax[0].set(xlabel='Year',ylabel='Avg Temp. ($^\circ$ C)')
#
#     ax1 = ax[0].twinx()
#     merged_df['potholes'].plot(ax=ax1, color='orange')
#     ax1.set(ylabel='# potholes')
#     ax1.yaxis.label.set_color('orange')
#     ax1.tick_params(axis='y', colors='orange')
#
#
#     # rolling pearson r
#     rolling_r.plot(ax=ax[1])
#     ax[1].set(xlabel='Year',ylabel='Pearson r')
#     plt.suptitle(f"Pothole and Temperature data with rolling {r_window_size}-day window correlation")


def crosscorr(datax, datay, lag=0, wrap=False):
    """ Lag-N cross correlation.
    Shifted data filled with NaNs

    Parameters
    ----------
    lag : int, default 0
    datax, datay : pandas.Series objects of equal length
    Returns
    ----------
    crosscorr : float
    """
    if wrap:
        shiftedy = datay.shift(lag)
        shiftedy.iloc[:lag] = datay.iloc[-lag:].values
        return datax.corr(shiftedy)
    else:
        return datax.corr(datay.shift(lag))


d1 = merged_df['potholes']
d2 = merged_df['temp']

days = 365
rs = [crosscorr(d1, d2, lag) for lag in range(-days, 0)]
offset = np.argmax(rs)
f, ax = plt.subplots(figsize=(14, 3))
ax.plot(rs)
ax.axvline(np.argmax(rs), color='r', linestyle='--', label='Peak synchrony')
ax.set(title=f'Time-Lagged Cross-correlation between temperature and potholes: \n temperature leads leads potholes by {offset} days', xlabel='Days of Lag',
       ylabel='Pearson r')
plt.legend()

plt.show()
