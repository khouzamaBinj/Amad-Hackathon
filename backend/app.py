from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Log file path
LOG_FILE = 'logs.csv'

# Setup basic logging for your backend (for server visibility)
logging.basicConfig(level=logging.INFO)

@app.route('/log', methods=['POST'])
def log_data():
    try:
        data = request.get_json()

        # Validate required fields
        if not all(k in data for k in ('timestamp', 'url', 'indicator')):
            return jsonify({"error": "Missing required fields"}), 400

        # Optional: validate timestamp format
        try:
            datetime.fromisoformat(data['timestamp'].replace("Z", ""))
        except ValueError:
            return jsonify({"error": "Invalid timestamp format"}), 400

        # Print for debugging
        app.logger.info(f"📥 Received phishing signal: {data}")

        # Check if CSV file exists
        file_exists = os.path.isfile(LOG_FILE)

        with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Write headers if this is a new file
            if not file_exists:
                writer.writerow(['timestamp', 'url', 'indicator'])

            # Write the log entry
            writer.writerow([data['timestamp'], data['url'], data['indicator']])

        return jsonify({"status": "received"}), 200

    except Exception as e:
        app.logger.error(f"❌ Failed to log data: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Use 0.0.0.0 to make it reachable from external devices (e.g., phones or VMs)
    app.run(host='0.0.0.0', port=5000, debug=True)
