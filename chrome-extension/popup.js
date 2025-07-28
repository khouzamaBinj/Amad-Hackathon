// Adds interactivity to the popup for manual reporting
document.getElementById("report").addEventListener("click", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const currentURL = tabs[0].url;

    fetch("http://localhost:5000/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: currentURL,
        indicator: "manual_report",
        timestamp: new Date().toISOString()
      })
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("✅ Report sent successfully:", data);
        document.getElementById("status").innerText = "Reported 🚨";
      })
      .catch((error) => {
        console.error("❌ Error sending report:", error);
        document.getElementById("status").innerText = "Error reporting ⚠️";
      });
  });
});
