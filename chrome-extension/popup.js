document.getElementById('report-manual').addEventListener('click', () => {
  chrome.runtime.sendMessage({ type: "report_manual" });
});

document.getElementById('report-sms').addEventListener('click', () => {
  chrome.runtime.sendMessage({ type: "report_sms" });
});
