# PotHoles_DSCI400

## Project Description
Objective is to develop a model to predict pothole formation.
To do so, we analyze the following datasets:

pothole service requests from the City of Houston, from http://www.houstontx.gov/311/  <br />
weather data from the National Weather Service from https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ <br />
flooding service requests from the City of Houston, from http://www.houstontx.gov/311/<br />
Pavement Condition Index data from the City of Houston, via communication with the Director of Innovation, Jesse Bounds <br />

From this data, we explore potential correlations and generate a table with all relevant information.

## Current Project Status

We are currently in the exploration stage of the data science pipeline for the potholes and weather, with some early modeling in the form of correlations.
For flooding data, we recently received access to data from Rice's UrbanInstitute so we are in wrangling and exploration.

## Installing
How to install here

## Usage
### Data Gathering

Fill in here

### Data Visualization

run python runtime/util/DataViz to see visualizations on:

1. A pothole count vs time bar graph for a specific year
2. The average overdue time to repair a pothole vs time for a given year
3. A count vs channel type bar graph for potholes where channel Type is the method of
 reporting a potholes i.e. Web, Phone, etc.

run python runtime/util/WeatherVSPothole to see visualization on:

- The recorded temperature and precipitation recorded at a specific weather station and the
number of potholes that formed around this weather station (within a specified radius) during 
this time
