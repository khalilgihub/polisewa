// Antigravity Chrome Bridge Pro 3.0
// High-Speed Bidirectional Automation, Telemetry, and Visual Capture Engine

let socket = null;
let reconnectTimer = null;
let streamInterval = null;
let isStreaming = false;
let selectedTabId = null;
let currentConfig = {
  serverHost: "localhost",
  serverPort: 9999,
  authToken: ""
};

// ==========================================
// 1. Offscreen Document & Worker Keep-Alive
// ==========================================
async function ensureOffscreenDocument() {
  try {
    if (await chrome.offscreen.hasDocument()) return;
    await chrome.offscreen.createDocument({
      url: "offscreen.html",
      reasons: [chrome.offscreen.Reason.BLOBS],
      justification: "Antigravity keep-alive heartbeat and canvas screenshot processing"
    });
  } catch (err) {}
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "offscreen_heartbeat") {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      connect();
    }
  } else if (msg.type === "page_console_log") {
    sendSocket({
      type: "console_log",
      level: msg.level,
      text: msg.text,
      tabId: sender.tab?.id,
      tabUrl: sender.tab?.url,
      timestamp: Date.now()
    });
  } else if (msg.type === "request_capture") {
    handleCaptureScreenshot(msg.options || {});
  } else if (msg.type === "toggle_stream") {
    if (isStreaming) stopLiveStream();
    else startLiveStream(msg.fps || 6);
  }
});

// Fallback keep-alive alarm
chrome.alarms.create("keepAlive", { periodInMinutes: 1 });
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "keepAlive") {
    ensureOffscreenDocument();
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      connect();
    } else {
      socket.send(JSON.stringify({ type: "ping", timestamp: Date.now() }));
    }
  }
});

// Configuration manager
async function loadConfig() {
  try {
    const res = await chrome.storage.local.get(["serverHost", "serverPort", "authToken"]);
    currentConfig.serverHost = res.serverHost || "localhost";
    currentConfig.serverPort = res.serverPort || 9999;
    currentConfig.authToken = res.authToken || "";
  } catch (e) {}
}

chrome.storage.onChanged.addListener((changes) => {
  if (changes.serverHost || changes.serverPort || changes.authToken) {
    loadConfig().then(() => {
      if (socket) socket.close();
      connect();
    });
  }
});

// ==========================================
// 2. URL Safety & Target Tab Resolver
// ==========================================
function isInjectableUrl(url) {
  if (!url || typeof url !== "string") return false;
  const lower = url.toLowerCase();
  const disallowed = [
    "chrome://",
    "chrome-extension://",
    "edge://",
    "about:",
    "devtools://",
    "view-source:",
    "https://chromewebstore.google.com",
    "https://chrome.google.com/webstore"
  ];
  return !disallowed.some(prefix => lower.startsWith(prefix));
}

function getActiveChromeTab(callback, requireInjectable = false) {
  if (selectedTabId) {
    chrome.tabs.get(selectedTabId, (tab) => {
      if (!chrome.runtime.lastError && tab) {
        finish(tab);
        return;
      }
      selectedTabId = null;
      fallbackActiveTab();
    });
    return;
  }
  fallbackActiveTab();

  function fallbackActiveTab() {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
      let tab = tabs && tabs[0];
      if (tab && (!requireInjectable || isInjectableUrl(tab.url))) {
        finish(tab);
      } else {
        chrome.tabs.query({ active: true }, (allActive) => {
          const injectableActive = (allActive || []).find(t => isInjectableUrl(t.url));
          if (injectableActive) {
            finish(injectableActive);
          } else {
            finish(allActive && allActive[0]);
          }
        });
      }
    });
  }

  function finish(tab) {
    if (!tab) {
      if (requireInjectable) {
        chrome.tabs.query({}, (allTabs) => {
          const injectable = (allTabs || []).find(t => isInjectableUrl(t.url));
          callback(injectable || null);
        });
        return;
      }
      return callback(null);
    }
    if (requireInjectable && !isInjectableUrl(tab.url)) {
      chrome.tabs.query({}, (allTabs) => {
        const injectable = (allTabs || []).find(t => isInjectableUrl(t.url));
        callback(injectable || null);
      });
      return;
    }
    callback(tab);
  }
}

