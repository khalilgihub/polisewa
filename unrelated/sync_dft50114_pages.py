"""
sync_dft50114_pages.py
Audits final_report.pdf (42 pages) to find exact 1-indexed page locations
of all preliminary lists, chapters, sections, figures, and tables.
Then updates final_report.html and recompiles final_report.pdf.
"""
import os
import re
import subprocess
import pymupdf

BASE_DIR = r"c:\Users\abdul\OneDrive\Documents\polisewa"
HTML_PATH = os.path.join(BASE_DIR, "final_report.html")
PDF_PATH = os.path.join(BASE_DIR, "final_report.pdf")

doc = pymupdf.open(PDF_PATH)
print(f"Total pages in PDF: {len(doc)}")

page_texts = {p: doc[p - 1].get_text("text") for p in range(1, len(doc) + 1)}

def find_body_page(pattern, min_p=11):
    regex = re.compile(pattern, re.IGNORECASE)
    for p in range(min_p, len(doc) + 1):
        if regex.search(page_texts[p]):
            return p
    return None

# Prelims
print("\n--- PRELIMINARY PAGES ---")
prelim_items = [
    ("Declaration", r"DECLARATION", 2),
    ("Approval for Submission", r"APPROVAL\s+FOR\s+SUBMISSION", 3),
    ("Acknowledgments", r"ACKNOWLEDGMENTS", 4),
    ("Abstract", r"\bABSTRACT\b", 5),
    ("Abstrak", r"\bABSTRAK\b", 6),
    ("Table of Contents", r"TABLE\s+OF\s+CONTENTS", 7),
    ("List of Figures", r"LIST\s+OF\s+FIGURES", 8),
    ("List of Tables", r"LIST\s+OF\s+TABLES", 10),
]

for name, pat, start_p in prelim_items:
    p = find_body_page(pat, start_p)
    print(f"{name} -> Page {p}")

# Chapters
print("\n--- CHAPTER & SECTION LOCATIONS ---")
toc_patterns = [
    ("CHAPTER 1: INTRODUCTION", r"CHAPTER\s+1:\s*INTRODUCTION", 11),
    ("1.0 Introduction", r"1\.0\s+Introduction", 11),
    ("1.1 Problem Statement", r"1\.1\s+Problem Statement", 11),
    ("1.2 Project Scope", r"1\.2\s+Project Scope", 11),
    ("1.3 Aim and Objectives", r"1\.3\s+Aim and Objectives", 12),
    ("1.4 Methodology (Agile SDLC)", r"1\.4\s+Methodology", 12),
    ("1.5 Significance of the Project", r"1\.5\s+Significance", 13),
    ("1.6 Project Schedule (Gantt Chart)", r"1\.6\s+Project Schedule", 13),
    ("1.7 Cost Planning & Actual Azure Cloud Expenditure Analysis", r"1\.7\s+Cost Planning", 13),
    
    ("CHAPTER 2: LITERATURE REVIEW", r"CHAPTER\s+2:\s*LITERATURE\s+REVIEW", 16),
    ("2.0 Introduction", r"2\.0\s+Introduction", 16),
    ("2.1 High Availability and Cloud Fault Tolerance Models", r"2\.1\s+High Availability", 16),
    ("2.2 Student Rental Portals and Scam Prevention Studies", r"2\.2\s+Student Rental", 17),
    ("2.3 Cloud Infrastructure, Redundancy, and Load Balancing", r"2\.3\s+Cloud Infrastructure", 17),
    ("2.4 Comparative Analysis of Existing Systems vs. PoliSewa", r"2\.4\s+Comparative Analysis", 18),
    ("2.5 Chapter Summary", r"2\.5\s+Chapter Summary", 19),
    
    ("CHAPTER 3: ANALYSIS AND DESIGN", r"CHAPTER\s+3:\s*ANALYSIS\s+AND\s+DESIGN", 19),
    ("3.0 Introduction", r"3\.0\s+Introduction", 19),
    ("3.1 Requirement Analysis", r"3\.1\s+Requirement Analysis", 19),
    ("3.2 High Availability System Architecture", r"3\.2\s+High Availability", 20),
    ("3.3 Data Flow Diagrams (DFD)", r"3\.3\s+Data Flow Diagrams", 22),
    ("3.4 Database Design", r"3\.4\s+Database Design", 23),
    ("3.5 User Interface (UI/UX) Design", r"3\.5\s+User Interface", 24),
    ("3.6 Chapter Summary", r"3\.6\s+Chapter Summary", 26),
    
    ("CHAPTER 4: IMPLEMENTATION", r"CHAPTER\s+4:\s*IMPLEMENTATION", 26),
    ("4.0 Introduction", r"4\.0\s+Introduction", 26),
    ("4.1 Cloud Infrastructure Deployment", r"4\.1\s+Cloud Infrastructure Deployment", 26),
    ("4.2 Application Code Development", r"4\.2\s+Application Code Development", 29),
    ("4.3 Chapter Summary", r"4\.3\s+Chapter Summary", 31),
    
    ("CHAPTER 5: TESTING AND VERIFICATION", r"CHAPTER\s+5:\s*TESTING\s+AND\s+VERIFICATION", 31),
    ("5.0 Introduction", r"5\.0\s+Introduction", 31),
    ("5.1 Cloud High Availability and Failover Testing", r"5\.1\s+Cloud High Availability", 31),
    ("5.2 Software Functional Testing", r"5\.2\s+Software Functional", 34),
    ("5.3 User Scenario Walkthroughs", r"5\.3\s+User Scenario", 38),
    ("5.4 Test Results Summary", r"5\.4\s+Test Results", 39),
    ("5.5 Chapter Summary", r"5\.5\s+Chapter Summary", 39),
    
    ("CHAPTER 6: CONCLUSION AND FUTURE WORKS", r"CHAPTER\s+6:\s*CONCLUSION", 40),
    ("6.0 Introduction", r"6\.0\s+Introduction", 40),
    ("6.1 Objective Achievement Review", r"6\.1\s+Objective Achievement", 40),
    ("6.2 Challenges and Problem Solving", r"6\.2\s+Challenges and Problem Solving", 40),
    ("6.3 Future Works and Enhancements", r"6\.3\s+Future Works", 41),
    ("6.4 Conclusion", r"6\.4\s+Conclusion", 41),
    
    ("REFERENCES", r"REFERENCES", 41)
]

