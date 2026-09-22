import asyncio
import json
import websockets
import base64
import os

SCREENSHOTS_DIR = r"c:\Users\abdul\OneDrive\Documents\polisewa\screenshots"

async def test_cf():
    uri = "ws://localhost:9999"
    async with websockets.connect(uri) as ws:
        # Switch to Cloudflare tab
        print("[*] Switching to Cloudflare tab 1396489095...")
        await ws.send(json.dumps({"command": "switchTab", "tabId": 1396489095}))
        await asyncio.sleep(1.0)
        
        # Click on polisewa.me
        print("[*] Clicking polisewa.me...")
        await ws.send(json.dumps({"command": "click", "text": "polisewa.me"}))
        await asyncio.sleep(4.0)
        
        # Take a screenshot
        print("[*] Taking screenshot...")
        await ws.send(json.dumps({"command": "captureScreenshot", "tag": "fig4_1_2_cloudflare_edge.png"}))
        
        for _ in range(25):
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                data = json.loads(msg)
                if data.get("type") == "screenshot" and data.get("tag") == "fig4_1_2_cloudflare_edge.png":
                    durl = data.get("dataUrl")
                    if durl and "," in durl:
                        _, enc = durl.split(",", 1)
                        img = base64.b64decode(enc)
                        target = os.path.join(SCREENSHOTS_DIR, "fig4_1_2_cloudflare_edge.png")
                        with open(target, "wb") as f:
                            f.write(img)
                        print(f"[OK] Saved fig4_1_2_cloudflare_edge.png ({len(img)} bytes)")
                        return
            except asyncio.TimeoutError:
                pass

if __name__ == "__main__":
    asyncio.run(test_cf())
