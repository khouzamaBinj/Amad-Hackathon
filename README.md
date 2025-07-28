# 🍯 HoneyWall
# 🛡️ Saudi PhishGuard

**HoneyWall** is a Chrome Extension designed to detect and report phishing websites, with a focus on targeting Saudi fintech platforms. It combines real-time browser-based phishing detection with a backend threat intelligence system inspired by Honeynet's Honeywall.

---

## 🚀 Features

- 🧠 **Real-time phishing detection** on page load
- 🔍 URL analysis using heuristics (keywords, typosquatting, etc.)
- 🧬 Integration with external threat intelligence sources
- 📡 Reporting and logging phishing attempts to a Flask-based API
- 🌐 Local threat mapping with support for Saudi banks and fintech services
- 🔬 Future Support: Phishing sandbox and AI-based analysis

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
saudi-phishguard/
│
├── manifest.json           # Chrome extension manifest (v3)
├── popup.js           # Background script for event handling
├── scanner.js              # URL analysis and phishing detection logic
├── popup.html              # Extension popup UI
├── styles.css               # Styling for popup
├── icon.png                # Extension icon
│
├── backend/
│   ├── app.py              # Flask API for phishing report intake
│   ├── logs.csv        # Local SQLite DB (or use MongoDB/PostgreSQL)
│   ├── requirements.txt
│   └── utils/              # Threat intelligence enrichment, sandboxing
│
├── dashboard/
│   └── dashboard.py
├── docs/
│   ├── tast_list.md
│   └── threat_model.md
│
└── README.md

