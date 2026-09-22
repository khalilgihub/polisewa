import os
import subprocess
import pymupdf

BASE_DIR = r"c:\Users\abdul\OneDrive\Documents\polisewa"
HTML_PATH = os.path.join(BASE_DIR, "final_report.html")
PDF_PATH = os.path.join(BASE_DIR, "final_report.pdf")

edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_exe):
    edge_exe = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

cmd = [
    edge_exe,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={PDF_PATH}",
    HTML_PATH
]
subprocess.run(cmd, check=True)

doc = pymupdf.open(PDF_PATH)
print("Total pages after test:", len(doc))
os.makedirs("pdf_previews", exist_ok=True)
pix = doc[0].get_pixmap(dpi=150)
pix.save("pdf_previews/page_1.png")
print("=== Page 1 ===\n", doc[0].get_text('text')[:200].strip())
print("=== Page 2 ===\n", doc[1].get_text('text')[:200].strip())
print("=== Page 3 ===\n", doc[2].get_text('text')[:200].strip())


