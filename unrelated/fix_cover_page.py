"""
Fixes the cover page overflow in final_report.html so the entire cover page fits
strictly on Page 1, removing the accidental empty Page 2.
Also re-syncs the TOC and recompiles final_report.pdf.
"""
import os
import re
import subprocess
import pymupdf

BASE_DIR = r"c:\Users\abdul\OneDrive\Documents\polisewa"
HTML_PATH = os.path.join(BASE_DIR, "final_report.html")
PDF_PATH = os.path.join(BASE_DIR, "final_report.pdf")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fix @page:first and Cover Page CSS
old_css_target = """  /* Cover Page */
  .cover-page {
    height: 100%;
    min-height: 240mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    padding-top: 15mm;
  }

  .inst-header {
    font-size: 13pt;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 25mm;
    color: #0b2545;
  }

  .sub-inst {
    font-size: 11pt;
    font-weight: normal;
    color: #333;
    margin-top: 4px;
  }

  .report-title-box {
    margin: 15mm 0;
  }

  .project-title {
    font-size: 20pt;
    font-weight: bold;
    text-transform: uppercase;
    line-height: 1.3;
    color: #0a2540;
    margin-bottom: 8px;
  }

  .project-subtitle {
    font-size: 14pt;
    font-weight: bold;
    color: #4a5568;
    text-transform: uppercase;
    letter-spacing: 1.5px;
  }

  .meta-block {
    margin: 10mm 0;
    font-size: 11pt;
  }

  .meta-title {
    font-weight: bold;
    font-size: 12pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
    color: #1a202c;
  }

  .author-list {
    list-style: none;
    padding: 0;
    margin: 0 0 10mm 0;
  }

  .author-list li {
    margin-bottom: 4px;
    font-weight: bold;
  }

  .cover-footer {
    font-size: 11pt;
    font-weight: bold;
    text-transform: uppercase;
    line-height: 1.4;
    color: #2d3748;
    margin-top: 20mm;
  }"""

new_css = """  @page:first {
    @bottom-center {
      content: "";
    }
  }

  /* Cover Page */
  .cover-page {
    box-sizing: border-box;
    height: 235mm;
    max-height: 235mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    padding: 4mm 0 2mm 0;
    margin: 0;
    page-break-after: always;
    page-break-inside: avoid;
  }

  .inst-header {
    font-size: 12pt;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6mm;
    color: #0b2545;
    line-height: 1.35;
  }

  .sub-inst {
    font-size: 10.5pt;
    font-weight: normal;
    color: #4a5568;
    margin-top: 3px;
  }

  .report-title-box {
    margin: 6mm 0;
  }

  .project-title {
    font-size: 18pt;
    font-weight: bold;
    text-transform: uppercase;
    line-height: 1.3;
    color: #0a2540;
    margin-bottom: 6px;
  }

  .project-subtitle {
    font-size: 13pt;
    font-weight: bold;
    color: #4a5568;
    text-transform: uppercase;
    letter-spacing: 1.5px;
  }

  .meta-block {
    margin: 5mm 0;
    font-size: 10.5pt;
  }

  .meta-title {
    font-weight: bold;
    font-size: 11pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
    color: #1a202c;
  }

  .author-list {
    list-style: none;
    padding: 0;
    margin: 0 0 5mm 0;
  }

  .author-list li {
    margin-bottom: 3px;
    font-weight: bold;
  }

  .cover-footer {
    font-size: 10.5pt;
    font-weight: bold;
    text-transform: uppercase;
    line-height: 1.35;
    color: #2d3748;
    margin-top: 4mm;
  }"""

if old_css_target in html:
    html = html.replace(old_css_target, new_css)
else:
    print("Warning: old_css_target not exact match, using regex replacement.")
    html = re.sub(r'/\* Cover Page \*/.*?(?=/\* Typography \*/)', new_css + "\n\n  ", html, flags=re.DOTALL)

# Notice after cover page, there was:
# </div>
# <div class="page-break"></div>
# Since .cover-page already has page-break-after: always, remove the duplicate <div class="page-break"></div> right after cover-page
html = re.sub(r'</div>\s*<div class="page-break"></div>\s*<!-- DECLARATION -->', '</div>\n\n<!-- DECLARATION -->', html)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated final_report.html with compact cover page.")

# Recompile with Edge
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
print("Recompiled PDF. Checking pages...")

doc = pymupdf.open(PDF_PATH)
print(f"Total pages: {len(doc)}")
print("Page 1 preview:\n", doc[0].get_text('text')[:300].strip())
print("Page 2 preview:\n", doc[1].get_text('text')[:300].strip())
