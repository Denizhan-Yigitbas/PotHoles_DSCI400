# PotHoles_DSCI400

## Project Description
Objective is to develop a model to predict pothole formation.
To do so, we analyze the following datasets:

pothole service requests from the City of Houston, from http://www.houstontx.gov/311/  <br />
weather data from the National Weather Service from https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ <br />
flooding service requests from the City of Houston, from http://www.houstontx.gov/311/<br />
flooding reports from Houston Fire Department, collected by Dr. Steven Perry <br />
Pavement Condition Index data from the City of Houston, via communication with the Director of Innovation, Jesse Bounds <br />


From this data, we explore potential correlations and generate a table with all relevant information.

## Current Project Status

We are currently in the exploration stage of the data science pipeline for the potholes and weather, with some early modeling in the form of correlations.
For flooding data, we recently received access to data from Rice's UrbanInstitute so we are in wrangling and exploration.

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

#### 3D Clustering of potholes based off of location and time of formation within a specific year
<i> This plot uses spatiotemporal clusters of pothole requests around all of Houston over a specific year </i>

run: `python run_this.py potholes_meanshift`


### <u>Modeling</u>
<i><b><u>IMPORTANT NOTE:</u></b></i> cd into the runtime directory</u></b></i>

run: `python run_this.py model`

## Project Structure
### Packages

#### Dataloader
2 Classes: Houston311Data, Weather Data

---

<b> Houston311Data </b>
Produces various DataFrames allowing for different exploration methods through data provided by Houston 311 about pothole service requests and flooding service requests.
Structure:
- Super Class: Houston311Data()
- Sub Classes of Houston311Data(): PotholeData(), FloodingData()

---

<b> WeatherData </b>
Produces various DataFrames about data recorded by various weather statations around Houston
- Class: WeatherData()
