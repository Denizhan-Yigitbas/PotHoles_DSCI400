import os

import pandas as pd


class PotholeData(object):
    """
    Container class for loading pothole data.
    """

    # This operation ensures the path to the data is correct,
    # regardless of what directory it is called from.
    root_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(
        root_path,
        '../../data/output/'
    )

    def __init__(self):
        """
        Loads weather dataframe and merge in the station data for each reading.
        """
        self.data2015 = pd.read_csv(PotholeData.data_path + "potholePiped2015.csv")
        self.data2016 = pd.read_csv(PotholeData.data_path + "potholePiped2016.csv")
        self.data2017 = pd.read_csv(PotholeData.data_path + "potholePiped2017.csv")
        self.data2018 = pd.read_csv(PotholeData.data_path + "potholePiped2018.csv")
        self.data2019 = pd.read_csv(PotholeData.data_path + "potholePiped2019.csv")

        pothole_df_list = []
        for year in range(2015, 2019 + 1, 1):
            year_df = pd.read_csv("../../data/output/potholePiped" + str(year) + ".csv")
            pothole_df_list.append(year_df)

        self.pothole_df = pd.concat(pothole_df_list)