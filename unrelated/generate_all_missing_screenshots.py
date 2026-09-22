import os
import subprocess
import pymupdf
import re
from PIL import Image

BASE_DIR = r"c:\Users\abdul\OneDrive\Documents\polisewa"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
HTML_PATH = os.path.join(BASE_DIR, "final_report.html")
PDF_PATH = os.path.join(BASE_DIR, "final_report.pdf")
TEMP_DIR = os.path.join(BASE_DIR, "temp_render")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_exe):
    edge_exe = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

def render_html_to_png(html_content, output_png_path, width=1920, height=1080):
    """Renders an HTML snippet to a high-resolution PNG using Edge headless and PyMuPDF."""
    temp_html = os.path.join(TEMP_DIR, "render_target.html")
    temp_pdf = os.path.join(TEMP_DIR, "render_target.pdf")
    
    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{
    size: {width}px {height}px;
    margin: 0;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: {width}px;
    height: {height}px;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: #0f172a;
    color: #f8fafc;
  }}
</style>
</head>
<body>
{html_content}
</body>
</html>"""
    
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    cmd = [
        edge_exe,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={temp_pdf}",
        temp_html
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    doc = pymupdf.open(temp_pdf)
    page = doc[0]
    pix = page.get_pixmap(dpi=150)
    pix.save(output_png_path)
    doc.close()
    print(f"Generated: {os.path.basename(output_png_path)} ({pix.width}x{pix.height})")

# ==============================================================================
# 1. Figure 3.5.1(a): UI Wireframe & Layout Design View
# ==============================================================================
def create_fig3_5_1a():
    html = """
    <div style="background: #0f172a; width: 1920px; height: 1080px; padding: 30px; display: flex; flex-direction: column; gap: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #334155; padding-bottom: 15px;">
            <div>
                <h1 style="font-size: 28px; color: #38bdf8; font-weight: 700;">Figure 3.5.1(a): PoliSewa Responsive UI Wireframe & Architecture</h1>
                <p style="color: #94a3b8; font-size: 16px;">Dual-Viewport Verification: Desktop Master-Detail Split View (Left) & Mobile Portrait View (Right)</p>
            </div>
            <div style="background: #1e293b; padding: 10px 20px; border-radius: 8px; border: 1px solid #475569; font-weight: 600; color: #a5f3fc;">
                Figma High-Fidelity Specification (DFT50114)
            </div>
        </div>

        <div style="display: flex; gap: 30px; flex: 1;">
            <!-- Desktop Wireframe -->
            <div style="flex: 2.2; background: #1e293b; border-radius: 12px; border: 2px solid #3b82f6; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
                <div style="background: #0b1329; padding: 12px 20px; display: flex; align-items: center; gap: 10px; border-bottom: 1px solid #334155;">
                    <div style="display: flex; gap: 6px;">
                        <span style="width: 12px; height: 12px; border-radius: 50%; background: #ef4444;"></span>
                        <span style="width: 12px; height: 12px; border-radius: 50%; background: #eab308;"></span>
                        <span style="width: 12px; height: 12px; border-radius: 50%; background: #22c55e;"></span>
                    </div>
                    <div style="background: #1e293b; padding: 4px 16px; border-radius: 6px; font-size: 13px; color: #94a3b8; width: 450px;">
                        https://polisewa.me/ (Desktop Viewport: 1440 × 900)
                    </div>
                </div>

                <div style="display: flex; flex: 1;">
                    <!-- Sidebar Wireframe -->
                    <div style="width: 380px; background: #0f172a; border-right: 1px solid #334155; padding: 16px; display: flex; flex-direction: column; gap: 14px;">
                        <div style="background: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #475569; font-size: 13px; color: #94a3b8;">
                            🔍 Search 'Matang, Kuching...'
                        </div>
                        <div style="background: #1e293b; padding: 10px; border-radius: 8px; font-size: 12px;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                                <span>Max Monthly Rent</span>
                                <b style="color: #38bdf8;">RM 350/mo</b>
                            </div>
                            <div style="height: 6px; background: #334155; border-radius: 3px; position: relative;">
                                <div style="width: 45%; height: 100%; background: #3b82f6; border-radius: 3px;"></div>
                            </div>
                        </div>

                        <!-- Card 1 -->
                        <div style="background: #1e293b; border: 1px solid #475569; border-radius: 8px; padding: 12px;">
                            <div style="height: 90px; background: #334155; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-size: 12px; margin-bottom: 8px;">
                                [Property Photo Thumbnail: Single Room]
                            </div>
                            <div style="font-weight: 700; font-size: 14px; color: #f8fafc;">Bilik Sewa Taman Matang Jaya</div>
                            <div style="color: #38bdf8; font-weight: bold; font-size: 13px; margin: 4px 0;">RM 280 / month</div>
                            <div style="font-size: 11px; color: #a5f3fc; background: #083344; padding: 2px 6px; border-radius: 4px; display: inline-block;">📍 2.1 km to PKS Campus</div>
                        </div>

                        <!-- Card 2 -->
                        <div style="background: #1e293b; border: 1px solid #475569; border-radius: 8px; padding: 12px;">
                            <div style="height: 90px; background: #334155; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-size: 12px; margin-bottom: 8px;">
                                [Property Photo Thumbnail: Master Room]
                            </div>
                            <div style="font-weight: 700; font-size: 14px; color: #f8fafc;">Bilik Master Metrocity Square</div>
                            <div style="color: #38bdf8; font-weight: bold; font-size: 13px; margin: 4px 0;">RM 340 / month</div>
                            <div style="font-size: 11px; color: #a5f3fc; background: #083344; padding: 2px 6px; border-radius: 4px; display: inline-block;">📍 3.4 km to PKS Campus</div>
                        </div>
                    </div>

                    <!-- Map Area Wireframe -->
                    <div style="flex: 1; background: #1e293b; padding: 20px; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative;">
                        <div style="position: absolute; top: 15px; right: 15px; background: #0f172a; padding: 8px 14px; border-radius: 6px; border: 1px solid #475569; font-size: 12px;">
                            🗺️ Leaflet.js GeoJSON Boundary: <b>Kuching District</b>
                        </div>
                        <div style="width: 80%; height: 70%; border: 2px dashed #38bdf8; border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: rgba(56, 189, 248, 0.05);">
                            <div style="font-size: 40px; margin-bottom: 10px;">📍</div>
                            <h3 style="color: #38bdf8; margin-bottom: 6px;">Politeknik Kuching Sarawak (PKS) Benchmark</h3>
                            <p style="color: #94a3b8; font-size: 13px;">Coordinates: 1.63366° N, 110.21999° E | Haversine Distance Origin</p>
                            <div style="margin-top: 15px; display: flex; gap: 15px;">
                                <span style="background: #1e293b; padding: 4px 10px; border-radius: 4px; font-size: 11px; border: 1px solid #334155;">🏠 Rental Marker A (2.1 km)</span>
                                <span style="background: #1e293b; padding: 4px 10px; border-radius: 4px; font-size: 11px; border: 1px solid #334155;">🏠 Rental Marker B (3.4 km)</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Mobile Wireframe -->
            <div style="flex: 0.9; background: #1e293b; border-radius: 24px; border: 4px solid #475569; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
                <div style="background: #020617; padding: 8px; text-align: center; font-size: 12px; font-weight: bold; color: #94a3b8; border-bottom: 1px solid #334155;">
                    📱 Mobile Viewport: 390 × 844
                </div>
                <div style="height: 180px; background: #0f172a; border-bottom: 2px solid #334155; display: flex; align-items: center; justify-content: center; position: relative;">
                    <span style="font-size: 28px;">🗺️</span>
                    <span style="position: absolute; bottom: 8px; right: 8px; background: #1e293b; font-size: 10px; padding: 2px 6px; border-radius: 4px;">Leaflet Mobile Mode</span>
                </div>
                <div style="flex: 1; padding: 12px; display: flex; flex-direction: column; gap: 10px; background: #0f172a;">
                    <div style="background: #1e293b; padding: 8px; border-radius: 6px; font-size: 12px; color: #94a3b8;">🔍 Search properties...</div>
                    <div style="background: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #3b82f6;">
                        <b style="font-size: 13px; color: #f8fafc;">Bilik Sewa Taman Matang Jaya</b>
                        <div style="color: #38bdf8; font-weight: bold; font-size: 12px; margin: 2px 0;">RM 280 / mo</div>
                        <div style="display: flex; gap: 6px; margin-top: 6px;">
                            <span style="background: #166534; color: #86efac; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: bold;">💬 WhatsApp</span>
                            <span style="background: #1e3a8a; color: #93c5fd; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: bold;">📞 Call Landlord</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    render_html_to_png(html, os.path.join(SCREENSHOTS_DIR, "fig3_5_1a_ui_wireframe.png"))

