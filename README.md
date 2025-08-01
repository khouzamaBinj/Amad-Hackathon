# 🍯 HoneyWall
# 🛡️ Saudi PhishGuard

**HoneyWall** is a Chrome Extension designed to detect phishing websites, with a focus on targeting Saudi fintech platforms. It combines real-time browser-based phishing detection with a backend threat intelligence system inspired by Honeynet's Honeywall.

---

##  🚀  Key Features
🧠 Real-Time Phishing Detection
Automatically analyzes websites as you visit them, detecting phishing behavior instantly.

🔍 Heuristic-Based URL Analysis
Evaluates URLs using static features such as:

Use of IP addresses

Suspicious keywords

HTTPS presence

Length and entropy

🤖 ML-Powered Risk Scoring
Extracted features are sent to a Flask backend with a trained ML model to determine phishing likelihood.

📡 Backend Logging for Threat Intelligence
Every detection (auto or manual) is logged via API into structured .csv files, enabling data-driven insights for FinTech institutions.

🌐 Local Threat Mapping for Saudi FinTech
Tailored to detect phishing attempts targeting major Saudi banking and financial services.

🧱 Modular Architecture
Clean separation between Chrome extension (frontend) and Python backend (Flask), allowing future integration of:

WHOIS caching

External threat feeds

AI behavioral analysis

🧪 Future Plans:

Phishing sandbox environment for safe testing and interaction logging

Deeper AI-based behavioral detection beyond URL patterns

Integration with banking SOC dashboards or APIs

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
