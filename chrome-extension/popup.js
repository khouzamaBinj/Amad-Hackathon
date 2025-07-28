//This adds interactivity to the popup like letting the user manually report a site.
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
    });

    document.getElementById("status").innerText = "Reported 🚨";
  });
});