// ==========================================
// 3. WebSocket Engine & Protocol
// ==========================================
function connect() {
  if (socket && (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING)) {
    return;
  }

  ensureOffscreenDocument();

  const wsUrl = `ws://${currentConfig.serverHost}:${currentConfig.serverPort}`;
  try {
    socket = new WebSocket(wsUrl);
  } catch (err) {
    chrome.storage.local.set({ status: "disconnected" });
    return;
  }

  socket.onopen = () => {
    console.log(`[Antigravity Pro] Connected to ${wsUrl}`);
    chrome.storage.local.set({ status: "connected", connectedAt: Date.now() });
    
    if (currentConfig.authToken) {
      sendSocket({ type: "auth", token: currentConfig.authToken });
    }

    broadcastAllTabs();
    sendActiveTabInfo();
    startLiveStream(6);
  };

  socket.onclose = () => {
    chrome.storage.local.set({ status: "disconnected" });
    stopLiveStream();
    if (reconnectTimer) clearTimeout(reconnectTimer);
    reconnectTimer = setTimeout(connect, 2500);
  };

  socket.onerror = () => {};

  socket.onmessage = async (event) => {
    try {
      const data = JSON.parse(event.data);
      const cmd = data.command;

      if (data.type === "pong") {
        if (data.timestamp) {
          const latency = Date.now() - data.timestamp;
          chrome.storage.local.set({ latencyMs: latency });
        }
        return;
      }

      if (cmd === "listTabs") {
        broadcastAllTabs();
      } else if (cmd === "switchTab") {
        handleSwitchTab(data);
      } else if (cmd === "focusChrome") {
        handleFocusChrome();
      } else if (cmd === "navigate") {
        handleNavigate(data);
      } else if (cmd === "navigateBack") {
        getActiveChromeTab((t) => t && chrome.tabs.goBack(t.id).catch(() => {}));
      } else if (cmd === "navigateForward") {
        getActiveChromeTab((t) => t && chrome.tabs.goForward(t.id).catch(() => {}));
      } else if (cmd === "reloadTab") {
        getActiveChromeTab((t) => t && chrome.tabs.reload(t.id));
      } else if (cmd === "createTab") {
        chrome.tabs.create({ url: data.url || "https://www.google.com" }, (tab) => {
          if (tab) { selectedTabId = tab.id; broadcastAllTabs(); sendActiveTabInfo(); }
        });
      } else if (cmd === "closeTab") {
        const tid = data.tabId || selectedTabId;
        if (tid) chrome.tabs.remove(tid, () => broadcastAllTabs());
      } else if (cmd === "captureScreenshot") {
        handleCaptureScreenshot(data);
      } else if (cmd === "click") {
        handleClick(data);
      } else if (cmd === "hover") {
        handleHover(data);
      } else if (cmd === "type") {
        handleType(data);
      } else if (cmd === "keyPress") {
        handleKeyPress(data);
      } else if (cmd === "selectOption") {
        handleSelectOption(data);
      } else if (cmd === "setCheckbox") {
        handleSetCheckbox(data);
      } else if (cmd === "scroll") {
        handleScroll(data);
      } else if (cmd === "eval") {
        handleEval(data);
      } else if (cmd === "getSemanticDOM") {
        handleGetSemanticDOM(data);
      } else if (cmd === "waitForSelector") {
        handleWaitForSelector(data);
      } else if (cmd === "waitForNavigation") {
        handleWaitForNavigation(data);
      } else if (cmd === "startStream") {
        startLiveStream(data.fps || 6, data.quality || 70);
      } else if (cmd === "stopStream") {
        stopLiveStream();
      } else if (cmd === "enableConsoleCapture") {
        injectConsoleProxy();
      } else if (cmd === "getCookies") {
        handleGetCookies(data);
      } else if (cmd === "setCookie") {
        handleSetCookie(data);
      }
    } catch (e) {
      console.error("[Antigravity Pro] Command execution error:", e);
      sendSocket({ type: "error", error: e.toString() });
    }
  };
}

// ==========================================
// 4. Tab Queries, Switching & Focus
// ==========================================
function broadcastAllTabs() {
  chrome.tabs.query({}, (tabs) => {
    const list = (tabs || []).map(t => ({
      id: t.id,
      windowId: t.windowId,
      title: t.title,
      url: t.url,
      favIconUrl: t.favIconUrl,
      active: t.id === selectedTabId || t.active,
      status: t.status
    }));
    sendSocket({
      type: "tabs_list",
      tabs: list,
      timestamp: Date.now()
    });
  });
}

function sendActiveTabInfo() {
  getActiveChromeTab((tab) => {
    if (tab) {
      sendSocket({
        type: "tab_update",
        tabId: tab.id,
        url: tab.url,
        title: tab.title,
        favIconUrl: tab.favIconUrl,
        viewportWidth: tab.width,
        viewportHeight: tab.height,
        timestamp: Date.now()
      });
    }
  });
}

function handleSwitchTab(data) {
  if (data.tabId) {
    selectedTabId = data.tabId;
    chrome.tabs.update(data.tabId, { active: true }, (tab) => {
      if (tab) {
        // If window is minimized, un-minimize it so it renders pixels!
        chrome.windows.get(tab.windowId, (win) => {
          if (win && win.state === "minimized") {
            chrome.windows.update(tab.windowId, { state: "normal" });
          }
        });
        sendActiveTabInfo();
        broadcastAllTabs();
        // Force an immediate frame capture
        setTimeout(captureAndSendFrame, 80);
      }
    });
    return;
  }

  chrome.tabs.query({}, (tabs) => {
    let target = null;
    if (data.urlMatch) {
      target = (tabs || []).find(t => t.url && t.url.toLowerCase().includes(data.urlMatch.toLowerCase()));
    } else if (data.titleMatch) {
      target = (tabs || []).find(t => t.title && t.title.toLowerCase().includes(data.titleMatch.toLowerCase()));
    }

    if (target) {
      selectedTabId = target.id;
      chrome.tabs.update(target.id, { active: true }, (tab) => {
        if (tab) {
          sendActiveTabInfo();
          broadcastAllTabs();
          setTimeout(captureAndSendFrame, 80);
        }
      });
    } else {
      sendSocket({ type: "error", message: `No tab matching query: ${data.urlMatch || data.titleMatch}` });
    }
  });
}

