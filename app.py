"""
Flask APP for ride share application
"""

from flask import Flask, jsonify, request
import json
import traceback
from models.user import User
from ride import RideManager
from models.in_memory_data import MemoryData

memory_data = MemoryData.instance()

app = Flask(__name__)

@app.route("/")
def welcome():
    return jsonify(status="success")

@app.route("/user", methods=["POST"])
def onboard_user():
    try:
        data = json.loads(request.data)
        if User.register_user(data):
            print "Successfully Add user"
            print memory_data.users
            return jsonify(status="success")
    except:
        print traceback.format_exc()
        print "Error: invalid input data"
    return jsonify(status="error")

@app.route("/vehicle", methods=["POST"])
def onboard_vehicle():
    try:
        data = json.loads(request.data)
        if User.addVehicle(data):
            print memory_data.vehicles
            print "Successfully added vehicle"
            return jsonify(status="success")
    except:
        print traceback.format_exc()
        print "Error: invalid input data"
    return jsonify(status="error")

@app.route("/ride/start", methods=["POST"])
def start_ride():
    try:
        data = json.loads(request.data)
        ride_mgr = RideManager.instance()
        if ride_mgr.start_ride(data):
            print "Successfully started ride"
            return jsonify(status="success")
    except:
        print traceback.format_exc()
        print "Error: invalid input data"
    return jsonify(status="error")

@app.route("/ride/stop", methods=["POST"])
def stop_ride():
    try:
        data = json.loads(request.data)
        ride_mgr = RideManager.instance()
        if ride_mgr.stopRide(data):
            print "Successfully stopped ride"
            return jsonify(status="success")
    except:
        print traceback.format_exc()
        print "Error: invalid input data"
    return jsonify(status="error")


@app.route("/ride/request", methods=["POST"])
def requst_ride():
    try:
        data = json.loads(request.data)
        ride_mgr = RideManager.instance()
        if ride_mgr.requestRide(data):
            print "Successfully assigned ride"
            return jsonify(status="success")
    except:
        print traceback.format_exc()
        print "Error: invalid input data"
    return jsonify(status="error")

@app.route('/reports', methods=["GET"])
def reports():
    try:
        if "user_id" not in request.args:
            print "provide user_id"
            return jsonify(status="error")
        ride_mgr = RideManager.instance()
        reports = ride_mgr.reports(request.args["user_id"])
        return jsonify(status="success", reports=reports)
    except:
        print traceback.format_exc()
        print "Error: invalid input data"
    return jsonify(status="error")


if __name__ == "__main__":
    app.run()
