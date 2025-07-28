console.log("👀 Phishing scanner is active on this page");

window.addEventListener("load", () => {
  const passwordFields = document.querySelectorAll("input[type='password']");
  if (passwordFields.length > 0) {
    console.warn("⚠️ Potential phishing: password field detected");

    // Send phishing report to backend
    fetch("http://localhost:5000/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: window.location.href,
        indicator: "password_field_detected",
        timestamp: new Date().toISOString()
      })
    });
  } else {
    console.log("✅ No password fields detected on this page");
  }
});
