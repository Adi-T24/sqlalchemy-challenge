# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite://hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
# Base.prepare(autoload_with = engine)
Base.prepare(engine, reflect=True)
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station= Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route(&quot;/&quot;)
def home():
    return (

        f&quot;Welcome to the Climate Analysis API!&lt;br/&gt;&quot;
        f&quot;Available Routes:&lt;br/&gt;&quot;
        f&quot;/api/v1.0/precipitation&lt;br/&gt;&quot;
        f&quot;/api/v1.0/stations&lt;br/&gt;&quot;
        f&quot;/api/v1.0/tobs&lt;br/&gt;&quot;
        f&quot;/api/v1.0/&amp;lt;start&amp;gt;&lt;br/&gt;&quot;
        f&quot;/api/v1.0/&amp;lt;start&amp;gt/&amp;lt;end&amp;gt&quot;
    )
@app.route(&quot;/api/v1.0/precipitation&quot;)
def precipitation():
    session = Session(engine)
    most_recent_date =
session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    start_date = datetime.strptime(most_recent_date, &#39;%Y-%m-%d&#39;) -
timedelta(days=365)
    precipitation_data = session.query(Measurement.date,
Measurement.prcp).filter(Measurement.date &gt;= start_date).all()
    session.close()
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    return jsonify(precipitation_dict)
@app.route(&quot;/api/v1.0/stations&quot;)
def stations():
    session = Session(engine)
    station_list = session.query(Station.station).all()
    session.close()
    return jsonify(station_list)
# Adding routes for /api/v1.0/tobs, /api/v1.0/&lt;start&gt;, and
/api/v1.0/&lt;start&gt;/&lt;end&gt;
@app.route(&quot;/api/v1.0/tobs&quot;)
def tobs():
    session = Session(engine)
    most_active_station = session.query(Measurement.station,
func.count(Measurement.station)).\
       
group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).fi
rst()[0]
   
    most_recent_date =
session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    start_date = datetime.strptime(most_recent_date, &#39;%Y-%m-%d&#39;) -
timedelta(days=365)
   
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station, Measurement.date &gt;=
start_date).all()
   
    session.close()
    temperature_dict = {date: tobs for date, tobs in temperature_data}
    return jsonify(temperature_dict)
@app.route(&quot;/api/v1.0/&lt;start&gt;&quot;)
def start_date(start):
    session = Session(engine)
    start_date = datetime.strptime(start, &#39;%Y-%m-%d&#39;)
   
    temperature_data = session.query(func.min(Measurement.tobs),
func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date &gt;= start_date).all()
   
    session.close()
    temperature_stats = {&quot;TMIN&quot;: temperature_data[0][0], &quot;TAVG&quot;:
temperature_data[0][1], &quot;TMAX&quot;: temperature_data[0][2]}
    return jsonify(temperature_stats)
@app.route(&quot;/api/v1.0/&lt;start&gt;/&lt;end&gt;&quot;)
def start_end_date(start, end):
    session = Session(engine)
    start_date = datetime.strptime(start, &#39;%Y-%m-%d&#39;)
    end_date = datetime.strptime(end, &#39;%Y-%m-%d&#39;)
   
    temperature_data = session.query(func.min(Measurement.tobs),
func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date &gt;= start_date, Measurement.date &lt;=
end_date).all()
   
    session.close()
    temperature_stats = {&quot;TMIN&quot;: temperature_data[0][0], &quot;TAVG&quot;:
temperature_data[0][1], &quot;TMAX&quot;: temperature_data[0][2]}
    return jsonify(temperature_stats)
if __name__ == &quot;__main__&quot;:

    app.run(debug=True)

    return jsonify(station_list)