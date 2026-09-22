"""
PoliSewa Final Report Generator
Compiles the comprehensive Academic Final Report for PoliSewa:
"Cloud Based High Availability Room Rental System"
Following the UNIMAS / Polytechnic FYP report standard (final test v13 format).
Generates both Markdown (final_report.md) and HTML (final_report.html), then compiles to final_report.pdf.
"""

import os
import subprocess
import sys

# Define base paths
BASE_DIR = r"c:\Users\abdul\OneDrive\Documents\polisewa"
MD_FILE = os.path.join(BASE_DIR, "final_report.md")
HTML_FILE = os.path.join(BASE_DIR, "final_report.html")
PDF_FILE = os.path.join(BASE_DIR, "final_report.pdf")

print("Starting generation of PoliSewa Final Report...")
