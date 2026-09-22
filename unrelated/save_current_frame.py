import urllib.request
import json
import sys

def save(filename):
    req = urllib.request.Request(
        "http://localhost:9998/api/save_figure",
        data=json.dumps({"filename": filename}).encode(),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            print("Status:", resp.status)
            print("Body:", resp.read().decode())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "fig4_1_2_cloudflare_edge.png"
    save(fname)
