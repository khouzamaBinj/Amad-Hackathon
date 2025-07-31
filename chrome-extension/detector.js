document.getElementById("reportBtn").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const fromSms = document.getElementById("fromSms").checked;

  fetch("http://localhost:5000/report", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      url: tab.url,
      from_sms: fromSms
    })
  })
  .then(() => alert("URL reported to HoneyWall backend"));
});