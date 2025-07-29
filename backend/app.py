from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)
LOG_PATH = "backend/logs.csv"

@app.route('/log', methods=['POST'])
def log_data():
    data = request.json
    print("📥 Data received:", data)

    # Create CSV if not exists, then write row
    file_exists = os.path.isfile(LOG_PATH)
    with open(LOG_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["timestamp", "url", "indicator"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": data.get("timestamp"),
            "url": data.get("url"),
            "indicator": data.get("indicator")
        })

    return jsonify({"status": "saved"}), 200

if __name__ == '__main__':
    app.run(debug=True)

