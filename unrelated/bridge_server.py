import asyncio
import json
import http.server
import socketserver
import threading
import os
import base64
import subprocess
import sys

try:
    import websockets
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets"])
    import websockets

CONNECTED_EXTENSION = None
CONNECTED_VIEWERS = set()
ALL_TABS = []
ACTIVE_TAB = {}
LATEST_FRAME = None
CONSOLE_LOGS = []

BASE_DIR = os.path.dirname(__file__)
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

FIGURE_MAPPING = [
    ("fig1_7a_azure_spending.png", "Fig 1.7(a): Azure Subscription Cost Analysis"),
    ("fig1_7b_azure_resources.png", "Fig 1.7(b): Azure Resource Inventory (polisewa)"),
    ("fig3_5_1a_ui_wireframe.png", "Fig 3.5.1(a): Responsive UI Wireframe"),
    ("fig4_1_1b_dual_azure_vms.png", "Fig 4.1.1(b): Dual Azure VMs Running Status"),
    ("fig4_1_2_cloudflare_edge.png", "Fig 4.1.2(a): Cloudflare Edge Status"),
    ("fig4_1_3_azure_sql_firewall.png", "Fig 4.1.3(a): Azure SQL Firewall Rules"),
    ("fig4_1_4_vm_linux_terminal.png", "Fig 4.1.4(a): VM Linux Terminal"),
    ("fig4_2_3_azure_sql_query_editor.png", "Fig 4.2.3: Azure SQL Query Editor"),
    ("fig4_2_1_polisewa_map_ui.png", "Fig 4.2.1: Polisewa Map UI"),
    ("fig5_1_1a_cloudflare_connectors.png", "Fig 5.1.1(a): Cloudflare Dual Connectors"),
    ("fig5_1_2a_vm1_termination.png", "Fig 5.1.2(a): VM1 Service Termination"),
    ("fig5_1_2b_uninterrupted_http200.png", "Fig 5.1.2(b): DevTools HTTP 200 OK Failover"),
    ("fig5_2_2a_search_filtering.png", "Fig 5.2.2(a): Search & Price Filtering"),
    ("fig5_2_3a_otp_modal.png", "Fig 5.2.3(a): 6-Box Email OTP Dialog"),
    ("fig5_2_3b_otp_gmail.png", "Fig 5.2.3(b): PoliSewa OTP Email in Gmail"),
    ("fig5_2_4a_property_modal.png", "Fig 5.2.4(a): Landlord Property Modal"),
    ("fig5_2_5a_whatsapp_verified.png", "Fig 5.2.5(a): WhatsApp Listing Card"),
    ("fig5_2_6a_account_deletion.png", "Fig 5.2.6(a): Permanent Account Deletion")
]

def wake_chrome_native():
    try:
        # Use PowerShell ComObject to bring Chrome window to the foreground
        cmd = ['powershell', '-NoProfile', '-Command', '$wshell = New-Object -ComObject WScript.Shell; $wshell.AppActivate("Google Chrome")']
        subprocess.Popen(cmd)
    except Exception as e:
        print(f"[!] Error activating Chrome: {e}")

async def ws_handler(websocket):
    global CONNECTED_EXTENSION, ALL_TABS, ACTIVE_TAB, LATEST_FRAME, CONSOLE_LOGS
    
    print(f"[*] Connection received: {websocket.remote_address}")
    CONNECTED_VIEWERS.add(websocket)

    # Immediately hydrate newly connected viewer with latest state & frame
    try:
        if ALL_TABS:
            await websocket.send(json.dumps({
                "type": "tabs_list",
                "tabs": ALL_TABS
            }))
        if LATEST_FRAME:
            await websocket.send(json.dumps({
                "type": "screenshot",
                "dataUrl": LATEST_FRAME,
                "tabTitle": ACTIVE_TAB.get("title", ""),
                "tabUrl": ACTIVE_TAB.get("url", "")
            }))
    except Exception:
        pass
    
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                msg_type = data.get("type")
                
                # Ping / Pong Keep-Alive
                if msg_type == "ping":
                    await websocket.send(json.dumps({
                        "type": "pong",
                        "timestamp": data.get("timestamp")
                    }))
                    continue

                # Messages from Chrome Extension
                if msg_type in ["tabs_list", "tab_update", "screenshot", "action_result", "eval_result", "semantic_dom", "console_log", "stream_status"]:
                    CONNECTED_EXTENSION = websocket
                    if msg_type == "tabs_list":
                        ALL_TABS = data.get("tabs", [])
                    elif msg_type == "tab_update":
                        ACTIVE_TAB = data
                    elif msg_type == "console_log":
                        CONSOLE_LOGS.append(data)
                        if len(CONSOLE_LOGS) > 200:
                            CONSOLE_LOGS.pop(0)
                    elif msg_type == "screenshot":
                        LATEST_FRAME = data.get("dataUrl")
                        tag = data.get("tag")
                        if tag and tag.endswith(".png"):
                            save_frame_to_disk(tag, data.get("dataUrl"))
                            
                    # Forward to all connected Studio viewers
                    dead = set()
                    for v in CONNECTED_VIEWERS:
                        if v != websocket:
                            try:
                                await v.send(message)
                            except:
                                dead.add(v)
                    CONNECTED_VIEWERS.difference_update(dead)
                    
                # Commands from AI or Web Studio Dashboard
                elif data.get("command"):
                    cmd = data.get("command")
                    if cmd == "focusChrome":
                        wake_chrome_native()
                    if CONNECTED_EXTENSION:
                        try:
                            await CONNECTED_EXTENSION.send(message)
                        except Exception as err:
                            print(f"[!] Failed to forward command to Chrome: {err}")
                    else:
                        print("[!] Chrome extension not currently connected to WebSocket")
            except Exception as parse_err:
                print(f"[!] Message parse error: {parse_err}")
    finally:
        CONNECTED_VIEWERS.discard(websocket)
        if CONNECTED_EXTENSION == websocket:
            CONNECTED_EXTENSION = None
            print("[-] Chrome extension disconnected")