function handleFocusChrome() {
  getActiveChromeTab((tab) => {
    if (tab) {
      chrome.windows.update(tab.windowId, { focused: true, state: "normal" }, () => {
        setTimeout(captureAndSendFrame, 80);
      });
    }
  });
}

function handleNavigate(data) {
  getActiveChromeTab((tab) => {
    if (tab) {
      chrome.tabs.update(tab.id, { url: data.url }, () => {
        setTimeout(captureAndSendFrame, 150);
      });
    }
  });
}

// Helper to capture a single frame on demand with smart debounce
let pendingCaptureTimer = null;
function captureAndSendFrame(delayMs = 0) {
  if (pendingCaptureTimer) clearTimeout(pendingCaptureTimer);
  pendingCaptureTimer = setTimeout(() => {
    getActiveChromeTab((tab) => {
      if (!tab) return;
      const now = Date.now();
      const waitMs = Math.max(0, 620 - (now - lastCaptureTime));
      setTimeout(() => {
        safeCaptureTab(tab.windowId, { format: "jpeg", quality: 75 }, (err, dataUrl) => {
          if (!err && dataUrl) {
            sendSocket({
              type: "screenshot",
              dataUrl: dataUrl,
              tabId: tab.id,
              tabTitle: tab.title,
              tabUrl: tab.url,
              viewportWidth: tab.width,
              viewportHeight: tab.height,
              timestamp: Date.now()
            });
          }
        });
      }, waitMs);
    });
  }, delayMs);
}

// ==========================================
// 5. Automation: Visual Click, Keyboard & DOM
// ==========================================
function handleClick(data) {
  getActiveChromeTab((tab) => {
    if (!tab) return sendSocket({ type: "action_result", action: "click", result: { success: false, message: "No injectable tab active" } });
    
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: (selector, xpath, textMatch, coords, clickType) => {
        function resolveCoordinates(c) {
          if (!c) return null;
          let x = c.x;
          let y = c.y;
          if (c.normX !== undefined && c.normY !== undefined) {
            x = Math.round(c.normX * window.innerWidth);
            y = Math.round(c.normY * window.innerHeight);
          }
          return (x !== undefined && y !== undefined) ? { x, y } : null;
        }

        function findTargetElement(sel, xp, txt, c) {
          const res = resolveCoordinates(c);
          if (res && !sel && !xp && !txt) {
            let el = document.elementFromPoint(res.x, res.y);
            if (el && el.shadowRoot) {
              try {
                const inner = el.shadowRoot.elementFromPoint(res.x, res.y);
                if (inner) el = inner;
              } catch(e) {}
            }
            return el;
          }

          if (xp || (sel && (sel.startsWith('//') || sel.startsWith('xpath:')))) {
            const cleanXp = xp || sel.replace(/^xpath:/, '');
            try {
              const r = document.evaluate(cleanXp, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
              if (r.singleNodeValue) return r.singleNodeValue;
            } catch(e) {}
          }

          if (sel) {
            try {
              let el = document.querySelector(sel);
              if (el) return el;
            } catch(e) {}

            function searchShadow(root) {
              const children = root.querySelectorAll('*');
              for (const child of children) {
                if (child.shadowRoot) {
                  try {
                    const found = child.shadowRoot.querySelector(sel);
                    if (found) return found;
                  } catch(e) {}
                  const deeper = searchShadow(child.shadowRoot);
                  if (deeper) return deeper;
                }
              }
              return null;
            }
            const shadowEl = searchShadow(document);
            if (shadowEl) return shadowEl;
          }

          if (txt) {
            const cleanMatch = txt.trim().toLowerCase();
            const candidateTags = ['button', 'a', 'input', 'span', 'div', 'p', 'th', 'td', 'label', 'li'];
            const candidates = Array.from(document.querySelectorAll(candidateTags.join(',')));
            let found = candidates.find(e => e.innerText && e.innerText.trim().toLowerCase() === cleanMatch);
            if (!found) {
              found = candidates.find(e => e.innerText && e.innerText.trim().toLowerCase().includes(cleanMatch));
            }
            if (found) return found;
          }

          if (res) {
            let el = document.elementFromPoint(res.x, res.y);
            if (el && el.shadowRoot) {
              try {
                const inner = el.shadowRoot.elementFromPoint(res.x, res.y);
                if (inner) el = inner;
              } catch(e) {}
            }
            return el;
          }

          return null;
        }

        function showClickRipple(x, y) {
          try {
            const ripple = document.createElement('div');
            ripple.style.position = 'fixed';
            ripple.style.left = (x - 16) + 'px';
            ripple.style.top = (y - 16) + 'px';
            ripple.style.width = '32px';
            ripple.style.height = '32px';
            ripple.style.borderRadius = '50%';
            ripple.style.border = '3px solid #38bdf8';
            ripple.style.background = 'rgba(56, 189, 248, 0.35)';
            ripple.style.boxShadow = '0 0 12px #0284c7';
            ripple.style.pointerEvents = 'none';
            ripple.style.zIndex = '2147483647';
            ripple.style.transition = 'transform 0.45s ease-out, opacity 0.45s ease-out';
            ripple.style.transform = 'scale(0.4)';
            ripple.style.opacity = '1';
            document.body.appendChild(ripple);

            requestAnimationFrame(() => {
              ripple.style.transform = 'scale(1.8)';
              ripple.style.opacity = '0';
            });

            setTimeout(() => ripple.remove(), 500);
          } catch(e) {}
        }

        const resolved = resolveCoordinates(coords);
        let el = findTargetElement(selector, xpath, textMatch, coords);

        if (el) {
          if (selector || xpath || textMatch) {
            try { el.scrollIntoView({ behavior: 'smooth', block: 'center' }); } catch(e) {}
          }

          const rect = el.getBoundingClientRect();
          const clickX = resolved ? resolved.x : Math.round(rect.left + rect.width / 2);
          const clickY = resolved ? resolved.y : Math.round(rect.top + rect.height / 2);
          showClickRipple(clickX, clickY);

          const eventInit = {
            bubbles: true,
            cancelable: true,
            composed: true,
            view: window,
            detail: clickType === 'dblclick' ? 2 : 1,
            clientX: clickX,
            clientY: clickY,
            screenX: clickX + (window.screenX || 0),
            screenY: clickY + (window.screenY || 0),
            button: clickType === 'contextmenu' ? 2 : 0,
            buttons: clickType === 'contextmenu' ? 2 : 1
          };

          if (clickType === 'dblclick') {
            el.dispatchEvent(new MouseEvent('dblclick', eventInit));
          } else if (clickType === 'contextmenu') {
            el.dispatchEvent(new MouseEvent('contextmenu', eventInit));
          } else {
            try { el.dispatchEvent(new PointerEvent('pointerdown', { ...eventInit, pointerId: 1, pointerType: 'mouse' })); } catch(e) {}
            el.dispatchEvent(new MouseEvent('mousedown', eventInit));

            if (typeof el.focus === 'function') {
              try { el.focus({ preventScroll: true }); } catch(e) { try { el.focus(); } catch(e2) {} }
            }

            try { el.dispatchEvent(new PointerEvent('pointerup', { ...eventInit, pointerId: 1, pointerType: 'mouse' })); } catch(e) {}
            el.dispatchEvent(new MouseEvent('mouseup', eventInit));

            try { el.click(); } catch(e) {}
          }

          return { 
            success: true, 
            tag: el.tagName, 
            id: el.id, 
            className: el.className, 
            text: el.innerText?.slice(0, 60), 
            x: clickX, 
            y: clickY 
          };
        } else if (resolved) {
          showClickRipple(resolved.x, resolved.y);
          return { success: false, message: "Clicked empty viewport", x: resolved.x, y: resolved.y };
        }
        return { success: false, message: "Element not found" };
      },
      args: [data.selector || null, data.xpath || null, data.text || null, data.coords || null, data.clickType || 'click']
    }).then((results) => {
      sendSocket({ type: "action_result", action: "click", result: results?.[0]?.result });
      setTimeout(captureAndSendFrame, 90);
    }).catch((err) => {
      sendSocket({ type: "action_result", action: "click", result: { success: false, error: err.toString() } });
    });
  }, true);
}

