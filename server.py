from flask import Flask, jsonify

app = Flask(__name__)

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


@app.route("/")
def index():
    return jsonify({"Message": "Hello World"})   
        
    

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8000,  debug=True)
