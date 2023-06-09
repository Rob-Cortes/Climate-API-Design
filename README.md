# Climate API Design
This is a climate analysis of Honolulu in Python and SQLAlchemy, along with a Flask API for accessing the climate data. 

### Set-Up
First we call the SQLAlchemy create_engine() function to connect to the SQLite database (path is in the Resources folder).

We then call the automap_base() function to reflect the database tables into classes, called 'station' and 'measurement'.

Lastly, we create our SQLAlchemy session by calling the Session() function.

### Precipitation Analysis
The first step in the precipitation analysis is to find the most recent date in the dataset and querying the previous 12 months of data.

We then load the query results into a Pandas DataFrame, and sort the DataFrame values by "date".

Lastly, we plot the results by using the DataFrame .plot() method...

![image](https://github.com/Rob-Cortes/sqlalchemy-challenge/assets/124944383/460a707a-b9af-4f6d-b8de-622e4d183708)

...and print summary statistics using .describe().

![image](https://github.com/Rob-Cortes/sqlalchemy-challenge/assets/124944383/39bf6b67-4f1e-4259-a35e-f6d5ecd831de)

### Station Analysis
The station analysis finds temperature observations for the most active climate stations. 

First, we list the stations and observation counts in descending order. This allows us to identify the station with the most observations.  

Next, we write a query that calculates the lowest, highest, and average temperatures that filters on the id of the most active station. We also write a query to get the previous 12 months of temperature observation (TOBS) data.

Lastly, we plot a histogram of the temperature observations, as shown in the following image:

![image](https://github.com/Rob-Cortes/sqlalchemy-challenge/assets/124944383/68cf5d31-b2f0-4628-9245-a78560c84ab1)

### Design Your Climate App
In this section, we design a Flask API based on the queries above.

First, we list all the available routes on the homepage. The routes do the following:

/api/v1.0/precipitation

Converts the query results from the precipitation analysis to a dictionary using date as the key and prcp as the value. Returns a JSON representation of the dictionary.

/api/v1.0/stations

Returns a JSON list of stations.

/api/v1.0/tobs

Queries the dates and temperature observations of the most active station for the previous year of data. Temperature observations returned as a JSON list.

/api/v1.0/<start> and /api/v1.0/<start>/<end>

Returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
For a specified start, calculates TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
For a specified start date and end date, calculates TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
