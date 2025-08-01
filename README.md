# 🍯 HoneyWall
# 🛡️ Saudi PhishGuard

**HoneyWall** is a Chrome Extension designed to detect phishing websites, with a focus on targeting Saudi fintech platforms. It combines real-time browser-based phishing detection with a backend threat intelligence system inspired by Honeynet's Honeywall.

---

## 🚀 Features
HoneyWall is a Chrome Extension + Flask Backend system designed to protect users and fintech institutions from phishing attacks, with a special focus on the Saudi ecosystem.

- 🧠 Real-Time Phishing Detection
Automatically scans websites on page load.

Flags potential phishing attempts before users interact with malicious content.

- 🔍 Heuristic-Based URL Analysis
Extracts and analyzes static features from URLs:

Presence of HTTPS

IP addresses in domain

Suspicious keywords

URL length, entropy, and character anomalies

- 🤖 Machine Learning Risk Scoring
Backend Flask API receives extracted features.

Predicts phishing risk using a trained ML model (phishing_model.pkl).

Returns verdict (phishing / benign) with confidence score.

- 📡 Threat Logging for Analysis
Every scan result is logged into logs.csv on the server.

Enables future threat intelligence and detection trend analysis.

- 🌐 Local FinTech Target Awareness
Custom rules and ML features tailored for phishing targeting:

Saudi banks

E-wallets

Fintech platforms

- 🧱 Modular Architecture
Frontend: Chrome Extension (popup.html, scanner.js, etc.)

Backend: Flask API (/ml_score, /log)

Easily extendable with:

WHOIS enrichment

Domain reputation APIs

Threat intelligence feeds

- 🔬 Future Enhancements
✅ Phishing sandbox environment for dynamic interaction logging

✅ AI-based behavioral analysis of page content and interaction patterns

✅ Dashboard for banks and SOC teams for real-time alerts and insights

---
## 🧪 How it Works
- When a user visits a page, scanner.js scans the URL and content.

- If phishing patterns are detected (e.g., keywords like mada-login, lookalike domains, etc.), the extension:

- Shows a warning in the popup

- Sends a report to the Flask API backend

- The backend logs the attempt, enriches it with open threat intel (e.g., OpenPhish, PhishTank), and stores it for analysis.




---
## 🗂️ Project Structure

```bash
Amad-Hackathon/
├── backend/       # Flask backend server 
│   ├── ai_model/
│   │      ├── dataset.csv
│   │      ├── features.py
│   │      ├── generate_dataset.py
│   │      ├── generate_whois_cache.py
│   │      ├── phishing_model.pkl
│   │      ├── train_model.py
│   │      └── whois_cache.csv
│   ├── app.py
│   ├── payload.json          ← sample JSON for curl testing
│   ├── requirements.txt     
│   └── log.csv
├── chrome-extension/    # Chrome extension for phishing detection
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   ├── scanner.js
│   └── styles.css
├── dashboard/           # Streamlit dashboard to display phishing logs
│   └── dashboard.py
├── docs/                # Threat model, notes, task list
│   ├── threat_model.md
│   └── task_list.md
└── README.md