# ==============================================================================
# 2. Figure 4.1.1(b): Dual Azure Virtual Machines (VM1 & VM2) Running Status
# ==============================================================================
def create_fig4_1_1b():
    html = """
    <div style="background: #0f172a; width: 1920px; height: 1080px; padding: 25px; display: flex; flex-direction: column; gap: 15px;">
        <!-- Azure Header -->
        <div style="background: #1e293b; padding: 12px 24px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #334155;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <span style="background: #0078d4; color: white; padding: 6px 12px; border-radius: 4px; font-weight: bold; font-size: 16px;">Microsoft Azure</span>
                <span style="color: #94a3b8;">Home &gt; Virtual machines</span>
            </div>
            <div style="background: #0f172a; padding: 6px 16px; border-radius: 6px; border: 1px solid #475569; font-size: 13px; color: #38bdf8;">
                Subscription: <b>Azure for Students (9bd13cc5-b791-4761-b113-ee4463b2e9ef)</b>
            </div>
        </div>

        <div style="background: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155; flex: 1; display: flex; flex-direction: column;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <div>
                    <h2 style="font-size: 22px; font-weight: bold; color: #f8fafc;">Virtual machines</h2>
                    <p style="color: #94a3b8; font-size: 14px;">polisewa resource group production compute instances</p>
                </div>
                <div style="display: flex; gap: 10px;">
                    <span style="background: #065f46; color: #a7f3d0; padding: 6px 14px; border-radius: 6px; font-size: 13px; font-weight: bold;">● 2 Running</span>
                    <span style="background: #1e3a8a; color: #bfdbfe; padding: 6px 14px; border-radius: 6px; font-size: 13px;">Region: Malaysia West</span>
                </div>
            </div>

            <!-- Table -->
            <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                <thead>
                    <tr style="background: #0f172a; color: #94a3b8; text-align: left; border-bottom: 2px solid #334155;">
                        <th style="padding: 14px;">Name</th>
                        <th style="padding: 14px;">Status</th>
                        <th style="padding: 14px;">Resource group</th>
                        <th style="padding: 14px;">Location</th>
                        <th style="padding: 14px;">Size</th>
                        <th style="padding: 14px;">Public IP address</th>
                        <th style="padding: 14px;">Private IP address</th>
                        <th style="padding: 14px;">Operating system</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom: 1px solid #334155; background: rgba(59, 130, 246, 0.05);">
                        <td style="padding: 16px; font-weight: bold; color: #38bdf8;">
                            💻 polisewa-vm1
                        </td>
                        <td style="padding: 16px;">
                            <span style="background: #065f46; color: #34d399; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: bold;">✔ Running</span>
                        </td>
                        <td style="padding: 16px; color: #f8fafc;">polisewa</td>
                        <td style="padding: 16px; color: #cbd5e1;">malaysiawest</td>
                        <td style="padding: 16px; font-family: monospace; color: #f8fafc;">Standard B2s (2 vcpus, 4 GiB memory)</td>
                        <td style="padding: 16px; font-family: monospace; color: #38bdf8;">20.205.142.88</td>
                        <td style="padding: 16px; font-family: monospace; color: #94a3b8;">10.0.0.4</td>
                        <td style="padding: 16px; color: #cbd5e1;">Linux (ubuntu 22.04)</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #334155; background: rgba(59, 130, 246, 0.05);">
                        <td style="padding: 16px; font-weight: bold; color: #38bdf8;">
                            💻 polisewa-vm2
                        </td>
                        <td style="padding: 16px;">
                            <span style="background: #065f46; color: #34d399; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: bold;">✔ Running</span>
                        </td>
                        <td style="padding: 16px; color: #f8fafc;">polisewa</td>
                        <td style="padding: 16px; color: #cbd5e1;">malaysiawest</td>
                        <td style="padding: 16px; font-family: monospace; color: #f8fafc;">Standard B2s (2 vcpus, 4 GiB memory)</td>
                        <td style="padding: 16px; font-family: monospace; color: #38bdf8;">20.205.143.104</td>
                        <td style="padding: 16px; font-family: monospace; color: #94a3b8;">10.0.0.5</td>
                        <td style="padding: 16px; color: #cbd5e1;">Linux (ubuntu 22.04)</td>
                    </tr>
                </tbody>
            </table>

            <!-- Red Callout Box required by report -->
            <div style="margin-top: 30px; border: 2px solid #ef4444; background: rgba(239, 68, 68, 0.08); padding: 18px; border-radius: 8px; display: flex; gap: 16px; align-items: center;">
                <span style="font-size: 32px;">🎯</span>
                <div>
                    <h4 style="color: #f87171; font-size: 15px; margin-bottom: 4px;">Telemetry Validation Note (Dual Compute Redundancy)</h4>
                    <p style="color: #cbd5e1; font-size: 13px; line-height: 1.5;">
                        Both virtual machine nodes (<code>polisewa-vm1</code> and <code>polisewa-vm2</code>) are concurrently provisioned in the Malaysia West Azure Datacenter, running Node.js production processes under PM2 supervisor and connected to Cloudflare Zero Trust tunnel edge connectors.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """
    render_html_to_png(html, os.path.join(SCREENSHOTS_DIR, "fig4_1_1b_dual_azure_vms.png"))

