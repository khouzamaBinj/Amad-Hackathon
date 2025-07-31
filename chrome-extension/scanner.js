console.log("👀 HoneyWall scanner is active");

// -------------------- Password Field Detection --------------------
function detectPasswordFields() {
  const passwordFields = document.querySelectorAll("input[type='password']");
  if (passwordFields.length > 0) {
    console.warn("⚠️ Password field detected");

    fetch("http://localhost:5000/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: window.location.href,
        indicator: "password_field_detected",
        timestamp: new Date().toISOString()
      })
    });

    return true;
  }
  return false;
}

// -------------------- Main Detection Flow --------------------
window.addEventListener("load", async () => {
  try {
    // Dynamic import of the detector module
    const { isSuspicious } = await import(chrome.runtime.getURL("detector.js"));
    
    const currentUrl = window.location.href;
    const detectionResult = isSuspicious(currentUrl);
    const hasPassword = detectPasswordFields();

    if (detectionResult.suspicious || hasPassword) {
      const reasons = [...detectionResult.reasons];
      if (hasPassword) reasons.push("password_field_detected");

      alert(
        "⚠️ HoneyWall Warning:\nSuspicious activity detected!\n\nReasons:\n- " +
          reasons.join("\n- ")
      );

      fetch("http://localhost:5000/log", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url: currentUrl,
          indicator: "combined_detection",
          reasons: reasons,
          suspicion_score: detectionResult.score + (hasPassword ? 1 : 0),
          timestamp: new Date().toISOString()
        })
      }).catch(err => {
        console.error("❌ Logging failed:", err);
      });
    } else {
      console.log("✅ HoneyWall: No phishing indicators detected.");
    }
  } catch (error) {
    console.error("❌ Failed to load detector module:", error);
  }
});