import pandas as pd
import numpy as  np
import os
from sklearn.cluster import MeanShift, estimate_bandwidth

"""
	Inputs: datetime string in "YYYY-MM-DD HH:MM:SS"
	Output: Day in year
"""
def datetime_to_number(dt):
	dt_map = {12:334, 11:304, 10:273, 9:243, 8:212, 7:181, 6:151, 5:120,4:90,3:59, 2:31, 1:0}
	date, time = dt.split()
	year, month, day = date.split('-')
	hour, minute, second = time.split(':')

	month = dt_map[int(month)]
	day = int(day)

	return month + day
"""
	Inputs: float coor - geographical coordinate, tuple ranges - ranges of latitude/longitude in dataset, 
	tuple mini - minimum values in dataset, int ax - 1 = latitude, 2 = longitude
	Output: Expands (streches) the range to 365
"""
def expand_range(coor, rang, mini, ax):
	percent = (coor - mini[ax]) / rang[ax]
	return percent * 365


pot_df = pd.read_csv('../data/output/potholepiped2019.csv')

dt_map = {12:334, 11:304, 10:273, 9:243, 8:212, 7:181, 6:151, 5:120,4:90,3:59, 2:31, 1:0} #mapping of months to days

del pot_df['Unnamed: 0'] #delete the extra column from format

pot_df = pot_df[['SR CREATE DATE', 'LATITUDE', 'LONGITUDE']] #pull relevant columns

#Delete columns without geo-tags, convert remaining to numeric values
pot_df = pot_df[pot_df['LATITUDE'].notna()]
pot_df = pot_df.loc[pot_df['LATITUDE'] != 'Unknown']
pot_df['LATITUDE'] = pd.to_numeric(pot_df['LATITUDE'])
pot_df['LONGITUDE'] = pd.to_numeric(pot_df['LONGITUDE'])

#convert datetimes to day in year ( * / 365)
pot_df['SR CREATE DATE'] = pot_df['SR CREATE DATE'].apply(datetime_to_number)

#Grab maximums/minimums for range expansion
maximums = pot_df.max()
minimums = pot_df.min()

lat_range = maximums['LATITUDE'] - minimums['LATITUDE']
lon_range = maximums['LONGITUDE'] - minimums['LONGITUDE']

minimums = minimums[1:]
ranges = (lat_range, lon_range)

old = pot_df.values

lati = old[:,1]
longi = old[:,2]

#expand ranges
pot_df['LATITUDE'] = pot_df['LATITUDE'].apply(lambda x: expand_range(x, ranges, minimums, 0))
pot_df['LONGITUDE'] = pot_df['LONGITUDE'].apply(lambda x: expand_range(x, ranges, minimums, 1))

#print(pot_df.to_string())

#Grab numpy array for modelling
dat_mat = pot_df.values

#-----------MODELLING------------------#

#bandwidth = estimate_bandwidth(dat_mat, quantile=0.2)

bandwidth = 34.0

print("bandwidth: " + str(bandwidth))

ms = MeanShift(bandwidth = bandwidth, bin_seeding = True, cluster_all = False)
ms.fit(dat_mat)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

labeled = []

for i in range(len(labels)):
	if labels[i] != -1:
		labeled.append(i)
#print(labels)

#-----------PLOTTING------------------#

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

fig = plt.figure()
fig2 = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax2 = fig2.add_subplot(111, projection = '3d')

print("num clusters: " + str(n_clusters_))
print("num orphans: " + str(len(labels) - len(labeled)))

ax.scatter(longi, lati, dat_mat[:,0], zdir = 'z', s =10, c = labels, depthshade = True, cmap = cm.get_cmap(name = 'tab20b'))

ax.set_xlabel('LONGITUDE')
ax.set_ylabel('LATITUDE')
ax.set_zlabel('Time')

ax2.scatter(longi[labeled], lati[labeled], dat_mat[labeled,0], zdir = 'z', s =10, c = labels[labeled], depthshade = True, cmap = cm.get_cmap(name = 'tab20b'))

ax2.set_xlabel('LONGITUDE')
ax2.set_ylabel('LATITUDE')
ax2.set_zlabel('Time')

plt.show()