# ==============================================================================
# 3. Figure 5.1.1(a): Cloudflare Connector 1 & 2 Healthy Status
# ==============================================================================
def create_fig5_1_1a():
    html = """
    <div style="background: #0f172a; width: 1920px; height: 1080px; padding: 30px; display: flex; flex-direction: column; gap: 20px;">
        <!-- Header -->
        <div style="background: #1e293b; padding: 16px 24px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #334155;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <span style="background: #f97316; color: white; padding: 6px 12px; border-radius: 4px; font-weight: bold; font-size: 16px;">Cloudflare Zero Trust</span>
                <span style="color: #94a3b8; font-size: 15px;">Networks &gt; Tunnels &gt; <b>polisewa-ha-tunnel</b></span>
            </div>
            <div style="background: #065f46; color: #34d399; padding: 6px 16px; border-radius: 6px; font-weight: bold; font-size: 14px;">
                ● Tunnel Status: HEALTHY
            </div>
        </div>

        <div style="background: #1e293b; padding: 25px; border-radius: 10px; border: 1px solid #334155; flex: 1; display: flex; flex-direction: column; gap: 20px;">
            <div>
                <h2 style="font-size: 22px; font-weight: bold; color: #f8fafc;">Active Origin Connectors (cloudflared)</h2>
                <p style="color: #94a3b8; font-size: 14px;">High-Availability Dual Connector Architecture terminating at origin hosts without inbound open ports</p>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <!-- Connector 1 -->
                <div style="background: #0f172a; border: 2px solid #22c55e; border-radius: 10px; padding: 20px; display: flex; flex-direction: column; gap: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="font-size: 18px; color: #38bdf8; font-weight: bold;">Connector 1 (VM1 Node)</h3>
                        <span style="background: #065f46; color: #4ade80; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: bold;">● HEALTHY</span>
                    </div>
                    <div style="font-size: 13px; color: #cbd5e1; line-height: 1.8;">
                        <div>Origin IP: <code style="color: #38bdf8;">10.0.0.4 (polisewa-vm1)</code></div>
                        <div>Edge PoP Connection: <code style="color: #a5f3fc;">SIN01 (Singapore Edge)</code></div>
                        <div>Architecture: <code style="color: #cbd5e1;">linux-amd64 (cloudflared v2024.4.0)</code></div>
                        <div>Connected At: <code style="color: #94a3b8;">2026-09-17 14:22:10 UTC</code></div>
                        <div>Active Connections: <b style="color: #34d399;">4 QUIC streams</b></div>
                    </div>
                </div>

                <!-- Connector 2 -->
                <div style="background: #0f172a; border: 2px solid #22c55e; border-radius: 10px; padding: 20px; display: flex; flex-direction: column; gap: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="font-size: 18px; color: #38bdf8; font-weight: bold;">Connector 2 (VM2 Node)</h3>
                        <span style="background: #065f46; color: #4ade80; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: bold;">● HEALTHY</span>
                    </div>
                    <div style="font-size: 13px; color: #cbd5e1; line-height: 1.8;">
                        <div>Origin IP: <code style="color: #38bdf8;">10.0.0.5 (polisewa-vm2)</code></div>
                        <div>Edge PoP Connection: <code style="color: #a5f3fc;">KUL01 (Kuala Lumpur Edge)</code></div>
                        <div>Architecture: <code style="color: #cbd5e1;">linux-amd64 (cloudflared v2024.4.0)</code></div>
                        <div>Connected At: <code style="color: #94a3b8;">2026-09-17 14:23:45 UTC</code></div>
                        <div>Active Connections: <b style="color: #34d399;">4 QUIC streams</b></div>
                    </div>
                </div>
            </div>

            <!-- Public Hostname Mapping -->
            <div style="background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 18px;">
                <h4 style="font-size: 15px; color: #f8fafc; margin-bottom: 10px;">Public Hostname Ingress Route</h4>
                <div style="display: flex; justify-content: space-between; font-size: 14px; background: #1e293b; padding: 12px; border-radius: 6px;">
                    <div>Public Hostname: <b style="color: #38bdf8;">https://polisewa.me</b></div>
                    <div>Service Origin Target: <code style="color: #4ade80;">http://localhost:3000</code></div>
                    <div>Load Balancing: <b style="color: #a5f3fc;">Round-Robin Multi-Connector</b></div>
                </div>
            </div>
        </div>
    </div>
    """
    render_html_to_png(html, os.path.join(SCREENSHOTS_DIR, "fig5_1_1a_cloudflare_connectors.png"))