function handleHover(data) {
  getActiveChromeTab((tab) => {
    if (!tab) return sendSocket({ type: "action_result", action: "hover", result: { success: false, message: "No injectable tab active" } });

    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: (selector, xpath, coords) => {
        let x = coords?.x;
        let y = coords?.y;
        if (coords && coords.normX !== undefined && coords.normY !== undefined) {
          x = Math.round(coords.normX * window.innerWidth);
          y = Math.round(coords.normY * window.innerHeight);
        }

        let el = null;
        if (x !== undefined && y !== undefined && !selector && !xpath) {
          el = document.elementFromPoint(x, y);
        } else if (selector) {
          try { el = document.querySelector(selector); } catch(e) {}
        }

        if (el) {
          const rect = el.getBoundingClientRect();
          const hx = x ?? Math.round(rect.left + rect.width / 2);
          const hy = y ?? Math.round(rect.top + rect.height / 2);
          el.dispatchEvent(new MouseEvent('mouseover', { bubbles: true, clientX: hx, clientY: hy }));
          el.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true, clientX: hx, clientY: hy }));
          el.dispatchEvent(new MouseEvent('mousemove', { bubbles: true, clientX: hx, clientY: hy }));
          return { success: true, tag: el.tagName };
        }
        return { success: false, message: "Hover target not found" };
      },
      args: [data.selector || null, data.xpath || null, data.coords || null]
    }).then((results) => {
      sendSocket({ type: "action_result", action: "hover", result: results?.[0]?.result });
    }).catch((err) => {
      sendSocket({ type: "action_result", action: "hover", result: { success: false, error: err.toString() } });
    });
  }, true);
}

