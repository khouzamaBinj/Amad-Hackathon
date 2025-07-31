from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib, csv, datetime
import pandas as pd

app = Flask(__name__)
CORS(app)
model = joblib.load("model/phishing_model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    url_features = extract_features(data['url'])
    prediction = model.predict([url_features])[0]
    return jsonify({"prediction": prediction})

@app.route("/report", methods=["POST"])
def report():
    data = request.json
    with open("logs.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.datetime.now(), data['url'], data['from_sms']])
    return "Logged"

def extract_features(url):
    # Simplified placeholder
    return [len(url), url.count("@"), url.count("-")]

if __name__ == "__main__":
    app.run(debug=True)