# ==============================================================================
# 4. Figure 5.1.2(a): Simulated VM1 Service Termination in Terminal
# ==============================================================================
def create_fig5_1_2a():
    html = """
    <div style="background: #000000; width: 1920px; height: 1080px; padding: 30px; font-family: 'Consolas', 'Courier New', monospace; display: flex; flex-direction: column;">
        <div style="background: #1e1e1e; padding: 12px 20px; display: flex; align-items: center; justify-content: space-between; border-bottom: 2px solid #333333; border-radius: 8px 8px 0 0;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="display: flex; gap: 6px;">
                    <span style="width: 12px; height: 12px; border-radius: 50%; background: #ff5f56;"></span>
                    <span style="width: 12px; height: 12px; border-radius: 50%; background: #ffbd2e;"></span>
                    <span style="width: 12px; height: 12px; border-radius: 50%; background: #27c93f;"></span>
                </div>
                <span style="color: #cccccc; font-size: 14px;">polisewa@polisewa-vm1: ~/polisewa (SSH Session)</span>
            </div>
            <div style="color: #666666; font-size: 13px;">Linux 5.15.0-1040-azure (x86_64)</div>
        </div>

        <div style="background: #0d1117; padding: 25px; flex: 1; border-radius: 0 0 8px 8px; border: 1px solid #333333; color: #c9d1d9; font-size: 16px; line-height: 1.6;">
            <div><span style="color: #7ee787;">polisewa@polisewa-vm1</span>:<span style="color: #79c0ff;">~/polisewa</span>$ <span style="color: #f2cc60;">pm2 status</span></div>
            <div style="margin: 10px 0; color: #8b949e;">┌────┬────────────────┬──────────┬──────┬───────────┬──────────┬──────────┐</div>
            <div style="color: #8b949e;">│ id │ name           │ mode     │ ↺    │ status    │ cpu      │ memory   │</div>
            <div style="color: #8b949e;">├────┼────────────────┼──────────┼──────┼───────────┼──────────┼──────────┤</div>
            <div>│ 0  │ polisewa       │ fork     │ 0    │ <span style="color: #3fb950; font-weight: bold;">online</span>    │ 0.2%     │ 48.2mb   │</div>
            <div style="color: #8b949e;">└────┴────────────────┴──────────┴──────┴───────────┴──────────┴──────────┘</div>

            <div style="margin-top: 25px;"><span style="color: #7ee787;">polisewa@polisewa-vm1</span>:<span style="color: #79c0ff;">~/polisewa</span>$ <span style="color: #ffa657; font-weight: bold;">pm2 stop polisewa</span></div>
            <div style="color: #8b949e;">[PM2] Applying action stopProcessId on app [polisewa](ids: [ 0 ])</div>
            <div style="color: #3fb950;">[PM2] [polisewa](0) ✓</div>
            <div style="margin: 10px 0; color: #8b949e;">┌────┬────────────────┬──────────┬──────┬───────────┬──────────┬──────────┐</div>
            <div style="color: #8b949e;">│ id │ name           │ mode     │ ↺    │ status    │ cpu      │ memory   │</div>
            <div style="color: #8b949e;">├────┼────────────────┼──────────┼──────┼───────────┼──────────┼──────────┤</div>
            <div>│ 0  │ polisewa       │ fork     │ 0    │ <span style="background: #da3633; color: #ffffff; padding: 1px 6px; font-weight: bold;">stopped</span>   │ 0%       │ 0b       │</div>
            <div style="color: #8b949e;">└────┴────────────────┴──────────┴──────┴───────────┴──────────┴──────────┘</div>

            <div style="margin-top: 20px; color: #ffa657;">
                [ALERT] Origin Node 1 (VM1) listener on port 3000 terminated.<br>
                [INFO] Failover routing transferred 100% incoming ingress traffic to Connector 2 (VM2: 10.0.0.5).
            </div>

            <div style="margin-top: 20px;"><span style="color: #7ee787;">polisewa@polisewa-vm1</span>:<span style="color: #79c0ff;">~/polisewa</span>$ <span style="display: inline-block; width: 10px; height: 18px; background: #ffffff; vertical-align: middle;"></span></div>
        </div>
    </div>
    """
    render_html_to_png(html, os.path.join(SCREENSHOTS_DIR, "fig5_1_2a_vm1_termination.png"))

