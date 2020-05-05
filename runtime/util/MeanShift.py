import numpy as  np
from sklearn.cluster import MeanShift, estimate_bandwidth
from dataloader import PotholeData
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

class MeanShiftComp():
    def __init__(self):
        self.pot_df = PotholeData().all_data_in_year_list([2019])
    
    def expand_range(self, coor, rang, mini, ax):
        """
        Expands the range or coords to 365
        
        :param coor: float - geographical coordinate
        :param rang: tuple - ranges of latitude/longitude in dataset
        :param mini: tuple - minimum values in dataset
        :param ax: int - 1 = latitude, 2 = longitude
        :return: Expands (streches) the range to 365
        """
        percent = (coor - mini[ax]) / rang[ax]
        return percent * 365
    
    def meanshift(self):
        """
        Performs mean shift by gathering data, modeling, and plotting
        :return: plot
        """
        pot_df = self.pot_df[['SR CREATE DATE', 'LATITUDE', 'LONGITUDE']] #pull relevant columns
        
        pot_df['SR CREATE DATE'] = pot_df['SR CREATE DATE'].apply(lambda x: x.dayofyear)

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
        pot_df['LATITUDE'] = pot_df['LATITUDE'].apply(lambda x: self.expand_range(x, ranges, minimums, 0))
        pot_df['LONGITUDE'] = pot_df['LONGITUDE'].apply(lambda x: self.expand_range(x, ranges, minimums, 1))
        
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
        
        print("PLOTTING")
        fig = plt.figure(figsize=[13,5])
        # fig2 = plt.figure()
        ax = fig.add_subplot(121, projection='3d')
        ax2 = fig.add_subplot(122, projection = '3d')

        
        print("num clusters: " + str(n_clusters_))
        print("num orphans: " + str(len(labels) - len(labeled)))
        
        ax.scatter(longi, lati, dat_mat[:,0], zdir = 'z', s =10, c = labels, depthshade = True, cmap = cm.get_cmap(name = 'tab20b'))

        ax.set_title("All Data", pad=15)
        ax.set_xlabel('LONGITUDE')
        ax.set_ylabel('LATITUDE')
        ax.set_zlabel('Time')
        
        ax2.scatter(longi[labeled], lati[labeled], dat_mat[labeled,0], zdir = 'z', s =10, c = labels[labeled], depthshade = True, cmap = cm.get_cmap(name = 'tab20b'))

        ax2.set_title("Removed Unnecessary Data", pad=15)
        ax2.set_xlabel('LONGITUDE')
        ax2.set_ylabel('LATITUDE')
        ax2.set_zlabel('Time')
        
        plt.show()
        
if __name__ == "__main__":
    # pass
    m = MeanShiftComp()
    m.meanshift()