found_toc = {}
for name, pat, min_p in toc_patterns:
    p = find_body_page(pat, min_p)
    found_toc[name] = p
    print(f"{name} -> Page {p}")

print("\n--- FIGURES ---")
figure_patterns = [
    ("Figure 1.4(a)", r"Figure\s+1\.4\(a\)", 11),
    ("Figure 1.6(a)", r"Figure\s+1\.6\(a\)", 11),
    ("Figure 1.7(a)", r"Figure\s+1\.7\(a\)", 13),
    ("Figure 1.7(b)", r"Figure\s+1\.7\(b\)", 13),
    ("Figure 3.2.1(a)", r"Figure\s+3\.2\.1\(a\)", 20),
    ("Figure 3.2.2(a)", r"Figure\s+3\.2\.2\(a\)", 20),
    ("Figure 3.3.1(a)", r"Figure\s+3\.3\.1\(a\)", 22),
    ("Figure 3.4.1(a)", r"Figure\s+3\.4\.1\(a\)", 23),
    ("Figure 3.5.1(a)", r"Figure\s+3\.5\.1\(a\)", 24),
    ("Figure 4.1.1(a)", r"Figure\s+4\.1\.1\(a\)", 26),
    ("Figure 4.1.1(b)", r"Figure\s+4\.1\.1\(b\)", 26),
    ("Figure 4.1.2(a)", r"Figure\s+4\.1\.2\(a\)", 27),
    ("Figure 4.1.3(a)", r"Figure\s+4\.1\.3\(a\)", 28),
    ("Figure 4.1.4(a)", r"Figure\s+4\.1\.4\(a\)", 28),
    ("Figure 4.2.2(a)", r"Figure\s+4\.2\.2\(a\)", 29),
    ("Figure 4.2.3(a)", r"Figure\s+4\.2\.3\(a\)", 30),
    ("Figure 4.2.5(a)", r"Figure\s+4\.2\.5\(a\)", 30),
    ("Figure 5.1.1(a)", r"Figure\s+5\.1\.1\(a\)", 31),
    ("Figure 5.1.2(a)", r"Figure\s+5\.1\.2\(a\)", 32),
    ("Figure 5.1.2(b)", r"Figure\s+5\.1\.2\(b\)", 32),
    ("Figure 5.1.3(a)", r"Figure\s+5\.1\.3\(a\)", 33),
    ("Figure 5.2.1(a)", r"Figure\s+5\.2\.1\(a\)", 34),
    ("Figure 5.2.2(a)", r"Figure\s+5\.2\.2\(a\)", 35),
    ("Figure 5.2.3(a)", r"Figure\s+5\.2\.3\(a\)", 35),
    ("Figure 5.2.3(b)", r"Figure\s+5\.2\.3\(b\)", 36),
    ("Figure 5.2.4(a)", r"Figure\s+5\.2\.4\(a\)", 36),
    ("Figure 5.2.5(a)", r"Figure\s+5\.2\.5\(a\)", 37),
    ("Figure 5.2.6(a)", r"Figure\s+5\.2\.6\(a\)", 37),
    ("Figure 5.3.1(a)", r"Figure\s+5\.3\.1\(a\)", 38),
    ("Figure 5.3.2(a)", r"Figure\s+5\.3\.2\(a\)", 38),
    ("Figure 5.3.3(a)", r"Figure\s+5\.3\.3\(a\)", 38),
]

found_figures = {}
for name, pat, min_p in figure_patterns:
    p = find_body_page(pat, min_p)
    found_figures[name] = p
    print(f"{name} -> Page {p}")

print("\n--- TABLES ---")
table_patterns = [
    ("Table 1.7(a)", r"Table\s+1\.7\(a\)", 13),
    ("Table 2.4(a)", r"Table\s+2\.4\(a\)", 18),
    ("Table 3.1.1(a)", r"Table\s+3\.1\.1\(a\)", 19),
    ("Table 3.1.2(a)", r"Table\s+3\.1\.2\(a\)", 19),
    ("Table 3.4.2(a)", r"Table\s+3\.4\.2\(a\)", 23),
    ("Table 3.4.2(b)", r"Table\s+3\.4\.2\(b\)", 23),
    ("Table 5.1.2(a)", r"Table\s+5\.1\.2\(a\)", 32),
    ("Table 5.2.7(a)", r"Table\s+5\.2\.7\(a\)", 39),
    ("Table 5.2.7(b)", r"Table\s+5\.2\.7\(b\)", 39),
    ("Table 5.3.4(a)", r"Table\s+5\.3\.4\(a\)", 39),
    ("Table 6.1(a)", r"Table\s+6\.1\(a\)", 40),
]

found_tables = {}
for name, pat, min_p in table_patterns:
    p = find_body_page(pat, min_p)
    found_tables[name] = p
    print(f"{name} -> Page {p}")
