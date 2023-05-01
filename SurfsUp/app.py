# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate<br/>"
        f"/api/v1.0/startdate/enddate<br/>"
        f"DATES MUST BE ENTERED IN THE FOLLOWING FORMAT: YYYY-M-D"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to set start date
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    end_date = dt.datetime.strptime(latest_date[0], '%Y-%m-%d').date()
    start_date = end_date - dt.timedelta(days=365)

    # Query precipitation data
    qry_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= start_date).\
        order_by(Measurement.date.desc()).all()

    # Close session
    session.close()
    
    # Create a dictionary from the query results
    prcp_data = []
    for result in qry_results:
        prcp_dict = {}
        prcp_dict[result[0]] = result[1]
        prcp_data.append(prcp_dict)
    
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query station names
    qry_results = session.query(Station.name).all()

    # Close session
    session.close()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(qry_results))

    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to set start date
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    end_date = dt.datetime.strptime(latest_date[0], '%Y-%m-%d').date()
    start_date = end_date - dt.timedelta(days=365)

    # Query to find most active station for the previous year of data
    station_counts = session.query(Measurement.station, func.count(Measurement.station)).\
        filter(Measurement.date >= start_date).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()
    
    most_active = station_counts[0][0]

    # Query to retrieve temperature observations and dates
    qry_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.station==most_active).\
        order_by(Measurement.date.desc()).all()
    
    # Close session
    session.close()

    # Create a dictionary from the query results
    temp_data = []
    for result in qry_results:
        temp_dict = {}
        temp_dict[result[0]] = result[1]
        temp_data.append(temp_dict)
    
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>")
def tobs_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert given date string into date object
    start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()

    # Query temperature observations
    qry_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    # Close session
    session.close()

    # Create a dictionary from the query results
    temp_data = []
    for result in qry_results:
        temp_dict = {}
        temp_dict['TMIN'] = result[0]
        temp_dict['TAVG'] = result[2]
        temp_dict['TMAX'] = result[1]
        temp_data.append(temp_dict)
    
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def tobs_range(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert given date strings into date objects
    start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()

    # Query temperature observations
    qry_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()

    # Close session
    session.close()

    # Create a dictionary from the query results
    temp_data = []
    for result in qry_results:
        temp_dict = {}
        temp_dict['TMIN'] = result[0]
        temp_dict['TAVG'] = result[2]
        temp_dict['TMAX'] = result[1]
        temp_data.append(temp_dict)
    
    return jsonify(temp_data)



if __name__ == '__main__':
    app.run(debug=True)
