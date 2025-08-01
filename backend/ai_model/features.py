import re
import socket
import pandas as pd
from urllib.parse import urlparse

# Load cached WHOIS data once
import os
script_dir = os.path.dirname(__file__)
cache_path = os.path.join(script_dir, "whois_cache.csv")
try:
    whois_cache = pd.read_csv(cache_path).set_index("domain")
except:
    whois_cache = pd.DataFrame(columns=["domain_age", "ip_mismatch"]).set_index("domain")


trusted_suffixes = [
    ".edu", ".gov", ".mil", ".edu.sa", ".gov.sa", ".mil.sa", ".org.sa", ".sa"
]

def has_trusted_tld(domain):
    return any(domain.endswith(suffix) for suffix in trusted_suffixes)

# Suspicious words often used in phishing URLs
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

def get_cached_whois(domain):
    if domain in whois_cache.index:
        age = whois_cache.loc[domain, "domain_age"]
        mismatch = whois_cache.loc[domain, "ip_mismatch"]
        return int(age), int(mismatch)
    else:
        return 7, 1  # Fallback defaults

def extract_features(url):
    if not url or not isinstance(url, str) or url.strip() == "":
        return {
            "contains_https": 0,
            "has_ip": 0,
            "has_suspicious_words": 0,
            "url_length": 0,
            "num_dots": 0,
            "is_mobile_site": 0,
            "password_field_detected": 0,
            "domain_age": 7,
            "ip_mismatch": 1
            
        }

    domain = get_domain(url)
    domain_age, ip_mismatch = get_cached_whois(domain)

    return {
        "contains_https": url.startswith("https://"),
        "has_ip": domain.replace('.', '').isdigit() if domain else False,
        "has_suspicious_words": any(word in url.lower() for word in suspicious_keywords),
        "url_length": len(url),
        "num_dots": url.count("."),
        "is_mobile_site": domain.startswith("m.") if domain else False,
        "password_field_detected": 0,  # only for runtime
        "domain_age": domain_age,
        "ip_mismatch": ip_mismatch,
        "trusted_tld": has_trusted_tld(domain)

    }