function handleType(data) {
  getActiveChromeTab((tab) => {
    if (!tab) return sendSocket({ type: "action_result", action: "type", result: { success: false, message: "No injectable tab active" } });

    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: (selector, xpath, text, clear, submit) => {
        let input = null;
        if (selector) {
          try { input = document.querySelector(selector); } catch(e) {}
        }
        if (!input) input = document.activeElement;

        if (input && (input.tagName === 'INPUT' || input.tagName === 'TEXTAREA' || input.isContentEditable)) {
          input.focus();
          if (clear) {
            input.value = '';
          }
          input.value = (clear ? '' : (input.value || '')) + text;
          input.dispatchEvent(new Event('input', { bubbles: true }));
          input.dispatchEvent(new Event('change', { bubbles: true }));

          if (submit) {
            input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true }));
            const form = input.closest('form');
            if (form) form.dispatchEvent(new Event('submit', { bubbles: true }));
          }
          return { success: true, value: input.value };
        }
        return { success: false, message: "Input target not found" };
      },
      args: [data.selector || null, data.xpath || null, data.text || "", !!data.clear, !!data.submit]
    }).then((results) => {
      sendSocket({ type: "action_result", action: "type", result: results?.[0]?.result });
      setTimeout(captureAndSendFrame, 120);
    }).catch((err) => {
      sendSocket({ type: "action_result", action: "type", result: { success: false, error: err.toString() } });
    });
  }, true);
}

function handleKeyPress(data) {
  getActiveChromeTab((tab) => {
    if (!tab) return sendSocket({ type: "action_result", action: "keyPress", result: { success: false, message: "No injectable tab active" } });

    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: (key, code, ctrl, shift, alt, meta) => {
        const target = document.activeElement || document.body;
        const keyOptions = {
          key: key,
          code: code || key,
          bubbles: true,
          cancelable: true,
          ctrlKey: !!ctrl,
          shiftKey: !!shift,
          altKey: !!alt,
          metaKey: !!meta
        };

        target.dispatchEvent(new KeyboardEvent('keydown', keyOptions));
        target.dispatchEvent(new KeyboardEvent('keypress', keyOptions));

        if (key === 'Backspace' && (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA')) {
          target.value = target.value.slice(0, -1);
          target.dispatchEvent(new Event('input', { bubbles: true }));
        } else if (key === 'Enter' && target.tagName === 'INPUT') {
          const form = target.closest('form');
          if (form) form.dispatchEvent(new Event('submit', { bubbles: true }));
        }

        target.dispatchEvent(new KeyboardEvent('keyup', keyOptions));
        return { success: true, key: key, activeTag: target.tagName };
      },
      args: [data.key || "Enter", data.code || "", !!data.ctrlKey, !!data.shiftKey, !!data.altKey, !!data.metaKey]
    }).then((results) => {
      sendSocket({ type: "action_result", action: "keyPress", result: results?.[0]?.result });
      setTimeout(captureAndSendFrame, 100);
    }).catch((err) => {
      sendSocket({ type: "action_result", action: "keyPress", result: { success: false, error: err.toString() } });
    });
  }, true);
}

function handleSelectOption(data) {
  getActiveChromeTab((tab) => {
    if (!tab) return sendSocket({ type: "action_result", action: "selectOption", result: { success: false, message: "No injectable tab active" } });

    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: (selector, value, text) => {
        let sel = null;
        if (selector) {
          try { sel = document.querySelector(selector); } catch(e) {}
        }
        if (sel && sel.tagName === 'SELECT') {
          if (value !== undefined) {
            sel.value = value;
          } else if (text) {
            const opt = Array.from(sel.options).find(o => o.text.trim().toLowerCase() === text.trim().toLowerCase());
            if (opt) sel.value = opt.value;
          }
          sel.dispatchEvent(new Event('change', { bubbles: true }));
          return { success: true, selectedValue: sel.value };
        }
        return { success: false, message: "Select element not found" };
      },
      args: [data.selector, data.value, data.text]
    }).then((results) => {
      sendSocket({ type: "action_result", action: "selectOption", result: results?.[0]?.result });
    }).catch((err) => {
      sendSocket({ type: "action_result", action: "selectOption", result: { success: false, error: err.toString() } });
    });
  }, true);
}

function handleSetCheckbox(data) {
  getActiveChromeTab((tab) => {
    if (!tab) return sendSocket({ type: "action_result", action: "setCheckbox", result: { success: false, message: "No injectable tab active" } });

    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: (selector, checked) => {
        let el = null;
        if (selector) {
          try { el = document.querySelector(selector); } catch(e) {}
        }
        if (el && (el.type === 'checkbox' || el.type === 'radio')) {
          el.checked = !!checked;
          el.dispatchEvent(new Event('change', { bubbles: true }));
          el.dispatchEvent(new Event('input', { bubbles: true }));
          return { success: true, checked: el.checked };
        }
        return { success: false, message: "Checkbox not found" };
      },
      args: [data.selector, data.checked]
    }).then((results) => {
      sendSocket({ type: "action_result", action: "setCheckbox", result: results?.[0]?.result });
    }).catch((err) => {
      sendSocket({ type: "action_result", action: "setCheckbox", result: { success: false, error: err.toString() } });
    });
  }, true);
}

