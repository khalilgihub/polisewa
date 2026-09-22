import os
import re
import subprocess
import pymupdf

BASE_DIR = r"c:\Users\abdul\OneDrive\Documents\polisewa"
HTML_PATH = os.path.join(BASE_DIR, "final_report.html")
PDF_PATH = os.path.join(BASE_DIR, "final_report.pdf")

edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_exe):
    edge_exe = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

def compile_pdf():
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

# First compile to ensure HTML is current
compile_pdf()

doc = pymupdf.open(PDF_PATH)
print(f"Loaded PDF with {len(doc)} pages.")

# Scan only the body of the report (page 12 onwards) to avoid reading the TOC/LOF itself
fig_map = {}
tbl_map = {}
section_map = {}

for page_idx, page in enumerate(doc):
    page_num = page_idx + 1
    if page_num < 12:
        continue # Skip preliminary pages (cover, declaration, TOC, LOF, LOT)

    text = page.get_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    for l in lines:
        # Match figures e.g. "Figure 1.7(a):"
        m_fig = re.match(r'(Figure\s+[\d\.]+\([a-z]\))', l)
        if m_fig:
            fig_id = m_fig.group(1)
            if fig_id not in fig_map:
                fig_map[fig_id] = page_num
                
        # Match tables e.g. "Table 1.7(a):"
        m_tbl = re.match(r'(Table\s+[\d\.]+\([a-z]\))', l)
        if m_tbl:
            tbl_id = m_tbl.group(1)
            if tbl_id not in tbl_map:
                tbl_map[tbl_id] = page_num

        # Match Chapter headings (exact heading text)
        if l in ["CHAPTER 1: INTRODUCTION", "Chapter 1: Introduction", "1.0 Introduction"]:
            if "chap_1" not in section_map: section_map["chap_1"] = page_num
        if l in ["CHAPTER 2: LITERATURE REVIEW", "Chapter 2: Literature Review", "2.0 Introduction"]:
            if "chap_2" not in section_map: section_map["chap_2"] = page_num
        if l in ["CHAPTER 3: ANALYSIS AND DESIGN", "Chapter 3: Analysis and Design", "3.0 Introduction"]:
            if "chap_3" not in section_map: section_map["chap_3"] = page_num
        if l in ["CHAPTER 4: IMPLEMENTATION", "Chapter 4: Implementation", "4.0 Introduction"]:
            if "chap_4" not in section_map: section_map["chap_4"] = page_num
        if l in ["CHAPTER 5: TESTING AND VERIFICATION", "Chapter 5: Testing and Verification", "5.0 Introduction"]:
            if "chap_5" not in section_map: section_map["chap_5"] = page_num
        if l in ["CHAPTER 6: CONCLUSION AND FUTURE WORKS", "Chapter 6: Conclusion and Future Works", "6.0 Introduction"]:
            if "chap_6" not in section_map: section_map["chap_6"] = page_num
        if l == "REFERENCES" or l == "References":
            if "refs" not in section_map: section_map["refs"] = page_num

print("Detected Figures:", fig_map)
print("Detected Sections:", section_map)

# Update HTML Table of Contents and List of Figures with exact page numbers
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Update Figure pages in List of Figures
for fig_id, p in fig_map.items():
    escaped_id = re.escape(fig_id)
    pattern = r'(<span class=[\"\']toc-title[\"\']>' + escaped_id + r'[^<]*</span>\s*<span class=[\"\']toc-page[\"\']>)\d+(</span>)'
    html = re.sub(pattern, rf'\g<1>{p}\g<2>', html)

# Update Chapter pages in Table of Contents
chap_keys = [
    ("chap_1", "CHAPTER 1: INTRODUCTION"),
    ("chap_2", "CHAPTER 2: LITERATURE REVIEW"),
    ("chap_3", "CHAPTER 3: ANALYSIS AND DESIGN"),
    ("chap_4", "CHAPTER 4: IMPLEMENTATION"),
    ("chap_5", "CHAPTER 5: TESTING AND VERIFICATION"),
    ("chap_6", "CHAPTER 6: CONCLUSION AND FUTURE WORKS"),
    ("refs", "REFERENCES")
]

for k, title in chap_keys:
    if k in section_map:
        p = section_map[k]
        pattern = r'(<span class=[\"\']toc-title[\"\']><strong>' + re.escape(title) + r'</strong></span>\s*<span class=[\"\']toc-page[\"\']><strong>)\d+(</strong></span>)'
        html = re.sub(pattern, rf'\g<1>{p}\g<2>', html)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Recompiling final PDF with synchronized page numbers...")
compile_pdf()

doc_final = pymupdf.open(PDF_PATH)
print(f"Final Report PDF Generated: {len(doc_final)} pages, {os.path.getsize(PDF_PATH)} bytes.")
