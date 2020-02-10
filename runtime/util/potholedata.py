import pandas as pd

# Read Pothole Data
from runtime.util.dataViz import dataViz

pothole_data = "../../data/raw/311-Public-Data-Extract-2019-clean.txt"

# Create DataFrame for Pothole Service Request
def create_service_dataframe(pothole_data):
    df_service = pd.read_csv(pothole_data, delimiter='|', error_bad_lines=False)
    df_service.columns = df_service.columns.str.strip()
    df_service_trimmed = df_service.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    return df_service_trimmed


# Finds pothole based service requests
def find_pothole_request(df_service):
    idx = df_service.columns.get_loc('SR TYPE')
    not_pot = []
    for i in range(len(df_service)):
        if df_service.iloc[i, idx] != 'Pothole':
            not_pot.append(i)
    df_pothole = df_service.drop(not_pot)
    df_pothole.reset_index()
    return df_pothole


def create_piped_csv(pothole_data):
    df_service = create_service_dataframe(pothole_data)
    df_pothole = find_pothole_request(df_service)
    df_pothole.to_csv("../../data/output/potholePiped2019.csv")


create_piped_csv(pothole_data)
