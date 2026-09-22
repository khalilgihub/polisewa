import asyncio
import json
import websockets

async def check():
    async with websockets.connect('ws://localhost:9999') as ws:
        await ws.send(json.dumps({'command': 'listTabs'}))
        for _ in range(10):
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                data = json.loads(msg)
                if data.get('type') == 'tabs_list':
                    tabs = data.get('tabs', [])
                    print(f"Total tabs: {len(tabs)}")
                    for t in tabs:
                        act = "[ACTIVE]" if t.get('active') else "        "
                        print(f"{act} Tab: {t.get('id')} | Win: {t.get('windowId')} | Title: {t.get('title')[:30]} | URL: {t.get('url')[:60]}")
                    break
            except asyncio.TimeoutError:
                pass

if __name__ == '__main__':
    asyncio.run(check())
