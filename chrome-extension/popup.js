document.addEventListener("DOMContentLoaded", function () {
  const scanButton = document.getElementById("scanButton");
  const resultDiv = document.getElementById("result");
  const loadingDiv = document.getElementById("loading");

  scanButton.addEventListener("click", function () {
    // Show scanning status and clear previous result
    loadingDiv.style.display = "block";
    resultDiv.textContent = "";
    resultDiv.style.color = "black";

    // Get active tab URL
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const tab = tabs[0];
      if (!tab || !tab.url.startsWith("http")) {
        loadingDiv.style.display = "none";
        resultDiv.textContent = "❌ Unsupported URL";
        return;
      }

      // Prepare data for backend
      const url = tab.url;

      fetch("http://127.0.0.1:5000/ml_score", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          url: url,
          password_field_detected: 0
        })
      })
        .then(response => response.json())
        .then(data => {
          loadingDiv.style.display = "none";

          if (!data.verdict || typeof data.score !== "number") {
            resultDiv.textContent = "⚠️ Invalid server response";
            resultDiv.style.color = "orange";
            return;
          }

          if (data.verdict === "phishing") {
            resultDiv.textContent = `❌ Risky site detected (Confidence: ${((1-data.score) * 100).toFixed(1)}%)`;
            resultDiv.style.color = "red";
          } else {
            resultDiv.textContent = `✅ Site is safe (Confidence: ${((1-data.score) * 100).toFixed(1)}%)`;
            resultDiv.style.color = "green";
          }
        })
        .catch(error => {
          loadingDiv.style.display = "none";
          resultDiv.textContent = "❌ Could not connect to backend";
          resultDiv.style.color = "orange";
          console.error("Scan error:", error);
        });
    });
  });
});
