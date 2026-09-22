import asyncio
import json
import websockets
import base64
import os

SCREENSHOTS_DIR = r"c:\Users\abdul\OneDrive\Documents\polisewa\screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

async def capture_all_tabs():
    uri = "ws://localhost:9999"
    print("[*] Connecting to Bridge Server...")
    
    async with websockets.connect(uri) as ws:
        # 1. Ask for list of open tabs
        print("[*] Requesting open Chrome tabs list...")
        await ws.send(json.dumps({"command": "listTabs"}))
        
        tabs = []
        for _ in range(10):
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                data = json.loads(msg)
                if data.get("type") == "tabs_list":
                    tabs = data.get("tabs", [])
                    break
            except asyncio.TimeoutError:
                pass

        if not tabs:
            print("[!] Could not retrieve tab list from Chrome.")
            return

        print(f"[*] Found {len(tabs)} tabs in Chrome:")
        for t in tabs:
            print(f"  - ID {t.get('id')}: {t.get('title')} ({t.get('url')})")

        # Find Azure and Cloudflare tabs
        azure_tabs = [t for t in tabs if "azure.com" in (t.get("url") or "") or "Azure" in (t.get("title") or "")]
        cf_tabs = [t for t in tabs if "cloudflare.com" in (t.get("url") or "") or "Cloudflare" in (t.get("title") or "")]

        async def snap_tab(tab, filename):
            print(f"[*] Switching to tab: {tab.get('title')} (ID {tab.get('id')})...")
            await ws.send(json.dumps({"command": "switchTab", "tabId": tab.get("id")}))
            await asyncio.sleep(1.8) # Allow Chrome window to switch and render
            
            print(f"[*] Capturing screenshot for {filename}...")
            await ws.send(json.dumps({"command": "captureScreenshot", "filename": filename, "tag": filename}))
            
            # Wait for screenshot response
            for _ in range(15):
                try:
                    res_msg = await asyncio.wait_for(ws.recv(), timeout=1.5)
                    res_data = json.loads(res_msg)
                    if res_data.get("type") == "screenshot" and res_data.get("dataUrl"):
                        data_url = res_data.get("dataUrl")
                        if "," in data_url:
                            _, encoded = data_url.split(",", 1)
                            raw = base64.b64decode(encoded)
                            filepath = os.path.join(SCREENSHOTS_DIR, filename)
                            with open(filepath, "wb") as f:
                                f.write(raw)
                            print(f"[OK] Successfully saved: {filename} ({len(raw)} bytes)")
                            return True
                except asyncio.TimeoutError:
                    pass
            print(f"[!] Timeout waiting for screenshot of {filename}")
            return False

        # Capture Azure
        if azure_tabs:
            print(f"[*] Capturing primary Azure tab...")
            await snap_tab(azure_tabs[0], "fig1_7b_azure_resources.png")
            if len(azure_tabs) > 1:
                print(f"[*] Capturing secondary Azure tab...")
                await snap_tab(azure_tabs[1], "fig1_7a_azure_spending.png")
        else:
            print("[!] No Azure tab found in Chrome.")

        # Capture Cloudflare
        if cf_tabs:
            print(f"[*] Capturing Cloudflare tab...")
            await snap_tab(cf_tabs[0], "fig4_1_2_cloudflare_edge.png")
        else:
            print("[!] No Cloudflare tab found in Chrome.")

if __name__ == "__main__":
    asyncio.run(capture_all_tabs())
