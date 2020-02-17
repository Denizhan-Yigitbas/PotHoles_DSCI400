import pandas as pd

pothole_data = {
    2019: "../../data/raw/311-Public-Data-Extract-2019-clean.txt",
    2018: "../../data/raw/311-Public-Data-Extract-2018-clean.txt",
    2017: "../../data/raw/311-Public-Data-Extract-2017-clean.txt"
}


class PipedData():
    
    def __init__(self):
        pass
    
    """
    Private method that creates a DataFrame for Pothole Service Request
    """
    def __create_service_dataframe(self, pothole_data):
        # Reads piped text file of service requests into DataFrame
        df_service = pd.read_csv(pothole_data, delimiter='|', error_bad_lines=False)
        df_service.columns = df_service.columns.str.strip()
        # Removes spaces before and after strings in every row/column
        df_service_trimmed = df_service.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df_service_trimmed
    
    """
    Private method to find pothole based on service requests
    """
    def __find_pothole_request(self, df_service):
        idx = df_service.columns.get_loc('SR TYPE')
        not_pot = []
        # Find the row index of all service requests unrelated to potholes and compile into list
        for i in range(len(df_service)):
            if df_service.iloc[i, idx] != 'Pothole':
                not_pot.append(i)
        # Remove all indexed rows from DataFrame
        df_pothole = df_service.drop(not_pot)
        # Reset index of DataFrame
        df_pothole.reset_index()
        return df_pothole
    
    """
    Public method that exports a csv of the pothole data into data/outputs/ directory
    """
    def create_piped_csv(self, year):
        df_service = self.__create_service_dataframe(pothole_data[year])
        df_pothole = self.__find_pothole_request(df_service)
        df_pothole.to_csv("../../data/output/potholePiped" + str(year) + ".csv")

if __name__ == "__main__":
    piper = PipedData()
    year = 2019
    piper.create_piped_csv(year)