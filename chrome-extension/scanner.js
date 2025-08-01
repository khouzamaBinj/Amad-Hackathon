// ────────────────────────────────────────────────────────────
// Saudi PhishGuard – scanner.js
// Injected by content_script into every HTTP(S) page.
// Collects basic phishing signals and POSTs them to backend.
//
// 1. Waits for DOM to load (~1s delay)
// 2. Collects basic heuristics (e.g., password field, iframe)
// 3. Sends to /ml_score → gets {verdict, score}
// 4. Logs result to /log
// 5. Sends message to popup.js (if open)
// ────────────────────────────────────────────────────────────

console.log("HoneyWall test script loaded");

function collectSignals() {
  const url = window.location.href;
  const domain = new URL(url).hostname;

  const passwordFieldDetected = !!document.querySelector("input[type='password']");
  const iframeCount = document.querySelectorAll("iframe").length;

  return {
    url,
    contains_https: url.startsWith("https://") ? 1 : 0,
    has_ip: /^\d{1,3}(?:\.\d{1,3}){3}$/.test(domain) ? 1 : 0,
    has_suspicious_words: /(login|verify|bank|secure|update|signin|confirm)/i.test(url) ? 1 : 0,
    url_length: url.length,
    num_dots: (domain.match(/\./g) || []).length,
    is_mobile_site: domain.startsWith("m.") || url.includes("/m/") ? 1 : 0,
    password_field_detected: passwordFieldDetected ? 1 : 0,
    // These 3 will be handled server-side in extract_features()
    domain_age: 0,
    ip_mismatch: 0,
    trusted_tld: 0,
    iframe_count: iframeCount
  };
}

async function sendToBackend(signals) {
  try {
    const mlRes = await fetch("http://127.0.0.1:5000/ml_score", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(signals)
    });

    const { verdict, score } = await mlRes.json();
    console.log(`🛡️ Verdict: ${verdict} (${score})`);

    // Log to backend
    fetch("http://127.0.0.1:5000/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ...signals,
        indicator: verdict,
        score,
        timestamp: new Date().toISOString()
      })
    }).catch(() => {});

    // Send message to popup (optional visual update)
    chrome.runtime.sendMessage({ verdict, score });

  } catch (err) {
    console.error("❌ Backend communication failed:", err);
  }
}

// Wait 1 second for DOM to stabilize, then scan
setTimeout(() => {
  const signals = collectSignals();
  sendToBackend(signals);
}, 1000);
