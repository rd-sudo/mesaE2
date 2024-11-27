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

from CarAgent import CarAgent
from TrafficLightAgent import TrafficLightAgent



# Initialize the Flask application
app = Flask(__name__)


# Initialize the TrafficModel with the specified parameters
model = TrafficModel(
    num_agents=10,
    width=24,
    height=24,
    left_coords= left_coords,
    right_coords=right_coords,
    up_coords=up_coords,
    down_coords=down_coords,
    buildings_coords=buildings_coords,
    parking_coords=parking_spots,
    traffic_light_coords=traffic_light_coords
)

cars = None
trafficLights = None


@app.route("/")
def index():
    """
    Default route that returns a simple JSON message.
    """
    global cars, trafficLights
    model.step()
    cars, trafficLights = model.get_global_map()
    return jsonify({"Step": model.steps})


@app.route("/cars")
def get_cars():
    global cars
    return jsonify(cars)


@app.route("/trafficLights")
def get_trafficLights():
    global trafficLights
    model.step()
    return jsonify(trafficLights)


if __name__ == "__main__":
    # Run the Flask application on localhost at port 3000
    app.run(host="127.0.0.1", port=3000, debug=True)
