from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)
LOG_PATH = "logs.csv"

@app.route('/log', methods=['POST'])
def log_data():
    data = request.json
    print("📥 Data received:", data)

    required_fields = ["timestamp", "url", "indicator"]
    row = {key: data.get(key, "") for key in required_fields}

    # Append to CSV safely
    file_exists = os.path.isfile(LOG_PATH)
    with open(LOG_PATH, mode='a', newline='\n', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=required_fields)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    return jsonify({"status": "logged"}), 200

if __name__ == '__main__':
    app.run(debug=True)


