# Import the dependencies.
import numpy as np 

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
#session = Session(engine)

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
        f"/api/v1./<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def Precipitation():
    session = Session(engine)
    results = session.query(Measurement.prcp, Measurement.date).\
    filter(Measurement.date > '2016-08-23').\
    order_by(Measurement.date).all()
    session.close()
    prcp_results = {date: x for date, x in results}
    return jsonify(prcp_results)



@app.route("/api/v1.0/stations")
def Stations():
    session = Session(engine)
    stns = session.query(Station.station).all().\
    session.close()
    station_list = list(np.ravel(stns))
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def Most_Active():

    session = Session(engine)
    tobs = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2017,8,23').all()
    session.close()
    tobs_list = list(np.ravel(tobs))
    return jsonify (tobs_list)


@app.route("/api/v1./<start>")
def Start():
    session = Session(engine)
    start_date = dt.datetime.strptime(start,'%Y-%m-%d')
    prev_year = dt.timedelta(days=365)
    start = start_date - prev_year
    end = dt.date(2017,8,23)
    date_period = session.query(func.min(Measurements.tobs), func.ave(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    session.close()
    period = list(np.ravel(date_period))
    return jsonify(period)

@app.route ("/api/v1.0/<start>/<end>")
def Start_End():
    session = Session(engine)
    start_date = dt.datetime.strptime(start,'%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    prev_year = dt.timedelta(days=365)
    start = start_date - prev_year
    end = end_date = prev_year
    time_period = session.query(func.min(Measurements.tobs), func.ave(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    session.close()
    prd = list(np.ravel(trip_data))
    return jsonify(trip)


if __name__ == '__main__':
    app.run(debug=True)