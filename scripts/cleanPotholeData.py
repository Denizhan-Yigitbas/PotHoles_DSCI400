import sys
import os
import pandas as pd
sys.path.append(os.path.abspath("../runtime/"))
from datetime import datetime
import calendar
from dataloader import WeatherData, PotholeData

p = PotholeData
# 2011 has different format

data_df = pd.read_csv("../data/output/potholePiped2011.csv")
data_df["SR CREATE DATE"] = data_df["SR CREATE DATE"] \
    .apply(lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M'))
data_df["SR CREATE DATE"] = data_df["SR CREATE DATE"] \
    .apply(lambda x: datetime.strftime(x, '%Y-%m-%d %H:%M:00'))
data_df.to_csv("../data/output/potholePiped2011.csv")