console.log("🔍 Phishing scanner activated");

// Helper to extract features from the current page
function extractPageFeatures() {
  const url = window.location.href;

  return {
    url: url,
    timestamp: new Date().toISOString(),
    contains_https: url.startsWith("https://") ? 1 : 0,
    has_ip: /\b(?:\d{1,3}\.){3}\d{1,3}\b/.test(url) ? 1 : 0,
    has_suspicious_words: /(login|secure|update|verify|account|webscr|signin)/i.test(url) ? 1 : 0,
    url_length: url.length || 0,
    num_dots: (url.match(/\./g) || []).length,
    is_mobile_site: /m\.|\/m\//i.test(url) ? 1 : 0,
    password_field_detected: document.querySelector('input[type="password"]') ? 1 : 0,
    domain_age: 7,        // default fallback
    ip_mismatch: 1        // default fallback
  };
}

// Send features to the ML backend
async function analyzePage() {
  const features = extractPageFeatures();

  console.log("🧪 Features being sent:", features);

  try {
    const response = await fetch("http://127.0.0.1:5000/ml_score", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(features)
    });

    const result = await response.json();
    console.log("🤖 AI Result:", result);

    // Log to /log endpoint
    await fetch("http://127.0.0.1:5000/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: features.url,
        indicator: result.verdict || "unknown",
        timestamp: features.timestamp
      })
    });

  } catch (error) {
    console.error("❌ AI scoring failed:", error);
  }
}

// Wait for the page to load, then analyze
setTimeout(analyzePage, 1000);
