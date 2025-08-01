// ────────────────────────────────────────────────────────────
// HoneyWall – lightweight content-script
// Sends the current tab’s URL (plus a few client-side signals)
// to your Flask backend and logs the verdict.
//
// 1. Injected on *every* http(s) page via manifest.json
// 2. Waits ~1 s so the DOM can finish building
// 3. Detects common risk clues (password fields, iframes, etc.)
// 4. POSTs to /ml_score  →  receives {verdict, score}
// 5. POSTs a copy to /log for your dashboard
// ────────────────────────────────────────────────────────────

console.log("🔍 HoneyWall scanner active");

function collectSignals() {
  // a) Is there at least one <input type="password"> on the page?
  const passwordFieldDetected = !!document.querySelector("input[type='password']");

  // b) Does the page embed remote content via <iframe>?
  const iframeCount = document.querySelectorAll("iframe").length;

  // c) Basic heuristic: long URL or a lot of dots
  const url = window.location.href;
  return {
    url,
    password_field_detected: passwordFieldDetected ? 1 : 0,
    iframe_count: iframeCount,
    url_length: url.length,
    num_dots: (url.match(/\./g) || []).length
  };
}

async function sendToBackend(signals) {
  try {
    // ── 1. Ask ML model
    const res = await fetch("http://127.0.0.1:5000/ml_score", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(signals)
    });
    const { verdict, score } = await res.json();
    console.log(`🛡️ HoneyWall verdict: ${verdict} (${score})`);

    // ── 2. Log the result (non-blocking)
    fetch("http://127.0.0.1:5000/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ...signals,
        indicator: verdict,
        score,
        timestamp: new Date().toISOString()
      })
    }).catch(() => { /* silent */ });

  } catch (err) {
    console.error("❌ HoneyWall backend error:", err);
  }
}

// Kick off after a brief delay so the DOM is mostly ready
setTimeout(() => sendToBackend(collectSignals()), 1000);
