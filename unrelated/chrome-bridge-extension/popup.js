// Popup logic for Antigravity Chrome Bridge Pro 3.0

document.addEventListener("DOMContentLoaded", async () => {
  const statusBadge = document.getElementById("statusBadge");
  const statusText = document.getElementById("statusText");
  const pingText = document.getElementById("pingText");
  const activeTitle = document.getElementById("activeTitle");
  const activeUrl = document.getElementById("activeUrl");
  const tabIdBadge = document.getElementById("tabIdBadge");

  const cfgHost = document.getElementById("cfgHost");
  const cfgPort = document.getElementById("cfgPort");
  const cfgToken = document.getElementById("cfgToken");
  const btnSaveConfig = document.getElementById("btnSaveConfig");
  const statusMsg = document.getElementById("statusMsg");
  const toggleSettings = document.getElementById("toggleSettings");
  const settingsForm = document.getElementById("settingsForm");

  // 1. Load Stored Settings & Status
  chrome.storage.local.get(["status", "latencyMs", "serverHost", "serverPort", "authToken"], (res) => {
    updateStatus(res.status === "connected", res.latencyMs);
    cfgHost.value = res.serverHost || "localhost";
    cfgPort.value = res.serverPort || 9999;
    cfgToken.value = res.authToken || "";
  });

  // Listen for live updates from background
  chrome.storage.onChanged.addListener((changes) => {
    if (changes.status || changes.latencyMs) {
      chrome.storage.local.get(["status", "latencyMs"], (res) => {
        updateStatus(res.status === "connected", res.latencyMs);
      });
    }
  });

  function updateStatus(isConnected, latencyMs) {
    if (isConnected) {
      statusBadge.classList.add("connected");
      statusText.innerText = "Connected";
      pingText.innerText = latencyMs ? `(${latencyMs}ms)` : "";
    } else {
      statusBadge.classList.remove("connected");
      statusText.innerText = "Disconnected";
      pingText.innerText = "";
    }
  }

  // 2. Load Active Tab Info
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs && tabs[0]) {
      const tab = tabs[0];
      activeTitle.innerText = tab.title || "Untitled";
      activeUrl.innerText = tab.url || "";
      tabIdBadge.innerText = `Tab #${tab.id}`;
    }
  });

  // 3. Button Actions
  document.getElementById("btnSnapViewport").addEventListener("click", () => {
    chrome.runtime.sendMessage({ type: "request_capture", options: { mode: "viewport", tag: "manual_viewport.png" } });
    showTemporaryFeedback("btnSnapViewport", "📸 Captured!");
  });

  document.getElementById("btnSnapFull").addEventListener("click", () => {
    chrome.runtime.sendMessage({ type: "request_capture", options: { mode: "fullPage", tag: "manual_fullpage.png" } });
    showTemporaryFeedback("btnSnapFull", "📜 Stitching...");
  });

  document.getElementById("btnToggleStream").addEventListener("click", () => {
    chrome.runtime.sendMessage({ type: "toggle_stream", fps: 5 });
    showTemporaryFeedback("btnToggleStream", "⚡ Toggled!");
  });

  document.getElementById("btnDOM").addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs && tabs[0]) {
        chrome.tabs.sendMessage(tabs[0].id, { command: "getSemanticDOM" }, () => {});
      }
    });
    showTemporaryFeedback("btnDOM", "🧠 Sent to IDE!");
  });

  document.getElementById("btnOpenStudio").addEventListener("click", () => {
    const port = cfgPort.value || 9998;
    const studioPort = parseInt(port) === 9999 ? 9998 : (parseInt(port) - 1);
    chrome.tabs.create({ url: `http://localhost:${studioPort}` });
  });

  // 4. Settings Toggle & Save
  toggleSettings.addEventListener("click", () => {
    const isOpen = settingsForm.style.display === "block";
    settingsForm.style.display = isOpen ? "none" : "block";
    toggleSettings.innerText = isOpen ? "⚙️ Bridge Server Settings ▾" : "⚙️ Bridge Server Settings ▴";
  });

  btnSaveConfig.addEventListener("click", () => {
    const host = cfgHost.value.trim() || "localhost";
    const port = parseInt(cfgPort.value.trim()) || 9999;
    const token = cfgToken.value.trim();

    chrome.storage.local.set({
      serverHost: host,
      serverPort: port,
      authToken: token
    }, () => {
      statusMsg.style.display = "block";
      setTimeout(() => { statusMsg.style.display = "none"; }, 2500);
    });
  });

  function showTemporaryFeedback(btnId, text) {
    const btn = document.getElementById(btnId);
    const orig = btn.innerText;
    btn.innerText = text;
    setTimeout(() => { btn.innerText = orig; }, 1800);
  }
});
