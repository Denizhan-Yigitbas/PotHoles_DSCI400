import pandas as pd

pothole_data = {
    2019: "../../data/raw/311-Public-Data-Extract-2019-clean.txt",
    2018: "../../data/raw/311-Public-Data-Extract-2018-clean.txt",
    2017: "../../data/raw/311-Public-Data-Extract-2017-clean.txt",
    2016: "../../data/raw/311-Public-Data-Extract-2016-clean.txt",
    2015: "../../data/raw/311-Public-Data-Extract-2015-clean.txt",
    'Harvey': "../../data/raw/311-Public-Data-Extract-Harvey-clean.txt",
    2014: "../../data/raw/311-Public-Data-Extract-2014-clean.txt",
    2013: "../../data/raw/311-Public-Data-Extract-2013-clean.txt",
    2012: "../../data/raw/311-Public-Data-Extract-2012-clean.txt",
    2011: "../../data/raw/311-Public-Data-Extract-2011-clean.txt",

}

class GenerateData(object):
    
    def __init__(self):
        pass
    
    def __create_service_dataframe(self, pothole_data):
        """
        Private method that creates a DataFrame for Pothole Service Request
        :param pothole_data: data dictionary
        """
        # Reads piped text file of service requests into DataFrame
        df_service = pd.read_csv(pothole_data, delimiter='|', error_bad_lines=False)
        df_service.columns = df_service.columns.str.strip()
        # Removes spaces before and after strings in every row/column
        df_service_trimmed = df_service.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df_service_trimmed
    
    def __find_pothole_request(self, df_service):
        """
        Private method to find pothole based on service requests
        :param df_service: service request dataframe
        """
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

    def __find_flooding_request(self, df_service):
        idx = df_service.columns.get_loc('SR TYPE')
        not_flood = []
        # Find the row index of all service requests unrelated to flooding and compile into list
        for i in range(len(df_service)):
            if df_service.iloc[i, idx] != 'Flooding':
                not_flood.append(i)
        # Remove all indexed rows from DataFrame
        df_flooding = df_service.drop(not_flood)
        # Reset index of DataFrame
        df_flooding.reset_index()
        return df_flooding

    def create_piped_csv(self, year):
        """
        Public method that exports a csv of the pothole data into data/outputs/ directory
        :param year: input year
        """
        df_service = self.__create_service_dataframe(pothole_data[year])
        df_pothole = self.__find_pothole_request(df_service)
        df_flooding = self.__find_flooding_request(df_service)

        # Need to add Harvey service requests to the 2017 data
        if year == 2017:
            df_service_harvey = self.__create_service_dataframe(pothole_data['Harvey'])
            df_pothole_harvey = self.__find_pothole_request(df_service_harvey)
            df_flooding_harvey = self.__find_flooding_request(df_service_harvey)
            df_pothole = df_pothole.append(df_pothole_harvey)
            df_flooding = df_flooding.append(df_flooding_harvey)

        df_pothole.to_csv("../../data/output/potholePiped" + str(year) + ".csv", index=False)
        df_flooding.to_csv("../../data/output/floodingPiped" + str(year) + ".csv", index=False)


    """
    Public method that exports a csv of concatenated pothole csv's over multiple years
    """
    def concat_multi_year_potholes(self, start_year, end_year):
        df_list = []
        for year in range(start_year, end_year+1, 1):
            year_df = pd.read_csv("../../data/output/potholePiped" + str(year) + ".csv")
            df_list.append(year_df)
        
        df_final = pd.concat(df_list)
        df_final.to_csv("../../data/output/potholePiped" + str(start_year) + "-" + str(end_year) + ".csv", index=False)

if __name__ == "__main__":
    piper = GenerateData()
    # year = 2019
    #for year in list(range(2011, 2020)):
    # piper.create_piped_csv(2017)
    piper.concat_multi_year_potholes(2011, 2018)