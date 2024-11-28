from flask import Flask, jsonify
from TrafficModel import TrafficModel

"""
Import the mapBuild module and the necessary files to create the model.
"""
from mapBuild.parkingSpots import parking_spots
from mapBuild.buildings import buildings_coords
from mapBuild.trafficLights import traffic_light_coords

from mapBuild.leftCoords import left_coords
from mapBuild.rightCoords import right_coords
from mapBuild.upCoords import up_coords
from mapBuild.downCoords import down_coords

from mapBuild.downLeftCoords import down_left_coords
from mapBuild.downRightCoords import down_right_coords
from mapBuild.upLeftCoords import up_left_coords
from mapBuild.upRightCoords import up_right_coords

from mapBuild.monitoring_coords import monitoring_coords

# Storing the coordinates in a dictionary
coords = {
    "left_coords": left_coords,
    "right_coords": right_coords,
    "up_coords": up_coords,
    "down_coords": down_coords,
    "down_left_coords": down_left_coords,
    "down_right_coords": down_right_coords,
    "up_left_coords": up_left_coords,
    "up_right_coords": up_right_coords,
    "monitoring_coords": monitoring_coords,
}

# Initialize the Flask application
app = Flask(__name__)


# Initialize the TrafficModel with the specified parameters
model = TrafficModel(
    num_agents=10,
    width=24,
    height=24,
    coords=coords,
    buildings_coords=buildings_coords,
    parking_coords=parking_spots,
    traffic_light_coords=traffic_light_coords,
)


cars = None
trafficLights = None


@app.route("/test")
def index():
    """
    Default route that returns a simple JSON message.
    """
    global cars, trafficLights
    model.step()
    cars, trafficLights = model.get_global_map()
    return jsonify({"Step": model.steps})


@app.route("/TestCars")
def get_cars():
    global cars
    return jsonify(cars)


@app.route("/TestTrafficLights")
def get_trafficLights():
    global trafficLights
    model.step()
    return jsonify(trafficLights)


@app.route("/global_map")
def get_global_map():
    """
    Route to get the global map of the model.
    """
    # Run the model for a specified number of steps and store the global map
    model.step()
    # Obtén el mapa global
    global_map = model.get_global_map()
    # Envolver el mapa en una lista
    return jsonify({"global_map": [global_map]})


if __name__ == "__main__":
    # Run the Flask application on localhost at port 3000
    app.run(host="127.0.0.1", port=3000, debug=True)
