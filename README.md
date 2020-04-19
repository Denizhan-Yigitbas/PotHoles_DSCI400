# PotHoles_DSCI400

## Project Description

This project explores the spatiotemporal patterns of pothole formation, existence, and repairs in Houston as it relates to possible underlying factors. Among these factors are weather, road condition and traffic. Currently, Houston Public Works relies partly on citizens logging 311 service requests to report potholes and identify road repairs. Based on our communication with Jesse Bounds, Houston’s Director of Innovation, there is no internal predictive model that influences repairs, so our work will aim to fill that gap, by identifying patterns in the location and timing of potholes.

This project will therefore use publicly available data on service requests and pothole repairs dating back to 2011, and compare this to the historical data on weather drawn from more than 30 weather stations spread out across the city. We will explore both time series and geographic patterns, separately and together, and identify relationships between each of these factors and potholes. To explore the spatial aspect, we will first explore two dimensional maps of weather and potholes and make 2D correlations between these maps. We will also explore clusters of potholes or weather-pothole correlations. In exploring the temporal patterns we wrangle the weather and pothole data such that they can be merged into the same table with a column for the date. Then we explore similar correlations between the data sets. From this exploration we have identified weather features, particularly temperature, rainfall, and flooding to factor into pothole formation. We have also identified a relationship with the Pothole Condition Index (PCI), which will be described in a later section. From here, we will develop a predictive model, including regression, and explore more sophisticated models including classifier algorithms like ElasticNet Regression. We aim to make predictions for the formation of potholes through these models and identify possible locations that lie at risk, and suggest improvements to pothole repairs.


Datasets:

pothole service requests from the City of Houston, from http://www.houstontx.gov/311/  <br />
weather data from the National Weather Service from https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ <br />
flooding service requests from the City of Houston, from http://www.houstontx.gov/311/<br />
flooding reports from Houston Fire Department, collected by Dr. Steven Perry <br />
Pavement Condition Index data from the City of Houston, via communication with the Director of Innovation, Jesse Bounds <br />


From this data, we explore potential correlations and generate a table with all relevant information.

## Current Project Status

We are currently working on producing a model to understand variosu correlations between weather and potholes

## Installing

run `pip install -r requirements.txt`

## Usage
### <u>Data Visualization</u>
<i><b><u>IMPORTANT NOTE:</u></b></i> cd into the runtime directory</u></b></i> 

#### A pothole count vs time bar graph for a specific year
<i> This graph displays the amount of potholes that were recorded through service requests acculated every month for a single year </i>

run: `python run_this.py potholes_by_month [YEAR]`

#### A flood count vs time bar graph for a specific year
<i> This graph displays the amount of flooding that was recorded through service requests acculated every month for a single year </i>

run: `python run_this.py floods_by_month [YEAR]`

#### The effects of temperature and precipitation on pothole formation around a specific weather statoin  count vs time bar graph for a specific year
<i> This graph plots 3 main components: potholes, temperature, and precipitation. The graph counts the number of potholes formed around a specific radius of a single weather station and plots the temperature and precipitation data recorded at this weather station </i>

run: `python run_this.py pothole_vs_weather`

#### Correlating aggregate pothole requests and the average daily precipitation and temperature recordings across Houston.
<i> This graph plots 2 graphs. The top one is the aggreagate daily potholes requests and the average daily weather recordings (specified by the user) as two time series, sharing the same x axis. The bottom graph is the rolling r value, using a specified window size in days. The inputs will default to 45 and 'temp' if no input is given. </i>
  
run: `python run_this.py pothole_weather_correlation [rolling_r_window_size (days)] [weather type: 'temp' or 'prcp']


#### 3D Clustering of potholes based off of location and time of formation within a specific year
<i> This plot uses spatiotemporal clusters of pothole requests around all of Houston over a specific year </i>

run: `python run_this.py potholes_meanshift`


### <u>Modeling</u>
<i><b><u>IMPORTANT NOTE:</u></b></i> cd into the runtime directory</u></b></i>

run: `python run_this.py model`

## Project Structure
### Packages: dataloader, util

#### dataloader
2 Classes: Houston311Data, Weather Data


1. <b> Houston311Data </b>
Produces various DataFrames allowing for different exploration methods through data provided by Houston 311 about pothole service requests and flooding service requests.
Structure:
- Super Class: Houston311Data()
- Sub Classes of Houston311Data(): PotholeData(), FloodingData()

2. <b> WeatherData </b>
Produces various DataFrames about data recorded by various weather statations around Houston
- Class: WeatherData()

***


#### util
6 Classes: DataViz(), GenerateData(), Interpolation(), MeanShift(), Modeler(), WeatherVSPothole()


1. DataViz() - visualizations


2. GenerateData() - produce CSV


3. Interpolation() - interpolates data


4. MeanShift() - spatiotemporal visual


5. Modeler() - models


6. WeatherVSPotholes() - Compares weather and potholes for a single station, and examines correlations between daily pothole requests and average daily weather recordings from all stations
