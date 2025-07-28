
from flask import Flask, request, jsonify
from flask_cors import CORS 
import csv
import os

app = Flask(__name__)
CORS(app)
LOG_FILE = 'logs.csv'

@app.route('/log', methods=['POST'])
def log_data():
    data = request.json
    print(f"Received: {data}")  # For debug

    # Save to CSV
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['timestamp', 'url', 'indicator'])  # Write headers
        writer.writerow([data['timestamp'], data['url'], data['indicator']])

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(debug=True)
