from flask import Flask, redirect, url_for, render_template, request, jsonify
from predict import predict

app = Flask(__name__)


@app.route("/")
def home():
    return "Home"


@app.route("/predict_home_price", methods=["POST"])
def predict_home_price():
    # Get form data
    area_type = request.form["area_type"]
    availability = request.form["availability"]
    location = request.form["location"]
    size = int(request.form["size"])
    total_sqft = float(request.form["total_sqft"])
    bath = int(request.form["bath"])

    # area_type = "Super_built_up_Area"
    # availability = "Not Ready to Move"
    # location = "Devarachikkanahalli"
    # size = 3
    # total_sqft = 1250
    # bath = 2

    # Predict home price with our ML model
    pred_price = predict(area_type, availability, location, size, total_sqft, bath)

    # Create response
    response = jsonify(str({"estimated_price": pred_price}))

    response.headers.add("Access-Control-Allow-Origin", "*")

    # return str(pred_price)
    return response


if __name__ == "__main__":
    app.run(debug=True)
