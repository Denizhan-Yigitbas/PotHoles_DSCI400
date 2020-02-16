from collections import deque

import pandas as pd

weather_data = "../../data/raw/all_tx_weather.csv"

class WeatherVSPotholes():
    def __init__(self):
        pass
    
    def explore(self):
        df = pd.read_csv(weather_data)
        print(df)
        # with open(weather_data, 'r') as f:
        #     q = deque(f, 2)  # replace 2 with n (lines read at the end)
        # print(q)
        
        
if __name__ == "__main__":
    comparer = WeatherVSPotholes()
    comparer.explore()