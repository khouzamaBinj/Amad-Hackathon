import re
import socket
import whois
from urllib.parse import urlparse
from datetime import datetime

suspicious_keywords = [
    "verify", "update", "confirm", "urgent", "suspended",
    "blocked", "expire", "alert", "warning", "secure",
    "validate", "authenticate", "hack", "phishing", "fake"
]

def get_domain(url):
    try:
        return urlparse(url).hostname
    except:
        return ""

def get_domain_age(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
        if creation_date:
            return (datetime.now() - creation_date).days
    except Exception as e:
        print(f"⚠️ WHOIS failed for {domain}: {e}")
    return 7  # fallback: assume it's new (young = risky)

def check_ip_mismatch(domain):
    try:
        resolved_ip = socket.gethostbyname(domain)
        w = whois.whois(domain)

        whois_ips = []
        if hasattr(w, "emails") and w.emails:
            whois_ips = [socket.gethostbyname(e.split("@")[-1]) for e in w.emails if "@" in e]
        elif hasattr(w, "registrar") and w.registrar:
            whois_ips = [socket.gethostbyname(w.registrar)]

        if resolved_ip and whois_ips:
            return int(resolved_ip not in whois_ips)
    except Exception as e:
        print(f"⚠️ IP mismatch check failed for {domain}: {e}")
    return 1  # fallback: assume mismatch (some suspicion)

def extract_features(url):
    domain = get_domain(url)

    return {
        "contains_https": url.startswith("https://"),
        "has_ip": domain.replace('.', '').isdigit() if domain else False,
        "has_suspicious_words": any(word in url.lower() for word in suspicious_keywords),
        "url_length": len(url),
        "num_dots": url.count("."),
        "is_mobile_site": domain.startswith("m.") if domain else False,
        "password_field_detected": 0,
        "domain_age": get_domain_age(domain),
        "ip_mismatch": check_ip_mismatch(domain)
    }
