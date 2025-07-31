import requests
import pandas as pd

# Fetch phishing URLs from OpenPhish
response = requests.get("https://openphish.com/feed.txt")
phishing_urls = response.text.strip().split("\n")

# Add safe URLs manually
safe_urls = [
    "https://stc.com.sa",
    "https://alrajhibank.com.sa",
    "https://riyadbank.com",
    "https://samba.com",
    "https://bank.sa",
    "https://www.alahli.com",
    "https://www.alinma.com",
    "https://www.fransi.com.sa",
    "https://www.sabb.com",
    "https://www.gib.com"
]

# Combine & label
df = pd.DataFrame(phishing_urls + safe_urls, columns=["url"])
df["label"] = [1] * len(phishing_urls) + [0] * len(safe_urls)

df.to_csv("dataset.csv", index=False)
print("✅ dataset.csv saved")
