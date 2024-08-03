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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
# Base.prepare(autoload_with = engine)
Base.prepare(autoload_with = engine, reflect=True)
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

#last 12 month variable 
prev_year_date = '2016-08-23'
#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt/&lt;end&gt")

#Define route to retrieve stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_list = session.query(Station.station, Station.name).all()
    session.close()
    #Convert the query results into dictionary
    stat_dict = [{"station":station, "name":name} for station, name in station_list]

    return jsonify(stat_dict)
    
# Return a JSON list of Temperature Observations (tobs) for the previous year
# Adding routes for /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobstobs = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= prev_year_date).all()
    session.close()

    temperature_dict = [{"date":date, "Station": station, "Temperature Observations":tobs} for date, station, tobs in tobstobs]
    return jsonify(temperature_dict)

@app.route("/api/v1.0/<start>")
def start_date(start):
    
    session = Session(engine)
    
    temperature_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close()

    temperature_stats = {"TMIN": temperature_data[0][0], "TAVG": temperature_data[0][1], "TMAX": temperature_data[0][2]}
    return jsonify(temperature_stats)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)
    
    temperature_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()
    
    session.close()

    temperature_stats = {"TMIN": temperature_data[0][0], "TAVG": temperature_data[0][1], "TMAX": temperature_data[0][2]}
    return jsonify(temperature_stats)

if __name__ == "_main_":
    app.run(debug=True)

#  Old Code DONOT RUN
# def precipitation():
#     session = Session(engine)
#     most_recent_date =
# session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
#     start_date = datetime.strptime(most_recent_date, &#39;%Y-%m-%d&#39;) -
# timedelta(days=365)
#     precipitation_data = session.query(Measurement.date,
# Measurement.prcp).filter(Measurement.date &gt;= start_date).all()
#     session.close()
#     precipitation_dict = {date: prcp for date, prcp in precipitation_data}
#     return jsonify(precipitation_dict)
# @app.route(&quot;/api/v1.0/stations&quot;)
# def stations():
#     session = Session(engine)
#     station_list = session.query(Station.station).all()
#     session.close()
#     return jsonify(station_list)
# # Adding routes for /api/v1.0/tobs, /api/v1.0/&lt;start&gt;, and
# /api/v1.0/&lt;start&gt;/&lt;end&gt;
# @app.route(&quot;/api/v1.0/tobs&quot;)
# def tobs():
#     session = Session(engine)
#     most_active_station = session.query(Measurement.station,
# func.count(Measurement.station)).\
#        
# group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).fi
# rst()[0]
#    
#     most_recent_date =
# session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

#     start_date = datetime.strptime(most_recent_date, &#39;%Y-%m-%d&#39;) -
# timedelta(days=365)
#    
#     temperature_data = session.query(Measurement.date, Measurement.tobs).\
#         filter(Measurement.station == most_active_station, Measurement.date &gt;=
# start_date).all()
#    
#     session.close()
#     temperature_dict = {date: tobs for date, tobs in temperature_data}
#     return jsonify(temperature_dict)
# @app.route(&quot;/api/v1.0/&lt;start&gt;&quot;)
# def start_date(start):
#     session = Session(engine)
#     start_date = datetime.strptime(start, &#39;%Y-%m-%d&#39;)
#    
#     temperature_data = session.query(func.min(Measurement.tobs),
# func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date &gt;= start_date).all()
#    
#     session.close()
#     temperature_stats = {&quot;TMIN&quot;: temperature_data[0][0], &quot;TAVG&quot;:
# temperature_data[0][1], &quot;TMAX&quot;: temperature_data[0][2]}
#     return jsonify(temperature_stats)
# @app.route(&quot;/api/v1.0/&lt;start&gt;/&lt;end&gt;&quot;)
# def start_end_date(start, end):
#     session = Session(engine)
#     start_date = datetime.strptime(start, &#39;%Y-%m-%d&#39;)
#     end_date = datetime.strptime(end, &#39;%Y-%m-%d&#39;)
#    
#     temperature_data = session.query(func.min(Measurement.tobs),
# func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date &gt;= start_date, Measurement.date &lt;=
# end_date).all()
#    
#     session.close()
#     temperature_stats = {&quot;TMIN&quot;: temperature_data[0][0], &quot;TAVG&quot;:
# temperature_data[0][1], &quot;TMAX&quot;: temperature_data[0][2]}
#     return jsonify(temperature_stats)
# if __name__ == &quot;__main__&quot;:

#     app.run(debug=True)

#     return jsonify(station_list)