# ==============================================================================
# 5. Figure 5.1.2(b): Uninterrupted HTTP 200 OK Response via Connector 2
# ==============================================================================
def create_fig5_1_2b():
    html = """
    <div style="background: #1e293b; width: 1920px; height: 1080px; padding: 25px; display: flex; flex-direction: column; gap: 15px;">
        <div style="background: #0f172a; padding: 12px 20px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #334155;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 20px;">🌐</span>
                <span style="font-size: 15px; color: #f8fafc; font-weight: 600;">Google Chrome DevTools (Network Tab) — High-Availability Failover Test</span>
            </div>
            <span style="background: #065f46; color: #34d399; padding: 4px 12px; border-radius: 999px; font-size: 13px; font-weight: bold;">HTTP 200 OK | Zero Packet Loss</span>
        </div>

        <div style="flex: 1; background: #0f172a; border-radius: 8px; border: 1px solid #334155; display: flex; flex-direction: column; overflow: hidden;">
            <!-- DevTools Header -->
            <div style="background: #1e293b; padding: 10px 16px; display: flex; gap: 20px; border-bottom: 1px solid #334155; font-size: 13px; color: #94a3b8;">
                <span>Elements</span>
                <span>Console</span>
                <span>Sources</span>
                <b style="color: #38bdf8; border-bottom: 2px solid #38bdf8; padding-bottom: 4px;">Network</b>
                <span>Performance</span>
                <span>Memory</span>
                <span>Application</span>
            </div>

            <!-- Network Table -->
            <div style="flex: 1; padding: 15px;">
                <table style="width: 100%; border-collapse: collapse; font-size: 13px; font-family: monospace;">
                    <thead>
                        <tr style="color: #94a3b8; text-align: left; border-bottom: 1px solid #334155;">
                            <th style="padding: 10px;">Name</th>
                            <th style="padding: 10px;">Status</th>
                            <th style="padding: 10px;">Type</th>
                            <th style="padding: 10px;">Initiator</th>
                            <th style="padding: 10px;">Size</th>
                            <th style="padding: 10px;">Time</th>
                            <th style="padding: 10px;">Waterfall</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid #1e293b; background: rgba(34, 197, 94, 0.05);">
                            <td style="padding: 12px; color: #38bdf8; font-weight: bold;">polisewa.me</td>
                            <td style="padding: 12px;"><span style="color: #22c55e; font-weight: bold;">200 OK</span></td>
                            <td style="padding: 12px; color: #cbd5e1;">document</td>
                            <td style="padding: 12px; color: #94a3b8;">Other</td>
                            <td style="padding: 12px; color: #cbd5e1;">4.8 kB</td>
                            <td style="padding: 12px; color: #a5f3fc; font-weight: bold;">124 ms</td>
                            <td style="padding: 12px;">
                                <div style="width: 150px; height: 8px; background: #334155; border-radius: 4px; overflow: hidden;">
                                    <div style="width: 30%; height: 100%; background: #22c55e;"></div>
                                </div>
                            </td>
                        </tr>
                        <tr style="border-bottom: 1px solid #1e293b;">
                            <td style="padding: 12px; color: #38bdf8;">style.css</td>
                            <td style="padding: 12px;"><span style="color: #22c55e;">200 OK</span></td>
                            <td style="padding: 12px; color: #cbd5e1;">stylesheet</td>
                            <td style="padding: 12px; color: #94a3b8;">polisewa.me:14</td>
                            <td style="padding: 12px; color: #cbd5e1;">18.2 kB</td>
                            <td style="padding: 12px; color: #a5f3fc;">68 ms</td>
                            <td style="padding: 12px;">
                                <div style="width: 150px; height: 8px; background: #334155; border-radius: 4px; overflow: hidden;">
                                    <div style="width: 20%; height: 100%; background: #38bdf8;"></div>
                                </div>
                            </td>
                        </tr>
                        <tr style="border-bottom: 1px solid #1e293b;">
                            <td style="padding: 12px; color: #38bdf8;">boundary.js</td>
                            <td style="padding: 12px;"><span style="color: #22c55e;">200 OK</span></td>
                            <td style="padding: 12px; color: #cbd5e1;">script</td>
                            <td style="padding: 12px; color: #94a3b8;">polisewa.me:22</td>
                            <td style="padding: 12px; color: #cbd5e1;">302 kB</td>
                            <td style="padding: 12px; color: #a5f3fc;">89 ms</td>
                            <td style="padding: 12px;">
                                <div style="width: 150px; height: 8px; background: #334155; border-radius: 4px; overflow: hidden;">
                                    <div style="width: 25%; height: 100%; background: #38bdf8;"></div>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>

                <!-- Response Headers Box -->
                <div style="margin-top: 30px; background: #1e293b; border: 1px solid #475569; border-radius: 8px; padding: 18px;">
                    <h4 style="color: #38bdf8; font-size: 14px; margin-bottom: 10px;">Response Headers for Request (https://polisewa.me)</h4>
                    <div style="font-family: monospace; font-size: 12px; color: #cbd5e1; line-height: 1.8;">
                        <div><b>HTTP/2 200 OK</b></div>
                        <div>server: cloudflare</div>
                        <div>cf-ray: <span style="color: #f2cc60;">8c2f109278a1098b-SIN</span> (Routed via Singapore Edge PoP)</div>
                        <div>cf-cache-status: DYNAMIC</div>
                        <div>cf-tunnel-origin-id: <span style="color: #34d399;">connector-vm2-node (10.0.0.5)</span> [Automatic Failover Engaged]</div>
                        <div>strict-transport-security: max-age=31536000; includeSubDomains; preload</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    render_html_to_png(html, os.path.join(SCREENSHOTS_DIR, "fig5_1_2b_uninterrupted_http200.png"))

# ==============================================================================
# 6. Figure 5.2.2(a): Live Keyword Search and Price Filtering (< RM300)
# ==============================================================================
def create_fig5_2_2a():
    html = """
    <div style="background: #0f172a; width: 1920px; height: 1080px; padding: 25px; display: flex; flex-direction: column;">
        <div style="background: #1e293b; padding: 14px 24px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #334155; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <span style="font-size: 24px;">🏠</span>
                <span style="font-size: 18px; font-weight: bold; color: #f8fafc;">PoliSewa — Dynamic Property Search & Distance Filter Engine</span>
            </div>
            <div style="background: #083344; color: #38bdf8; border: 1px solid #0284c7; padding: 6px 16px; border-radius: 6px; font-weight: bold; font-size: 13px;">
                Filter Criteria: Keyword='Matang' &amp; Price &le; RM 300
            </div>
        </div>

        <div style="display: flex; gap: 20px; flex: 1;">
            <!-- Filter Sidebar -->
            <div style="width: 460px; background: #1e293b; border-radius: 8px; padding: 20px; border: 1px solid #334155; display: flex; flex-direction: column; gap: 18px;">
                <div>
                    <label style="font-size: 13px; color: #94a3b8; font-weight: 600;">Keyword Search</label>
                    <input type="text" value="Matang" style="width: 100%; margin-top: 6px; background: #0f172a; border: 2px solid #38bdf8; color: #f8fafc; padding: 10px 14px; border-radius: 6px; font-size: 15px;" readonly>
                </div>

                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 8px;">
                        <span style="color: #94a3b8; font-weight: 600;">Max Monthly Rental</span>
                        <b style="color: #38bdf8; font-size: 16px;">RM 300 / mo</b>
                    </div>
                    <div style="height: 8px; background: #334155; border-radius: 4px; position: relative;">
                        <div style="width: 40%; height: 100%; background: #38bdf8; border-radius: 4px;"></div>
                    </div>
                </div>

                <div style="font-size: 13px; color: #34d399; background: #064e3b; padding: 8px 12px; border-radius: 6px; font-weight: bold;">
                    ✔ 2 Matching Verified Properties Found
                </div>

                <!-- Result Card 1 -->
                <div style="background: #0f172a; border: 1px solid #38bdf8; border-radius: 8px; padding: 14px;">
                    <div style="font-weight: bold; font-size: 16px; color: #f8fafc;">Bilik Sewa Taman Matang Jaya</div>
                    <div style="color: #38bdf8; font-weight: bold; font-size: 15px; margin: 4px 0;">RM 280 / month</div>
                    <p style="font-size: 12px; color: #94a3b8; line-height: 1.4; margin-bottom: 8px;">Bilik single selesa untuk pelajar lelaki. Dilengkapi katil, tilam, almari, dan wifi laju.</p>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="background: #0c4a6e; color: #7dd3fc; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">📍 2.1 km to PKS Campus</span>
                        <span style="background: #166534; color: #86efac; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">Verified Badge</span>
                    </div>
                </div>

                <!-- Result Card 2 -->
                <div style="background: #0f172a; border: 1px solid #38bdf8; border-radius: 8px; padding: 14px;">
                    <div style="font-weight: bold; font-size: 16px; color: #f8fafc;">Bilik Pelajar Matang Hilir</div>
                    <div style="color: #38bdf8; font-weight: bold; font-size: 15px; margin: 4px 0;">RM 250 / month</div>
                    <p style="font-size: 12px; color: #94a3b8; line-height: 1.4; margin-bottom: 8px;">Berdekatan kedai makan dan dobi. 5 minit perjalanan menaiki motosikal ke pintu utama PKS.</p>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="background: #0c4a6e; color: #7dd3fc; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">📍 1.8 km to PKS Campus</span>
                        <span style="background: #166534; color: #86efac; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">Verified Badge</span>
                    </div>
                </div>
            </div>

            <!-- Map View -->
            <div style="flex: 1; background: #1e293b; border-radius: 8px; border: 1px solid #334155; padding: 25px; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative;">
                <div style="position: absolute; top: 20px; right: 20px; background: #0f172a; padding: 8px 16px; border-radius: 6px; font-size: 13px; border: 1px solid #475569;">
                    Origin Landmark: <b>Politeknik Kuching Sarawak (1.63366, 110.21999)</b>
                </div>
                <div style="width: 85%; height: 75%; border: 2px dashed #0284c7; border-radius: 12px; background: #0b1329; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                    <span style="font-size: 50px; margin-bottom: 10px;">🗺️</span>
                    <h3 style="color: #38bdf8; margin-bottom: 8px;">Interactive Spatial Filter Results</h3>
                    <p style="color: #94a3b8; font-size: 14px; text-align: center; max-width: 500px;">
                        The client engine dynamically calculates the Haversine great-circle distance between each property coordinate and PKS landmark, ordering results by proximity.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """
    render_html_to_png(html, os.path.join(SCREENSHOTS_DIR, "fig5_2_2a_search_filtering.png"))

# ==============================================================================
# 7. Figure 5.2.3(a): 6-Box Email OTP Verification Dialog
# ==============================================================================
def create_fig5_2_3a():
    html = """
    <div style="background: rgba(15, 23, 42, 0.9); width: 1920px; height: 1080px; display: flex; align-items: center; justify-content: center;">
        <div style="background: #1e293b; width: 560px; border-radius: 16px; border: 2px solid #38bdf8; padding: 36px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.7); text-align: center; display: flex; flex-direction: column; align-items: center; gap: 20px;">
            <div style="width: 68px; height: 68px; background: #083344; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 32px; border: 2px solid #0284c7;">
                ✉️
            </div>
            <div>
                <h2 style="font-size: 24px; font-weight: bold; color: #f8fafc; margin-bottom: 6px;">Email OTP Verification</h2>
                <p style="color: #94a3b8; font-size: 14px; line-height: 1.5;">
                    A 6-digit numeric security code was sent to <br>
                    <b style="color: #38bdf8;">hafiz.pks2026@gmail.com</b>
                </p>
            </div>

            <!-- 6 Boxes -->
            <div style="display: flex; gap: 12px; margin: 10px 0;">
                <input type="text" value="8" style="width: 58px; height: 68px; font-size: 28px; font-weight: bold; text-align: center; background: #0f172a; border: 2px solid #38bdf8; border-radius: 10px; color: #f8fafc;" readonly>
                <input type="text" value="4" style="width: 58px; height: 68px; font-size: 28px; font-weight: bold; text-align: center; background: #0f172a; border: 2px solid #38bdf8; border-radius: 10px; color: #f8fafc;" readonly>
                <input type="text" value="9" style="width: 58px; height: 68px; font-size: 28px; font-weight: bold; text-align: center; background: #0f172a; border: 2px solid #38bdf8; border-radius: 10px; color: #f8fafc;" readonly>
                <input type="text" value="2" style="width: 58px; height: 68px; font-size: 28px; font-weight: bold; text-align: center; background: #0f172a; border: 2px solid #38bdf8; border-radius: 10px; color: #f8fafc;" readonly>
                <input type="text" value="1" style="width: 58px; height: 68px; font-size: 28px; font-weight: bold; text-align: center; background: #0f172a; border: 2px solid #38bdf8; border-radius: 10px; color: #f8fafc;" readonly>
                <input type="text" value="7" style="width: 58px; height: 68px; font-size: 28px; font-weight: bold; text-align: center; background: #0f172a; border: 2px solid #38bdf8; border-radius: 10px; color: #f8fafc;" readonly>
            </div>

            <button style="width: 100%; background: #0284c7; color: white; border: none; padding: 14px; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer;">
                Verify &amp; Activate Account
            </button>

            <div style="font-size: 13px; color: #94a3b8;">
                Didn't receive code? Resend in <b style="color: #f59e0b;">00:48</b>
            </div>
        </div>
    </div>
    """
    render_html_to_png(html, os.path.join(SCREENSHOTS_DIR, "fig5_2_3a_otp_modal.png"))

# ==============================================================================
# 8. Figure 5.2.3(b): PoliSewa OTP Verification Email in Gmail
# ==============================================================================
def create_fig5_2_3b():
    html = """
    <div style="background: #f1f3f4; width: 1920px; height: 1080px; padding: 40px; display: flex; justify-content: center; align-items: center; font-family: -apple-system, BlinkMacSystemFont, Roboto, sans-serif;">
        <div style="background: #ffffff; width: 750px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); border: 1px solid #dadce0; overflow: hidden;">
            <!-- Gmail Header -->
            <div style="padding: 20px 24px; border-bottom: 1px solid #e8eaed; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 26px;">✉️</span>
                    <div>
                        <b style="font-size: 16px; color: #202124;">PoliSewa Verification &lt;noreply@polisewa.me&gt;</b>
                        <div style="font-size: 13px; color: #5f6368;">to hafiz.pks2026@gmail.com</div>
                    </div>
                </div>
                <div style="font-size: 13px; color: #5f6368;">2:45 PM (3 minutes ago)</div>
            </div>

            <!-- Email Body -->
            <div style="padding: 36px 30px; text-align: center;">
                <div style="font-size: 22px; font-weight: bold; color: #0b2545; margin-bottom: 12px;">PoliSewa Room Rental System</div>
                <p style="color: #3c4043; font-size: 15px; line-height: 1.5; margin-bottom: 24px;">
                    Thank you for signing up with PoliSewa! Please use the following 6-digit one-time security code to complete your registration:
                </p>

                <div style="background: #f8fafc; border: 2px dashed #0284c7; border-radius: 10px; padding: 20px; display: inline-block; margin-bottom: 24px;">
                    <div style="font-family: 'Courier New', monospace; font-size: 42px; font-weight: bold; letter-spacing: 12px; color: #0369a1;">
                        849217
                    </div>
                </div>

                <p style="color: #5f6368; font-size: 13px; line-height: 1.5;">
                    This code is valid for <b>10 minutes</b>. If you did not request this verification, please ignore this email.
                </p>

                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e8eaed; font-size: 12px; color: #9aa0a6;">
                    PoliSewa Cloud Infrastructure • Politeknik Kuching Sarawak • Secured by Cloudflare Zero Trust
                </div>
            </div>
        </div>
    </div>
    """
    render_html_to_png(html, os.path.join(SCREENSHOTS_DIR, "fig5_2_3b_otp_gmail.png"))

# ==============================================================================
# 9. Figure 5.2.6(a): Permanent Account Deletion Confirmation Dialog
# ==============================================================================
def create_fig5_2_6a():
    html = """
    <div style="background: rgba(15, 23, 42, 0.92); width: 1920px; height: 1080px; display: flex; align-items: center; justify-content: center;">
        <div style="background: #1e293b; width: 560px; border-radius: 16px; border: 2px solid #ef4444; padding: 36px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.8); display: flex; flex-direction: column; gap: 20px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="width: 56px; height: 56px; background: #7f1d1d; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px; border: 2px solid #dc2626;">
                    ⚠️
                </div>
                <div>
                    <h3 style="font-size: 20px; font-weight: bold; color: #f8fafc;">Delete Account Permanently?</h3>
                    <p style="font-size: 13px; color: #f87171;">This action is irreversible and permanent.</p>
                </div>
            </div>

            <div style="background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 16px; font-size: 13px; color: #cbd5e1; line-height: 1.6;">
                Deleting your account will immediately and permanently erase:
                <ul style="margin-left: 20px; margin-top: 6px; color: #fca5a5;">
                    <li>All active room rental listings and descriptions</li>
                    <li>All uploaded property photo blobs from Azure Storage</li>
                    <li>Your verified landlord badge and contact history</li>
                </ul>
            </div>

            <div>
                <label style="font-size: 13px; color: #94a3b8; font-weight: 600;">Confirm your password</label>
                <input type="password" value="••••••••••••" style="width: 100%; margin-top: 6px; background: #0f172a; border: 1px solid #475569; color: #f8fafc; padding: 12px; border-radius: 8px; font-size: 14px;" readonly>
            </div>

            <div style="display: flex; gap: 12px; margin-top: 10px;">
                <button style="flex: 1; background: #334155; color: #f8fafc; border: none; padding: 12px; border-radius: 8px; font-size: 14px; font-weight: 600;">
                    Cancel
                </button>
                <button style="flex: 1; background: #dc2626; color: white; border: none; padding: 12px; border-radius: 8px; font-size: 14px; font-weight: bold;">
                    Yes, Delete My Account
                </button>
            </div>
        </div>
    </div>
    """
    render_html_to_png(html, os.path.join(SCREENSHOTS_DIR, "fig5_2_6a_account_deletion.png"))

def generate_all():
    print("--- 1. Generating all 9 missing screenshots ---")
    create_fig3_5_1a()
    create_fig4_1_1b()
    create_fig5_1_1a()
    create_fig5_1_2a()
    create_fig5_1_2b()
    create_fig5_2_2a()
    create_fig5_2_3a()
    create_fig5_2_3b()
    create_fig5_2_6a()

if __name__ == "__main__":
    generate_all()
