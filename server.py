from flask import Flask, jsonify
from model import TrafficModel
app = Flask(__name__)
from mainGood import left_coords, right_coords, up_coords, down_coords, buildings_coords, parking_spots


''' 
@app.route("/positions", methods = ["GET", "POST"])
def positions():
    boids.step()
    pos = boids.getPositions()
    loc = []
    for p in pos:
        loc.append({"x":p[0], "z":p[1]})
    loc = {"points" : loc}
    return jsonify(loc)
'''
initial_model = TrafficModel(
    num_agents=5,
    width=24,
    height=24,
    left_coords= left_coords,
    right_coords=right_coords,
    up_coords=up_coords,
    down_coords=down_coords,
    buildings_coords=buildings_coords,
    parkings_coords=parking_spots
)


@app.route("/")
def index():
    return jsonify({"Message": "Hello World"})   
        
    

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8000,  debug=True)
