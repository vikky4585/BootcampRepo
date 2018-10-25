from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
import datetime as dt

app = Flask(__name__)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
prcp_data = session.query(Measurement.date,Measurement.station,Measurement.prcp,Measurement.tobs).\
    filter(Measurement.date >= year_ago).\
    order_by(Measurement.date.desc()).all()


def calc_temps(start_date, end_date):
    
    temp_session = Session(engine)

    return temp_session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

@app.route("/api/v1.0/precipitation")
def getdetails():
    details ={}
    for data in prcp_data:
        details[data.date] = data.tobs
    
    return jsonify(details)

@app.route("/api/v1.0/stations")
def stations():
    st = []
    for data in prcp_data:
            st.append(data.station)
    return jsonify(st)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs = []
    for data in prcp_data:
            tobs.append(data.tobs)
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def startdate(start):
        enddate = '2017-08-23'
        data = calc_temps(start,enddate)
        d = {}
        d['tmin'] = data[0][0]
        d['tavg'] = data[0][1]
        d['tmax'] = data[0][2]    
        print(f'data fetched {d}')
        return jsonify(d)

@app.route("/api/v1.0/<start>/<end>")
def startenddate(start,end):
        data = calc_temps(start,end)
        d = {}
        d['tmin'] = data[0][0]
        d['tavg'] = data[0][1]
        d['tmax'] = data[0][2]    
        print(f'data fetched {d}')
        return jsonify(d)
        

if __name__ == "__main__":
    app.run(debug=True)