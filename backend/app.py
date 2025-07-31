from flask import Flask, request, jsonify
from flask_cors import CORS
import csv, os, joblib
from urllib.parse import urlparse

# ✅ Import custom feature extractor
from ai_model.features import extract_features

# ✅ Flask app setup
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ✅ Load ML model
model_path = os.path.join(os.path.dirname(__file__), "ai_model", "phishing_model.pkl")
model, feature_names = joblib.load(model_path)

LOG_PATH = "logs.csv"

# ✅ Whitelist of trusted domains
WHITELIST = [
    "alrajhibank.com.sa", "stcpay.com.sa", "alahli.com", "riyadbank.com",
    "samba.com", "bank.sa", "anb.com.sa", "alinma.com", "albilad.com.sa",
    "bankaljazira.com", "sab.com", "sabb.com", "bsf.com.sa"
]

def is_whitelisted(url):
    try:
        parsed = urlparse(url)
        domain = parsed.hostname or ""
        return any(allowed in domain for allowed in WHITELIST)
    except Exception:
        return False

# --------------------------
@app.route("/ml_score", methods=["POST", "OPTIONS"])
def ml_score():
    if request.method == "OPTIONS":
        return '', 204  # Preflight CORS response

    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON payload"}), 400

    # ✅ Skip trusted domains
    if is_whitelisted(data.get("url", "")):
        return jsonify({
            "verdict": "benign",
            "score": 0.0,
            "reason": "trusted domain"
        })

    try:
        features = [
            data["contains_https"],
            data["has_ip"],
            data["has_suspicious_words"],
            data["is_mobile_site"],
            data["length"],
            data["num_dots"],
            data["password_field_detected"]
        ]
    except KeyError as e:
        return jsonify({"error": f"Missing feature: {str(e)}"}), 400

    try:
        score = model.predict_proba([features])[0][1]
        verdict = "phishing" if score >= 0.7 else "benign"
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

    # ✅ Log to terminal
    print(f"\n🌐 URL: {data.get('url')}")
    print(f"🤖 Score: {score:.2f}")
    print(f"🔍 Verdict: {verdict}")

    return jsonify({
        "verdict": verdict,
        "score": round(score, 2)
    })


# --------------------------
@app.route("/log", methods=["POST"])
def log_data():
    data = request.json
    print("📥 Data received:", data)

    _log({
        "timestamp": data.get("timestamp", ""),
        "url": data.get("url", ""),
        "indicator": data.get("indicator", "")
    })

    return jsonify({"status": "logged"}), 200

# --------------------------
def _log(row):
    file_exists = os.path.isfile(LOG_PATH)
    with open(LOG_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

# --------------------------
if __name__ == '__main__':
    app.run(debug=True)
