// scanner.js
// 👀 This script runs in the context of every page the user visits.
// It detects potential phishing attempts based on presence of password fields
// and sends that data to backend for threat intelligence collection.

console.log("👀 Phishing scanner is active on this page");

window.addEventListener("load", () => {
  try {
    // 1. Detect if password input fields exist on the page
    const passwordFields = document.querySelectorAll("input[type='password']");

    // 2. If password fields exist, flag potential phishing
    if (passwordFields.length > 0) {
      console.warn("⚠️ Potential phishing: password field detected");

      // 3. Send report to backend
      fetch("http://localhost:5000/log", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url: window.location.href,
          indicator: "password_field_detected",
          timestamp: new Date().toISOString()
        })
      })
      .then((response) => {
        if (!response.ok) {
          console.error("🚨 Failed to log phishing attempt:", response.statusText);
        } else {
          console.log("✅ Phishing activity reported to backend");
        }
      })
      .catch((error) => {
        console.error("❌ Error reporting to backend:", error);
      });

    } else {
      // If no password fields, the page is probably safe
      console.log("✅ No password fields detected on this page");
    }
  } catch (error) {
    console.error("❌ Scanner error:", error);
  }
});
