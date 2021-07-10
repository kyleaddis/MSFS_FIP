from flask import Flask, render_template, jsonify
from SimConnect import *
from SimConnect.simconnect_mobiflight import SimConnectMobiFlight
from SimConnect.mobiflight_variable_requests import MobiFlightVariableRequests
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Create simconnection
sm = SimConnect()
ae = AircraftEvents(sm)
aq = AircraftRequests(sm, _time=10)


# Create request holders
# These are groups of datapoints which it is convenient to call as a group because they fulfill a specific function
request_location = [
    'PLANE_ALTITUDE',
    'PLANE_LATITUDE',
    'PLANE_LONGITUDE',
]

request_compass = [
    'WISKEY_COMPASS_INDICATION_DEGREES',
    'PARTIAL_PANEL_COMPASS',
    'ADF_CARD',  # ADF compass rose setting
    'MAGNETIC_COMPASS',  # Compass reading
    'INDUCTOR_COMPASS_PERCENT_DEVIATION',  # Inductor compass deviation reading
    'INDUCTOR_COMPASS_HEADING_REF',  # Inductor compass heading
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/status')
def status():
    if sm:
        return jsonify({"STATUS": "RUNNING"})
    else:
        return jsonify({"STATUS": "ERROR"})


@app.route('/sixpack')
async def alt():
    try:
        altitude = await aq.get("PLANE_ALTITUDE")
        return jsonify(altitude)
    except:
        return jsonify({"Error": "Sim not running"})


@app.route('/location', methods=["GET"])
async def output_json_dataset():
    dataset_map = {}

    # This uses get_dataset() to pull in a bunch of different datapoint names into a dictionary which means they can
    # then be requested from the sim
    # data_dictionary = get_dataset(dataset_name)

    for datapoint_name in request_location:
        print(datapoint_name)
        dataset_map[datapoint_name] = await aq.get(datapoint_name)
    response = jsonify(dataset_map)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


app.run()
