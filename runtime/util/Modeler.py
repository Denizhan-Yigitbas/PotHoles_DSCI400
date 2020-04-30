from util import Interpolation
import pandas as pd
import numpy as np
from sklearn.linear_model import ElasticNetCV
from sklearn.model_selection import cross_val_score

from dataloader.Houston311Data import PotholeData

class Modeler():
    def __init__(self):
        self.Interpolator = Interpolation.Interpolator()
        self.grid_size = .35
        self.grid_dim = 8
        self.step_size = self.grid_size / self.grid_dim
        self.left = -95.5500
        self.bottom = 29.5500
        self.trained = False
        self.pothole = PotholeData()
        
    def train(self, build_dmat = False):
        """
        Training for the model
        :param build_dmat: determines if to construct a new data matrix (default: true). If false, uses
        existing data matrix from data/output directory
        :return: prints correlation console
        """
        labels = self.build_labels_vector()
        if build_dmat:
            dmat = self.build_data_mat()
        else:
            dmat = np.loadtxt('../data/output/data_matrix.csv', delimiter = ',')

        print('Training Model')

        self.model = ElasticNetCV(cv = 5, random_state = 0, normalize=True, fit_intercept=True)
        self.model.fit(dmat, labels)
        self.trained = True

        print('Cross validation scores')
        for score in cross_val_score(self.model, dmat, labels, cv = 10):
            print(score)
        print("")
        
    def prediction(self, lat, lon, date):
        """
        Predictor for potholes
        :param lat: latitude coordinate
        :param lon: longitude coordinate
        :param date: date
        :return:
        """
        if not self.trained:
            print('Model has not been trained yet, train the model first with the train() method')
        else:
            vector = self.Interpolator.interpolate_point(lat, lon, date)
            vector = vector.reshape(1,-1)
            print(self.model.predict(vector))
            
    def build_data_mat(self):
        """
        helper method to construct a new data matrix
        :return: np.array for data matrix
        """
        coords = []
        step = self.grid_size / self.grid_dim
        lleft = self.left + step / 2
        top = self.bottom + self.grid_size  - step / 2

        data_matrix = np.zeros((3840, 10))

        for i in range(8):
            for j in range(8):
                coords.append( (top - i * step, lleft + j * step))
        
        for year in [2015,2016,2017,2018,2019]:
            for month in [1,2,3,4,5,6,7,8,9,10,11,12]:
                print("Generating feature vectors for month " + str(month) + " in year " + str(year))
                for i, coord in enumerate(coords):
                    data_matrix[(year - 2015) * 768 + (month - 1) * 64 + i] = self.Interpolator.interpolate_point(coord[0],coord[1], year * 10000 + month * 100 + 1)

        return data_matrix
    
    def build_labels_vector(self):
        """
        Constructs the label vector
        :return: np.array
        """
        pot_df = self.pothole.all_data_in_year_list([2015, 2016, 2017, 2018, 2019])
        pot_df = pot_df[['SR CREATE DATE', 'LATITUDE', 'LONGITUDE']]

        labels = np.zeros((3840,))
        print('Counting label entries')
        for row in pot_df.iterrows():
            row_ = row[1]
            
            date = pd.to_datetime(row_['SR CREATE DATE'], format = "%Y-%m-%d")
            
            if row_['LATITUDE'] < self.bottom or row_['LONGITUDE'] < self.left or row_['LATITUDE'] > self.bottom + self.grid_size or row_['LONGITUDE'] > self.left + self.grid_size:
                continue
            else:
                lat_diff = row_['LATITUDE'] - self.bottom
                lon_diff = row_['LONGITUDE'] - self.left
                lat_coord = int(((lat_diff / self.grid_size) * 100) / 12.5)
                lon_coord = int(((lon_diff / self.grid_size) * 100) / 12.5)

                inner_pos = lat_coord * 8 + lon_coord
                outer_pos = (date.year - 2015) * 768 + (date.month - 1) * 64

                labels[outer_pos + inner_pos] += 1

        return labels