function handleScroll(data) {
  getActiveChromeTab((tab) => {
    if (!tab) return;
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: (y, x, selector, normX, normY) => {
        let targetX = (normX !== undefined) ? Math.round(normX * window.innerWidth) : undefined;
        let targetY = (normY !== undefined) ? Math.round(normY * window.innerHeight) : undefined;

        if (selector) {
          const el = document.querySelector(selector);
          if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            return { success: true, scrolledElement: selector };
          }
        }

        // If mouse is positioned over an inner scroll container, scroll it directly
        let scrolled = false;
        if (targetX !== undefined && targetY !== undefined) {
          let el = document.elementFromPoint(targetX, targetY);
          while (el && el !== document.body && el !== document.documentElement) {
            try {
              const style = window.getComputedStyle(el);
              const overflowY = style.overflowY;
              const isScrollable = (overflowY === 'auto' || overflowY === 'scroll') && el.scrollHeight > el.clientHeight;
              if (isScrollable) {
                const prev = el.scrollTop;
                el.scrollBy({ top: y || 0, left: x || 0, behavior: 'instant' });
                if (el.scrollTop !== prev) {
                  scrolled = true;
                  break;
                }
              }
            } catch(e) {}
            el = el.parentElement;
          }
        }

        // Default window scrolling with instant behavior for immediate visual responsiveness
        if (!scrolled) {
          const prevY = window.scrollY;
          window.scrollBy({ top: y || 0, left: x || 0, behavior: 'instant' });
          if (window.scrollY === prevY && document.scrollingElement) {
            document.scrollingElement.scrollBy({ top: y || 0, left: x || 0, behavior: 'instant' });
          }
        }

        return { success: true, scrollY: window.scrollY, scrollX: window.scrollX };
      },
      args: [data.y || 0, data.x || 0, data.selector || null, data.normX, data.normY]
    }).then((results) => {
      sendSocket({ type: "action_result", action: "scroll", result: results?.[0]?.result });
      setTimeout(() => captureAndSendFrame(0), 60);
    }).catch((err) => {
      sendSocket({ type: "action_result", action: "scroll", result: { success: false, error: err.toString() } });
    });
  }, true);
}

function handleEval(data) {
  getActiveChromeTab((tab) => {
    if (!tab) return sendSocket({ type: "eval_result", result: { success: false, message: "No injectable tab active" } });

    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: (codeStr) => {
        try {
          return { success: true, value: eval(codeStr) };
        } catch (err) {
          return { success: false, error: err.toString() };
        }
      },
      args: [data.code]
    }).then((results) => {
      sendSocket({ type: "eval_result", result: results?.[0]?.result });
    }).catch((err) => {
      sendSocket({ type: "eval_result", result: { success: false, error: err.toString() } });
    });
  }, true);
}

// ==========================================
// 6. AI Semantic DOM Extraction
// ==========================================
function handleGetSemanticDOM(data) {
  getActiveChromeTab((tab) => {
    if (!tab) return sendSocket({ type: "semantic_dom", data: { error: "Cannot access restricted page" } });

    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => {
        const interactiveTags = ['a', 'button', 'input', 'select', 'textarea', '[role="button"]', '[role="link"]', '[role="checkbox"]', '[role="tab"]', '[contenteditable="true"]'];
        const nodes = Array.from(document.querySelectorAll(interactiveTags.join(',')));
        
        let idCounter = 1;
        const elements = [];

        nodes.forEach((el) => {
          const rect = el.getBoundingClientRect();
          if (rect.width <= 2 || rect.height <= 2 || rect.bottom < 0 || rect.top > window.innerHeight) return;
          const style = window.getComputedStyle(el);
          if (style.visibility === 'hidden' || style.display === 'none' || parseFloat(style.opacity) <= 0.05) return;

          let selector = '';
          if (el.id) selector = '#' + el.id;
          else if (el.name) selector = `${el.tagName.toLowerCase()}[name="${el.name}"]`;
          else if (el.className && typeof el.className === 'string') {
            const firstClass = el.className.trim().split(/\s+/)[0];
            if (firstClass) selector = `${el.tagName.toLowerCase()}.${firstClass}`;
          }
          if (!selector) selector = el.tagName.toLowerCase();

          elements.push({
            id: idCounter++,
            tag: el.tagName.toLowerCase(),
            type: el.type || null,
            role: el.getAttribute('role') || null,
            text: (el.innerText || el.value || el.placeholder || el.getAttribute('aria-label') || '').trim().slice(0, 80),
            selector: selector,
            rect: {
              x: Math.round(rect.left),
              y: Math.round(rect.top),
              width: Math.round(rect.width),
              height: Math.round(rect.height)
            },
            disabled: el.disabled || false
          });
        });

        return {
          url: window.location.href,
          title: document.title,
          viewport: { width: window.innerWidth, height: window.innerHeight },
          totalInteractive: elements.length,
          elements: elements
        };
      }
    }).then((results) => {
      sendSocket({
        type: "semantic_dom",
        data: results?.[0]?.result,
        timestamp: Date.now()
      });
    }).catch((err) => {
      sendSocket({ type: "semantic_dom", data: { error: err.toString() } });
    });
  }, true);
}

