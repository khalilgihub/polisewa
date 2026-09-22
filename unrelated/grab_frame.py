import asyncio
import json
import websockets
import base64
import os
import sys

SCREENSHOTS_DIR = r"c:\Users\abdul\OneDrive\Documents\polisewa\screenshots"

async def grab(filename, target_tab_id=None):
    uri = "ws://localhost:9999"
    print(f"[*] Connecting to {uri} to capture {filename}...")
    async with websockets.connect(uri) as ws:
        if target_tab_id:
            print(f"[*] Switching to tab {target_tab_id}...")
            await ws.send(json.dumps({"command": "switchTab", "tabId": target_tab_id}))
            await asyncio.sleep(2.0)
            
        # Drain old frames
        while True:
            try:
                await asyncio.wait_for(ws.recv(), timeout=0.1)
            except asyncio.TimeoutError:
                break

        print("[*] Requesting high-res snapshot...")
        await ws.send(json.dumps({"command": "captureScreenshot", "tag": filename}))
        
        # Listen for the specifically tagged frame
        for _ in range(40):
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                data = json.loads(msg)
                if data.get("type") == "screenshot" and data.get("tag") == filename:
                    durl = data.get("dataUrl")
                    if durl and "," in durl:
                        _, enc = durl.split(",", 1)
                        img_bytes = base64.b64decode(enc)
                        target = os.path.join(SCREENSHOTS_DIR, filename)
                        with open(target, "wb") as f:
                            f.write(img_bytes)
                        print(f"[SUCCESS] Saved high-res {filename} ({len(img_bytes)} bytes)")
                        return True
            except asyncio.TimeoutError:
                pass
        print(f"[FAIL] Did not receive frame for {filename}")
        return False

if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "snap.png"
    tid = int(sys.argv[2]) if len(sys.argv) > 2 else None
    asyncio.run(grab(fname, tid))
