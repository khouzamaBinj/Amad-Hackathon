import pandas as pd
import socket
import whois
from urllib.parse import urlparse
from datetime import datetime
import time
import os

# ----------- CONFIG -------------
DATASET_NAME = "dataset.csv"  # name of your dataset file
OUTPUT_NAME = "whois_cache.csv"
WHOIS_DELAY = 1.5  # seconds between requests
# --------------------------------

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
    except:
        pass
    return 7  # fallback: assume risky

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
    except:
        pass
    return 1  # fallback: assume mismatch

# --- MAIN EXECUTION ---
print("🔍 Loading dataset...")

# Resolve dataset path
script_dir = os.path.dirname(__file__)
dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset.csv"))
df = pd.read_csv(dataset_path)

# Parse domain from each URL
df["domain"] = df["url"].apply(get_domain)
unique_domains = df["domain"].dropna().unique()

print(f"📦 Found {len(unique_domains)} unique domains. Starting WHOIS caching...")

rows = []
for i, domain in enumerate(unique_domains):
    print(f"🔎 ({i+1}/{len(unique_domains)}) Processing {domain}...")

    try:
        age = get_domain_age(domain)
        mismatch = check_ip_mismatch(domain)
    except Exception as e:
        print(f"⚠️ WHOIS failed for {domain}: {e}")
        age, mismatch = 7, 1  # fallback

    rows.append({
        "domain": domain,
        "domain_age": age,
        "ip_mismatch": mismatch
    })

    time.sleep(WHOIS_DELAY)

# Save WHOIS cache
output_path = os.path.join(script_dir, OUTPUT_NAME)
pd.DataFrame(rows).to_csv(output_path, index=False)
print(f"✅ {OUTPUT_NAME} saved to {output_path}")
