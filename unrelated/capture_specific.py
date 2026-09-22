import asyncio
import json
import websockets
import base64
import os

SCREENSHOTS_DIR = r"c:\Users\abdul\OneDrive\Documents\polisewa\screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

async def capture_tab(tab_id, filename):
    uri = "ws://localhost:9999"
    print(f"[*] Connecting to Bridge Server for {filename} (Tab {tab_id})...")
    async with websockets.connect(uri) as ws:
        # Switch tab
        await ws.send(json.dumps({"command": "switchTab", "tabId": tab_id}))
        await asyncio.sleep(2.0)
        
        # Request high-quality PNG capture tagged with filename
        print(f"[*] Requesting capture with tag '{filename}'...")
        await ws.send(json.dumps({
            "command": "captureScreenshot",
            "tag": filename,
            "filename": filename
        }))
        
        # Listen for the tagged screenshot
        for _ in range(30):
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                data = json.loads(msg)
                if data.get("type") == "screenshot" and data.get("tag") == filename:
                    data_url = data.get("dataUrl")
                    if data_url and "," in data_url:
                        _, encoded = data_url.split(",", 1)
                        img_data = base64.b64decode(encoded)
                        filepath = os.path.join(SCREENSHOTS_DIR, filename)
                        with open(filepath, "wb") as f:
                            f.write(img_data)
                        print(f"[SUCCESS] Saved {filename} ({len(img_data)} bytes)")
                        return filepath
            except asyncio.TimeoutError:
                pass
        print(f"[ERROR] Timed out waiting for tagged screenshot {filename}")
        return None

async def main():
    # 1. Capture Cloudflare
    await capture_tab(1396489095, "fig4_1_2_cloudflare_edge.png")
    # 2. Capture Azure 1
    await capture_tab(1396489064, "fig1_7b_azure_resources.png")
    # 3. Capture Azure 2
    await capture_tab(1396489071, "fig1_7a_azure_spending.png")

if __name__ == "__main__":
    asyncio.run(main())