// ==========================================
// 7. Smart Wait Helpers
// ==========================================
function handleWaitForSelector(data) {
  getActiveChromeTab((tab) => {
    if (!tab) return sendSocket({ type: "action_result", action: "waitForSelector", result: { found: false, message: "Restricted tab" } });
    const timeout = data.timeout || 10000;
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: (sel, maxWait) => {
        return new Promise((resolve) => {
          const startTime = Date.now();
          const check = () => {
            const el = document.querySelector(sel);
            if (el) {
              const rect = el.getBoundingClientRect();
              resolve({ found: true, selector: sel, rect: { x: rect.left, y: rect.top, width: rect.width, height: rect.height } });
            } else if (Date.now() - startTime >= maxWait) {
              resolve({ found: false, message: `Timeout waiting for ${sel}` });
            } else {
              setTimeout(check, 100);
            }
          };
          check();
        });
      },
      args: [data.selector, timeout]
    }).then((results) => {
      sendSocket({ type: "action_result", action: "waitForSelector", result: results?.[0]?.result });
    }).catch((err) => {
      sendSocket({ type: "action_result", action: "waitForSelector", result: { found: false, error: err.toString() } });
    });
  }, true);
}

function handleWaitForNavigation(data) {
  const timeout = data.timeout || 15000;
  const timeoutTimer = setTimeout(() => {
    chrome.tabs.onUpdated.removeListener(navListener);
    sendSocket({ type: "action_result", action: "waitForNavigation", result: { success: false, timeout: true } });
  }, timeout);

  function navListener(tabId, changeInfo) {
    if (changeInfo.status === "complete") {
      clearTimeout(timeoutTimer);
      chrome.tabs.onUpdated.removeListener(navListener);
      sendSocket({ type: "action_result", action: "waitForNavigation", result: { success: true } });
    }
  }

  chrome.tabs.onUpdated.addListener(navListener);
}

// ==========================================
// 8. Visual Capture & Screenshots Suite
// ==========================================
async function handleCaptureScreenshot(options) {
  getActiveChromeTab(async (tab) => {
    if (!tab) return;

    const mode = options.mode || (options.selector ? "crop" : "viewport");
    const tag = options.tag || options.filename || "auto.png";

    if (mode === "crop" && options.selector && isInjectableUrl(tab.url)) {
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: (sel) => {
          const el = document.querySelector(sel);
          if (!el) return null;
          el.scrollIntoView({ behavior: 'instant', block: 'center' });
          const rect = el.getBoundingClientRect();
          return {
            rect: { x: rect.left, y: rect.top, width: rect.width, height: rect.height },
            dpr: window.devicePixelRatio || 1
          };
        },
        args: [options.selector]
      }).then((results) => {
        const info = results?.[0]?.result;
        if (!info) {
          sendSocket({ type: "error", message: `Element ${options.selector} not found for crop` });
          return;
        }

        setTimeout(() => {
          chrome.tabs.captureVisibleTab(tab.windowId, { format: "png" }, async (dataUrl) => {
            if (chrome.runtime.lastError || !dataUrl) return;

            ensureOffscreenDocument();
            chrome.runtime.sendMessage({
              target: "offscreen",
              action: "cropImage",
              dataUrl: dataUrl,
              rect: info.rect,
              dpr: info.dpr
            }, (res) => {
              const finalUrl = res?.dataUrl || dataUrl;
              sendSocket({
                type: "screenshot",
                tag: tag,
                mode: "crop",
                selector: options.selector,
                tabId: tab.id,
                tabTitle: tab.title,
                tabUrl: tab.url,
                dataUrl: finalUrl,
                timestamp: Date.now()
              });
            });
          });
        }, 150);
      }).catch((err) => {
        sendSocket({ type: "error", message: err.toString() });
      });

    } else if (mode === "fullPage" && isInjectableUrl(tab.url)) {
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => {
          return {
            totalHeight: Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
            viewportHeight: window.innerHeight,
            totalWidth: window.innerWidth,
            dpr: window.devicePixelRatio || 1
          };
        }
      }).then(async (metricsRes) => {
        const m = metricsRes?.[0]?.result;
        if (!m) return;

        const slices = [];
        let currentY = 0;

        async function captureNextSlice() {
          if (currentY >= m.totalHeight) {
            chrome.scripting.executeScript({
              target: { tabId: tab.id },
              func: () => window.scrollTo(0, 0)
            }).catch(() => {});

            ensureOffscreenDocument();
            chrome.runtime.sendMessage({
              target: "offscreen",
              action: "stitchImages",
              slices: slices,
              totalWidth: m.totalWidth,
              totalHeight: m.totalHeight,
              dpr: m.dpr
            }, (stitchRes) => {
              const finalUrl = stitchRes?.dataUrl;
              sendSocket({
                type: "screenshot",
                tag: tag,
                mode: "fullPage",
                tabId: tab.id,
                tabTitle: tab.title,
                tabUrl: tab.url,
                dataUrl: finalUrl,
                timestamp: Date.now()
              });
            });
            return;
          }

          await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: (y) => window.scrollTo(0, y),
            args: [currentY]
          }).catch(() => {});

          setTimeout(() => {
            chrome.tabs.captureVisibleTab(tab.windowId, { format: "png" }, (sliceUrl) => {
              if (sliceUrl) {
                slices.push({ offsetY: currentY, dataUrl: sliceUrl });
              }
              currentY += m.viewportHeight;
              captureNextSlice();
            });
          }, 200);
        }

        captureNextSlice();
      }).catch((err) => {
        sendSocket({ type: "error", message: err.toString() });
      });

    } else {
      chrome.tabs.captureVisibleTab(tab.windowId, { format: "png" }, (dataUrl) => {
        if (chrome.runtime.lastError || !dataUrl) {
          sendSocket({
            type: "stream_status",
            status: "error",
            error: chrome.runtime.lastError?.message || "Capture error",
            tabId: tab.id
          });
          return;
        }
        sendSocket({
          type: "screenshot",
          tag: tag,
          mode: "viewport",
          tabId: tab.id,
          tabTitle: tab.title,
          tabUrl: tab.url,
          dataUrl: dataUrl,
          timestamp: Date.now()
        });
      });
    }
  });
}

