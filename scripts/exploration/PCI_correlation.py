import pandas as pd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import GoogleV3
import numpy as np
import re
import math

# Read Pothole Data from files
PCI_data = "/Users/sang-hyunlee/Desktop/PavementRating_PCI_2015_2016.csv"
pothole_data = "/Users/sang-hyunlee/Desktop/311-Public-Data-Extract-2015-clean.txt"


# Create DataFrame for Pothole Service Request
def create_service_dataframe(pothole_data):
    df_service = pd.read_csv(pothole_data, delimiter='|', error_bad_lines=False)
    df_service.columns = df_service.columns.str.strip()
    df_service_trimmed = df_service.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    return df_service_trimmed


# Creates dataframe for PCI index per location
def create_PCI_dataframe(PCI_data):
    df_PCI = pd.read_csv(PCI_data, delimiter=';')
    df_PCI.columns = df_PCI.columns.str.strip()

    return df_PCI


# Filters non pothole-related service requests from dataframe
def find_pothole_request(df_service):
    idx = df_service.columns.get_loc('SR TYPE')
    not_pot = []
    for i in range(len(df_service)):
        if df_service.iloc[i, idx] != 'Pothole':
            not_pot.append(i)
    df_pothole = df_service.drop(not_pot)
    df_pothole.reset_index()
    return df_pothole


# Finds corresponding PCI value for each pothole location
def potholePCIcorr(df_pothole, df_PCI):
    """
    This function takes in two dataframes built on pothole data and PCI data, and appends the PCI value of each pothole
    location as a new column in the pothole dataframe.


    Input:
        df_pothole -- pothole dataframe
        df_PCI -- PCI dataframe
    """

    # Initialize dictionary
    pci_col = []
    pciloc = df_PCI.columns.get_loc('RoadName')
    potloc = df_pothole.columns.get_loc('SR LOCATION')

    for potidx in range(len(df_pothole)):
        if df_pothole.iloc[potidx, potloc + 1] != "Unknown":
            s = str(df_pothole.iloc[potidx, potloc])
            if "Intersection" in s:
                snew = s.replace("Intersection ", "")
                street1 = snew.split("&")[0]
                street_num = street1.split(" ", 1)[0]
                street_name = street1.split(" ", 1)[1]

            else:
                try:
                    street = s.split(",")[0]
                    street_num = street.split(" ", 1)[0]
                    street_num = re.findall('\d+', street_num)[0]
                    street_name = street.split(" ", 1)[1]

                except IndexError:
                    pci_col.append(None)
                    continue

            df_match = df_PCI.loc[df_PCI["RoadName"].str.contains(street_name)]
            df_match2 = df_match.loc[df_match["BegLocatio"].str.isdigit() & df_match["EndLocatio"].str.isdigit()]

            if df_match.empty:
                pci_col.append(None)

            elif df_match2.empty:

                df_match["CurrentPCI"].astype(int)
                pci_col.append(math.floor(df_match['CurrentPCI'].sum() / len(df_match["CurrentPCI"])))

            else:
                try:
                    df_match3 = df_match2.loc[(df_match2["BegLocatio"].astype(int) <= int(street_num)) & (
                            df_match2["EndLocatio"].astype(int) >= int(street_num))]
                    pci_col.append(df_match3["CurrentPCI"].iloc[0])

                except IndexError:
                    pci_col.append(math.floor(df_match['CurrentPCI'].sum() / len(df_match["CurrentPCI"])))

                except ValueError:
                    pci_col.append(math.floor(df_match['CurrentPCI'].sum() / len(df_match["CurrentPCI"])))

        else:
            pci_col.append(None)

            """
            try:
                df_match = df_PCI.loc[df_PCI["RoadName"].isin([street_name])
                                      & (df_PCI["BegLocatio"].astype(int) <= int(street_num) <= df_PCI["EndLocatio"].astype(int))]

                pci_col.append(df_match.iloc["CurrentPCI"].iloc[0])

            except ValueError:
                try:
                    df_match = df_PCI.loc[df_PCI["RoadName"].isin([street_name])]
                    pci_col.append(df_match["CurrentPCI"].iloc[0])

                except IndexError:
                    pci_col.append("NO MATCH")

            except IndexError:
                pci_col.append("NO MATCH")

        else:
            pci_col.append("NO MATCH")
            '''
            for pciidx in range(len(df_PCI)):
                ps = df_PCI.iloc[pciidx, pciloc]
                start_num = df_PCI.iloc[pciidx, pciloc - 2]
                end_num = df_PCI.iloc[pciidx, pciloc - 1]
                try:
                    if street_name in ps and int(start_num) <= int(street_num) <= int(end_num):
                        pci_col.append(df_PCI.iloc[pciidx, pciloc - 3])
                        break
                except ValueError:
                    if street_name in ps:
                        pci_col.append(df_PCI.iloc[pciidx, pciloc - 3])
                        break
            '''
            """
    df_pothole["PCI"] = pci_col
    return df_pothole




