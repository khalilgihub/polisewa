import asyncio
import json
import websockets
import base64
import os

SCREENSHOTS_DIR = r"c:\Users\abdul\OneDrive\Documents\polisewa\screenshots"

async def test_action():
    uri = "ws://localhost:9999"
    async with websockets.connect(uri) as ws:
        # Switch to Azure tab 1396489071
        print("[*] Switching to Azure tab 1396489071...")
        await ws.send(json.dumps({"command": "switchTab", "tabId": 1396489071}))
        await asyncio.sleep(1.0)
        
        # Click on "Cost Management"
        print("[*] Clicking Cost Management...")
        await ws.send(json.dumps({"command": "click", "text": "Cost Management"}))
        await asyncio.sleep(3.0)
        
        # Take a screenshot
        print("[*] Taking screenshot...")
        await ws.send(json.dumps({"command": "captureScreenshot", "tag": "test_azure_click.png"}))
        
        for _ in range(20):
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                data = json.loads(msg)
                if data.get("type") == "screenshot" and data.get("tag") == "test_azure_click.png":
                    durl = data.get("dataUrl")
                    if durl and "," in durl:
                        _, enc = durl.split(",", 1)
                        img = base64.b64decode(enc)
                        target = os.path.join(SCREENSHOTS_DIR, "test_azure_click.png")
                        with open(target, "wb") as f:
                            f.write(img)
                        print(f"[OK] Saved test_azure_click.png ({len(img)} bytes)")
                        return
            except asyncio.TimeoutError:
                pass

if __name__ == "__main__":
    asyncio.run(test_action())
