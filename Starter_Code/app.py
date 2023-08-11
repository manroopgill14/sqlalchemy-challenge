# Import the dependencies.
import numpy as np 
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table

Station = Base.classes.station
Measurement = Base.classes.measurement
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
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1./start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def Precipitation():
    
    # results = session.query(Measurement.prcp, Measurement.date).\
    # filter(Measurement.date > '2016-08-23').\
    # order_by(Measurement.date).all()
    # session.close()
    # prcp_results = {date: x for date, x in results}
    # print(prcp_results)
    # return jsonify(prcp_results)
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()

    session.close()
    # Dict with date as the key and prcp as the value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def Stations():
    """Return a list of stations."""
    results = session.query(Station.station).all()

    session.close()

    # Unravel results into a 1D array and convert to a list
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

    # stns = session.query(Station.station).all()
    # session.close()
    # station_list = list(np.ravel(stns))
    # return jsonify(stations = station_list)


@app.route("/api/v1.0/tobs")
def Most_Active():

    
    tobs = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2017,8,23').all()
    session.close()
    tobs_list = list(np.ravel(tobs))
    return jsonify (tobs_list)



@app.route("/api/v1./<start>")
@app.route ("/api/v1.0/<start>/<end>")
def Start_End():
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
         #code for just start value
         start_date = dt.datetime.strptime(start,'%Y-%m-%d')

    #code for start and end values
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    prev_year = dt.timedelta(days=365)
    start = start_date - prev_year
    end = end_date = prev_year

    time_period = session.query(func.min(Measurements.tobs), func.ave(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    session.close()
    prd = list(np.ravel(trip_data))
    return jsonify(prd)


if __name__ == '__main__':
    app.run(debug=True)