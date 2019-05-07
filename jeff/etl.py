import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from flask.ext.mongoalchemy import MongoAlchemy

import datetime as dt
import numpy as np


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


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
        f"/api/precipitation<br/>"
        f"/api/stations<br/>"
        f"/api/temperature<br/>"
        f"/api/<start><br/>"
        f"/api/<start>/<end>"
    )


@app.route("/api/precipitation")
def precipitation():
    """Return the amounts of precipitation"""
    # Query for precipitation on date
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Create a dictionary from the row data and append to a list of prcp data
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {date:prcp}
        all_prcp.append(prcp_dict)

        return jsonify(all_prcp)


@app.route("/api/stations")
def stations():
    """Return a list of stations from the dataset"""
    # Query all stations
    results = session.query(Station.station, Station.name).all()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name in results:
        station_dict = {station:name}
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/temperature")
def temps():
    """Return a list of the most recent year of temperature data from the dataset"""
    # Query all stations
    msmt = [Measurement.date, Measurement.tobs]

    past_year = session.query(*msmt).\
        filter(Measurement.date > year_ago_date).\
        order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list of all_temps
    all_temps = []
    for year in past_year:
        temp_dict = {year[0]:year[1]}
        all_temps.append(temp_dict)

    return jsonify(all_temps)


@app.route("/api/<start>")
def starting(start):
    """Return a list of the most recent year of temperature data from the dataset"""
    # Query all stations
    msmt = [Measurement.date, Measurement.tobs]

    from_date = session.query(*msmt).\
        filter(Measurement.date >= start).\
        order_by(Measurement.date).all()

    # Create a dictionary from the row data and calculate min, max, and avg temps since start date
    start_dict = {}
    start_dict["tmin"] = min(from_date)[1]
    start_dict["tmax"] = max(from_date)[1]
    start_dict["tavg"] = np.mean(float(from_date)[1])

    return jsonify(start_dict)


if __name__ == '__main__':
    app.run(debug=True)