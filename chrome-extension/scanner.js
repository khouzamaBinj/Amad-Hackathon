console.log("🔍 Phishing scanner activated");

// Helper to extract features from the current page
function extractPageFeatures() {
  const url = window.location.href;
  const hasHttps = url.startsWith("https://");
  const hasIP = !!url.match(/\b(?:\d{1,3}\.){3}\d{1,3}\b/);
  const hasSuspiciousWords = /(login|secure|update|verify|account|webscr|signin)/i.test(url);
  const isMobile = /m\.|\/m\//i.test(url);
  const length = url.length;
  const numDots = (url.match(/\./g) || []).length;
  const passwordDetected = !!document.querySelector('input[type="password"]');

  const parsed = new URL(url);
  const domain = parsed.hostname;
  const path = parsed.pathname;

  return {
    url,
    domain,
    path,
    contains_https: hasHttps,
    has_ip: hasIP,
    has_suspicious_words: hasSuspiciousWords,
    is_mobile_site: isMobile,
    length,
    num_dots: numDots,
    password_field_detected: passwordDetected,
    timestamp: new Date().toISOString()
  };
}

// Send features to the ML backend
async function analyzePage() {
  const features = extractPageFeatures();

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
        indicator: result.verdict,
        timestamp: features.timestamp
      })
    });

  } catch (error) {
    console.error("❌ AI scoring failed:", error);
  }
}

// Wait a bit for page content to load, then analyze
setTimeout(analyzePage, 1000);
