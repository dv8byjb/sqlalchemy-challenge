import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import os 
os.chdir(os.path.dirname(os.path.abspath(__file__)))


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
session = Session(engine)
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():

    firstdate = dt.date(2017,8,23)-dt.timedelta(days=365)
    last12months = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date>=firstdate).all() 

   #precipitation_dic = {}
    # Convert list of tuples into normal list
   #for x in tobs_results:
      # temp_dict(x[0])= x[1]
    return jsonify(last12months)


@app.route("/api/v1.0/stations")
def names():
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations= list(np.ravel(results))

    return jsonify(all_stations)    


@app.route("/api/v1.0/tobs")
def passengers():
    # Create a dictionary from the row data and append to a list of all_passengers
    firstdate = dt.date(2017,8,23)-dt.timedelta(days=365)
    stnhightemp =session.query(Measurement.tobs).filter(Measurement.date>=firstdate).\
    filter(Measurement.station == "USC00519281").all()

    return jsonify(stnhightemp)


if __name__ == '__main__':
    app.run(debug=True)