"""
    potlat = df_pothole.columns.get_loc('LATITUDE')
    potlong = df_pothole.columns.get_loc('LONGITUDE')
    potname = df_pothole.columns.get_loc('SR LOCATION')

    for i in range(len(df_pothole)):
        if "Intersection" in df_pothole.iloc[i, potname]:
            # Split intersection into two street names
            s = splitstreet(df_pothole.iloc[i, potname])
            s1 = s[0]
            s2 = s[1]

            # Find coordinates of each street
            coord1 = coord(s1)
            coord2 = coord(s2)

            # Find coordinates of intersection
            coordi = [0.5 * (coord1.latitude + coord2.latitude), 0.5 * (coord1.longitude + coord2.longitude)]

        else:
            # Find coordinates of regular streets
            coordi = [df_pothole.iloc[i, potlat], df_pothole.iloc[i, potlong]]

        for i in range(len(df_PCI)):
            if streetname in df_PCI.iloc[i, pciloc]:
                try:
                    begin = int(df_PCI.iloc[i, pciloc] - 2)
                    end = int(df_PCI.iloc[i, pciloc] - 1)
                    if begin <= streetnum <= end:
                        pcival = df_PCI.iloc[i, 2]
                        hist[pcival] = hist[pcival] + 1
                    else:
                        pass
                except TypeError:
                    pass
    return hist
"""


"""
Function used if we had implemented the geolocator module for lat/long values. Due to slow speed, "string" check is 
currently implemented

def PCIcoord(df_PCI):
    startlat = []
    startlong = []
    endlat = []
    endlong = []

    for i in range(len(df_PCI)):
        try:
            start = str(df_PCI.iloc[i, 3]) + str(" ") + df_PCI.iloc[i, 5]
            end = str(df_PCI.iloc[i, 4]) + str(" ") + df_PCI.iloc[i, 5]
            startcoord = coord(start)
            endcoord = coord(end)


        except AttributeError as error:
            start = str(df_PCI.iloc[i, 3])
            end = str(df_PCI.iloc[i, 4])
            startcoord = coord(start)
            endcoord = coord(end)

        startlat.append(startcoord[0])
        startlong.append(startcoord[1])
        endlat.append(endcoord[0])
        endlong.append(endcoord[1])

    slat = pd.DataFrame({"START LATITUDE": startlat})
    slong = pd.DataFrame({"START LONGITUDE": startlong})
    elat = pd.DataFrame({"END LATITUDE": endlat})
    elong = pd.DataFrame({"END LONGITUDE": endlong})

    df_PCI.join(slat)
    df_PCI.join(slong)
    df_PCI.join(elat)
    df_PCI.join(elong)

    return df_PCI


# def PotholePCI():


def coord(streetname):
    geolocator = Nominatim(user_agent="sal10@rice.edu", format_string="%s, Houston, TX")
    # geolocator = GoogleV3(key='AIzaSyBRzGZxEDZKwVklhEGeXH4Bff9PUmx2cig', format_string="%s, Houston, TX")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    location = geolocator.geocode(streetname, timeout=10)
    try:
        latlong = [location.latitude, location.longitude]

    except AttributeError as error:
        latlong = [0, 0]

    return latlong


def splitstreet(streetname):
    s = str(streetname)
    s = s.replace("Intersection ", "")
    street1 = s.split("&")[0]
    street2 = s.split("&")[1]
    return [street1, street2]
"""

# Test Trial with 2015, 2016 pothole / PCI data
#df_service = create_service_dataframe(pothole_data)
#df_pothole = find_pothole_request(df_service)
#df_pothole.to_csv("/Users/sang-hyunlee/Desktop/pothole20152016.csv")

#df_PCI.to_csv("/Users/sang-hyunlee/Desktop/PCI20152016.csv")

"""
df_test = df_PCI.loc[df_PCI["RoadName"].str.contains('FALLBROOK')]
df_match2 = df_test.loc[df_test["BegLocatio"].str.isdigit() & df_test["EndLocatio"].str.isdigit()]
df_final = df_match2.loc[(df_match2["BegLocatio"].astype(int) <= int("111")) & (df_match2["EndLocatio"].astype(int) >= int("111"))]
pci = df_final["CurrentPCI"].iloc[0]
print(df_test)

"""
#df_potnew = potholePCIcorr(df_pothole, df_PCI)
#df_potnew.to_csv("/Users/sang-hyunlee/Desktop/pothole20152016extended.csv")
