
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log_data():
    data = request.json
    print(data)  # Just for testing
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(debug=True)