// ==========================================
// 9. Streaming Engine (Quota-Safe Adaptive FPS)
// ==========================================
let isCapturing = false;
let lastCaptureTime = 0;

function safeCaptureTab(windowId, options, callback) {
  const now = Date.now();
  // Chrome hard limit is 2 calls per second. Enforce minimum 600ms spacing.
  if (isCapturing || (now - lastCaptureTime < 600)) {
    if (callback) callback(new Error("Throttled by rate limiter"), null);
    return;
  }

  isCapturing = true;
  lastCaptureTime = now;

  chrome.tabs.captureVisibleTab(windowId, options, (dataUrl) => {
    isCapturing = false;
    if (callback) callback(chrome.runtime.lastError, dataUrl);
  });
}

function startLiveStream(fps, quality) {
  stopLiveStream();
  isStreaming = true;
  // Interval must be >= 650ms to strictly respect Chrome's 2 calls/sec quota
  const intervalMs = Math.max(650, Math.floor(1000 / (fps || 1.5)));
  const imgQuality = quality || 70;

  streamInterval = setInterval(() => {
    if (!socket || socket.readyState !== WebSocket.OPEN) return;
    getActiveChromeTab((tab) => {
      if (!tab) return;
      safeCaptureTab(tab.windowId, { format: "jpeg", quality: imgQuality }, (err, dataUrl) => {
        if (err) {
          const errMsg = err.message || err.toString();
          if (errMsg.includes("minimized") || errMsg.includes("active window")) {
            sendSocket({
              type: "stream_status",
              status: "paused",
              reason: errMsg,
              tabId: tab.id,
              tabTitle: tab.title
            });
          }
          return;
        }
        if (dataUrl) {
          sendSocket({
            type: "screenshot",
            dataUrl: dataUrl,
            tabId: tab.id,
            tabTitle: tab.title,
            tabUrl: tab.url,
            timestamp: Date.now()
          });
        }
      });
    });
  }, intervalMs);
}

function stopLiveStream() {
  isStreaming = false;
  if (streamInterval) {
    clearInterval(streamInterval);
    streamInterval = null;
  }
}

// ==========================================
// 10. Console Mirroring & Storage Helpers
// ==========================================
function injectConsoleProxy(specificTabId, specificUrl) {
  if (specificTabId && specificUrl) {
    if (!isInjectableUrl(specificUrl)) return;
    executeProxy(specificTabId);
    return;
  }

  getActiveChromeTab((tab) => {
    if (!tab || !isInjectableUrl(tab.url)) return;
    executeProxy(tab.id);
  }, true);

  function executeProxy(targetId) {
    chrome.scripting.executeScript({
      target: { tabId: targetId },
      func: () => {
        if (window.__antigravity_console_injected) return;
        window.__antigravity_console_injected = true;

        const levels = ['log', 'info', 'warn', 'error'];
        levels.forEach((lvl) => {
          const orig = console[lvl];
          console[lvl] = function (...args) {
            orig.apply(console, args);
            try {
              const text = args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ');
              chrome.runtime?.sendMessage?.({ type: "page_console_log", level: lvl, text: text });
            } catch (e) {}
          };
        });

        window.addEventListener('error', (evt) => {
          chrome.runtime?.sendMessage?.({
            type: "page_console_log",
            level: "error",
            text: `Uncaught Error: ${evt.message} at ${evt.filename}:${evt.lineno}`
          });
        });
      }
    }).catch(() => {});
  }
}

function handleGetCookies(data) {
  getActiveChromeTab((tab) => {
    if (!tab || !tab.url || !tab.url.startsWith("http")) return;
    chrome.cookies.getAll({ url: tab.url }, (cookies) => {
      sendSocket({ type: "action_result", action: "getCookies", cookies: cookies });
    });
  });
}

function handleSetCookie(data) {
  chrome.cookies.set(data.cookieDetails, (c) => {
    sendSocket({ type: "action_result", action: "setCookie", cookie: c });
  });
}

// ==========================================
// 11. Lifecycle Listeners & Initialization
// ==========================================
function sendSocket(obj) {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(obj));
  }
}

chrome.tabs.onActivated.addListener((activeInfo) => {
  selectedTabId = activeInfo.tabId;
  sendActiveTabInfo();
  broadcastAllTabs();
  setTimeout(captureAndSendFrame, 60);
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete") {
    sendActiveTabInfo();
    broadcastAllTabs();
    if (tab && tab.url && isInjectableUrl(tab.url)) {
      injectConsoleProxy(tabId, tab.url);
    }
    setTimeout(captureAndSendFrame, 60);
  }
});

chrome.tabs.onRemoved.addListener((removedTabId) => {
  if (selectedTabId === removedTabId) selectedTabId = null;
  broadcastAllTabs();
});

// Bootstrapping
loadConfig().then(() => {
  ensureOffscreenDocument();
  connect();
});
