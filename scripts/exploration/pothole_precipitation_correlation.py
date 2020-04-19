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
for timedelta in [0,30, 60, 135, 141]:
    prcp_avg = avg_prcp.loc[[d - pd.Timedelta(days=timedelta) for d in dates]] /10

    fig, ax = plt.subplots()
    ax.scatter(prcp_avg.values, date_counts.values)
    ax.set_xlabel('Average Precipitation (mm)')
    ax.set_ylabel('Number of Potholes (Daily)')

    x = prcp_avg.values
    y = date_counts.values

    m, b, r_value, p_value, std_err = stats.linregress(x, y)
    sorted_indices = np.argsort(x)
    sorted_x = x[sorted_indices]
    ax.plot(sorted_x, m * sorted_x + b, 'r', label='y={:.2f}x+{:.2f}; $r^2$={:.2f}; p={:.2f}'.format(m, b, r_value**2, p_value))

    # Make axis logarithmic
    if log_plot == True:
        ax.set_yticks([2**i for i in range(0,8)])
        xrange = [2**i for i in range(-1,8)]
        xrange.insert(0,0)
        ax.set_xticks(xrange)
        ax.set_yscale('log', basey=2)
        ax.set_xscale('log', basex=2)

    plt.legend()
    plt.title(f"Time delayed by {timedelta} days")


# find pearson r between two time series representation
plt.show()

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


#
# # plot rolling pearson R in a subplot with the time series on top
# for r_window_size in range(5,65,5):
#     # Compute rolling window synchrony
#     rolling_r = merged_df['potholes'].rolling(window=r_window_size, center=True).corr(merged_df['prcp'])
#     f,ax=plt.subplots(2,1,figsize=(14,6),sharex=True)
#     # merged_df.rolling(window=1,center=True).median().plot(ax=ax[0])
#
#     # plot both time series
#     merged_df['prcp'].plot(ax=ax[0])
#     ax[0].set(xlabel='Year',ylabel='Avg Precip. (mm)')
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
#     plt.suptitle(f"Pothole and Weather data with rolling {r_window_size}-day window correlation")
#
#
# def crosscorr(datax, datay, lag=0, wrap=False):
#     """ Lag-N cross correlation.
#     Shifted data filled with NaNs
#
#     Parameters
#     ----------
#     lag : int, default 0
#     datax, datay : pandas.Series objects of equal length
#     Returns
#     ----------
#     crosscorr : float
#     """
#     if wrap:
#         shiftedy = datay.shift(lag)
#         shiftedy.iloc[:lag] = datay.iloc[-lag:].values
#         return datax.corr(shiftedy)
#     else:
#         return datax.corr(datay.shift(lag))
#
#
# d1 = merged_df['potholes']
# d2 = merged_df['prcp']
#
# days = 365
# rs = [crosscorr(d1, d2, lag) for lag in range(-days*2, 0)]
# offset = np.argmax(rs)
# f, ax = plt.subplots(figsize=(14, 3))
# ax.plot(rs)
# ax.axvline(np.argmax(rs), color='r', linestyle='--', label='Peak synchrony')
# ax.set(title=f'Time-Lagged Cross-correlation between precipitation and potholes: \n precipitation leads potholes by {offset} days', xlabel='Days of Lag',
#        ylabel='Pearson r')
# plt.legend()
#
# plt.show()