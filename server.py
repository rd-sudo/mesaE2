from flask import Flask, jsonify
from TrafficModel import TrafficModel
import mapBuild
import mapBuild.buildings
import mapBuild.downCoords
import mapBuild.leftCoords
import mapBuild.parkingSpots
import mapBuild.rightCoords
import mapBuild.trafficLights
import mapBuild.upCoords

# Initialize the Flask application
app = Flask(__name__)

# Initialize the TrafficModel with the specified parameters
model = TrafficModel(
    width=24,
    height=24,
    num_agents=2,
    left_coords=mapBuild.leftCoords.left_coords,
    right_coords=mapBuild.rightCoords.right_coords,
    up_coords=mapBuild.upCoords.up_coords,
    down_coords=mapBuild.downCoords.down_coords,
    buildings_coords=mapBuild.buildings.buildings_coords,
    parking_coords=mapBuild.parkingSpots.parking_spots,
    traffic_light_coords=mapBuild.trafficLights.traffic_light_coords,
)

# Run the model for a specified number of steps and store the global map
global_map = []


@app.route("/")
def index():
    """
    Default route that returns a simple JSON message.
    """
    return jsonify({"Message": "Hello World"})


@app.route("/global_map")
def get_global_map():
    """
    Route to get the global map of the model.
    """
    # Run the model for a specified number of steps and store the global map
    model.step()
    return jsonify(model.get_global_map())


if __name__ == "__main__":
    # Run the Flask application on localhost at port 3000
    app.run(host="127.0.0.1", port=3000, debug=True)
