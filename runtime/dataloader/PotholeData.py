
import pandas as pd
import os



class PotholeData(object):
    """
    Container class for interfacing with pothole dataset
    """

    # This operation ensures the path to the data is correct,
    # regardless of what directory it is called from.
    root_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(
        root_path,
        '../../data/output/'
    )

    def __init__(self):

        self.pothole_df = pd.read_csv(os.path.join(PotholeData.data_path, "potholePiped2015-2019.csv"))




