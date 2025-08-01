"""
Feature extraction with live WHOIS + DNS checks and
automatic CSV caching for < second-run speed.
"""

import os, re, socket, ipaddress
from datetime import datetime, timezone
from urllib.parse import urlparse

import pandas as pd
import whois           # pip install python-whois

# --------------------------------------------------
SUSPICIOUS_KEYWORDS = {
    "verify", "update", "confirm", "urgent", "suspended",
    "blocked", "expire", "alert", "warning", "secure",
    "validate", "authenticate", "login", "signin", "webscr"
}
TRUSTED_SUFFIXES = {
    ".gov", ".edu", ".mil", ".gov.sa", ".edu.sa", ".mil.sa", ".sa"
}

SCRIPT_DIR   = os.path.dirname(__file__)
CACHE_PATH   = os.path.join(SCRIPT_DIR, "whois_cache.csv")

# --------------------------------------------------
def _load_cache() -> pd.DataFrame:
    if os.path.isfile(CACHE_PATH):
        return pd.read_csv(CACHE_PATH).set_index("domain")
    return pd.DataFrame(columns=["domain_age", "ip_mismatch"]).set_index("domain")

_CACHE = _load_cache()


def _save_cache() -> None:
    _CACHE.reset_index().to_csv(CACHE_PATH, index=False)


def _domain_age_days(domain: str) -> int:
    """Age of the domain in _days_ (0 if unknown)."""
    try:
        w = whois.whois(domain)
        created = w.creation_date
        # the whois lib may return list
        if isinstance(created, (list, tuple)):
            created = created[0]
        if created is None:
            return 0
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        return max((datetime.now(timezone.utc) - created).days, 0)
    except Exception:
        return 0


def _ip_mismatch(domain: str) -> int:
    """
    Heuristic: 1 if the domain **is** an IP, or resolves to a
    private-range IP (common in bogus URLs), else 0.
    """
    try:
        if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", domain):
            return 1
        ip_addr = socket.gethostbyname(domain)
        return int(ipaddress.ip_address(ip_addr).is_private)
    except Exception:
        # total failure → treat as suspicious
        return 1


def _trusted_tld(domain: str) -> int:
    return int(any(domain.endswith(sfx) for sfx in TRUSTED_SUFFIXES))


def _ensure_cached(domain: str) -> None:
    if domain in _CACHE.index:
        return
    _CACHE.loc[domain, "domain_age"]  = _domain_age_days(domain)
    _CACHE.loc[domain, "ip_mismatch"] = _ip_mismatch(domain)
    _save_cache()


# --------------------------------------------------
def extract_features(url: str) -> dict:
    """
    Returns a dict of numeric features expected by the RF model.
    Called both during training and at prediction time.
    """
    blank = {
        "contains_https": 0, "has_ip": 0, "has_suspicious_words": 0,
        "url_length": 0, "num_dots": 0, "is_mobile_site": 0,
        "password_field_detected": 0,     # Only known at client side
        "domain_age": 0, "ip_mismatch": 0, "trusted_tld": 0,
    }
    if not url:
        return blank

    url_lc  = url.lower()
    parsed  = urlparse(url_lc)
    domain  = parsed.hostname or ""

    # Cache WHOIS / DNS info on first sight
    _ensure_cached(domain)

    return {
        "contains_https": int(url_lc.startswith("https://")),
        "has_ip": int(re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", domain) is not None),
        "has_suspicious_words": int(any(k in url_lc for k in SUSPICIOUS_KEYWORDS)),
        "url_length": len(url_lc),
        "num_dots": domain.count("."),
        "is_mobile_site": int(domain.startswith("m.") or "/m/" in url_lc),
        # server-side can’t see DOM → always 0 (client fills this)
        "password_field_detected": 0,
        "domain_age": int(_CACHE.at[domain, "domain_age"]),
        "ip_mismatch": int(_CACHE.at[domain, "ip_mismatch"]),
        "trusted_tld": _trusted_tld(domain),
    }
