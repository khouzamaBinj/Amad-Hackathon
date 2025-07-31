import re
from urllib.parse import urlparse

suspicious_keywords = [
    "verify", "update", "confirm", "urgent", "suspended", 
    "blocked", "expire", "alert", "warning", "secure",
    "validate", "authenticate", "hack", "phishing", "fake"
]

from urllib.parse import urlparse

def extract_features(url):
    parser = urlparse(url)
    suspicious_words = [
        "verify", "update", "confirm", "urgent", "suspended",
        "blocked", "expire", "alert", "warning", "secure",
        "validate", "authenticate", "hack", "phishing", "fake"
    ]

    return {
        "contains_https": url.startswith("https://"),
        "has_ip": parser.hostname and parser.hostname.replace('.', '').isdigit(),
        "has_suspicious_words": any(word in url.lower() for word in suspicious_words),
        "url_length": len(url),
        "num_dots": url.count("."),
        "is_mobile_site": parser.hostname.startswith("m.") if parser.hostname else False,
        "password_field_detected": 0 
    }
