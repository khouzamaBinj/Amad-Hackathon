import csv
import random
from typing import List

def generate_saudi_synthetic_urls(output_file: str = "saudi_synthetic_banking_urls.csv"):
    """
    Generates synthetic URL patterns mimicking Saudi bank websites for training only.
    """

    # Clearly synthetic Saudi-based bank domains
    saudi_bank_domains = [
        "secure-stcpay.sa-test",
        "demo-alrajhi.sa-training",
        "mock-riyadbank.security.sa",
        "alinma-bank.phishinglab.sa",
        "simulated-ncb.sa-fake",
        "training-bank-aljazira.sa.dev",
        "faked-sabb.sa-secure",
        "phishing-snb.sa.test",
        "testbank-alinma.research.sa"
    ]

    url_paths = [
        "/login", "/signin", "/account/overview", "/services/cards", "/payments/government",
        "/support/contact", "/settings/security", "/account/statements",
        "/services/loans", "/transfer/domestic", "/transfer/international"
    ]

    languages = ["en", "ar"]
    mobile_prefixes = ["m.", "mobile.", ""]
    protocols = ["https://", "https://www."]

    urls = []

    for domain in saudi_bank_domains:
        for _ in range(12):
            protocol = random.choice(protocols)
            prefix = random.choice(mobile_prefixes)
            lang = random.choice(languages)
            path = random.choice(url_paths)

            if random.choice([True, False]):
                url = f"{protocol}{prefix}{domain}/{lang}{path}"
            else:
                url = f"{protocol}{prefix}{domain}{path}"

            urls.append({
                "url": url,
                "domain": domain,
                "path": path,
                "language": lang,
                "is_mobile": prefix != "",
                "label": "benign",
                "note": "saudi_synthetic"
            })

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["url", "domain", "path", "language", "is_mobile", "label", "note"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in urls:
            writer.writerow(entry)

    print(f"✅ Saved {len(urls)} synthetic Saudi URLs to {output_file}")
    return urls

# Run on script call
def main():
    print("🕌 Generating synthetic Saudi bank URLs...")
    generate_saudi_synthetic_urls()

if __name__ == "__main__":
    main()
