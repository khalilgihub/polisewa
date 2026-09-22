import re
from urllib.parse import urlparse, urljoin
from flask import Flask, request, Response, render_template_string
import requests

app = Flask(__name__)

# List of headers that block embedding in iframes
BLOCKED_HEADERS = [
    'x-frame-options',
    'content-security-policy',
    'content-security-policy-report-only',
    'frame-ancestors',
    'strict-transport-security'
]

NAV_BAR_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Antigravity Web Browser</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: system-ui, -apple-system, sans-serif; display: flex; flex-direction: column; height: 100vh; overflow: hidden; background: #0f172a; }
        #browser-bar {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            background: #1e293b;
            border-bottom: 1px solid #334155;
            color: #f8fafc;
        }
        .nav-btn {
            background: #334155;
            color: #f8fafc;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
        }
        .nav-btn:hover { background: #475569; }
        #url-input {
            flex: 1;
            padding: 8px 14px;
            border-radius: 6px;
            border: 1px solid #475569;
            background: #0f172a;
            color: #f8fafc;
            font-size: 14px;
            outline: none;
        }
        #url-input:focus { border-color: #38bdf8; }
        .go-btn {
            background: #0284c7;
            color: white;
            border: none;
            padding: 8px 18px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
        }
        .go-btn:hover { background: #0369a1; }
        .quick-links { display: flex; gap: 6px; }
        .quick-link {
            font-size: 12px;
            padding: 4px 8px;
            background: #0f172a;
            border-radius: 4px;
            color: #94a3b8;
            cursor: pointer;
            border: 1px solid #334155;
            text-decoration: none;
        }
        .quick-link:hover { color: #f8fafc; border-color: #38bdf8; }
        #viewport {
            flex: 1;
            width: 100%;
            height: 100%;
            border: none;
            background: white;
        }
    </style>
</head>
<body>
    <div id="browser-bar">
        <button class="nav-btn" onclick="historyBack()">◀</button>
        <button class="nav-btn" onclick="historyForward()">▶</button>
        <button class="nav-btn" onclick="reloadFrame()">🔄</button>
        
        <input type="text" id="url-input" placeholder="Enter full URL (e.g. https://www.wikipedia.org or https://www.youtube.com)" value="{{ current_url }}" />
        <button class="go-btn" onclick="navigate()">Go</button>
        
        <div class="quick-links">
            <span class="quick-link" onclick="quickNav('https://www.youtube.com')">YouTube</span>
            <span class="quick-link" onclick="quickNav('https://www.wikipedia.org')">Wikipedia</span>
            <span class="quick-link" onclick="quickNav('http://localhost:5500/final_report.html')">Local Report</span>
        </div>
    </div>

    <iframe id="viewport" src="{{ proxy_src }}"></iframe>

    <script>
        const input = document.getElementById('url-input');
        const frame = document.getElementById('viewport');

        function navigate() {
            let url = input.value.trim();
            if (!url) return;
            if (!url.startsWith('http://') && !url.startsWith('https://')) {
                url = 'https://' + url;
            }
            input.value = url;
            frame.src = '/proxy?url=' + encodeURIComponent(url);
        }

        function quickNav(url) {
            input.value = url;
            navigate();
        }

        function historyBack() {
            try { frame.contentWindow.history.back(); } catch(e) {}
        }
        function historyForward() {
            try { frame.contentWindow.history.forward(); } catch(e) {}
        }
        function reloadFrame() {
            frame.src = frame.src;
        }

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') navigate();
        });
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    initial_url = request.args.get("url", "https://www.wikipedia.org")
    proxy_src = f"/proxy?url={requests.utils.quote(initial_url)}"
    return render_template_string(NAV_BAR_HTML, current_url=initial_url, proxy_src=proxy_src)

@app.route("/proxy")
def proxy():
    target_url = request.args.get("url")
    if not target_url:
        return "Missing url parameter", 400

    try:
        # Forward user agent so websites render full desktop/mobile layout
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        resp = requests.get(target_url, headers=headers, timeout=12, stream=True, allow_redirects=True)

        # Filter out headers that block embedding
        response_headers = []
        for name, value in resp.headers.items():
            if name.lower() not in BLOCKED_HEADERS and not name.lower().startswith('content-encoding'):
                response_headers.append((name, value))

        content_type = resp.headers.get('Content-Type', '')
        
        # If HTML, rewrite links or inject base href so relative assets load properly
        if 'text/html' in content_type:
            html = resp.content.decode('utf-8', errors='replace')
            parsed = urlparse(target_url)
            base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            
            # Inject <base> tag to resolve images, CSS, and JS assets correctly
            base_tag = f'<base href="{base_url}">'
            if '<head>' in html:
                html = html.replace('<head>', f'<head>{base_tag}', 1)
            else:
                html = base_tag + html
            
            return Response(html, status=resp.status_code, headers=response_headers)

        return Response(resp.content, status=resp.status_code, headers=response_headers)

    except Exception as e:
        return f"<div style='font-family:sans-serif;padding:20px;'><h3>Failed to load {target_url}</h3><p>{str(e)}</p></div>", 500

if __name__ == "__main__":
    print("[Web Proxy Browser] Running on http://localhost:8888")
    app.run(host="0.0.0.0", port=8888, debug=False)