def save_frame_to_disk(filename, data_url):
    try:
        if "," in data_url:
            header, encoded = data_url.split(",", 1)
            img_bytes = base64.b64decode(encoded)
            target = os.path.join(SCREENSHOTS_DIR, filename)
            with open(target, "wb") as f:
                f.write(img_bytes)
            print(f"[Auto-Saved] {filename} ({len(img_bytes)} bytes)")
            return True
    except Exception as e:
        print(f"[!] Error saving frame: {e}")
    return False

def run_web_studio():
    PORT = 9998
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_POST(self):
            if self.path.startswith("/api/save_figure"):
                length = int(self.headers.get('Content-Length', 0))
                body = json.loads(self.rfile.read(length).decode('utf-8'))
                fname = body.get("filename")
                durl = body.get("dataUrl") or LATEST_FRAME
                if fname and durl and save_frame_to_disk(fname, durl):
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(b'{"success":true}')
                    return
                self.send_response(400)
                self.end_headers()
                return
            super().do_GET()

        def do_GET(self):
            clean_path = self.path.split("?")[0]
            if clean_path == "/api/latest_frame":
                if LATEST_FRAME and "," in LATEST_FRAME:
                    _, encoded = LATEST_FRAME.split(",", 1)
                    raw_bytes = base64.b64decode(encoded)
                    self.send_response(200)
                    self.send_header("Content-Type", "image/jpeg")
                    self.send_header("Content-Length", str(len(raw_bytes)))
                    self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                    self.end_headers()
                    self.wfile.write(raw_bytes)
                    return
                self.send_response(404)
                self.end_headers()
                return
            if clean_path in ["", "/", "/index.html"]:
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                options = "".join([f'<option value="{f[0]}">{f[1]}</option>' for f in FIGURE_MAPPING])
                
                html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>Antigravity Chrome Studio Pro</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        :root {{
            --bg-base: #07090e;
            --bg-surface: #0e131f;
            --bg-card: #141b2d;
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-accent: #0284c7;
            --cyan: #38bdf8;
            --emerald: #10b981;
            --violet: #8b5cf6;
            --amber: #f59e0b;
            --rose: #f43f5e;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --radius-lg: 12px;
            --radius-md: 8px;
            --radius-sm: 6px;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg-base);
            color: var(--text-main);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            user-select: none;
        }}

        /* ================= Header ================= */
        .top-navbar {{
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border-subtle);
            padding: 8px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            z-index: 20;
        }}
        .brand-cluster {{
            display: flex;
            align-items: center;
            gap: 10px;
            min-width: 220px;
        }}
        .logo-badge {{
            font-size: 13px;
            font-weight: 800;
            color: var(--cyan);
            letter-spacing: -0.3px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .status-pill {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 3px 9px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 600;
            background: rgba(239, 68, 68, 0.15);
            color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.3);
            transition: all 0.2s ease;
        }}
        .status-pill.connected {{
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border-color: rgba(16, 185, 129, 0.3);
        }}
        .status-dot {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: currentColor;
            box-shadow: 0 0 6px currentColor;
        }}

        /* Browser Navigation Bar */
        .nav-controls {{
            flex: 1;
            max-width: 580px;
            display: flex;
            align-items: center;
            gap: 6px;
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 3px 6px;
        }}
        .icon-btn {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            width: 28px;
            height: 28px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.15s ease;
        }}
        .icon-btn:hover {{
            background: rgba(255, 255, 255, 0.08);
            color: var(--text-main);
        }}
        .url-input {{
            flex: 1;
            background: transparent;
            border: none;
            color: var(--text-main);
            font-size: 12px;
            padding: 4px 6px;
            outline: none;
            font-family: monospace;
        }}
        .url-input::placeholder {{ color: #475569; }}

        /* Action Controls */
        .toolbar-actions {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        select.custom-select {{
            background: var(--bg-card);
            color: var(--text-main);
            border: 1px solid var(--border-subtle);
            padding: 6px 10px;
            border-radius: var(--radius-sm);
            font-size: 11px;
            max-width: 240px;
            outline: none;
            cursor: pointer;
        }}
        .btn {{
            padding: 6px 12px;
            border-radius: var(--radius-sm);
            font-size: 11px;
            font-weight: 600;
            border: 1px solid transparent;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.15s ease;
        }}
        .btn-wake {{
            background: rgba(56, 189, 248, 0.15);
            color: var(--cyan);
            border-color: rgba(56, 189, 248, 0.35);
        }}
        .btn-wake:hover {{
            background: rgba(56, 189, 248, 0.25);
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
        }}
        .btn-primary {{
            background: #0284c7;
            color: white;
        }}
        .btn-primary:hover {{ background: #0369a1; }}
        .btn-success {{
            background: #059669;
            color: white;
        }}
        .btn-success:hover {{ background: #047857; }}
        .btn-subtle {{
            background: var(--bg-card);
            color: var(--text-muted);
            border-color: var(--border-subtle);
        }}
        .btn-subtle:hover {{
            background: rgba(255, 255, 255, 0.06);
            color: var(--text-main);
        }}
        .btn-subtle.active {{
            background: rgba(139, 92, 246, 0.2);
            color: #a78bfa;
            border-color: #8b5cf6;
        }}

        /* ================= Browser Tabs Bar ================= */
        .tabs-strip {{
            background: var(--bg-base);
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            align-items: center;
            padding: 4px 12px 0 12px;
            gap: 4px;
            overflow-x: auto;
            scrollbar-width: none;
            min-height: 38px;
        }}
        .tabs-strip::-webkit-scrollbar {{ display: none; }}
        .tab-item {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-subtle);
            border-bottom: none;
            color: var(--text-muted);
            padding: 6px 12px;
            border-radius: 8px 8px 0 0;
            font-size: 11px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            max-width: 220px;
            min-width: 120px;
            white-space: nowrap;
            transition: all 0.15s ease;
            position: relative;
        }}
        .tab-item:hover {{
            background: rgba(255, 255, 255, 0.06);
            color: var(--text-main);
        }}
        .tab-item.active {{
            background: var(--bg-surface);
            color: var(--cyan);
            border-color: var(--border-subtle);
            border-top: 2px solid var(--cyan);
            font-weight: 600;
        }}
        .tab-item img {{
            width: 14px;
            height: 14px;
            border-radius: 2px;
            flex-shrink: 0;
        }}
        .tab-item .tab-title-text {{
            overflow: hidden;
            text-overflow: ellipsis;
            flex: 1;
        }}
        .tab-close-btn {{
            width: 14px;
            height: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            font-size: 10px;
            opacity: 0.5;
            transition: opacity 0.15s;
        }}
        .tab-close-btn:hover {{ opacity: 1; background: rgba(255, 255, 255, 0.2); }}

        /* ================= Workspace Layout ================= */
        .workspace {{
            flex: 1;
            display: flex;
            overflow: hidden;
            position: relative;
            background: #04060a;
        }}
        .viewport-pane {{
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            padding: 16px;
            overflow: auto;
        }}
        .mockup-window {{
            display: flex;
            flex-direction: column;
            border-radius: var(--radius-lg);
            border: 1px solid var(--border-subtle);
            background: #0a0e17;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.85);
            max-width: 100%;
            max-height: 100%;
            overflow: hidden;
            position: relative;
        }}
        .mockup-header {{
            background: #0f1523;
            border-bottom: 1px solid var(--border-subtle);
            padding: 6px 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 11px;
            color: var(--text-muted);
        }}
        .mac-dots {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .mac-dot {{ width: 9px; height: 9px; border-radius: 50%; }}
        .mac-dot.red {{ background: #ef4444; }}
        .mac-dot.yellow {{ background: #f59e0b; }}
        .mac-dot.green {{ background: #10b981; }}
        
        .mockup-canvas-wrapper {{
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #020408;
            overflow: hidden;
        }}
        #screen {{
            max-width: 100%;
            max-height: calc(100vh - 220px);
            object-fit: contain;
            cursor: crosshair;
            outline: none;
            display: none;
        }}
        #screen:focus {{
            box-shadow: inset 0 0 0 2px var(--cyan);
        }}

        /* Fallback Empty / Minimized State */
        .empty-stream-card {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 48px 32px;
            text-align: center;
            max-width: 440px;
        }}
        .empty-icon {{
            font-size: 36px;
            margin-bottom: 12px;
            filter: drop-shadow(0 0 16px rgba(56, 189, 248, 0.4));
        }}
        .empty-title {{
            font-size: 15px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 6px;
        }}
        .empty-desc {{
            font-size: 12px;
            color: var(--text-muted);
            line-height: 1.5;
            margin-bottom: 18px;
        }}

        /* Keyboard & Coordinates HUD */
        .viewport-footer {{
            background: #0f1523;
            border-top: 1px solid var(--border-subtle);
            padding: 6px 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 11px;
            color: var(--text-muted);
            gap: 12px;
        }}
        .quick-type-box {{
            display: flex;
            align-items: center;
            gap: 6px;
            flex: 1;
            max-width: 380px;
        }}
        .quick-type-input {{
            width: 100%;
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-sm);
            padding: 4px 8px;
            color: var(--text-main);
            font-size: 11px;
            outline: none;
        }}
        .quick-type-input:focus {{
            border-color: var(--cyan);
        }}

        /* Ripple effect */
        .click-dot {{
            position: absolute;
            width: 28px;
            height: 28px;
            border: 2px solid var(--cyan);
            border-radius: 50%;
            pointer-events: none;
            transform: translate(-50%, -50%) scale(0.4);
            opacity: 1;
            transition: all 0.45s cubic-bezier(0.1, 0.9, 0.2, 1);
            z-index: 500;
            background: rgba(56, 189, 248, 0.2);
        }}

        /* ================= Drawers (DOM & Logs) ================= */
        .side-drawer {{
            width: 360px;
            background: var(--bg-surface);
            border-left: 1px solid var(--border-subtle);
            display: flex;
            flex-direction: column;
            z-index: 15;
            transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .side-drawer.hidden {{ display: none; }}
        .drawer-header {{
            padding: 10px 14px;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border-subtle);
            font-weight: 700;
            font-size: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .drawer-search {{
            padding: 8px 12px;
            border-bottom: 1px solid var(--border-subtle);
            background: var(--bg-surface);
        }}
        .drawer-search input {{
            width: 100%;
            padding: 6px 10px;
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-sm);
            color: var(--text-main);
            font-size: 11px;
            outline: none;
        }}
        .drawer-body {{
            flex: 1;
            overflow-y: auto;
            padding: 8px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        .dom-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-sm);
            padding: 8px 10px;
            font-size: 11px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            transition: border-color 0.15s;
        }}
        .dom-card:hover {{ border-color: rgba(56, 189, 248, 0.4); }}
        .dom-badge {{
            font-size: 9px;
            padding: 2px 5px;
            border-radius: 4px;
            background: rgba(56, 189, 248, 0.15);
            color: var(--cyan);
            font-family: monospace;
            font-weight: bold;
        }}
        .dom-label {{
            color: #cbd5e1;
            font-size: 11px;
            max-width: 190px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            margin-top: 2px;
        }}

        /* Bottom Console Drawer */
        .console-drawer {{
            height: 180px;
            background: #06080d;
            border-top: 1px solid var(--border-subtle);
            display: flex;
            flex-direction: column;
            font-family: 'SF Mono', Menlo, monospace;
            font-size: 11px;
            z-index: 10;
        }}
        .console-drawer.hidden {{ display: none; }}
        .console-header {{
            padding: 6px 14px;
            background: #0e131f;
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .console-logs-pane {{
            flex: 1;
            overflow-y: auto;
            padding: 8px 14px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        .log-row {{ line-height: 1.4; word-break: break-all; }}
        .log-error {{ color: #f87171; }}
        .log-warn {{ color: #fbbf24; }}
        .log-info {{ color: #60a5fa; }}
        .log-log {{ color: #94a3b8; }}

        #toast {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: #059669;
            color: white;
            font-weight: 600;
            font-size: 12px;
            padding: 10px 18px;
            border-radius: var(--radius-md);
            display: none;
            z-index: 9999;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.6);
        }}
    </style>
</head>
<body>

    <!-- ================= 1. Top Navbar ================= -->
    <header class="top-navbar">
        <div class="brand-cluster">
            <div class="logo-badge">⚡ Antigravity Studio <span style="font-size:9px;background:rgba(56,189,248,0.2);padding:1px 5px;border-radius:4px;">PRO 3.0</span></div>
            <div id="connBadge" class="status-pill">
                <span class="status-dot"></span>
                <span id="connText">Connecting...</span>
            </div>
        </div>

        <!-- Browser Navigation Bar -->
        <div class="nav-controls">
            <button class="icon-btn" onclick="sendCmd('navigateBack')" title="Back">◀</button>
            <button class="icon-btn" onclick="sendCmd('navigateForward')" title="Forward">▶</button>
            <button class="icon-btn" onclick="sendCmd('reloadTab')" title="Reload Page">🔄</button>
            <input type="text" id="urlBar" class="url-input" placeholder="Enter URL or address..." onkeydown="handleUrlEnter(event)" />
            <button class="btn btn-subtle" style="padding:2px 8px;font-size:10px;" onclick="navigateCurrentUrl()">Go</button>
        </div>

        <!-- Toolbar Actions -->
        <div class="toolbar-actions">
            <button class="btn btn-wake" onclick="sendCmd('focusChrome')" title="Un-minimize & Focus Chrome Window">⚡ Wake Chrome</button>
            <button class="btn btn-subtle" onclick="sendCmd('captureScreenshot')" title="Force Screen Refresh">🔄 Refresh Screen</button>
            
            <select id="figSelect" class="custom-select">{options}</select>
            <select id="snapMode" class="custom-select" style="max-width:110px;">
                <option value="viewport">Viewport</option>
                <option value="fullPage">Full Page</option>
            </select>
            <button onclick="saveSelectedFigure()" class="btn btn-success">📸 Save</button>
            <button onclick="toggleDomDrawer()" class="btn btn-subtle" id="domToggleBtn">🧠 DOM (<span id="elemCount">0</span>)</button>
            <button onclick="toggleConsoleDrawer()" class="btn btn-subtle" id="logToggleBtn">📜 Logs (<span id="logCount">0</span>)</button>
        </div>
    </header>

    <!-- ================= 2. Browser Tabs Strip ================= -->
    <div class="tabs-strip" id="tabsBar">
        <div style="color:var(--text-muted);font-size:11px;padding:6px;">Connecting to Chrome tabs...</div>
    </div>

    <!-- ================= 3. Main Workspace ================= -->
    <div class="workspace">
        <div class="viewport-pane">
            <div class="mockup-window">
                <div class="mockup-header">
                    <div class="mac-dots">
                        <div class="mac-dot red"></div>
                        <div class="mac-dot yellow"></div>
                        <div class="mac-dot green"></div>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <div id="windowTabTitle" style="font-weight:600;max-width:320px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">Active Chrome Viewport</div>
                        <span id="statusNotice" style="font-size:10px;color:#34d399;font-weight:600;"></span>
                    </div>
                    <div id="hudCoords" style="font-family:monospace;font-size:10px;">X: - | Y: -</div>
                </div>

                <div class="mockup-canvas-wrapper" id="canvasWrapper" onwheel="handleScreenWheel(event)">
                    <!-- Placeholder Card when Chrome is minimized or not streaming -->
                    <div class="empty-stream-card" id="placeholder">
                        <div class="empty-icon">🖥️</div>
                        <div class="empty-title">Waiting for Chrome Pixels</div>
                        <div class="empty-desc">
                            Windows halts graphic rendering when Chrome is minimized to the taskbar or covered. Click below to bring Chrome to the foreground.
                        </div>
                        <button class="btn btn-wake" style="padding:10px 20px;font-size:13px;" onclick="sendCmd('focusChrome')">
                            ⚡ Wake & Un-minimize Chrome
                        </button>
                    </div>

                    <!-- Screen Element -->
                    <img id="screen" tabindex="0" onclick="handleScreenClick(event)" ondblclick="handleScreenDblClick(event)" oncontextmenu="handleScreenContextMenu(event)" onwheel="handleScreenWheel(event)" onmousemove="handleScreenMove(event)" onkeydown="handleScreenKeyDown(event)" alt="Live Chrome Viewport" />
                </div>

                <div class="viewport-footer">
                    <div class="quick-type-box">
                        <span style="font-size:12px;">⌨️</span>
                        <input type="text" id="quickTypeInput" class="quick-type-input" placeholder="Type text & hit Enter to fill active input..." onkeydown="handleQuickType(event)" />
                    </div>
                    <div style="display:flex;align-items:center;gap:12px;">
                        <span id="remoteKeyboardNotice" style="color:#38bdf8;font-size:10px;">Click canvas to relay keys directly</span>
                        <button class="icon-btn" onclick="sendCmd('captureScreenshot')" title="Force Screen Refresh">🔄</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= 4. Semantic DOM Side Drawer ================= -->
        <aside class="side-drawer hidden" id="domSidebar">
            <div class="drawer-header">
                <span>Interactive Elements (<span id="elemCountHeader">0</span>)</span>
                <button class="btn btn-subtle" style="padding:2px 8px;font-size:10px;" onclick="refreshDomScan()">Rescan</button>
            </div>
            <div class="drawer-search">
                <input type="text" id="domSearch" placeholder="Filter buttons, links, inputs..." oninput="filterDomElements()" />
            </div>
            <div class="drawer-body" id="domList">
                <div style="color:var(--text-muted);font-size:11px;padding:8px;">Click 'Rescan' to extract interactive DOM.</div>
            </div>
        </aside>
    </div>

    <!-- ================= 5. Live Console Bottom Drawer ================= -->
    <div class="console-drawer hidden" id="consoleDrawer">
        <div class="console-header">
            <div style="display:flex;align-items:center;gap:12px;">
                <b style="color:var(--text-main);">Browser Console Telemetry</b>
                <span id="consoleFilterLabel" style="color:var(--text-muted);font-size:10px;">Live Mirror</span>
            </div>
            <button class="btn btn-subtle" style="padding:2px 8px;font-size:10px;" onclick="clearConsole()">Clear Logs</button>
        </div>
        <div class="console-logs-pane" id="consoleLogs"></div>
    </div>

    <div id="toast"></div>

    <script>
        let ws;
        let currentFrame = null;
        let currentTabs = [];
        let domElements = [];
        let logsList = [];
        let activeTabId = null;
        let currentTabUrl = "";

        function init() {{
            // Preload latest frame from server
            fetch("/api/latest_frame")
                .then(r => r.ok ? r.blob() : null)
                .then(b => {{
                    if (b) {{
                        const url = URL.createObjectURL(b);
                        currentFrame = url;
                        const img = document.getElementById("screen");
                        img.src = url;
                        img.style.display = "block";
                        document.getElementById("placeholder").style.display = "none";
                        const sn = document.getElementById("statusNotice");
                        if (sn) sn.innerText = "● Snapshot Ready";
                    }}
                }}).catch(() => {{}});

            ws = new WebSocket("ws://localhost:9999");

            ws.onopen = () => {{
                const badge = document.getElementById("connBadge");
                const text = document.getElementById("connText");
                badge.classList.add("connected");
                text.innerText = "Connected :9999";
                sendCmd("listTabs");
                sendCmd("captureScreenshot");
                sendCmd("startStream", {{ fps: 1.5 }});
                sendCmd("enableConsoleCapture");
            }};

            ws.onclose = () => {{
                const badge = document.getElementById("connBadge");
                const text = document.getElementById("connText");
                badge.classList.remove("connected");
                text.innerText = "Disconnected";
                setTimeout(init, 2000);
            }};

            ws.onmessage = (event) => {{
                const data = JSON.parse(event.data);
                
                if (data.type === "tabs_list") {{
                    renderTabs(data.tabs);
                }} else if (data.type === "tab_update") {{
                    updateActiveTabBar(data);
                }} else if (data.type === "screenshot" && data.dataUrl) {{
                    currentFrame = data.dataUrl;
                    const img = document.getElementById("screen");
                    img.src = data.dataUrl;
                    img.style.display = "block";
                    document.getElementById("placeholder").style.display = "none";
                    if (data.tabTitle) document.getElementById("windowTabTitle").innerText = data.tabTitle;
                    if (data.tabUrl) {{
                        currentTabUrl = data.tabUrl;
                        document.getElementById("urlBar").value = data.tabUrl;
                        const isRestricted = data.tabUrl.startsWith("chrome://") || data.tabUrl.startsWith("edge://") || data.tabUrl.startsWith("about:") || data.tabUrl.startsWith("chrome-extension://");
                        const sn = document.getElementById("statusNotice");
                        if (sn) {{
                            if (isRestricted) {{
                                sn.innerText = "⚠️ Protected chrome:// tab (Select a website tab above to interact)";
                                sn.style.color = "#f59e0b";
                            }} else {{
                                sn.innerText = "● Interactive Live Stream Active";
                                sn.style.color = "#34d399";
                            }}
                        }}
                    }}
                }} else if (data.type === "console_log") {{
                    appendConsoleLog(data);
                }} else if (data.type === "semantic_dom") {{
                    renderDomElements(data.data?.elements || []);
                }} else if (data.type === "stream_status" && data.status === "paused") {{
                    if (!currentFrame) {{
                        document.getElementById("placeholder").style.display = "flex";
                    }} else {{
                        const sn = document.getElementById("statusNotice");
                        if (sn) {{
                            sn.innerText = "● Background Snapshot";
                            sn.style.color = "#f59e0b";
                        }}
                    }}
                }}
            }};
        }}

        function sendCmd(command, extra = {{}}) {{
            if (ws && ws.readyState === WebSocket.OPEN) {{
                ws.send(JSON.stringify({{ command, ...extra }}));
            }}
        }}

        function renderTabs(tabs) {{
            currentTabs = tabs;
            const bar = document.getElementById("tabsBar");
            bar.innerHTML = "";
            tabs.forEach(t => {{
                const item = document.createElement("div");
                item.className = "tab-item" + (t.active ? " active" : "");
                item.title = t.title + "\\n" + t.url;
                
                const icon = t.favIconUrl ? `<img src="${{t.favIconUrl}}" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 16 16%22><text y=%2214%22>🌐</text></svg>'">` : '🌐';
                item.innerHTML = `${{icon}}<span class="tab-title-text">${{t.title || 'Untitled'}}</span><span class="tab-close-btn" title="Close Tab">×</span>`;
                
                item.onclick = (e) => {{
                    if (e.target.classList.contains("tab-close-btn")) {{
                        e.stopPropagation();
                        sendCmd("closeTab", {{ tabId: t.id }});
                        return;
                    }}
                    activeTabId = t.id;
                    sendCmd("switchTab", {{ tabId: t.id }});
                }};
                bar.appendChild(item);
            }});
        }}

        function updateActiveTabBar(data) {{
            if (data.url) document.getElementById("urlBar").value = data.url;
            if (data.title) document.getElementById("windowTabTitle").innerText = data.title;
        }}

        let wheelDebounceTimer = null;
        let accumulatedDeltaY = 0;
        let accumulatedDeltaX = 0;

        function getNormalizedCoords(e, img) {{
            const rect = img.getBoundingClientRect();
            const normX = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
            const normY = Math.max(0, Math.min(1, (e.clientY - rect.top) / rect.height));
            const x = Math.round(normX * (img.naturalWidth || 1920));
            const y = Math.round(normY * (img.naturalHeight || 1080));
            return {{ normX, normY, x, y }};
        }}

        function triggerClickRipple(clientX, clientY) {{
            const wrapper = document.getElementById("canvasWrapper");
            const rect = wrapper.getBoundingClientRect();
            const dot = document.createElement("div");
            dot.className = "click-dot";
            dot.style.left = (clientX - rect.left) + "px";
            dot.style.top = (clientY - rect.top) + "px";
            wrapper.appendChild(dot);
            requestAnimationFrame(() => {{
                dot.style.transform = "translate(-50%, -50%) scale(2.2)";
                dot.style.opacity = "0";
            }});
            setTimeout(() => dot.remove(), 450);
        }}

        function handleScreenClick(e) {{
            if (currentTabUrl.startsWith("chrome://") || currentTabUrl.startsWith("edge://") || currentTabUrl.startsWith("chrome-extension://")) {{
                showToast("⚠️ Protected chrome:// tab. Click a website tab above to interact.");
                return;
            }}
            const img = document.getElementById("screen");
            const c = getNormalizedCoords(e, img);
            triggerClickRipple(e.clientX, e.clientY);

            sendCmd("click", {{ 
                coords: {{ normX: c.normX, normY: c.normY, x: c.x, y: c.y }},
                clickType: 'click'
            }});
            showToast("Clicked (" + c.x + ", " + c.y + ")");
            img.focus();
        }}

        function handleScreenDblClick(e) {{
            if (currentTabUrl.startsWith("chrome://") || currentTabUrl.startsWith("edge://") || currentTabUrl.startsWith("chrome-extension://")) return;
            const img = document.getElementById("screen");
            const c = getNormalizedCoords(e, img);
            triggerClickRipple(e.clientX, e.clientY);

            sendCmd("click", {{ 
                coords: {{ normX: c.normX, normY: c.normY, x: c.x, y: c.y }},
                clickType: 'dblclick'
            }});
            showToast("Double-Clicked (" + c.x + ", " + c.y + ")");
        }}

        function handleScreenContextMenu(e) {{
            e.preventDefault();
            if (currentTabUrl.startsWith("chrome://") || currentTabUrl.startsWith("edge://") || currentTabUrl.startsWith("chrome-extension://")) return;
            const img = document.getElementById("screen");
            const c = getNormalizedCoords(e, img);
            triggerClickRipple(e.clientX, e.clientY);

            sendCmd("click", {{ 
                coords: {{ normX: c.normX, normY: c.normY, x: c.x, y: c.y }},
                clickType: 'contextmenu'
            }});
            showToast("Right-Clicked (" + c.x + ", " + c.y + ")");
        }}

        function handleScreenWheel(e) {{
            e.preventDefault();
            if (currentTabUrl.startsWith("chrome://") || currentTabUrl.startsWith("edge://") || currentTabUrl.startsWith("chrome-extension://")) return;
            accumulatedDeltaY += e.deltaY;
            accumulatedDeltaX += e.deltaX;

            const img = document.getElementById("screen");
            const c = getNormalizedCoords(e, img);

            if (!wheelDebounceTimer) {{
                wheelDebounceTimer = setTimeout(() => {{
                    sendCmd("scroll", {{
                        y: Math.round(accumulatedDeltaY),
                        x: Math.round(accumulatedDeltaX),
                        normX: c.normX,
                        normY: c.normY
                    }});
                    accumulatedDeltaY = 0;
                    accumulatedDeltaX = 0;
                    wheelDebounceTimer = null;
                }}, 50);
            }}
        }}

        function handleScreenMove(e) {{
            const img = document.getElementById("screen");
            const c = getNormalizedCoords(e, img);
            document.getElementById("hudCoords").innerText = `X: ${{c.x}} | Y: ${{c.y}} (${{Math.round(c.normX * 100)}}%, ${{Math.round(c.normY * 100)}}%)`;
        }}

        function handleScreenKeyDown(e) {{
            if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Tab", "Backspace"].includes(e.key)) {{
                e.preventDefault();
            }}
            sendCmd("keyPress", {{
                key: e.key,
                code: e.code,
                ctrlKey: e.ctrlKey,
                shiftKey: e.shiftKey,
                altKey: e.altKey,
                metaKey: e.metaKey
            }});
        }}

        function handleQuickType(e) {{
            if (e.key === "Enter") {{
                const text = e.target.value;
                if (!text) return;
                sendCmd("type", {{ text: text, submit: true }});
                showToast("Sent: " + text);
                e.target.value = "";
            }}
        }}

        function handleUrlEnter(e) {{
            if (e.key === "Enter") navigateCurrentUrl();
        }}

        function navigateCurrentUrl() {{
            let url = document.getElementById("urlBar").value.trim();
            if (!url) return;
            if (!url.startsWith("http://") && !url.startsWith("https://") && !url.startsWith("chrome://")) {{
                url = "https://" + url;
            }}
            sendCmd("navigate", {{ url: url }});
            showToast("Navigating to: " + url);
        }}

        async function saveSelectedFigure() {{
            const sel = document.getElementById("figSelect");
            const filename = sel.value;
            const label = sel.options[sel.selectedIndex].text;
            const mode = document.getElementById("snapMode").value;

            if (mode === "fullPage") {{
                sendCmd("captureScreenshot", {{ mode: "fullPage", tag: filename }});
                showToast("⏳ Stitching Full-Page: " + label);
                return;
            }}

            if (!currentFrame) return alert("No frame available yet! Ensure Chrome is awake.");

            const resp = await fetch("/api/save_figure", {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify({{ filename: filename, dataUrl: currentFrame }})
            }});
            if (resp.ok) {{
                showToast("✅ Saved to Report: " + label);
            }}
        }}

        function toggleDomDrawer() {{
            const drawer = document.getElementById("domSidebar");
            drawer.classList.toggle("hidden");
            document.getElementById("domToggleBtn").classList.toggle("active", !drawer.classList.contains("hidden"));
            if (!drawer.classList.contains("hidden")) refreshDomScan();
        }}

        function refreshDomScan() {{
            sendCmd("getSemanticDOM");
            showToast("Extracting interactive elements...");
        }}

        function renderDomElements(elements) {{
            domElements = elements;
            document.getElementById("elemCount").innerText = elements.length;
            document.getElementById("elemCountHeader").innerText = elements.length;
            filterDomElements();
        }}

        function filterDomElements() {{
            const query = (document.getElementById("domSearch").value || "").toLowerCase();
            const list = document.getElementById("domList");
            list.innerHTML = "";

            const filtered = domElements.filter(e => 
                e.tag.includes(query) || (e.text && e.text.toLowerCase().includes(query)) || (e.selector && e.selector.toLowerCase().includes(query))
            );

            filtered.slice(0, 120).forEach(el => {{
                const item = document.createElement("div");
                item.className = "dom-card";
                item.innerHTML = `
                    <div>
                        <span class="dom-badge">#${{el.id}} &lt;${{el.tag}}&gt;</span>
                        <div class="dom-label" title="${{el.text || el.selector}}">${{el.text || el.selector}}</div>
                    </div>
                    <button class="btn btn-subtle" style="padding:3px 8px;font-size:10px;">Click</button>
                `;
                item.querySelector("button").onclick = () => {{
                    sendCmd("click", {{ selector: el.selector, coords: {{ x: el.rect.x + el.rect.width/2, y: el.rect.y + el.rect.height/2 }} }});
                    showToast("Triggered #" + el.id + " " + el.tag);
                }};
                list.appendChild(item);
            }});
        }}

        function toggleConsoleDrawer() {{
            const drawer = document.getElementById("consoleDrawer");
            drawer.classList.toggle("hidden");
            document.getElementById("logToggleBtn").classList.toggle("active", !drawer.classList.contains("hidden"));
        }}

        function appendConsoleLog(log) {{
            logsList.push(log);
            document.getElementById("logCount").innerText = logsList.length;
            const container = document.getElementById("consoleLogs");
            const line = document.createElement("div");
            line.className = "log-row log-" + (log.level || "log");
            const time = new Date(log.timestamp || Date.now()).toLocaleTimeString();
            line.innerText = `[${{time}}] [${{(log.level || 'log').toUpperCase()}}] ${{log.text}}`;
            container.appendChild(line);
            container.scrollTop = container.scrollHeight;
        }}

        function clearConsole() {{
            logsList = [];
            document.getElementById("logCount").innerText = "0";
            document.getElementById("consoleLogs").innerHTML = "";
        }}

        function showToast(msg) {{
            const t = document.getElementById("toast");
            t.innerText = msg;
            t.style.display = "block";
            setTimeout(() => t.style.display = "none", 2400);
        }}

        init();
    </script>
</body>
</html>"""
                self.wfile.write(html.encode('utf-8'))
            else:
                super().do_GET()

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

async def main():
    async with websockets.serve(ws_handler, "localhost", 9999):
        print("[Antigravity Pro Studio 3.0] WebSocket running on ws://localhost:9999")
        await asyncio.Future()

if __name__ == "__main__":
    t = threading.Thread(target=run_web_studio, daemon=True)
    t.start()
    asyncio.run(main())
