import json
from flask import Flask, request, jsonify, url_for, render_template
from utils.predict import predict
from utils.utils import get_possible_locations, area_type_map, availability_map

app = Flask(__name__)


# Home page
@app.route("/", methods=["GET", "POST"])
def predict_home_price():

    if request.method == "POST":
        # Get form data

        # -1: np.nan, 0: Super built-up area, 1: Built-up area, 2: Plot area, 3: Carpet area
        area_type_indices = int(request.form["area_type"])
        # -1: np.nan, 0: Ready to Move In, 1: Not Ready to Move In
        availability_indices = int(request.form["availability"])

        location = request.form["location"]
        size = int(request.form["size"])
        total_sqft = float(request.form["total_sqft"])
        bath = int(request.form["bath"])

        # map levels of area_type and availability
        area_type = area_type_map[area_type_indices + 1]
        availability = availability_map[availability_indices + 1]

        # Predict home price with our ML model
        predictions = predict(area_type, availability, location, size, total_sqft, bath)

        # pred_price is currently in np.float, need to convert this
        # to python float so that it can be converted to a JSON string
        # aka JSON serializable
        # res is a 1-D list of predictions (normally there X elements in this list, where X is the
        # number of rows in X_test)
        pred_price = predictions[0]
        pred_price = float(pred_price)
        pred_price = round(pred_price, 2)

        # Create response
        response = jsonify({"estimated_price": pred_price})
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response

    elif request.method == "GET":
        """User is viewing the page"""
        return render_template("index.html")


# Get possible locations
@app.route("/get_possible_locations")
def get_locations():
    response = jsonify({"possible_locations": get_possible_locations()})
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


if __name__ == "__main__":
    app.run(debug=True)
