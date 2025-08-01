"""
HoneyWall – Flask backend
Serves:
  • /ml_score   → returns ML verdict & probability
  • /log        → appends basic telemetry to logs.csv
"""

# ───────────────────────────────────────── Imports
import os, csv, re, joblib
from urllib.parse import urlparse
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

from ai_model.features import extract_features   # our custom extractor

# ───────────────────────────────────────── Config
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))

# ML model (RandomForest + feature list)
MODEL_PATH = os.path.join(BASE_DIR, "ai_model", "phishing_model.pkl")
model, FEATURE_ORDER = joblib.load(MODEL_PATH)

# Simple CSV log
LOG_PATH = os.path.join(BASE_DIR, "logs.csv")

# Hard-coded allow-list
WHITELIST = {
    "alrajhibank.com.sa", "stcpay.com.sa", "alahli.com",   "riyadbank.com",
    "samba.com",          "bank.sa",      "anb.com.sa",    "alinma.com",
    "albilad.com.sa",     "bankaljazira.com",              "sab.com",
    "sabb.com",           "bsf.com.sa"
}
TRUSTED_SUFFIXES = {".gov.sa", ".edu.sa", ".gov", ".edu", ".sa"}

# ───────────────────────────────────────── Helpers
def _hostname(url: str) -> str:
    return (urlparse(url).hostname or "").lower()

def is_whitelisted(url: str) -> bool:
    host = _hostname(url)
    return any(host.endswith(dom) for dom in WHITELIST)

def _write_log(row: dict) -> None:
    file_exists = os.path.isfile(LOG_PATH)
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

# ───────────────────────────────────────── Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ---------------------- ML inference endpoint
@app.route("/ml_score", methods=["POST", "OPTIONS"])
def ml_score():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json() or {}
    url  = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    # a) short-circuit trusted domains
    if is_whitelisted(url):
        return jsonify({"verdict": "benign",
                        "score": 0.0,
                        "reason": "trusted domain"})

    # b) feature extraction (+ trusted TLD check)
    feats = extract_features(url)
    feats["trusted_tld"] = int(any(_hostname(url).endswith(sfx)
                                   for sfx in TRUSTED_SUFFIXES))

    # c) reorder to training order
    try:
        X = [feats.get(col, 0) for col in FEATURE_ORDER]
    except Exception as e:
        return jsonify({"error": f"Bad feature vector: {e}"}), 500

    # d) prediction
    try:
        prob = float(model.predict_proba([X])[0][1])
    except Exception as e:
        return jsonify({"error": f"Model inference failed: {e}"}), 500

    verdict = "phishing" if prob >= 0.70 else "benign"
    response = {"verdict": verdict, "score": round(prob, 2)}

    # e) optional log of every scored URL
    _write_log({
        "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
        "url": url,
        "indicator": verdict,
        "score": f"{prob:.2f}"
    })

    return jsonify(response)

# ---------------------- Light telemetry endpoint
@app.route("/log", methods=["POST"])
def log_endpoint():
    data = request.get_json() or {}
    _write_log({
        "timestamp": data.get("timestamp",
                              datetime.utcnow().isoformat(timespec="seconds")),
        "url":       data.get("url", ""),
        "indicator": data.get("indicator", ""),
        "score":     data.get("score", "")
    })
    return jsonify({"status": "logged"}), 200

# ───────────────────────────────────────── Entrypoint
if __name__ == "__main__":
    app.run(debug=True)
