console.log("👀 Phishing scanner is active on this page");

//--------------------password field detection---------------------------
window.addEventListener("load", () => {
  const passwordFields = document.querySelectorAll("input[type='password']");
  if (passwordFields.length > 0) {
    console.warn("⚠️ Potential phishing: password field detected");

    // Try sending phishing report to backend
    try {
      fetch("http://localhost:5000/log", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url: window.location.href,
          indicator: "password_field_detected",
          timestamp: new Date().toISOString()
        })
      }).catch(error => {
        console.error("❌ Fetch failed (password field):", error);
      });
    } catch (err) {
      console.error("❌ Error in password field fetch:", err);
    }
  } else {
    console.log("✅ No password fields detected on this page");
  }
});


//-------------------websites detection----------------------------
//OPTIMIZE THIS PART WITH BACKEND
const suspiciousDomains = [
  "alrahjibank.com",
  "stcpayy.com",
  "snabb.com",
  "alinmma.com",
  "alinma.online",
  "example.com"
];

const currentHost = window.location.hostname;
const currentProtocol = window.location.protocol;

// Check if site is using http instead of https
const isUsingHTTP = currentProtocol === "http:";

//Trigger warning if domain is suspicious or if HTTP is used on known banking domains
const bankDomains = ["alinma.com", "alrajhibank.com.sa", "stcpay.com"];

if (
  suspiciousDomains.some(domain => currentHost.includes(domain)) ||
  (isUsingHTTP && bankDomains.some(domain => currentHost.includes(domain)))
) {
  console.warn("⚠️ Phishing risk detected on:", currentHost);
  alert("⚠️ This site may be unsafe — suspicious domain or insecure connection.");

  try {
    fetch("http://localhost:5000/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: window.location.href,
        indicator: isUsingHTTP ? "http_used_on_bank" : "suspicious_domain",
        timestamp: new Date().toISOString()
      })
    }).catch(error => {
      console.error("❌ Fetch failed:", error);
    });
  } catch (err) {
    console.error("❌ Error sending fetch:", err);
  }
}
