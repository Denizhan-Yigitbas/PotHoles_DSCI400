from util import Interpolation
import pandas as pd
import numpy as np
from sklearn.linear_model import ElasticNetCV
from sklearn.model_selection import cross_val_score

class Modeler():
	def __init__(self):
		self.Interpolator = Interpolation.Interpolator()
		self.grid_size = .35
		self.grid_dim = 8
		self.step_size = self.grid_size / self.grid_dim
		self.left = -95.5500
		self.bottom = 29.5500
		self.trained = False
	def train(self, build_dmat = False):
		labels = self.build_labels_vector()
		if build_dmat:
			dmat = self.build_data_mat()
		else:
			dmat = np.loadtxt('../data/output/data_matrix.csv', delimiter = ',')

		print('Training Model')

		self.model = ElasticNetCV(cv = 5, random_state = 0)
		self.model.fit(dmat, labels)
		self.trained = True

		print('Cross validation scores')
		for score in cross_val_score(self.model, dmat, labels, cv = 10):
			print(score)
		print("")
	def prediction(self, lat, lon, date):
		if not self.trained:
			print('Model has not been trained yet, train the model first with the train() method')
		else:
			vector = self.Interpolator.interpolate_point(lat, lon, date)
			vector = vector.reshape(1,-1)
			print(self.model.predict(vector))
	def build_data_mat(self):
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
		pot_df = pd.read_csv('../data/output/potholePiped2015-2019.csv')
		pot_df = pot_df[['SR CREATE DATE', 'LATITUDE', 'LONGITUDE']]

		pot_df = pot_df[pot_df['LATITUDE'].notna()]
		pot_df = pot_df.loc[pot_df['LATITUDE'] != 'Unknown']
		pot_df['LATITUDE'] = pd.to_numeric(pot_df['LATITUDE'])
		pot_df['LONGITUDE'] = pd.to_numeric(pot_df['LONGITUDE'])

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



